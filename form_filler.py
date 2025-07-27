"""
Auto-fill bot for job applications.
Fills out forms but does not submit - user must review and submit manually.
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import config_manager as config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobApplicationFiller:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_driver()
        
    def setup_driver(self):
        """Initialize the Chrome driver with appropriate options."""
        try:
            chrome_options = Options()
            
            # Add options for better automation
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Set headless mode if configured
            if config.BROWSER_SETTINGS["headless"]:
                chrome_options.add_argument("--headless")
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set timeouts
            self.driver.implicitly_wait(config.BROWSER_SETTINGS["implicit_wait"])
            self.driver.set_page_load_timeout(config.BROWSER_SETTINGS["page_load_timeout"])
            
            # Initialize wait object
            self.wait = WebDriverWait(self.driver, 10)
            
            # Remove automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Chrome driver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize driver: {e}")
            raise
    
    def find_element_safe(self, selectors, element_type="input"):
        """
        Try multiple selectors to find an element safely.
        
        Args:
            selectors (list): List of CSS selectors to try
            element_type (str): Type of element to look for (input, textarea, select)
            
        Returns:
            WebElement or None: Found element or None if not found
        """
        for selector in selectors:
            try:
                if element_type == "input":
                    element = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                elif element_type == "textarea":
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                elif element_type == "select":
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if element.is_displayed() and element.is_enabled():
                    return element
            except (TimeoutException, NoSuchElementException):
                continue
        
        return None
    
    def fill_text_field(self, value, field_selectors, field_name=""):
        """
        Fill a text input field with the given value.
        
        Args:
            value (str): Value to fill
            field_selectors (list): List of CSS selectors to try
            field_name (str): Name of the field for logging
        """
        element = self.find_element_safe(field_selectors)
        if element:
            try:
                # Clear existing content
                element.clear()
                time.sleep(0.5)
                
                # Fill with new value
                element.send_keys(value)
                logger.info(f"Filled {field_name}: {value}")
                return True
            except Exception as e:
                logger.warning(f"Failed to fill {field_name}: {e}")
        else:
            logger.warning(f"Could not find field for {field_name}")
        
        return False
    
    def fill_select_field(self, value, field_selectors, field_name=""):
        """
        Fill a dropdown/select field with the given value.
        
        Args:
            value (str): Value to select
            field_selectors (list): List of CSS selectors to try
            field_name (str): Name of the field for logging
        """
        element = self.find_element_safe(field_selectors, "select")
        if element:
            try:
                select = Select(element)
                select.select_by_visible_text(value)
                logger.info(f"Selected {field_name}: {value}")
                return True
            except Exception as e:
                logger.warning(f"Failed to select {field_name}: {e}")
        else:
            logger.warning(f"Could not find select field for {field_name}")
        
        return False
    
    def fill_textarea_field(self, value, field_selectors, field_name=""):
        """
        Fill a textarea field with the given value.
        
        Args:
            value (str): Value to fill
            field_selectors (list): List of CSS selectors to try
            field_name (str): Name of the field for logging
        """
        element = self.find_element_safe(field_selectors, "textarea")
        if element:
            try:
                # Clear existing content
                element.clear()
                time.sleep(0.5)
                
                # Fill with new value
                element.send_keys(value)
                logger.info(f"Filled {field_name}: {value[:50]}...")
                return True
            except Exception as e:
                logger.warning(f"Failed to fill {field_name}: {e}")
        else:
            logger.warning(f"Could not find textarea field for {field_name}")
        
        return False
    
    def fill_personal_info(self):
        """Fill out personal information fields."""
        logger.info("Filling personal information...")
        
        # Common selectors for personal info fields
        field_mappings = {
            "first_name": [
                "input[name*='first']", "input[name*='firstName']", "input[id*='first']",
                "input[placeholder*='First']", "input[placeholder*='first']"
            ],
            "last_name": [
                "input[name*='last']", "input[name*='lastName']", "input[id*='last']",
                "input[placeholder*='Last']", "input[placeholder*='last']"
            ],
            "email": [
                "input[type='email']", "input[name*='email']", "input[id*='email']",
                "input[placeholder*='Email']", "input[placeholder*='email']"
            ],
            "phone": [
                "input[type='tel']", "input[name*='phone']", "input[id*='phone']",
                "input[placeholder*='Phone']", "input[placeholder*='phone']"
            ],
            "address": [
                "input[name*='address']", "input[id*='address']", "input[placeholder*='Address']"
            ],
            "city": [
                "input[name*='city']", "input[id*='city']", "input[placeholder*='City']"
            ],
            "state": [
                "input[name*='state']", "input[id*='state']", "input[placeholder*='State']",
                "select[name*='state']", "select[id*='state']"
            ],
            "zip_code": [
                "input[name*='zip']", "input[name*='postal']", "input[id*='zip']",
                "input[placeholder*='Zip']", "input[placeholder*='Postal']"
            ]
        }
        
        filled_count = 0
        for field, selectors in field_mappings.items():
            if field in config.PERSONAL_INFO:
                value = config.PERSONAL_INFO[field]
                
                if field == "state":
                    success = self.fill_select_field(value, selectors, field)
                else:
                    success = self.fill_text_field(value, selectors, field)
                
                if success:
                    filled_count += 1
                time.sleep(0.5)  # Small delay between fields
        
        logger.info(f"Filled {filled_count} personal information fields")
        return filled_count
    
    def fill_work_experience(self):
        """Fill out work experience fields."""
        logger.info("Filling work experience...")
        
        # This is a simplified version - work experience fields vary greatly
        # You may need to customize this based on specific job sites
        
        if not config.WORK_EXPERIENCE:
            logger.info("No work experience configured")
            return 0
        
        # Try to fill most recent job
        latest_job = config.WORK_EXPERIENCE[0]
        
        field_mappings = {
            "company": [
                "input[name*='company']", "input[id*='company']", "input[placeholder*='Company']"
            ],
            "position": [
                "input[name*='title']", "input[name*='position']", "input[id*='title']",
                "input[placeholder*='Title']", "input[placeholder*='Position']"
            ],
            "start_date": [
                "input[name*='start']", "input[id*='start']", "input[placeholder*='Start']"
            ],
            "end_date": [
                "input[name*='end']", "input[id*='end']", "input[placeholder*='End']"
            ],
            "description": [
                "textarea[name*='description']", "textarea[id*='description']",
                "textarea[placeholder*='Description']"
            ]
        }
        
        filled_count = 0
        for field, selectors in field_mappings.items():
            if field in latest_job:
                value = latest_job[field]
                
                if field == "description":
                    success = self.fill_textarea_field(value, selectors, field)
                else:
                    success = self.fill_text_field(value, selectors, field)
                
                if success:
                    filled_count += 1
                time.sleep(0.5)
        
        logger.info(f"Filled {filled_count} work experience fields")
        return filled_count
    
    def fill_education(self):
        """Fill out education fields."""
        logger.info("Filling education information...")
        
        if not config.EDUCATION:
            logger.info("No education information configured")
            return 0
        
        # Use the highest degree by default, or the first one if none marked as highest
        education_info = None
        for edu in config.EDUCATION:
            if edu.get("is_highest", False):
                education_info = edu
                break
        
        if not education_info and config.EDUCATION:
            education_info = config.EDUCATION[0]  # Use first degree if none marked as highest
        
        if not education_info:
            logger.info("No education information available")
            return 0
        
        field_mappings = {
            "degree": [
                "input[name*='degree']", "input[id*='degree']", "select[name*='degree']",
                "select[id*='degree']", "input[placeholder*='Degree']"
            ],
            "field_of_study": [
                "input[name*='major']", "input[name*='field']", "input[id*='major']",
                "input[placeholder*='Major']", "input[placeholder*='Field']"
            ],
            "university": [
                "input[name*='school']", "input[name*='university']", "input[id*='school']",
                "input[placeholder*='School']", "input[placeholder*='University']"
            ],
            "graduation_year": [
                "input[name*='graduation']", "input[name*='year']", "input[id*='graduation']",
                "input[placeholder*='Graduation']", "input[placeholder*='Year']"
            ]
        }
        
        filled_count = 0
        for field, selectors in field_mappings.items():
            if field in education_info:
                value = education_info[field]
                
                if field == "degree":
                    success = self.fill_select_field(value, selectors, field)
                else:
                    success = self.fill_text_field(value, selectors, field)
                
                if success:
                    filled_count += 1
                time.sleep(0.5)
        
        logger.info(f"Filled {filled_count} education fields")
        return filled_count
    
    def fill_common_questions(self):
        """Fill out common application questions."""
        logger.info("Filling common questions...")
        
        # Common question field patterns
        question_patterns = [
            "textarea[name*='why']", "textarea[name*='interest']", "textarea[name*='motivation']",
            "textarea[name*='salary']", "textarea[name*='expectation']", "textarea[name*='availability']",
            "textarea[name*='relocation']", "textarea[name*='authorization']", "textarea[name*='notice']"
        ]
        
        filled_count = 0
        for pattern in question_patterns:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        # Try to match question content to appropriate answer
                        placeholder = element.get_attribute("placeholder") or ""
                        name = element.get_attribute("name") or ""
                        
                        # Simple matching logic
                        if any(word in (placeholder + name).lower() for word in ["why", "interest", "motivation"]):
                            answer = config.COMMON_ANSWERS.get("why_interested", "")
                        elif any(word in (placeholder + name).lower() for word in ["salary", "expectation"]):
                            answer = config.COMMON_ANSWERS.get("salary_expectation", "")
                        elif any(word in (placeholder + name).lower() for word in ["availability", "start"]):
                            answer = config.COMMON_ANSWERS.get("availability", "")
                        elif any(word in (placeholder + name).lower() for word in ["relocation"]):
                            answer = config.COMMON_ANSWERS.get("relocation", "")
                        elif any(word in (placeholder + name).lower() for word in ["authorization", "work"]):
                            answer = config.COMMON_ANSWERS.get("work_authorization", "")
                        elif any(word in (placeholder + name).lower() for word in ["notice"]):
                            answer = config.COMMON_ANSWERS.get("notice_period", "")
                        else:
                            continue
                        
                        if answer:
                            element.clear()
                            time.sleep(0.5)
                            element.send_keys(answer)
                            filled_count += 1
                            logger.info(f"Filled question field: {placeholder or name}")
                            break
            except Exception as e:
                logger.warning(f"Error filling question field: {e}")
        
        logger.info(f"Filled {filled_count} common question fields")
        return filled_count
    
    def auto_fill_application(self, url):
        """
        Main method to auto-fill a job application.
        
        Args:
            url (str): URL of the job application page
        """
        try:
            logger.info(f"Starting auto-fill for: {url}")
            
            # Navigate to the application page
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Fill out different sections
            personal_filled = self.fill_personal_info()
            work_filled = self.fill_work_experience()
            education_filled = self.fill_education()
            questions_filled = self.fill_common_questions()
            
            total_filled = personal_filled + work_filled + education_filled + questions_filled
            
            logger.info(f"Auto-fill completed! Filled {total_filled} fields total:")
            logger.info(f"  - Personal info: {personal_filled} fields")
            logger.info(f"  - Work experience: {work_filled} fields")
            logger.info(f"  - Education: {education_filled} fields")
            logger.info(f"  - Common questions: {questions_filled} fields")
            
            # Show notification
            self.show_completion_notification(total_filled)
            
            return total_filled
            
        except Exception as e:
            logger.error(f"Error during auto-fill: {e}")
            raise
    
    def show_completion_notification(self, fields_filled):
        """Show a notification that auto-fill is complete."""
        try:
            # Create a simple notification window
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            messagebox.showinfo(
                "Auto-Fill Complete!",
                f"Job application auto-fill completed!\n\n"
                f"Filled {fields_filled} fields automatically.\n\n"
                f"Please review the form and submit manually.\n"
                f"The browser will remain open for your review."
            )
            
            root.destroy()
            
        except Exception as e:
            logger.warning(f"Could not show notification: {e}")
            print(f"\n{'='*50}")
            print("AUTO-FILL COMPLETE!")
            print(f"Filled {fields_filled} fields automatically.")
            print("Please review the form and submit manually.")
            print(f"{'='*50}\n")
    
    def close(self):
        """Close the browser and clean up."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed") 