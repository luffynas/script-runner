import os
import random
import time
import logging
import sys
import requests
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


def setup_logging():
    """
    Setup logging mengikuti pattern cookie_robot.py
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s'))
    logging.getLogger(name='simple_advanced_robot').addHandler(console_handler)


class SimpleAdvancedRobot:
    """
    Simple Advanced Robot mengikuti pattern cookie_robot.py
    """
    
    def __init__(self, driver, process_advanced_features=True, random_behavior=True):
        self.driver = driver
        self.process_advanced_features = process_advanced_features
        self.random_behavior = random_behavior
        
        logging.info(f'SimpleAdvancedRobot initialized')
        logging.info(f'Advanced features processing: {self.process_advanced_features}')
        logging.info(f'Random behavior: {self.random_behavior}')
    
    def human_like_delay(self, min_delay=0.5, max_delay=3.0):
        """Generate human-like delay"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay
    
    def random_mouse_movement(self, duration=1.0):
        """Simple random mouse movement"""
        try:
            viewport_size = self.driver.execute_script("return {width: window.innerWidth, height: window.innerHeight}")
            start_time = time.time()
            
            while time.time() - start_time < duration:
                x = random.randint(0, viewport_size['width'])
                y = random.randint(0, viewport_size['height'])
                
                self.driver.execute_script(f"""
                    var event = new MouseEvent('mousemove', {{
                        clientX: {x},
                        clientY: {y},
                        bubbles: true
                    }});
                    document.dispatchEvent(event);
                """)
                time.sleep(random.uniform(0.1, 0.3))
                
        except Exception as e:
            logging.warning(f"Mouse movement failed: {e}")
    
    def random_scroll(self, min_scrolls=2, max_scrolls=5):
        """Random scrolling behavior"""
        try:
            scroll_count = random.randint(min_scrolls, max_scrolls)
            for _ in range(scroll_count):
                scroll_height = self.driver.execute_script("return document.body.scrollHeight")
                scroll_position = random.randint(0, scroll_height)
                
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                self.human_like_delay(0.5, 2.0)
                
        except Exception as e:
            logging.warning(f"Random scroll failed: {e}")
    
    def check_for_captcha(self):
        """Simple CAPTCHA detection"""
        try:
            captcha_selectors = [
                "iframe[src*='recaptcha']",
                ".g-recaptcha",
                "#captcha",
                ".captcha"
            ]
            
            for selector in captcha_selectors:
                try:
                    if self.driver.find_element(By.CSS_SELECTOR, selector):
                        logging.warning("CAPTCHA detected!")
                        return True
                except NoSuchElementException:
                    continue
            
            return False
        except Exception as e:
            logging.warning(f"Error checking for CAPTCHA: {e}")
            return False
    
    def open_article_with_referer(self, article_url, referer_url=None):
        """Open article with referer simulation"""
        try:
            logging.info(f"Opening article: {article_url}")
            
            if referer_url:
                logging.info(f"Using referer: {referer_url}")
                # Navigate to referer first
                self.driver.get(referer_url)
                self.human_like_delay(2, 4)
                
                # Simulate browsing on referer
                self.random_scroll(1, 3)
                self.random_mouse_movement(random.uniform(1, 2))
                self.human_like_delay(2, 4)
            
            # Navigate to article
            self.driver.get(article_url)
            
            # Wait for page load
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            logging.info("Article loaded successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error opening article: {e}")
            return False
    
    def browse_article_content(self, duration_minutes=5):
        """Browse article content with human-like behavior"""
        try:
            logging.info(f"Browsing article content for {duration_minutes} minutes")
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while time.time() < end_time:
                # Check for CAPTCHA
                if self.check_for_captcha():
                    logging.warning("CAPTCHA detected - implementing cooldown")
                    self.human_like_delay(10, 20)
                    continue
                
                # Random actions
                action = random.choice(['scroll', 'mouse_move', 'pause', 'click_link'])
                
                if action == 'scroll':
                    self.random_scroll(1, 3)
                elif action == 'mouse_move':
                    self.random_mouse_movement(random.uniform(0.5, 2.0))
                elif action == 'pause':
                    self.human_like_delay(2, 5)
                elif action == 'click_link':
                    self._try_click_random_link()
                
                # Wait between actions
                self.human_like_delay(1, 3)
            
            logging.info("Article browsing completed")
            return True
            
        except Exception as e:
            logging.error(f"Error browsing article content: {e}")
            return False
    
    def _try_click_random_link(self):
        """Try to click a random link"""
        try:
            # Find clickable links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            clickable_links = []
            
            for link in links:
                try:
                    if link.is_displayed() and link.is_enabled():
                        href = link.get_attribute("href")
                        if href and not href.startswith("javascript:"):
                            clickable_links.append(link)
                except:
                    continue
            
            if clickable_links:
                random_link = random.choice(clickable_links)
                
                # Move mouse to link
                ActionChains(self.driver).move_to_element(random_link).perform()
                self.human_like_delay(0.5, 1.5)
                
                # Click link
                random_link.click()
                
                # Wait for page load
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                logging.info("Clicked random link successfully")
                
        except Exception as e:
            logging.warning(f"Error clicking random link: {e}")
    
    def open_rexdl_cloud_article(self):
        """Open RexDL Cloud Migration article"""
        article_url = "https://rexdl.biz.id/cloud-migration-challenges-in-the-us-and-how-to-overcome-them/"
        referer_options = [
            "https://google.com", "https://yahoo.com", "https://bing.com",
            "https://reddit.com", "https://twitter.com", "https://linkedin.com",
            "https://github.com", "https://stackoverflow.com", "https://medium.com"
        ]
        
        referer_url = random.choice(referer_options)
        
        logging.info(f"Opening RexDL Cloud Migration article with referer: {referer_url}")
        
        success = self.open_article_with_referer(article_url, referer_url)
        if success:
            browse_success = self.browse_article_content(duration_minutes=3)
            if browse_success:
                logging.info("RexDL article browsing completed successfully")
                return True
            else:
                logging.error("RexDL article browsing failed")
                return False
        else:
            logging.error("Failed to open RexDL article")
            return False
    
    def run_automation(self):
        """Main automation function"""
        try:
            logging.info("Starting simple advanced automation")
            
            # Test basic driver functionality
            try:
                current_url = self.driver.current_url
                logging.info(f"Current URL: {current_url}")
            except Exception as e:
                logging.warning(f"Could not get current URL: {e}")
            
            # Maximize window
            try:
                self.driver.maximize_window()
                logging.info("Window maximized successfully")
            except Exception as e:
                logging.warning(f"Failed to maximize window: {e}")
            
            # Wait for initial setup
            self.human_like_delay(2, 4)
            
            if self.process_advanced_features:
                # Run advanced article browsing
                success = self.open_rexdl_cloud_article()
                
                if success:
                    logging.info("✅ Simple advanced automation completed successfully!")
                else:
                    logging.error("❌ Simple advanced automation failed")
            else:
                logging.info("Skipping advanced features processing")
            
            # Keep browser open for inspection
            logging.info("⏳ Keeping browser open for 30 seconds...")
            time.sleep(30)
            
            logging.info("✅ Simple advanced automation completed!")
            
        except Exception as e:
            logging.error(f"Error in simple advanced automation: {e}", exc_info=True)
            
            # Keep browser open even on error
            logging.info("⏳ Keeping browser open for 15 seconds after error...")
            time.sleep(15)
    
    def run(self):
        """Main run function mengikuti pattern cookie_robot.py"""
        self.run_automation()


# Setup logging
setup_logging()

# Input parameters (mengikuti pattern cookie_robot.py)
inputparams = inputparams or {}
process_advanced_features = True
random_behavior = True

# Override with input parameters
if 'process_advanced_features' in inputparams:
    process_advanced_features = inputparams['process_advanced_features']

if 'random_behavior' in inputparams:
    random_behavior = inputparams['random_behavior']

logging.info('Simple Advanced Robot started')
logging.info(f'inputparams: {inputparams}')
logging.info(f'process_advanced_features: {process_advanced_features}')
logging.info(f'random_behavior: {random_behavior}')

# Create and run robot (mengikuti pattern cookie_robot.py)
robot = SimpleAdvancedRobot(
    driver=driver,
    process_advanced_features=process_advanced_features,
    random_behavior=random_behavior
)

robot.run()
