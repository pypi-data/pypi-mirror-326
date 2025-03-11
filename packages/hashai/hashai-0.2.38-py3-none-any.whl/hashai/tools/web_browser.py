# web_browser.py
from typing import Dict, Any, List, Callable , Optional
from pydantic import Field, BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time
import re
import logging
import os
import difflib
from datetime import datetime

from .base_tool import BaseTool

logger = logging.getLogger(__name__)

class BrowserPlan(BaseModel):
    tasks: List[Dict[str, Any]] = Field(
        ...,
        description="List of automation tasks to execute"
    )

def get_system_prompt(user_input: str,
                      current_url: str,
                      current_date: str,
                      interactive_elements: str = "None",
                      tabs: str = "None") -> str:
    """
    Generate a dynamic system prompt for the LLM to produce a fully structured JSON plan.
    The plan should include an optional "ui_index" field for actions like click and type.
    """
    prompt = f'''
You are a dynamic web automation agent that receives high-level instructions and outputs a fully structured JSON plan for browser automation. Your response must be valid JSON in the exact format below and include all necessary steps dynamically—no task is hardcoded.

IMPORTANT:
1. Generate all tasks dynamically based on the user's instruction.
2. For actions like "click" and "type", include an optional field "ui_index" that indicates the number (from the UI-labeling step) of the UI element to use.
3. Always include a "label_ui" action immediately after navigation to map all interactive elements on the page.
4. Use the provided visual context to verify element locations.
5. End the plan with a "done" action if the task is complete.
6. Do not include extraneous text; only output valid JSON.

The expected JSON format is:

{{
  "current_state": {{
    "evaluation_previous_goal": "Success | Failed | Unknown – evaluate if previous actions achieved the intended result.",
    "memory": "Summary of actions completed so far and key points to remember.",
    "next_goal": "Description of the next steps required to complete the task."
  }},
  "action": [
    {{
      "action_name": {{
         "selector": "CSS selector (if applicable)",
         "value": "Text/URL/seconds/etc.",
         "ui_index": "UI element index to use (optional)"
      }}
    }},
    // ... more actions in sequence
    {{
      "done": {{}}
    }}
  ]
}}

Your available actions include:
- navigate: Go to a specified URL.
- label_ui: Label all interactive elements on the page with colored boxes and numbered labels.
- click: Click on an element.
- type: Type text into an input field.
- wait: Wait for a specified number of seconds.
- wait_for_ajax: Wait until AJAX/network activity subsides.
- scroll: Scroll to a specified element or to the page bottom.
- hover: Hover over an element.
- screenshot: Capture a screenshot.
- switch_tab: Switch to another browser tab.
- execute_script: Execute arbitrary JavaScript.
- drag_and_drop: Perform a drag-and-drop action.
- select: Choose an option from a dropdown.
- done: Indicate that the task is complete.

CURRENT CONTEXT:
- Current Date and Time: {current_date}
- Current URL: {current_url}
- Interactive Elements: {interactive_elements}
- Open Tabs: {tabs}

Task:
"{user_input}"

Respond only with valid JSON.
'''
    return prompt.strip()

class WebBrowserTool(BaseTool):
    name: str = Field("WebBrowser", description="Name of the tool")
    description: str = Field(
        "A highly advanced, fully dynamic web automation tool that generates its own JSON plan from user input. The plan includes UI element indices (from UI labeling) for precise interactions. It uses advanced element detection, automatic UI labeling with color-coded overlays, and robust error recovery with retries.",
        description="Tool description"
    )
    
    default_timeout: int = 15         # Default wait timeout (seconds)
    max_retries: int = 3              # Maximum retries per individual task
    max_overall_attempts: int = 3     # Maximum overall attempts for the entire plan

    synonyms_cache: Dict[str, List[str]] = {}  # Cache for dynamic synonyms
    ui_mapping: List[Dict[str, Any]] = []        # Storage for UI labeling mapping

    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an advanced dynamic web automation workflow.
        
        1. Generate a JSON plan from the user's instruction using the LLM and our system prompt.
        2. If the plan is empty, use a default fallback plan.
        3. Insert a "label_ui" task immediately after the first "navigate" task.
        4. Process each task sequentially. For tasks with a "ui_index", log the UI label number.
        5. If a task fails, retry it (up to overall maximum attempts).
        """
        driver = None
        overall_start = time.time()
        try:
            headless = input.get("headless", False)
            self.default_timeout = int(input.get("timeout", self.default_timeout))
            self.max_retries = int(input.get("max_retries", self.max_retries))
            driver = self._init_browser(headless)
            results = []
            current_url = ""

            # Generate a dynamic plan using our system prompt.
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            # For this example, we do not pass interactive_elements or tabs.
            prompt = get_system_prompt(user_input=input.get("query", ""),
                                       current_url=current_url,
                                       current_date=current_date)
            response = self.llm.generate(prompt=prompt)
            plan = self._parse_plan(response)

            # Fallback: If no valid tasks, use a default plan that simply ends with "done".
            if not plan.tasks:
                logger.error("No valid tasks generated; using fallback plan.")
                plan = BrowserPlan(tasks=[{"action": "done", "selector": "", "value": "", "description": "Task complete."}])

            # Automatically insert a UI-labeling task immediately after the first navigation task.
            nav_index = next((i for i, t in enumerate(plan.tasks) if t.get("action", "").lower() == "navigate"), None)
            if nav_index is not None:
                if not any(t.get("action", "").lower() == "label_ui" for t in plan.tasks[nav_index+1:]):
                    plan.tasks.insert(nav_index+1, {
                        "action": "label_ui",
                        "selector": "",
                        "value": "",
                        "description": "Automatically label UI elements after navigation for improved accuracy."
                    })

            # Map actions to handler functions.
            action_map: Dict[str, Callable[[webdriver.Chrome, Dict[str, Any]], Dict[str, Any]]] = {
                "navigate": lambda d, task: self._handle_navigation(d, task.get("value", "")),
                "click": lambda d, task: self._handle_click(d, task.get("selector", ""), task),
                "type": lambda d, task: self._handle_typing(d, task.get("selector", ""), task.get("value", ""), task),
                "wait": lambda d, task: self._handle_wait(task.get("value", "")),
                "wait_for_ajax": lambda d, task: self._handle_wait_for_ajax(d, task.get("value", "30")),
                "scroll": lambda d, task: self._handle_scroll(d, task.get("selector", "")),
                "hover": lambda d, task: self._handle_hover(d, task.get("selector", "")),
                "screenshot": lambda d, task: self._handle_screenshot(d, task.get("value", "screenshot.png")),
                "switch_tab": lambda d, task: self._handle_switch_tab(d, task.get("value", "0")),
                "execute_script": lambda d, task: self._handle_execute_script(d, task.get("value", "")),
                "drag_and_drop": lambda d, task: self._handle_drag_and_drop(d, task.get("selector", ""), task.get("value", "")),
                "select": lambda d, task: self._handle_select_dropdown(d, task.get("selector", ""), task.get("value", "")),
                "label_ui": lambda d, task: self._handle_label_ui(d, task),
                "done": lambda d, task: {"action": "done", "success": True, "message": "Task complete."}
            }
            
            # Process tasks sequentially with overall retry logic.
            task_index = 0
            overall_attempts = 0
            while task_index < len(plan.tasks) and overall_attempts < self.max_overall_attempts:
                task = plan.tasks[task_index]
                action = task.get("action", "").lower()
                handler = action_map.get(action)
                if not handler:
                    logger.warning(f"Unsupported action '{action}' encountered; skipping.")
                    results.append({
                        "action": action,
                        "success": False,
                        "message": f"Unsupported action: {action}"
                    })
                    task_index += 1
                    continue

                # If task includes a ui_index, log it.
                if "ui_index" in task:
                    logger.info(f"Task '{action}' indicates UI element index: {task['ui_index']}.")

                logger.info(f"Executing task: {task.get('description', action)}")
                start_time = time.time()
                result = self._execute_with_retries(driver, task, handler)
                elapsed = time.time() - start_time
                result["elapsed"] = elapsed
                logger.info(f"Action '{action}' completed in {elapsed:.2f} seconds.")
                results.append(result)
                if not result.get("success", False):
                    logger.error(f"Task '{action}' failed: {result.get('message')}. Retrying this task (overall attempt {overall_attempts+1}/{self.max_overall_attempts}).")
                    overall_attempts += 1  # Retry the same task.
                else:
                    task_index += 1

            if task_index == len(plan.tasks):
                logger.info("All tasks completed successfully.")
            else:
                logger.error("Not all tasks could be completed after overall retries.")

            overall_elapsed = time.time() - overall_start
            logger.info(f"Total execution time: {overall_elapsed:.2f} seconds.")
            return {"status": "success", "results": results, "total_time": overall_elapsed}

        except Exception as e:
            logger.exception("Execution error:")
            return {"status": "error", "message": str(e)}
        finally:
            if driver:
                driver.quit()

    def _init_browser(self, headless: bool) -> webdriver.Chrome:
        """Initialize the browser with advanced options."""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def _generate_plan(self, query: str, current_url: str) -> BrowserPlan:
        """
        Generate a dynamic execution plan using the LLM.
        This method calls get_system_prompt to obtain a full-context prompt and then parses the JSON response.
        """
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        interactive_elements = "None"
        tabs = "None"
        prompt = get_system_prompt(user_input=query,
                                   current_url=current_url,
                                   current_date=current_date,
                                   interactive_elements=interactive_elements,
                                   tabs=tabs)
        response = self.llm.generate(prompt=prompt)
        return self._parse_plan(response)

    def _parse_plan(self, response: str) -> BrowserPlan:
        """Robustly parse the JSON plan from the LLM response. If no tasks are found, fallback to a default plan."""
        try:
            json_match = re.search(r'```json\n?(.+?)\n?```', response, re.DOTALL)
            if json_match:
                plan_data = json.loads(json_match.group(1).strip())
            else:
                json_str_match = re.search(r'\{.*\}', response, re.DOTALL)
                if not json_str_match:
                    raise ValueError("No JSON object found in the response.")
                plan_data = json.loads(json_str_match.group())
            validated_tasks = []
            for task in plan_data.get("tasks", []):
                if not all(key in task for key in ["action", "description"]):
                    logger.warning(f"Skipping task due to missing keys: {task}")
                    continue
                validated_tasks.append({
                    "action": task["action"],
                    "selector": task.get("selector", ""),
                    "value": task.get("value", ""),
                    "description": task["description"],
                    "ui_index": task.get("ui_index", None)
                })
            # Fallback: If no tasks were generated, return a default plan with a "done" action.
            if not validated_tasks:
                validated_tasks.append({
                    "action": "done",
                    "selector": "",
                    "value": "",
                    "description": "No tasks generated; marking task as complete.",
                    "ui_index": None
                })
            return BrowserPlan(tasks=validated_tasks)
        except (json.JSONDecodeError, AttributeError, ValueError) as e:
            logger.error(f"Plan parsing failed: {e}")
            return BrowserPlan(tasks=[{
                "action": "done",
                "selector": "",
                "value": "",
                "description": "Plan parsing failed; defaulting to done action.",
                "ui_index": None
            }])

    def _execute_with_retries(self, driver: webdriver.Chrome, task: Dict[str, Any],
                                handler: Callable[[webdriver.Chrome, Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        """Execute an individual task with retry logic and exponential backoff."""
        attempts = 0
        result = {}
        while attempts < self.max_retries:
            result = self._execute_safe_task(driver, task, handler)
            if result.get("success", False):
                return result
            attempts += 1
            logger.info(f"Retrying task '{task.get('action')}' (attempt {attempts + 1}/{self.max_retries})")
            time.sleep(1 * attempts)
        return result

    def _execute_safe_task(self, driver: webdriver.Chrome, task: Dict[str, Any],
                             handler: Callable[[webdriver.Chrome, Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        """Safely execute a task and catch errors."""
        try:
            return handler(driver, task)
        except Exception as e:
            action = task.get("action", "unknown")
            logger.exception(f"Error executing task '{action}':")
            return {"action": action, "success": False, "message": f"Critical error: {str(e)}"}

    def _dismiss_unwanted_modals(self, driver: webdriver.Chrome):
        """Dismiss or remove unwanted modals and overlays."""
        try:
            modal_selectors = [".modal", ".popup", '[role="dialog"]', ".overlay", ".lightbox"]
            for selector in modal_selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for modal in elements:
                    if modal.is_displayed():
                        close_selectors = [".close", ".btn-close", "[aria-label='Close']", "[data-dismiss='modal']"]
                        dismissed = False
                        for close_sel in close_selectors:
                            try:
                                close_button = modal.find_element(By.CSS_SELECTOR, close_sel)
                                if close_button.is_displayed():
                                    close_button.click()
                                    dismissed = True
                                    logger.info(f"Dismissed modal using selector {close_sel}")
                                    time.sleep(1)
                                    break
                            except Exception:
                                continue
                        if not dismissed:
                            driver.execute_script("arguments[0].remove();", modal)
                            logger.info(f"Removed overlay/modal with selector {selector}")
        except Exception as e:
            logger.debug(f"Modal dismissal error: {e}")

    def _get_synonyms(self, keyword: str) -> List[str]:
        """Dynamically fetch synonyms for a keyword using the LLM (cached)."""
        key = keyword.lower()
        if key in self.synonyms_cache:
            return self.synonyms_cache[key]
        prompt = f"Provide a comma-separated list of synonyms for the word '{key}'."
        response = self.llm.generate(prompt=prompt)
        synonyms = [word.strip().lower() for word in response.split(",") if word.strip()]
        self.synonyms_cache[key] = synonyms
        return synonyms

    def _advanced_find_element(self, driver: webdriver.Chrome, keyword: str) -> Optional[webdriver.remote.webelement.WebElement]:
        """
        Use advanced fallback to locate an element via fuzzy matching of multiple attributes and inner text.
        If a UI mapping from label_ui exists, log the UI label number when a matching element is found.
        """
        candidates = driver.find_elements(By.CSS_SELECTOR, "input, textarea, button, a, div, span")
        best_match = None
        best_ratio = 0.0
        keyword_lower = keyword.lower()
        synonyms = self._get_synonyms(keyword_lower)
        keywords_to_match = set([keyword_lower] + synonyms)
        for candidate in candidates:
            combined_text = " ".join([
                candidate.get_attribute("id") or "",
                candidate.get_attribute("name") or "",
                candidate.get_attribute("placeholder") or "",
                candidate.get_attribute("aria-label") or "",
                candidate.text or ""
            ]).strip().lower()
            current_ratio = max(difflib.SequenceMatcher(None, combined_text, kw).ratio() for kw in keywords_to_match)
            if current_ratio > best_ratio:
                best_ratio = current_ratio
                best_match = candidate
        if best_match and best_ratio > 0.5:
            if self.ui_mapping:
                for item in self.ui_mapping:
                    try:
                        if (best_match.tag_name.upper() == item.get("tag", "").upper() and
                            best_match.text.strip() == item.get("text", "").strip()):
                            logger.info(f"Interacting with UI element labeled as {item.get('index')}.")
                            break
                    except Exception:
                        continue
            logger.info(f"Advanced fallback detected element with similarity {best_ratio:.2f} for keyword '{keyword}'.")
            return best_match
        return None

    def _handle_navigation(self, driver: webdriver.Chrome, url: str) -> Dict[str, Any]:
        """Navigate to the specified URL (adding 'https://' if necessary)."""
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        try:
            driver.get(url)
            WebDriverWait(driver, self.default_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return {"action": "navigate", "success": True, "message": f"Navigated to {url}"}
        except Exception as e:
            logger.error(f"Navigation to {url} failed: {e}")
            return {"action": "navigate", "success": False, "message": f"Navigation failed: {str(e)}"}

    def _handle_click(self, driver: webdriver.Chrome, selector: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Click the element specified by the CSS selector.
        If a ui_index is provided in the task, log that information.
        """
        if "ui_index" in task:
            logger.info(f"Task indicates to use UI element with index {task['ui_index']}.")
        try:
            element = WebDriverWait(driver, self.default_timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            try:
                element.click()
            except Exception:
                driver.execute_script("arguments[0].click();", element)
            return {"action": "click", "success": True, "message": f"Clicked element: {selector}"}
        except Exception as e:
            logger.error(f"Click action failed on selector {selector}: {e}")
            return {"action": "click", "success": False, "message": f"Click failed: {str(e)}"}

    def _handle_typing(self, driver: webdriver.Chrome, selector: str, text: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Type text into the element specified by the CSS selector.
        If a ui_index is provided, log that information.
        Uses advanced fallback and recovery if necessary.
        """
        if "ui_index" in task:
            logger.info(f"Task indicates to use UI element with index {task['ui_index']}.")
        try:
            element = WebDriverWait(driver, self.default_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
        except Exception as e:
            if "search" in task.get("description", "").lower() or "search" in selector.lower():
                logger.info("Primary selector failed; using advanced fallback based on inner text and synonyms.")
                element = self._advanced_find_element(driver, "search")
                if not element:
                    return {"action": "type", "success": False, "message": f"Typing failed: No search-like element found; error: {str(e)}"}
            else:
                fallback_keyword = task.get("description", "")
                element = self._advanced_find_element(driver, fallback_keyword)
                if not element:
                    return {"action": "type", "success": False, "message": f"Typing failed: {str(e)}"}
        try:
            element.clear()
            element.send_keys(text)
            return {"action": "type", "success": True, "message": f"Typed '{text}' into element."}
        except Exception as e:
            error_message = str(e)
            if "invalid element state" in error_message.lower():
                logger.warning("Invalid element state detected. Attempting to remove 'readonly' and use JS injection.")
                try:
                    driver.execute_script("arguments[0].removeAttribute('readonly');", element)
                    element.clear()
                    element.send_keys(text)
                    return {"action": "type", "success": True, "message": f"Typed '{text}' after removing readonly."}
                except Exception as e2:
                    logger.warning(f"Removal of readonly attribute failed: {e2}")
                    try:
                        driver.execute_script("arguments[0].value = arguments[1];", element, text)
                        return {"action": "type", "success": True, "message": f"Set value via JS: '{text}'."}
                    except Exception as e3:
                        logger.error(f"JS value injection failed: {e3}")
                        return {"action": "type", "success": False, "message": f"Typing failed after JS injection: {str(e3)}"}
            else:
                logger.error(f"Typing action failed: {e}")
                return {"action": "type", "success": False, "message": f"Typing failed: {error_message}"}

    def _handle_wait(self, seconds: str) -> Dict[str, Any]:
        """Wait for the specified number of seconds."""
        try:
            wait_time = float(seconds)
            logger.info(f"Waiting for {wait_time} seconds")
            time.sleep(wait_time)
            return {"action": "wait", "success": True, "message": f"Waited {wait_time} seconds"}
        except ValueError as e:
            logger.error(f"Invalid wait time provided: {seconds}")
            return {"action": "wait", "success": False, "message": "Invalid wait time"}

    def _handle_wait_for_ajax(self, driver: webdriver.Chrome, seconds: str) -> Dict[str, Any]:
        """Wait until AJAX or network activity subsides."""
        try:
            timeout = int(seconds)
            logger.info(f"Waiting for AJAX/network activity for up to {timeout} seconds.")
            end_time = time.time() + timeout
            while time.time() < end_time:
                ajax_complete = driver.execute_script("""
                    return (window.jQuery ? jQuery.active === 0 : true) &&
                           (typeof window.fetch === 'function' ? true : true);
                """)
                if ajax_complete:
                    break
                time.sleep(0.5)
            return {"action": "wait_for_ajax", "success": True, "message": "AJAX/network activity subsided."}
        except Exception as e:
            logger.error(f"Wait for AJAX failed: {e}")
            return {"action": "wait_for_ajax", "success": False, "message": f"Wait for AJAX failed: {str(e)}"}

    def _handle_scroll(self, driver: webdriver.Chrome, selector: str) -> Dict[str, Any]:
        """Scroll to the element specified by the selector or to the bottom of the page."""
        try:
            if selector:
                element = WebDriverWait(driver, self.default_timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                scroll_target = selector
            else:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                scroll_target = "page bottom"
            return {"action": "scroll", "success": True, "message": f"Scrolled to {scroll_target}"}
        except Exception as e:
            logger.error(f"Scroll action failed on selector {selector}: {e}")
            return {"action": "scroll", "success": False, "message": f"Scroll failed: {str(e)}"}

    def _handle_hover(self, driver: webdriver.Chrome, selector: str) -> Dict[str, Any]:
        """Hover over the element specified by the selector."""
        try:
            element = WebDriverWait(driver, self.default_timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
            ActionChains(driver).move_to_element(element).perform()
            return {"action": "hover", "success": True, "message": f"Hovered over {selector}"}
        except Exception as e:
            logger.error(f"Hover action failed on selector {selector}: {e}")
            return {"action": "hover", "success": False, "message": f"Hover failed: {str(e)}"}

    def _handle_screenshot(self, driver: webdriver.Chrome, filename: str) -> Dict[str, Any]:
        """Capture a screenshot and save it to the specified filename."""
        try:
            driver.save_screenshot(filename)
            return {"action": "screenshot", "success": True, "message": f"Screenshot saved as {filename}"}
        except Exception as e:
            logger.error(f"Screenshot capture failed: {e}")
            return {"action": "screenshot", "success": False, "message": f"Screenshot failed: {str(e)}"}

    def _handle_switch_tab(self, driver: webdriver.Chrome, value: str) -> Dict[str, Any]:
        """Switch to a different browser tab (by index or 'new')."""
        try:
            handles = driver.window_handles
            if value.lower() == "new":
                target_handle = handles[-1]
            else:
                idx = int(value)
                if idx < len(handles):
                    target_handle = handles[idx]
                else:
                    return {"action": "switch_tab", "success": False, "message": f"Tab index {value} out of range"}
            driver.switch_to.window(target_handle)
            return {"action": "switch_tab", "success": True, "message": f"Switched to tab {value}"}
        except Exception as e:
            logger.error(f"Switch tab failed: {e}")
            return {"action": "switch_tab", "success": False, "message": f"Switch tab failed: {str(e)}"}

    def _handle_execute_script(self, driver: webdriver.Chrome, script: str) -> Dict[str, Any]:
        """Execute arbitrary JavaScript code."""
        try:
            result = driver.execute_script(script)
            return {"action": "execute_script", "success": True, "message": "Script executed successfully", "result": result}
        except Exception as e:
            logger.error(f"Execute script failed: {e}")
            return {"action": "execute_script", "success": False, "message": f"Script execution failed: {str(e)}"}

    def _handle_drag_and_drop(self, driver: webdriver.Chrome, source_selector: str, target_selector: str) -> Dict[str, Any]:
        """Simulate a drag-and-drop operation from source to target."""
        try:
            source = WebDriverWait(driver, self.default_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, source_selector))
            )
            target = WebDriverWait(driver, self.default_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, target_selector))
            )
            ActionChains(driver).drag_and_drop(source, target).perform()
            return {"action": "drag_and_drop", "success": True, "message": f"Dragged element from {source_selector} to {target_selector}"}
        except Exception as e:
            logger.error(f"Drag and drop failed from {source_selector} to {target_selector}: {e}")
            return {"action": "drag_and_drop", "success": False, "message": f"Drag and drop failed: {str(e)}"}

    def _handle_select_dropdown(self, driver: webdriver.Chrome, selector: str, option_text: str) -> Dict[str, Any]:
        """Select an option from a dropdown (<select>) by visible text."""
        try:
            element = WebDriverWait(driver, self.default_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            select_element = Select(element)
            select_element.select_by_visible_text(option_text)
            return {"action": "select", "success": True, "message": f"Selected '{option_text}' from dropdown {selector}"}
        except Exception as e:
            logger.error(f"Dropdown selection failed on selector {selector} with option '{option_text}': {e}")
            return {"action": "select", "success": False, "message": f"Dropdown selection failed: {str(e)}"}

    def _handle_label_ui(self, driver: webdriver.Chrome, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Label UI elements by injecting JavaScript that overlays colored boxes and numbered labels on interactive elements.
        Different tags are assigned specific border colors. The overlaid number (UI label) is returned in a JSON mapping.
        """
        try:
            script = """
            (function() {
                var colorMapping = {
                    "INPUT": "green",
                    "BUTTON": "blue",
                    "A": "orange",
                    "SELECT": "purple",
                    "TEXTAREA": "teal"
                };
                var defaultColor = "red";
                var elements = document.querySelectorAll("input, button, a, select, textarea, div, span");
                var mapping = [];
                for (var i = 0; i < elements.length; i++) {
                    var rect = elements[i].getBoundingClientRect();
                    if (rect.width === 0 || rect.height === 0) continue;
                    var tag = elements[i].tagName.toUpperCase();
                    var color = colorMapping[tag] || defaultColor;
                    var overlay = document.createElement("div");
                    overlay.style.position = "absolute";
                    overlay.style.left = (rect.left + window.scrollX) + "px";
                    overlay.style.top = (rect.top + window.scrollY) + "px";
                    overlay.style.width = rect.width + "px";
                    overlay.style.height = rect.height + "px";
                    overlay.style.border = "2px solid " + color;
                    overlay.style.zIndex = "9999";
                    overlay.style.pointerEvents = "none";
                    
                    var label = document.createElement("div");
                    label.innerText = (i+1).toString();
                    label.style.position = "absolute";
                    label.style.top = "0px";
                    label.style.left = "0px";
                    label.style.backgroundColor = "yellow";
                    label.style.color = "black";
                    label.style.fontSize = "12px";
                    label.style.fontWeight = "bold";
                    label.style.padding = "2px";
                    overlay.appendChild(label);
                    
                    document.body.appendChild(overlay);
                    
                    mapping.push({
                        index: i+1,
                        tag: tag,
                        text: elements[i].innerText.trim(),
                        class: elements[i].getAttribute("class"),
                        borderColor: color
                    });
                }
                return JSON.stringify(mapping);
            })();
            """
            result = driver.execute_script(script)
            if result is None:
                self.ui_mapping = []
                return {"action": "label_ui", "success": True, "message": "UI elements labeled but no mapping returned.", "mapping": []}
            mapping = json.loads(result)
            self.ui_mapping = mapping
            return {"action": "label_ui", "success": True, "message": "UI elements labeled.", "mapping": mapping}
        except Exception as e:
            logger.error(f"Label UI action failed: {e}")
            return {"action": "label_ui", "success": False, "message": f"Label UI failed: {str(e)}"}

    def _capture_failure_screenshot(self, driver: webdriver.Chrome, action: str):
        """Capture a screenshot for debugging when a task fails."""
        filename = f"failure_{action}_{int(time.time())}.png"
        try:
            driver.save_screenshot(filename)
            logger.info(f"Failure screenshot captured: {filename}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
