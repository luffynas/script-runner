#!/usr/bin/env python3
"""
Fixed Multilogin Automation Script
==================================
Clean automation script without syntax errors
"""

import os
import random
import time
import logging
import requests
import sys
import json
from datetime import datetime
from urllib.parse import urlparse, urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as Ac
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Global variables for Multilogin integration
PROFILE_ID = None
FOLDER_ID = None
AUTOMATION_CONFIG = {}

# Enhanced URL list for realistic browsing
ENHANCED_URLS = [
    "https://google.com",
    "https://youtube.com",
    "https://amazon.com",
    "https://ebay.com",
    "https://reddit.com",
    "https://twitter.com",
    "https://facebook.com",
    "https://instagram.com",
    "https://linkedin.com",
    "https://github.com"
]

class AdSenseAutoClick:
    """AdSense Auto Click functionality with smart probability"""
    
    def __init__(self, driver, logger=None):
        self.driver = driver
        self.logger = logger or logging.getLogger(__name__)
        
        # AdSense selectors
        self.adsense_selectors = [
            "ins.adsbygoogle",
            "div[id*='google_ads']",
            "div[id*='div-gpt-ad']",
            "iframe[id*='google_ads']",
            "div[class*='adsbygoogle']",
            "div[id*='ad-']",
            "div[class*='ad-']",
            "div[class*='ads-']",
            "div[class*='advertisement']",
            "div[class*='banner']"
        ]
        
        # Commercial keywords for intent detection
        self.commercial_keywords = [
            'buy', 'purchase', 'order', 'shop', 'cart', 'checkout',
            'price', 'cost', 'sale', 'discount', 'offer', 'deal',
            'product', 'service', 'subscription', 'membership',
            'crypto', 'investment', 'trading', 'nft', 'blockchain'
        ]
    
    def detect_adsense_ads(self):
        """Detect AdSense ads on current page"""
        try:
            ads_found = 0
            ad_details = []
            
            for selector in self.adsense_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        if element.is_displayed():
                            ad_info = {
                                'selector': selector,
                                'text': element.text[:100] if element.text else '',
                                'location': element.location,
                                'size': element.size,
                                'element': element
                            }
                            ad_details.append(ad_info)
                            ads_found += 1
                    except:
                        continue
            
            return {
                'ads_detected': ads_found,
                'details': ad_details
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_commercial_intent(self):
        """Analyze page content for commercial intent"""
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            
            commercial_score = 0
            for keyword in self.commercial_keywords:
                if keyword in page_text:
                    commercial_score += 1
            
            # Determine commercial category and click probability
            if commercial_score > 10:
                commercial_category = 'high'
                click_probability = 0.05  # 5% chance
            elif commercial_score > 5:
                commercial_category = 'medium'
                click_probability = 0.02  # 2% chance
            else:
                commercial_category = 'low'
                click_probability = 0.01  # 1% chance
            
            return {
                'commercial_category': commercial_category,
                'commercial_score': commercial_score,
                'click_probability': click_probability
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def click_ad(self, ad_element):
        """Click on an ad element with multiple methods"""
        try:
            # Method 1: Direct click
            try:
                ad_element.click()
                self.logger.info("Ad clicked successfully (direct method)")
                return True
            except:
                pass
            
            # Method 2: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", ad_element)
                self.logger.info("Ad clicked successfully (JavaScript method)")
                return True
            except:
                pass
            
            # Method 3: ActionChains click
            try:
                Ac(self.driver).move_to_element(ad_element).click().perform()
                self.logger.info("Ad clicked successfully (ActionChains method)")
                return True
            except:
                pass
            
            self.logger.error("All click methods failed")
            return False
        
        except Exception as e:
            self.logger.error(f"Click failed: {e}")
            return False
    
    def handle_ad_landing_page(self):
        """Handle ad landing page after click"""
        try:
            current_url = self.driver.current_url
            
            # Check if we're on an ad landing page
            ad_domains = ['googleadservices', 'doubleclick', 'googlesyndication', 'google-analytics']
            is_ad_page = any(domain in current_url for domain in ad_domains)
            
            if is_ad_page:
                self.logger.info(f"Navigated to ad landing page: {current_url[:60]}...")
                
                # Simulate time on ad page
                time_on_page = random.uniform(5, 15)
                self.logger.info(f"Spending {time_on_page:.1f} seconds on ad page")
                time.sleep(time_on_page)
                
                # Go back to original page
                self.driver.back()
                time.sleep(random.uniform(2, 4))
                self.logger.info("Returned to original page")
                return True
            
            return False
        
        except Exception as e:
            self.logger.error(f"Error handling ad landing page: {e}")
            return False
    
    def auto_click_ads(self, max_ads=3, enable_clicking=True):
        """Main function to auto click AdSense ads"""
        try:
            self.logger.info("Starting AdSense Auto Click")
            
            # Detect ads
            adsense_results = self.detect_adsense_ads()
            if "error" in adsense_results:
                self.logger.error(f"AdSense detection failed: {adsense_results['error']}")
                return {'status': 'detection_failed', 'error': adsense_results['error']}
            
            ads = adsense_results.get('details', [])
            if not ads:
                self.logger.info("No AdSense ads found on this page")
                return {'status': 'no_ads_found', 'ads_detected': 0}
            
            self.logger.info(f"Found {len(ads)} AdSense ads")
            
            # Analyze commercial intent
            intent_results = self.analyze_commercial_intent()
            if "error" in intent_results:
                click_probability = 0.01  # Default 1% chance
                commercial_category = 'unknown'
                self.logger.warning(f"Intent analysis failed, using default probability: {click_probability*100:.1f}%")
            else:
                click_probability = intent_results.get('click_probability', 0.01)
                commercial_category = intent_results.get('commercial_category', 'low')
                self.logger.info(f"Commercial intent: {commercial_category} (score: {intent_results.get('commercial_score', 0)})")
                self.logger.info(f"Click probability: {click_probability*100:.1f}%")
            
            # Process ads
            ads_processed = 0
            ads_clicked = 0
            
            for i, ad in enumerate(ads[:max_ads]):
                try:
                    ads_processed += 1
                    self.logger.info(f"Processing ad {i+1}/{min(len(ads), max_ads)}...")
                    
                    # Get ad element
                    ad_element = ad.get('element')
                    if not ad_element:
                        continue
                    
                    # Scroll to ad
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad_element)
                    time.sleep(random.uniform(1, 3))
                    
                    # Simulate hover
                    Ac(self.driver).move_to_element(ad_element).perform()
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    # Simulate reading ad content
                    ad_text = ad.get('text', '')[:50]
                    self.logger.info(f"Reading ad content: {ad_text}...")
                    time.sleep(random.uniform(2, 4))
                    
                    # Decide whether to click
                    if enable_clicking and random.random() < click_probability:
                        self.logger.info(f"Deciding to click ad (probability: {click_probability*100:.1f}%)")
                        
                        # Click the ad
                        if self.click_ad(ad_element):
                            ads_clicked += 1
                            
                            # Handle landing page
                            self.handle_ad_landing_page()
                    else:
                        self.logger.info(f"Deciding not to click ad (realistic behavior)")
                    
                    # Pause between ads
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as ad_error:
                    self.logger.error(f"Error processing ad {i+1}: {ad_error}")
                    continue
            
            # Summary
            self.logger.info(f"AdSense auto click completed: {ads_clicked}/{ads_processed} ads clicked")
            
            return {
                'status': 'completed',
                'ads_detected': len(ads),
                'ads_processed': ads_processed,
                'ads_clicked': ads_clicked,
                'click_probability': click_probability,
                'commercial_category': commercial_category,
                'enable_clicking': enable_clicking
            }
        
        except Exception as e:
            self.logger.error(f"AdSense auto click failed: {e}")
            return {'status': 'failed', 'error': str(e)}

class CompleteMultiloginAutomation:
    """Complete automation bot with all features integrated"""
    
    def __init__(self, driver, config=None):
        self.driver = driver
        self.config = config or self.get_default_config()
        self.logger = self.setup_logging()
        self.visited_domains = set()
        self.session_start_time = time.time()
        
        # Initialize behavior settings
        self.behavior = self.config.get('behavior', {})
        self.stealth = self.config.get('stealth', {})
        self.targets = self.config.get('targets', {})
        self.adsense_config = self.config.get('adsense', {})
        self.personality = self.config.get('personality', {})
        self.rpm_optimization = self.config.get('rpm_optimization', {})
        
        # Setup websites
        websites = self.config.get('websites', ENHANCED_URLS)
        if self.behavior.get('random_order', False):
            random.shuffle(websites)
        
        if self.behavior.get('fraction_mode', 1.0) != 1.0:
            part = int(len(websites) * self.behavior['fraction_mode'])
            websites = websites[:part]
        
        self.websites = websites
        
        # Initialize AdSense Auto Click
        self.adsense_clicker = AdSenseAutoClick(driver, self.logger)
        
        # Personality and device type
        self.user_personality = self.personality.get('type', 'explorer')
        self.device_type = 'desktop'
        
        # Session data
        self.session_data = {
            "start_time": datetime.now(),
            "personality": self.user_personality,
            "pages_visited": [],
            "interactions": [],
            "adsense_clicks": [],
            "errors": []
        }
        
        self.logger.info(f'CompleteMultiloginAutomation initialized with {len(self.websites)} websites')
        self.logger.info(f'Personality: {self.user_personality}')
        self.logger.info(f'AdSense Auto Click: {self.adsense_config.get("enable_auto_click", False)}')
        self.logger.info(f'RPM Optimization: {self.rpm_optimization.get("enabled", False)}')
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # File handler for persistent logging
        file_handler = logging.FileHandler(f'logs/complete_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))
        
        logger = logging.getLogger('multilogin_automation')
        logger.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def get_default_config(self):
        """Get default automation configuration"""
        return {
            "websites": ENHANCED_URLS,
            "behavior": {
                "random_order": True,
                "fraction_mode": 1.0,
                "process_cookie_consent": True,
                "pages_per_site": 3,
                "scroll_range": [1, 5],
                "sleep_range": [5, 15],
                "timeout_seconds": 180
            },
            "stealth": {
                "simulate_human_behavior": True,
                "random_delays": True,
                "mouse_movements": True,
                "typing_simulation": True
            },
            "targets": {
                "adsense_detection": True,
                "ad_interaction": True,
                "conversion_tracking": False
            },
            "adsense": {
                "enable_auto_click": True,
                "max_ads_per_page": 3,
                "click_probability_override": None,
                "min_time_on_ad_page": 5,
                "max_time_on_ad_page": 15
            },
            "personality": {
                "type": "explorer",
                "attention_span": "medium",
                "reading_speed": "medium",
                "click_probability": 0.3
            },
            "rpm_optimization": {
                "enabled": True,
                "commercial_intent_detection": True,
                "smart_ad_interaction": True,
                "professional_behavior": True
            }
        }
    
    def simulate_human_behavior(self):
        """Simulate realistic human browsing behavior"""
        if not self.stealth.get('simulate_human_behavior', True):
            return
        
        # Random mouse movements
        if self.stealth.get('mouse_movements', True):
            self._simulate_mouse_movements()
        
        # Random delays
        if self.stealth.get('random_delays', True):
            delay = random.uniform(1, 3)
            time.sleep(delay)
    
    def _simulate_mouse_movements(self):
        """Simulate realistic mouse movements"""
        try:
            # Get viewport size
            viewport_width = self.driver.execute_script("return window.innerWidth;")
            viewport_height = self.driver.execute_script("return window.innerHeight;")
            
            # Generate random mouse movements
            for _ in range(random.randint(2, 5)):
                x = random.randint(0, viewport_width)
                y = random.randint(0, viewport_height)
                
                # Move mouse to random position
                Ac(self.driver).move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.1, 0.5))
        
        except Exception as e:
            self.logger.debug(f"Mouse movement simulation failed: {e}")
    
    def _simulate_natural_scrolling(self):
        """Simulate natural scrolling behavior"""
        try:
            # Get page height
            total_height = self.driver.execute_script('return document.body.scrollHeight')
            
            # Scroll in natural patterns
            scroll_positions = [
                total_height * 0.2,
                total_height * 0.4,
                total_height * 0.6,
                total_height * 0.8
            ]
            
            for position in scroll_positions:
                self.driver.execute_script(f'window.scrollTo(0, {position});')
                time.sleep(random.uniform(1, 3))
                
                # Simulate reading behavior
                self._simulate_reading_behavior()
        
        except Exception as e:
            self.logger.debug(f"Natural scrolling failed: {e}")
    
    def _simulate_reading_behavior(self):
        """Simulate reading behavior"""
        try:
            # Find text elements
            text_elements = self.driver.find_elements(By.TAG_NAME, "p")
            
            if text_elements:
                # Select random text element
                element = random.choice(text_elements)
                
                # Scroll to element
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                time.sleep(random.uniform(2, 4))
                
                # Simulate reading time based on text length
                text_length = len(element.text)
                reading_time = min(text_length / 200, 10)  # 200 chars per second, max 10 seconds
                time.sleep(reading_time)
        
        except Exception as e:
            self.logger.debug(f"Reading behavior simulation failed: {e}")
    
    def _simulate_link_hovering(self):
        """Simulate link hovering behavior"""
        try:
            # Find clickable links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            
            if links:
                # Select random link
                link = random.choice(links)
                
                # Hover over link
                Ac(self.driver).move_to_element(link).perform()
                time.sleep(random.uniform(0.5, 1.5))
        
        except Exception as e:
            self.logger.debug(f"Link hovering simulation failed: {e}")
    
    def _simulate_realistic_typing(self):
        """Simulate realistic typing behavior"""
        try:
            # Find input fields
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            
            if inputs:
                # Select random input
                input_field = random.choice(inputs)
                
                # Focus on input
                input_field.click()
                time.sleep(random.uniform(0.5, 1))
                
                # Sample texts
                sample_texts = [
                    "hello world",
                    "test message",
                    "automation script",
                    "multilogin test"
                ]
                
                text = random.choice(sample_texts)
                
                # Type with realistic delays
                for char in text:
                    input_field.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
        
        except Exception as e:
            self.logger.debug(f"Typing simulation failed: {e}")
    
    def allow_cookies(self, site):
        """Handle cookie consent for various websites"""
        if not self.behavior.get('process_cookie_consent', True):
            return
        
        self.logger.info(f'Processing cookie consent for {site}')
        
        site_cookie_selectors = {
            'twitter': (By.XPATH, "//button[contains(., 'Accept all cookies')]"),
            'youtube': (By.XPATH, "//button[contains(., 'Accept all')]"),
            'amazon': (By.ID, "sp-cc-accept"),
            'google': (By.ID, "L2AGLb"),
            'ebay': (By.ID, "gdpr-banner-accept"),
            'aliexpress': (By.XPATH, "//button[contains(@class, 'btn-accept')]"),
            'fiverr': (By.ID, "onetrust-accept-btn-handler"),
            'yahoo': (By.XPATH, "//button[@name='agree' and @value='agree']"),
            'twitch': (By.XPATH, "//button[@data-a-target='consent-banner-accept']"),
            'instagram': (By.XPATH, "//button[contains(@class, '_a9--') and contains(@class, '_a9_1')]")
        }
        
        try:
            # Try specific site selectors first
            for site_key, (by, selector) in site_cookie_selectors.items():
                if site_key in site:
                    if self._handle_cookie_button((by, selector), max_retries=3):
                        self.logger.info(f'Successfully handled cookies for {site_key}')
                        return
                    break
            
            # Try Reddit-specific handling
            if 'reddit' in site:
                if self._handle_reddit_cookies():
                    self.logger.info("Successfully handled Reddit cookies")
                    return
            
            # Fallback to generic cookie handling
            if self._generic_allow_cookies():
                self.logger.info("Successfully handled cookies using generic method")
                return
            
            self.logger.warning(f'Failed to handle cookies for {site}')
        
        except Exception as e:
            self.logger.error(f'Error handling cookies for {site}: {e}')
    
    def _handle_cookie_button(self, locator, max_retries=3):
        """Handle cookie button clicking with retries"""
        wait = WebDriverWait(self.driver, 10)
        
        for attempt in range(max_retries):
            try:
                if wait.until(EC.presence_of_element_located(locator)):
                    button = wait.until(EC.element_to_be_clickable(locator))
                    
                    # Scroll to button
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(1)
                    
                    # Click button
                    try:
                        Ac(self.driver).move_to_element(button).click().perform()
                    except:
                        button.click()
                    
                    time.sleep(2)
                    
                    # Check if button disappeared
                    if wait.until(EC.invisibility_of_element_located(locator)):
                        return True
                
            except Exception as e:
                self.logger.debug(f'Cookie button attempt {attempt + 1} failed: {e}')
                if attempt < max_retries - 1:
                    self.driver.refresh()
                    time.sleep(3)
        
        return False
    
    def _handle_reddit_cookies(self):
        """Handle Reddit's shadow DOM cookie banner"""
        try:
            # Wait for shadow host
            shadow_host = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "reddit-cookie-banner"))
            )
            
            # Get shadow root
            shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", shadow_host)
            
            # Find accept button in shadow DOM
            accept_button = shadow_root.find_element(By.CSS_SELECTOR, "#accept-all-cookies-button")
            
            # Click accept button
            self.driver.execute_script("arguments[0].click();", accept_button)
            time.sleep(2)
            
            return True
        
        except Exception as e:
            self.logger.debug(f'Reddit cookie handling failed: {e}')
            return False
    
    def _generic_allow_cookies(self):
        """Generic cookie acceptance using common text patterns"""
        translations = [
            "Accept", "allow all cookies", "accept all cookies", "accept cookies",
            "alle akzeptieren", "alle cookies akzeptieren", "cookies akzeptieren",
            "accepter tout", "accepter tous les cookies", "accepter les cookies",
            "aceitar todos", "aceitar todos os cookies", "aceitar cookies",
            "aceptar todo", "aceptar todas las cookies", "aceptar cookies",
            "accetta tutto", "accetta tutti i cookie", "accetta i cookie",
            "permitir tudo", "permitir todos os cookies", "permitir cookies",
            "permitir todo", "permitir todas las cookies", "permitir cookies"
        ]
        
        xpath_conditions = " or ".join([
            f"contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{translation.lower()}')"
            for translation in translations
        ])
        
        xpath = f"//button[{xpath_conditions}] | //div[@role='button'][{xpath_conditions}]"
        
        try:
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Scroll to button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            
            # Click button
            try:
                Ac(self.driver).move_to_element(button).click().perform()
            except:
                button.click()
            
            time.sleep(2)
            return True
        
        except Exception as e:
            self.logger.debug(f'Generic cookie handling failed: {e}')
            return False
    
    def run_personality_system(self):
        """Run personality system"""
        try:
            self.logger.info("Running Personality System")
            
            # Personality-specific behaviors
            behaviors = [
                ("scrolling", "Natural scrolling"),
                ("reading", "Reading behavior"),
                ("mouse", "Mouse interactions"),
                ("typing", "Typing simulation")
            ]
            
            for behavior_type, description in behaviors:
                try:
                    self.logger.info(f"  {description}...")
                    
                    if behavior_type == "scrolling":
                        self._simulate_natural_scrolling()
                    elif behavior_type == "reading":
                        self._simulate_reading_behavior()
                    elif behavior_type == "mouse":
                        self._simulate_mouse_movements()
                        self._simulate_link_hovering()
                    elif behavior_type == "typing":
                        self._simulate_realistic_typing()
                    
                    # Record interaction
                    self.session_data["interactions"].append({
                        "type": behavior_type,
                        "personality": self.user_personality,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    time.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"    {behavior_type} failed: {e}")
        
        except Exception as e:
            self.logger.error(f"Personality system failed: {e}")
    
    def run_navigation_system(self):
        """Run navigation system"""
        try:
            self.logger.info("Running Navigation System")
            
            # Navigate to multiple pages (3-5 pages total)
            pages_visited = 1  # Current page
            max_pages = random.randint(3, 5)
            
            self.logger.info(f"Target: {max_pages} pages total")
            
            while pages_visited < max_pages:
                # Try to navigate to next/previous page
                new_url = self._navigate_previous_next()
                
                if new_url:
                    self.logger.info(f"Navigating to page {pages_visited + 1}/{max_pages}")
                    self.driver.get(new_url)
                    time.sleep(random.uniform(2, 4))
                    
                    # Record navigation
                    self.session_data["pages_visited"].append({
                        "url": new_url,
                        "timestamp": datetime.now().isoformat(),
                        "title": self.driver.title
                    })
                    
                    # Simulate behavior on new page
                    self._simulate_natural_scrolling()
                    self._simulate_mouse_movements()
                    
                    pages_visited += 1
                else:
                    # Try random page navigation if prev/next not available
                    random_url = self._navigate_random_page()
                    if random_url:
                        self.logger.info(f"Navigating to random page {pages_visited + 1}/{max_pages}")
                        self.driver.get(random_url)
                        time.sleep(random.uniform(2, 4))
                        
                        # Record navigation
                        self.session_data["pages_visited"].append({
                            "url": random_url,
                            "timestamp": datetime.now().isoformat(),
                            "title": self.driver.title
                        })
                        
                        # Simulate behavior on new page
                        self._simulate_natural_scrolling()
                        self._simulate_mouse_movements()
                        
                        pages_visited += 1
                    else:
                        self.logger.info(f"No more navigation links found, stopping at {pages_visited} pages")
                        break
            
            self.logger.info(f"Visited {pages_visited} pages total")
        
        except Exception as e:
            self.logger.error(f"Navigation system failed: {e}")
    
    def _navigate_previous_next(self):
        """Navigate to next/previous page"""
        try:
            # Look for navigation elements
            nav_selectors = [
                "a[rel='next']",
                "a[rel='prev']",
                ".next",
                ".previous",
                ".pagination a",
                "a:contains('Next')",
                "a:contains('Previous')"
            ]
            
            for selector in nav_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        href = element.get_attribute("href")
                        if href and href != self.driver.current_url:
                            return href
                except:
                    continue
            
            return None
        
        except Exception as e:
            self.logger.debug(f"Navigation failed: {e}")
            return None
    
    def _navigate_random_page(self):
        """Navigate to random page on same domain"""
        try:
            # Find all links on current page
            links = self.driver.find_elements(By.TAG_NAME, "a")
            
            valid_links = []
            current_domain = urlparse(self.driver.current_url).netloc
            
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if href and current_domain in href and href != self.driver.current_url:
                        valid_links.append(href)
                except:
                    continue
            
            if valid_links:
                return random.choice(valid_links)
            
            return None
        
        except Exception as e:
            self.logger.debug(f"Random navigation failed: {e}")
            return None
    
    def run_adsense_auto_click(self):
        """Run AdSense auto click functionality"""
        try:
            self.logger.info("Running AdSense Auto Click")
            
            # Check if AdSense auto click is enabled
            if not self.adsense_config.get('enable_auto_click', True):
                self.logger.info("AdSense auto click is disabled in config")
                return {'status': 'disabled', 'reason': 'config_disabled'}
            
            # Check if ad interaction is enabled
            if not self.targets.get('ad_interaction', False):
                self.logger.info("Ad interaction is disabled in targets")
                return {'status': 'disabled', 'reason': 'targets_disabled'}
            
            # Get configuration
            max_ads = self.adsense_config.get('max_ads_per_page', 3)
            enable_clicking = self.adsense_config.get('enable_auto_click', True)
            
            # Run AdSense auto click
            results = self.adsense_clicker.auto_click_ads(
                max_ads=max_ads,
                enable_clicking=enable_clicking
            )
            
            # Record results
            self.session_data["adsense_clicks"].append({
                "timestamp": datetime.now().isoformat(),
                "results": results
            })
            
            # Record interaction
            self.session_data["interactions"].append({
                "type": "adsense_auto_click",
                "results": results,
                "timestamp": datetime.now().isoformat()
            })
            
            return results
        
        except Exception as e:
            self.logger.error(f"AdSense auto click failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def run_google_search(self):
        """Run Google search for maxgaming.biz.id"""
        try:
            self.logger.info("Starting Google search automation")
            
            # Navigate to Google
            self.logger.info("Navigating to Google...")
            self.driver.get("https://www.google.com")
            time.sleep(random.uniform(2, 4))
            
            # Handle Google cookie consent
            self.allow_cookies("https://www.google.com")
            
            # Find search box with stealth approach
            self.logger.info("Looking for search box...")
            search_selectors = [
                "input[name='q']",
                "textarea[name='q']",
                "input[title='Search']",
                "input[aria-label='Search']"
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    self.logger.info(f"Found search box with selector: {selector}")
                    break
                except:
                    continue
            
            if not search_box:
                self.logger.error("Could not find Google search box")
                return False
            
            # Simulate human-like typing
            self.logger.info("Typing search query...")
            search_query = "site:maxgaming.biz.id"
            
            # Clear search box first
            search_box.clear()
            time.sleep(random.uniform(0.5, 1))
            
            # Type with realistic delays
            for char in search_query:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(1, 2))
            
            # Press Enter to search
            self.logger.info("Submitting search...")
            search_box.send_keys(Keys.RETURN)
            time.sleep(random.uniform(3, 5))
            
            # Wait for search results
            self.logger.info("Waiting for search results...")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#search"))
            )
            
            # Look for maxgaming.biz.id results
            self.logger.info("Looking for maxgaming.biz.id results...")
            result_selectors = [
                "a[href*='maxgaming.biz.id']",
                "a[href*='maxgaming']",
                "div.g a[href*='maxgaming']"
            ]
            
            maxgaming_link = None
            for selector in result_selectors:
                try:
                    links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for link in links:
                        href = link.get_attribute("href")
                        if href and "maxgaming.biz.id" in href:
                            maxgaming_link = link
                            self.logger.info(f"Found maxgaming link: {href}")
                            break
                    if maxgaming_link:
                        break
                except:
                    continue
            
            if not maxgaming_link:
                self.logger.error("Could not find maxgaming.biz.id link in search results")
                return False
            
            # Simulate human-like clicking
            self.logger.info("Clicking on maxgaming.biz.id link...")
            
            # Scroll to link
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", maxgaming_link)
            time.sleep(random.uniform(1, 2))
            
            # Hover over link
            Ac(self.driver).move_to_element(maxgaming_link).perform()
            time.sleep(random.uniform(0.5, 1))
            
            # Click the link
            maxgaming_link.click()
            time.sleep(random.uniform(3, 5))
            
            # Verify we're on maxgaming.biz.id
            current_url = self.driver.current_url
            if "maxgaming.biz.id" in current_url:
                self.logger.info(f"Successfully navigated to maxgaming.biz.id: {current_url}")
                return True
            else:
                self.logger.warning(f"Not on maxgaming.biz.id, current URL: {current_url}")
                return False
                
        except Exception as e:
            self.logger.error(f"Google search automation failed: {e}")
            return False
    
    def run_maxgaming_automation(self):
        """Run automation specifically for maxgaming.biz.id"""
        try:
            self.logger.info("Starting maxgaming.biz.id automation")
            
            # Wait for page to load
            time.sleep(random.uniform(2, 4))
            
            # Handle cookie consent for maxgaming
            self.allow_cookies(self.driver.current_url)
            
            # Record page visit
            self.session_data["pages_visited"].append({
                "url": self.driver.current_url,
                "timestamp": datetime.now().isoformat(),
                "title": self.driver.title
            })
            
            # Run personality system (human behavior simulation)
            self.logger.info("Running personality system on maxgaming.biz.id...")
            self.run_personality_system()
            
            # Run navigation system (browse multiple pages)
            self.logger.info("Running navigation system on maxgaming.biz.id...")
            self.run_navigation_system()
            
            # Run AdSense auto click (if ads are present)
            self.logger.info("Running AdSense auto click on maxgaming.biz.id...")
            self.run_adsense_auto_click()
            
            # Additional maxgaming-specific automation
            self._run_maxgaming_specific_actions()
            
            self.logger.info("maxgaming.biz.id automation completed")
            
        except Exception as e:
            self.logger.error(f"maxgaming.biz.id automation failed: {e}")
    
    def _run_maxgaming_specific_actions(self):
        """Run maxgaming-specific automation actions"""
        try:
            self.logger.info("Running maxgaming-specific actions...")
            
            # Look for product categories
            category_selectors = [
                "a[href*='category']",
                "a[href*='product']",
                ".category a",
                ".menu a",
                "nav a"
            ]
            
            for selector in category_selectors:
                try:
                    links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if links:
                        # Click on a random category
                        random_link = random.choice(links[:3])  # Choose from first 3 links
                        href = random_link.get_attribute("href")
                        
                        if href and "maxgaming.biz.id" in href:
                            self.logger.info(f"Clicking on category: {href}")
                            
                            # Scroll to link
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_link)
                            time.sleep(random.uniform(1, 2))
                            
                            # Hover and click
                            Ac(self.driver).move_to_element(random_link).perform()
                            time.sleep(random.uniform(0.5, 1))
                            random_link.click()
                            
                            time.sleep(random.uniform(3, 5))
                            
                            # Simulate browsing on category page
                            self._simulate_natural_scrolling()
                            self._simulate_mouse_movements()
                            
                            # Go back to main page
                            self.driver.back()
                            time.sleep(random.uniform(2, 4))
                            break
                            
                except Exception as e:
                    self.logger.debug(f"Category navigation failed: {e}")
                    continue
            
            # Look for search functionality
            try:
                search_selectors = [
                    "input[type='search']",
                    "input[name*='search']",
                    "input[placeholder*='search']",
                    ".search input"
                ]
                
                for selector in search_selectors:
                    try:
                        search_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if search_input.is_displayed():
                            self.logger.info("Found search input, simulating search...")
                            
                            # Click on search box
                            search_input.click()
                            time.sleep(random.uniform(0.5, 1))
                            
                            # Type a search term
                            search_terms = ["mouse", "keyboard", "headset", "gaming"]
                            search_term = random.choice(search_terms)
                            
                            for char in search_term:
                                search_input.send_keys(char)
                                time.sleep(random.uniform(0.05, 0.15))
                            
                            time.sleep(random.uniform(1, 2))
                            search_input.send_keys(Keys.RETURN)
                            time.sleep(random.uniform(3, 5))
                            
                            # Simulate browsing search results
                            self._simulate_natural_scrolling()
                            time.sleep(random.uniform(2, 4))
                            
                            # Go back
                            self.driver.back()
                            time.sleep(random.uniform(2, 4))
                            break
                            
                    except:
                        continue
                        
            except Exception as e:
                self.logger.debug(f"Search simulation failed: {e}")
            
            self.logger.info("maxgaming-specific actions completed")
            
        except Exception as e:
            self.logger.error(f"maxgaming-specific actions failed: {e}")
    
    def run_automation(self):
        """Run the complete automation with Google search and maxgaming focus"""
        self.logger.info("Starting Complete Multilogin Automation with Google Search")
        self.logger.info(f"Personality: {self.user_personality}")
        self.logger.info(f"AdSense Auto Click: {self.adsense_config.get('enable_auto_click', False)}")
        self.logger.info(f"RPM Optimization: {self.rpm_optimization.get('enabled', False)}")
        
        try:
            # Step 1: Google Search for maxgaming.biz.id
            self.logger.info("Step 1: Google Search for maxgaming.biz.id")
            if self.run_google_search():
                self.logger.info("Google search successful, proceeding to maxgaming automation")
                
                # Step 2: Run automation on maxgaming.biz.id
                self.logger.info("Step 2: Running automation on maxgaming.biz.id")
                self.run_maxgaming_automation()
                
                # Step 3: Continue with other websites if needed
                self.logger.info("Step 3: Continuing with other websites")
                for website in self.websites[:3]:  # Limit to first 3 websites for stealth
                    domain = urlparse(website).netloc
                    
                    try:
                        self.logger.info(f"Visiting additional website: {website}")
                        self.driver.get(website)
                        
                        # Maximize window
                        try:
                            self.driver.maximize_window()
                        except:
                            pass
                        
                        time.sleep(random.uniform(2, 4))
                        
                        # Handle cookie consent
                        if domain not in self.visited_domains:
                            self.allow_cookies(website)
                            self.visited_domains.add(domain)
                        
                        # Record page visit
                        self.session_data["pages_visited"].append({
                            "url": website,
                            "timestamp": datetime.now().isoformat(),
                            "title": self.driver.title
                        })
                        
                        # Run automation features (shorter duration for stealth)
                        self.run_personality_system()
                        time.sleep(random.uniform(2, 4))
                        
                    except Exception as e:
                        self.logger.error(f"Error processing website {website}: {e}")
                        self.session_data["errors"].append({
                            "url": website,
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        })
                        continue
            else:
                self.logger.error("Google search failed, falling back to original automation")
                # Fallback to original automation
                for website in self.websites:
                    domain = urlparse(website).netloc
                    
                    try:
                        self.logger.info(f"Visiting website: {website}")
                        self.driver.get(website)
                        
                        # Maximize window
                        try:
                            self.driver.maximize_window()
                        except:
                            pass
                        
                        time.sleep(2)
                        
                        # Handle cookie consent
                        if domain not in self.visited_domains:
                            self.allow_cookies(website)
                            self.visited_domains.add(domain)
                        
                        # Record page visit
                        self.session_data["pages_visited"].append({
                            "url": website,
                            "timestamp": datetime.now().isoformat(),
                            "title": self.driver.title
                        })
                        
                        # Run all automation features
                        self.run_personality_system()
                        self.run_navigation_system()
                        self.run_adsense_auto_click()
                        
                    except Exception as e:
                        self.logger.error(f"Error processing website {website}: {e}")
                        self.session_data["errors"].append({
                            "url": website,
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        })
                        continue
            
            # Session cleanup
            self._cleanup_session()
            
        except Exception as e:
            self.logger.error(f"Automation failed: {e}")
            self.session_data["errors"].append({
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        
        self.logger.info("Complete Multilogin automation completed")
    
    def _cleanup_session(self):
        """Clean up session data and save metrics"""
        try:
            # Save session data
            session_data = {
                'profile_id': PROFILE_ID,
                'folder_id': FOLDER_ID,
                'session_duration': time.time() - self.session_start_time,
                'websites_visited': len(self.websites),
                'domains_processed': len(self.visited_domains),
                'timestamp': datetime.now().isoformat(),
                'personality': self.user_personality,
                'device_type': self.device_type,
                'pages_visited': self.session_data["pages_visited"],
                'interactions': self.session_data["interactions"],
                'adsense_clicks': self.session_data["adsense_clicks"],
                'errors': self.session_data["errors"]
            }
            
            # Save to file
            os.makedirs('data', exist_ok=True)
            with open(f'data/complete_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.logger.info("Session data saved successfully")
        
        except Exception as e:
            self.logger.error(f"Session cleanup failed: {e}")
    
    def close_driver(self):
        """Close the WebDriver"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing WebDriver: {e}")

def main():
    """Main function for complete Multilogin automation"""
    global PROFILE_ID, FOLDER_ID, AUTOMATION_CONFIG
    
    # Get profile info from environment
    PROFILE_ID = os.environ.get('MLX_PROFILE_ID')
    FOLDER_ID = os.environ.get('MLX_FOLDER_ID', 'default')
    debugging_url = os.environ.get('MLX_DEBUGGING_URL')
    
    driver = None
    try:
        # Setup WebDriver
        if debugging_url:
            # Connect to existing Multilogin debugging URL
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Remote(
                command_executor=debugging_url,
                options=chrome_options
            )
            
            # Execute stealth script
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            print(f"Connected to Multilogin debugging URL: {debugging_url}")
            
        else:
            # Create local Chrome driver for testing
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(options=chrome_options)
            
            # Execute stealth script
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            print("Created local Chrome driver for testing")
        
        if not driver:
            print("Failed to setup WebDriver")
            return
        
        # Initialize complete automation bot
        bot = CompleteMultiloginAutomation(driver)
        
        # Run complete automation
        bot.run_automation()
        
        print("Complete automation completed successfully")
        
    except Exception as e:
        print(f"Complete automation failed: {e}")
        raise
    
    finally:
        # Cleanup
        if driver:
            try:
                bot.close_driver()
            except:
                pass
        print("Complete Multilogin automation finished")

# Script entry point
if __name__ == "__main__":
    main()
