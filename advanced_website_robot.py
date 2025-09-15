import os
import random
import time
import logging
import sys
import json
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import requests


def setup_logging():
    """
    Setup logging mengikuti pattern cookie_robot.py
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s'))
    logging.getLogger(name='advanced_website_robot').addHandler(console_handler)


class Configuration:
    """Advanced configuration management"""
    def __init__(self):
        self.config = {
            'timing': {
                'min_delay': 0.5,
                'max_delay': 3.0,
                'page_load_timeout': 30,
                'element_wait_timeout': 10,
                'long_pause_chance': 0.05,
                'long_pause_min': 3.0,
                'long_pause_max': 8.0,
                'human_typing_delay_range': (0.1, 0.3),
                'human_scroll_delay_range': (1, 5),
                'human_click_delay_range': (0.5, 2.0)
            },
            'stealth': {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'window_size': (1920, 1080),
                'disable_images': False,
                'disable_javascript': False,
                'enable_stealth_scripts': True,
                'behavioral_stealth': True
            },
            'behavior': {
                'scroll_intensity': 'medium',
                'typing_speed': 'normal',
                'mouse_movement': True,
                'random_delays': True,
                'human_like_scrolling': True,
                'bezier_mouse_movement': True,
                'behavioral_profiles': ['casual', 'focused', 'exploratory', 'research']
            },
            'risk': {
                'max_requests_per_minute': 30,
                'detection_threshold': 0.7,
                'cooldown_period': 60,
                'emergency_protocol_threshold': 0.9,
                'slow_down_threshold': 0.6
            },
            'ad_clicking': {
                'enabled': True,
                'click_chance': 0.15,
                'max_clicks_per_session': 5,
                'conservative_mode': True,
                'ad_types': ['google_adsense']  # Focus only on Google AdSense
            },
            'navigation': {
                'enabled': True,
                'max_navigation_depth': 3,
                'same_domain_preference': 0.8,
                'random_link_clicking': True
            }
        }
    
    def get(self, key_path, default=None):
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value


class TimingSystem:
    """Advanced timing system with human-like behavior"""
    def __init__(self):
        self.config = Configuration()
        self.last_action_time = 0
        self.action_history = []
        self.base_delay = 1.0
        self.delay_variability = 0.7
        self.long_pause_chance = self.config.get('timing.long_pause_chance', 0.05)
        self.long_pause_min = self.config.get('timing.long_pause_min', 3.0)
        self.long_pause_max = self.config.get('timing.long_pause_max', 8.0)
    
    def advanced_random_delay(self, base_delay=None, variability=None):
        """Generate advanced random delay dengan distribusi normal"""
        if base_delay is None:
            base_delay = self.base_delay
        if variability is None:
            variability = self.delay_variability
        
        # Check for long pause chance
        if random.random() < self.long_pause_chance:
            long_pause = random.uniform(self.long_pause_min, self.long_pause_max)
            return long_pause
        
        # Generate delay dengan distribusi normal
        delay = random.normalvariate(base_delay, base_delay * variability)
        
        # Ensure minimum delay
        delay = max(0.1, delay)
        
        return delay
    
    def human_like_delay(self, delay_type="normal"):
        """Generate human-like delays berdasarkan tipe perilaku"""
        if delay_type == "typing":
            delay_range = self.config.get('timing.human_typing_delay_range', (0.1, 0.3))
            delay = random.uniform(*delay_range)
        elif delay_type == "scrolling":
            delay_range = self.config.get('timing.human_scroll_delay_range', (1, 5))
            delay = random.uniform(*delay_range)
        elif delay_type == "clicking":
            delay_range = self.config.get('timing.human_click_delay_range', (0.5, 2.0))
            delay = random.uniform(*delay_range)
        else:
            delay = self.advanced_random_delay()
        
        return delay
    
    def smart_delay(self, context="general", intensity="medium"):
        """Generate smart delays berdasarkan konteks dan intensitas"""
        # Base delays by context
        context_delays = {
            "search": {"low": 1.0, "medium": 2.0, "high": 4.0},
            "navigation": {"low": 0.5, "medium": 1.5, "high": 3.0},
            "reading": {"low": 3.0, "medium": 8.0, "high": 15.0},
            "clicking": {"low": 0.2, "medium": 0.8, "high": 2.0},
            "scrolling": {"low": 0.5, "medium": 1.5, "high": 3.0},
            "general": {"low": 1.0, "medium": 2.0, "high": 4.0}
        }
        
        base_delay = context_delays.get(context, context_delays["general"])[intensity]
        
        # Add variation based on action history
        if len(self.action_history) > 3:
            recent_avg = sum(self.action_history[-3:]) / 3
            variation = random.uniform(0.8, 1.2)
            base_delay = recent_avg * variation
        
        self.action_history.append(base_delay)
        if len(self.action_history) > 10:
            self.action_history.pop(0)
        
        return self.advanced_random_delay(base_delay)
    
    def get_human_delay(self, base_delay=None):
        if base_delay is None:
            base_delay = random.uniform(
                self.config.get('timing.min_delay', 0.5),
                self.config.get('timing.max_delay', 3.0)
            )
        
        # Add variation based on action history
        if len(self.action_history) > 3:
            recent_avg = sum(self.action_history[-3:]) / 3
            variation = random.uniform(0.8, 1.2)
            base_delay = recent_avg * variation
        
        self.action_history.append(base_delay)
        if len(self.action_history) > 10:
            self.action_history.pop(0)
        
        return base_delay
    
    def wait_between_actions(self, min_delay=0.5, max_delay=3.0):
        delay = self.get_human_delay(random.uniform(min_delay, max_delay))
        time.sleep(delay)
        return delay


class DetectionPatterns:
    """Advanced detection patterns for various elements"""
    def __init__(self):
        self.ad_detection_patterns = {
            'google_adsense': [
                'ins[data-ad-client]',
                'ins[data-ad-slot]',
                '.adsbygoogle',
                '[data-ad-client]',
                '[data-ad-slot]',
                'ins[data-ad-format]',
                'ins[data-ad-layout]',
                'ins[data-ad-layout-key]',
                'ins[data-ad-test]',
                'ins[data-ad-status]',
                'ins[data-ad-type]',
                'ins[data-ad-version]',
                'ins[data-ad-region]',
                'ins[data-ad-provider]',
                'ins[data-ad-network]',
                'ins[data-ad-unit]',
                'ins[data-ad-placement]',
                'ins[data-ad-targeting]',
                'ins[data-ad-custom]',
                'ins[data-ad-responsive]',
                'ins[data-ad-auto]',
                'ins[data-ad-manual]',
                'ins[data-ad-optimized]',
                'ins[data-ad-enhanced]',
                'ins[data-ad-advanced]',
                'ins[data-ad-premium]',
                'ins[data-ad-pro]',
                'ins[data-ad-enterprise]',
                'ins[data-ad-business]',
                'ins[data-ad-commercial]',
                'ins[data-ad-sponsored]',
                'ins[data-ad-promoted]',
                'ins[data-ad-featured]',
                'ins[data-ad-highlighted]',
                'ins[data-ad-recommended]',
                'ins[data-ad-suggested]',
                'ins[data-ad-related]',
                'ins[data-ad-similar]',
                'ins[data-ad-matching]',
                'ins[data-ad-relevant]',
                'ins[data-ad-targeted]',
                'ins[data-ad-personalized]',
                'ins[data-ad-customized]',
                'ins[data-ad-tailored]'
            ]
        }
        
        self.captcha_patterns = [
            '#captcha', '.captcha', '.g-recaptcha', '[data-sitekey]',
            '.recaptcha', '[data-testid*="captcha"]'
        ]
        
        self.navigation_patterns = {
            'next': [
                'a[rel="next"]',
                '.next',
                '.next-page',
                '[aria-label*="next"]',
                'a:contains("Next")',
                'a:contains(">")'
            ],
            'previous': [
                'a[rel="prev"]',
                '.prev',
                '.previous',
                '.previous-page',
                '[aria-label*="previous"]',
                'a:contains("Previous")',
                'a:contains("<")'
            ]
        }
        
        self.behavioral_anomaly_patterns = [
            'webdriver',
            'selenium',
            'phantomjs',
            'headless',
            'automation'
        ]


class MouseMovementSimulator:
    """Advanced mouse movement simulation"""
    def __init__(self, driver):
        self.driver = driver
        self.config = Configuration()
        self.movement_history = []
    
    def human_like_movement(self, start_pos, end_pos, steps=None):
        if steps is None:
            distance = ((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5
            steps = max(5, min(20, int(distance / 50)))
        
        points = []
        for i in range(steps + 1):
            t = i / steps
            
            # Bezier curve for natural movement
            control1_x = start_pos[0] + (end_pos[0] - start_pos[0]) * 0.3 + random.randint(-50, 50)
            control1_y = start_pos[1] + (end_pos[1] - start_pos[1]) * 0.3 + random.randint(-50, 50)
            control2_x = start_pos[0] + (end_pos[0] - start_pos[0]) * 0.7 + random.randint(-50, 50)
            control2_y = start_pos[1] + (end_pos[1] - start_pos[1]) * 0.7 + random.randint(-50, 50)
            
            x = (1-t)**3 * start_pos[0] + 3*(1-t)**2*t * control1_x + 3*(1-t)*t**2 * control2_x + t**3 * end_pos[0]
            y = (1-t)**3 * start_pos[1] + 3*(1-t)**2*t * control1_y + 3*(1-t)*t**2 * control2_y + t**3 * end_pos[1]
            
            points.append((int(x), int(y)))
        
        return points
    
    def move_to_element(self, element, smooth=True):
        try:
            # Check if element is still valid
            try:
                # Test if element is still attached to DOM
                element.is_displayed()
            except Exception as e:
                logging.warning(f"Element is stale, skipping mouse movement: {e}")
                return False
            
            if smooth:
                try:
                    # Get element position safely
                    location = element.location_once_scrolled_into_view
                    size = element.size
                    center_x = location['x'] + size['width'] // 2
                    center_y = location['y'] + size['height'] // 2
                    
                    # Get current mouse position (approximate)
                    current_pos = (random.randint(0, 1920), random.randint(0, 1080))
                    target_pos = (center_x, center_y)
                    
                    # Generate movement path
                    movement_points = self.human_like_movement(current_pos, target_pos)
                    
                    # Execute movement with error handling
                    for point in movement_points:
                        try:
                            self.driver.execute_script(f"""
                                try {{
                                    var event = new MouseEvent('mousemove', {{
                                        clientX: {point[0]},
                                        clientY: {point[1]},
                                        bubbles: true
                                    }});
                                    document.dispatchEvent(event);
                                }} catch(e) {{
                                    // Ignore mouse movement errors
                                }}
                            """)
                        except Exception as e:
                            # Ignore individual mouse movement errors
                            pass
                        time.sleep(random.uniform(0.01, 0.05))
                except Exception as e:
                    logging.warning(f"Smooth mouse movement failed: {e}")
            
            # Move to element using ActionChains with error handling
            try:
                ActionChains(self.driver).move_to_element(element).perform()
                return True
            except Exception as e:
                logging.warning(f"ActionChains mouse movement failed: {e}")
                return False
                
        except Exception as e:
            logging.warning(f"Mouse movement failed: {e}")
            return False
    
    def random_mouse_movement(self, duration=1.0):
        try:
            # Get viewport size safely
            try:
                viewport_size = self.driver.execute_script("return {width: window.innerWidth, height: window.innerHeight}")
            except Exception as e:
                # Fallback viewport size
                viewport_size = {'width': 1920, 'height': 1080}
            
            start_time = time.time()
            current_pos = (random.randint(0, viewport_size['width']),
                          random.randint(0, viewport_size['height']))
            
            while time.time() - start_time < duration:
                try:
                    target_pos = (random.randint(0, viewport_size['width']),
                                 random.randint(0, viewport_size['height']))
                    movement_points = self.human_like_movement(current_pos, target_pos)
                    
                    for point in movement_points:
                        if time.time() - start_time >= duration:
                            break
                        
                        try:
                            # Safe mouse movement with error handling
                            self.driver.execute_script(f"""
                                try {{
                                    var event = new MouseEvent('mousemove', {{
                                        clientX: {point[0]},
                                        clientY: {point[1]},
                                        bubbles: true
                                    }});
                                    document.dispatchEvent(event);
                                }} catch(e) {{
                                    // Ignore mouse movement errors
                                }}
                            """)
                        except Exception as e:
                            # Ignore individual mouse movement errors
                            pass
                        
                        time.sleep(random.uniform(0.01, 0.05))
                    
                    current_pos = target_pos
                    time.sleep(random.uniform(0.1, 0.5))
                    
                except Exception as e:
                    # If there's an error in the movement loop, break out
                    break
                    
        except Exception as e:
            # Ignore mouse movement errors completely
            pass


class RiskMonitor:
    """Advanced risk monitoring system"""
    def __init__(self, driver):
        self.driver = driver
        self.config = Configuration()
        self.request_history = []
        self.detection_events = []
        self.risk_level = "low"
        self.request_count = 0
        self.last_request_time = 0
    
    def can_make_request(self) -> bool:
        current_time = time.time()
        max_requests = self.config.get('risk.max_requests_per_minute', 30)
        
        # Remove requests older than 1 minute
        self.request_history = [req_time for req_time in self.request_history 
                              if current_time - req_time < 60]
        
        return len(self.request_history) < max_requests
    
    def record_request(self):
        self.request_history.append(time.time())
        self.request_count += 1
        self.last_request_time = time.time()
    
    def check_detection_signals(self):
        signals = {
            'captcha_detected': False,
            'unusual_requests': False,
            'behavioral_anomalies': False,
            'automation_flags': False
        }
        
        try:
            # Check for CAPTCHA
            captcha_selectors = [
                "iframe[src*='recaptcha']",
                ".g-recaptcha",
                "#captcha",
                ".captcha"
            ]
            
            for selector in captcha_selectors:
                try:
                    if self.driver.find_element(By.CSS_SELECTOR, selector):
                        signals['captcha_detected'] = True
                        break
                except NoSuchElementException:
                    continue
            
            # Check for unusual requests
            if not self.can_make_request():
                signals['unusual_requests'] = True
            
            # Check for behavioral anomalies
            signals['behavioral_anomalies'] = self._detect_behavioral_anomalies()
            
            # Check for automation flags
            automation_indicators = [
                "webdriver",
                "selenium",
                "phantomjs",
                "headless"
            ]
            
            user_agent = self.driver.execute_script("return navigator.userAgent;")
            for indicator in automation_indicators:
                if indicator.lower() in user_agent.lower():
                    signals['automation_flags'] = True
                    break
        
        except Exception as e:
            logging.warning(f"Error checking detection signals: {e}")
        
        return signals
    
    def _detect_behavioral_anomalies(self) -> bool:
        try:
            # Check for too fast interactions
            if len(self.request_history) > 10:
                recent_requests = self.request_history[-10:]
                avg_interval = sum(recent_requests[i+1] - recent_requests[i] 
                                 for i in range(len(recent_requests)-1)) / (len(recent_requests)-1)
                if avg_interval < 1.0:  # Less than 1 second between requests
                    return True
            
            return False
        except Exception:
            return False
    
    def assess_risk_level(self, signals):
        risk_score = 0
        
        if signals['captcha_detected']:
            risk_score += 0.4
        if signals['unusual_requests']:
            risk_score += 0.3
        if signals['behavioral_anomalies']:
            risk_score += 0.2
        if signals['automation_flags']:
            risk_score += 0.1
        
        if risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def handle_risk(self, signals):
        risk_level = self.assess_risk_level(signals)
        self.risk_level = risk_level
        
        if risk_level == "high":
            return self._handle_high_risk()
        elif risk_level == "medium":
            return self._handle_medium_risk()
        else:
            return self._handle_low_risk()
    
    def _handle_high_risk(self):
        logging.warning("High risk detected - implementing extended cooldown")
        time.sleep(random.uniform(30, 60))
        return False
    
    def _handle_medium_risk(self):
        logging.warning("Medium risk detected - implementing short cooldown")
        time.sleep(random.uniform(10, 20))
        return True
    
    def _handle_low_risk(self):
        return True
    
    def get_risk_statistics(self):
        return {
            'current_risk_level': self.risk_level,
            'total_requests': self.request_count,
            'requests_last_minute': len(self.request_history),
            'detection_events': len(self.detection_events),
            'last_request_time': self.last_request_time
        }


class AdClickingSystem:
    """Advanced ad clicking system with conservative behavior"""
    
    def __init__(self, driver, timing_system, mouse_simulator):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.click_history = []
        self.config = Configuration()
        self.patterns = DetectionPatterns()
        
    def detect_ads(self, page_source=None):
        """Detect ads pada current page"""
        detected_ads = []
        
        try:
            # Use provided page source or get current page
            if page_source is None:
                page_source = self.driver.page_source
            
            # Check different ad patterns
            for ad_type, selectors in self.patterns.ad_detection_patterns.items():
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        for element in elements:
                            if self._is_valid_ad_element(element):
                                ad_info = {
                                    'element': element,
                                    'type': ad_type,
                                    'selector': selector,
                                    'position': element.location,
                                    'size': element.size,
                                    'is_visible': element.is_displayed(),
                                    'click_probability': self._calculate_click_probability(element, ad_type)
                                }
                                detected_ads.append(ad_info)
                                
                    except Exception as e:
                        continue
            
            return detected_ads
            
        except Exception as e:
            return []
    
    def _is_valid_ad_element(self, element):
        """Validate if element is a valid ad element"""
        try:
            # Check if element is visible and has reasonable size
            if not element.is_displayed():
                return False
            
            size = element.size
            if size['width'] < 50 or size['height'] < 50:
                return False
            
            # Check if element is in viewport
            location = element.location
            if location['x'] < 0 or location['y'] < 0:
                return False
            
            # Check for common ad attributes
            ad_attributes = ['data-ad', 'data-ad-client', 'data-ad-slot', 'data-ad-unit']
            for attr in ad_attributes:
                if element.get_attribute(attr):
                    return True
            
            # Check for ad-related classes
            class_name = element.get_attribute('class') or ''
            if any(keyword in class_name.lower() for keyword in ['ad', 'advertisement', 'adsbygoogle']):
                return True
            
            return True
            
        except Exception as e:
            return False
    
    def _calculate_click_probability(self, element, ad_type):
        """Calculate click probability - Focus only on Google AdSense"""
        # Only calculate for Google AdSense
        if ad_type != 'google_adsense':
            return 0.0
        
        base_probability = self.config.get('ad_clicking.click_chance', 0.15)
        
        try:
            # Higher base probability for Google AdSense
            base_probability *= 1.5  # 50% higher for AdSense
            
            # Adjust based on element size
            size = element.size
            area = size['width'] * size['height']
            
            if area > 100000:  # Large ads
                base_probability *= 0.8
            elif area < 10000:  # Small ads
                base_probability *= 0.4
            else:  # Medium ads
                base_probability *= 1.2
            
            # Adjust based on position
            location = element.location
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            if location['y'] > viewport_height * 0.8:  # Below fold
                base_probability *= 0.6
            elif location['y'] < viewport_height * 0.2:  # Above fold
                base_probability *= 1.3
            else:  # Middle fold
                base_probability *= 1.1
            
            # Check AdSense specific attributes
            if element.get_attribute('data-ad-client'):
                base_probability *= 1.2
            if element.get_attribute('data-ad-slot'):
                base_probability *= 1.1
            if element.get_attribute('data-ad-format'):
                base_probability *= 1.05
            
            # Ensure probability is within reasonable bounds
            return max(0.01, min(base_probability, 0.4))
            
        except Exception as e:
            return base_probability
    
    def click_ads(self, max_clicks=1, conservative=True):
        """Click ads dengan conservative behavior"""
        clicked_ads = []
        
        try:
            # Detect ads on current page
            detected_ads = self.detect_ads()
            
            if not detected_ads:
                return clicked_ads
            
            # Sort ads by click probability (highest first)
            detected_ads.sort(key=lambda x: x['click_probability'], reverse=True)
            
            # Click ads based on probability and limits
            clicks_attempted = 0
            for ad_info in detected_ads:
                if clicks_attempted >= max_clicks:
                    break
                
                if self._should_click_ad(ad_info, conservative):
                    if self._click_ad_safely(ad_info):
                        clicked_ads.append(ad_info)
                        clicks_attempted += 1
                        
                        # Add delay between clicks
                        if clicks_attempted < max_clicks:
                            delay = self.timing.human_like_delay("clicking")
                            time.sleep(delay)
            
            return clicked_ads
            
        except Exception as e:
            return clicked_ads
    
    def _should_click_ad(self, ad_info, conservative):
        """Determine if ad should be clicked - Focus only on Google AdSense"""
        try:
            # Only click Google AdSense ads
            if ad_info['type'] != 'google_adsense':
                return False
            
            # Check click probability
            if random.random() > ad_info['click_probability']:
                return False
            
            # Conservative checks for Google AdSense
            if conservative:
                # Don't click if we've clicked too many ads recently
                recent_clicks = [click for click in self.click_history 
                               if time.time() - click['timestamp'] < 1200]  # 20 minutes
                
                if len(recent_clicks) >= 3:  # Max 3 clicks per 20 minutes
                    return False
                
                # Don't click if ad is too small (higher threshold for AdSense)
                size = ad_info['size']
                if size['width'] < 120 or size['height'] < 60:
                    return False
                
                # Check if ad has proper AdSense attributes
                element = ad_info['element']
                if not (element.get_attribute('data-ad-client') or element.get_attribute('data-ad-slot')):
                    return False
            
            return True
            
        except Exception as e:
            return False
    
    def _click_ad_safely(self, ad_info):
        """Click ad safely dengan human-like behavior"""
        try:
            element = ad_info['element']
            
            # Scroll to ad first
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            
            # Wait for element to be clickable
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable(element))
            
            # Add human-like delay before clicking
            pre_click_delay = self.timing.human_like_delay("clicking")
            time.sleep(pre_click_delay)
            
            # Use mouse simulator for human-like clicking
            if self.mouse.move_to_element(element):
                element.click()
                
                # Record click in history
                click_record = {
                    'timestamp': time.time(),
                    'ad_type': ad_info['type'],
                    'position': ad_info['position'],
                    'size': ad_info['size']
                }
                self.click_history.append(click_record)
                
                # Add post-click delay
                post_click_delay = self.timing.human_like_delay("clicking")
                time.sleep(post_click_delay)
                
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def get_click_statistics(self):
        """Get ad clicking statistics"""
        current_time = time.time()
        
        # Calculate recent click statistics (last hour)
        recent_clicks = [click for click in self.click_history 
                        if current_time - click['timestamp'] < 3600]  # Last hour
        
        # Calculate clicks in last 20 minutes (rate limiting window)
        rate_limit_clicks = [click for click in self.click_history 
                            if current_time - click['timestamp'] < 1200]  # Last 20 minutes
        
        return {
            'total_clicks': len(self.click_history),
            'recent_clicks': len(recent_clicks),
            'rate_limit_clicks': len(rate_limit_clicks),
            'rate_limit_remaining': max(0, 3 - len(rate_limit_clicks)),
            'click_rate': len(recent_clicks) / 60,  # Clicks per minute
            'average_click_interval': self._calculate_average_interval(),
            'ad_types_clicked': self._get_clicked_ad_types()
        }
    
    def _calculate_average_interval(self):
        """Calculate average interval between clicks"""
        if len(self.click_history) < 2:
            return 0
        
        intervals = []
        for i in range(1, len(self.click_history)):
            interval = self.click_history[i]['timestamp'] - self.click_history[i-1]['timestamp']
            intervals.append(interval)
        
        return sum(intervals) / len(intervals) if intervals else 0
    
    def _get_clicked_ad_types(self):
        """Get count of clicked ad types"""
        ad_types = {}
        for click in self.click_history:
            ad_type = click['ad_type']
            ad_types[ad_type] = ad_types.get(ad_type, 0) + 1
        
        return ad_types


class HumanLikeScroller:
    """Advanced human-like scrolling system"""
    
    def __init__(self, driver, timing_system, mouse_simulator):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.scroll_history = []
        self.reading_sessions = []
        self.logger = logging.getLogger('advanced_website_robot')
    
    def smooth_scroll_to_position(self, target_position, duration=2.0):
        """Smooth scroll to specific position like human reading"""
        try:
            current_position = self.driver.execute_script("return window.pageYOffset")
            distance = target_position - current_position
            
            if abs(distance) < 50:  # Already close enough
                return True
            
            # Calculate number of steps for smooth scrolling - much more steps for human-like movement
            steps = max(50, min(150, int(abs(distance) / 25)))  # Much more steps, smaller distance per step
            step_size = distance / steps
            step_duration = duration / steps
            
            for step in range(steps):
                new_position = current_position + (step_size * (step + 1))
                self.driver.execute_script(f"window.scrollTo(0, {new_position});")
                
                # Variable delay between steps (like human reading speed) - much longer delays
                delay = step_duration * random.uniform(1.2, 2.5)  # Much longer delays
                time.sleep(delay)
                
                # Occasionally pause longer (like reading content) - more frequent and much longer
                if random.random() < 0.4:  # Increased chance for reading pause
                    reading_pause = random.uniform(2.0, 6.0)  # Much longer reading pause
                    time.sleep(reading_pause)
            
            return True
            
        except Exception as e:
            return False
    
    def reading_behavior_scroll(self, content_type="article"):
        """Simulate reading behavior with natural scrolling"""
        try:
            # Get page dimensions
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            
            # Reading behavior patterns - much longer pauses for better comprehension
            reading_patterns = {
                'article': {
                    'paragraph_scrolls': (3, 8),
                    'paragraph_pause': (8, 18),  # Much longer pauses
                    'section_pause': (12, 25),   # Much longer section pauses
                    're_read_chance': 0.35,      # Increased re-read chance
                    'mouse_tracking_chance': 0.5  # Increased mouse tracking
                },
                'news': {
                    'paragraph_scrolls': (2, 5),
                    'paragraph_pause': (6, 15),  # Much longer pauses
                    'section_pause': (10, 20),   # Much longer section pauses
                    're_read_chance': 0.25,      # Increased re-read chance
                    'mouse_tracking_chance': 0.4  # Increased mouse tracking
                },
                'blog': {
                    'paragraph_scrolls': (4, 10),
                    'paragraph_pause': (10, 20), # Much longer pauses
                    'section_pause': (15, 30),   # Much longer section pauses
                    're_read_chance': 0.45,      # Increased re-read chance
                    'mouse_tracking_chance': 0.6  # Increased mouse tracking
                }
            }
            
            pattern = reading_patterns.get(content_type, reading_patterns['article'])
            
            # Simulate reading paragraphs/sections
            num_paragraphs = random.randint(*pattern['paragraph_scrolls'])
            
            for paragraph in range(num_paragraphs):
                # Check if we're near the end
                current_scroll = self.driver.execute_script("return window.pageYOffset")
                remaining_height = page_height - current_scroll - viewport_height
                
                if remaining_height < 300:  # Near end, scroll up to re-read
                    scroll_up = random.randint(200, 500)
                    self.smooth_scroll_to_position(current_scroll - scroll_up, 1.5)
                    self.logger.info("Scrolled up to re-read (near end)")
                else:
                    # Normal paragraph reading scroll
                    scroll_amount = random.randint(200, 600)
                    
                    # Add variation based on content type
                    if content_type == 'article':
                        # Articles: more careful reading
                        scroll_amount = int(scroll_amount * random.uniform(0.7, 1.2))
                    elif content_type == 'news':
                        # News: faster reading
                        scroll_amount = int(scroll_amount * random.uniform(1.0, 1.5))
                    
                    new_position = current_scroll + scroll_amount
                    self.smooth_scroll_to_position(new_position, random.uniform(1.5, 3.0))
                
                # Reading pause (like actually reading the content) - much longer
                reading_pause = random.uniform(*pattern['paragraph_pause'])
                
                # Add mouse tracking (like following text with mouse) - longer duration
                if random.random() < pattern['mouse_tracking_chance']:
                    self.mouse.random_mouse_movement(random.uniform(1.0, 3.0))  # Longer mouse movement
                
                # Occasionally re-read (like humans do) - more frequent and longer
                if random.random() < pattern['re_read_chance']:
                    re_read_pause = random.uniform(5, 12)  # Much longer re-read pause
                    reading_pause += re_read_pause
                    self.logger.info(f"Re-reading pause: {re_read_pause:.1f}s")
                    
                    # Scroll up a bit to re-read
                    current_scroll = self.driver.execute_script("return window.pageYOffset")
                    re_read_scroll = random.randint(100, 300)
                    self.smooth_scroll_to_position(current_scroll - re_read_scroll, 2.0)  # Longer scroll duration
                
                time.sleep(reading_pause)
                
                # Section break pause (like finishing a section) - more frequent and longer
                if paragraph < num_paragraphs - 1 and random.random() < 0.5:  # Increased chance
                    section_pause = random.uniform(*pattern['section_pause'])
                    self.logger.info(f"Section break pause: {section_pause:.1f}s")
                    time.sleep(section_pause)
            
            # Final reading pause - much longer
            final_pause = random.uniform(8, 20)  # Much longer final pause
            self.logger.info(f"Final reading pause: {final_pause:.1f}s")
            time.sleep(final_pause)
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Error in reading behavior scroll: {e}")
            return False
    
    def quick_scan_scroll(self):
        """Quick scanning behavior (like skimming content)"""
        try:
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Quick scan: larger scrolls with shorter pauses
            scan_sections = random.randint(3, 6)
            section_height = page_height // scan_sections
            
            for section in range(scan_sections):
                target_position = section_height * (section + 1)
                
                # Quick scroll to section
                self.driver.execute_script(f"window.scrollTo(0, {target_position});")
                
                # Short scan pause
                scan_pause = random.uniform(0.5, 2.0)
                time.sleep(scan_pause)
                
                # Quick mouse movement (like scanning)
                if random.random() < 0.6:
                    self.mouse.random_mouse_movement(random.uniform(0.2, 0.8))
            
            return True
            
        except Exception as e:
            return False


class PostNavigator:
    """Previous/Next Post Navigation System for AdSense RPM Optimization"""
    def __init__(self, driver, timing_system, mouse_simulator, risk_monitor):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.risk_monitor = risk_monitor
        self.logger = logging.getLogger('advanced_website_robot')
        
        # Post navigation patterns
        self.previous_selectors = [
            'a[rel="prev"]', 'a[rel="previous"]', '.prev', '.previous', 
            '.post-nav-prev', '.navigation-prev', '.pagination-prev',
            'a:contains("Previous")', 'a:contains("Prev")', 'a:contains("←")',
            '.nav-previous', '.entry-nav-prev', '.single-nav-prev'
        ]
        
        self.next_selectors = [
            'a[rel="next"]', 'a[rel="next"]', '.next', '.next-post',
            '.post-nav-next', '.navigation-next', '.pagination-next',
            'a:contains("Next")', 'a:contains("→")', 'a:contains("Continue")',
            '.nav-next', '.entry-nav-next', '.single-nav-next'
        ]
        
        # Related posts selectors
        self.related_selectors = [
            '.related-posts', '.similar-posts', '.more-posts', '.recommended-posts',
            '.post-recommendations', '.suggested-posts', '.you-might-like',
            '.related-articles', '.similar-articles', '.more-articles'
        ]
    
    def find_navigation_links(self):
        """Find previous, next, and related post links"""
        try:
            self.logger.info("🔍 Searching for post navigation links")
            
            navigation_links = {
                'previous': None,
                'next': None,
                'related': []
            }
            
            # Find previous post link
            for selector in self.previous_selectors:
                try:
                    if ':contains(' in selector:
                        # Handle text-based selectors
                        text = selector.split(':contains("')[1].split('")')[0]
                        elements = self.driver.find_elements("xpath", f"//a[contains(text(), '{text}')]")
                        if elements:
                            navigation_links['previous'] = elements[0]
                            self.logger.info(f"✅ Found previous link: {text}")
                            break
                    else:
                        elements = self.driver.find_elements("css selector", selector)
                        if elements:
                            navigation_links['previous'] = elements[0]
                            self.logger.info(f"✅ Found previous link with selector: {selector}")
                            break
                except Exception as e:
                    continue
            
            # Find next post link
            for selector in self.next_selectors:
                try:
                    if ':contains(' in selector:
                        # Handle text-based selectors
                        text = selector.split(':contains("')[1].split('")')[0]
                        elements = self.driver.find_elements("xpath", f"//a[contains(text(), '{text}')]")
                        if elements:
                            navigation_links['next'] = elements[0]
                            self.logger.info(f"✅ Found next link: {text}")
                            break
                    else:
                        elements = self.driver.find_elements("css selector", selector)
                        if elements:
                            navigation_links['next'] = elements[0]
                            self.logger.info(f"✅ Found next link with selector: {selector}")
                            break
                except Exception as e:
                    continue
            
            # Find related posts
            for selector in self.related_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        # Find links within related posts section
                        links = element.find_elements("css selector", "a")
                        for link in links[:3]:  # Limit to 3 related posts
                            href = link.get_attribute('href')
                            if href and href not in [l.get_attribute('href') for l in navigation_links['related']]:
                                navigation_links['related'].append(link)
                    if navigation_links['related']:
                        self.logger.info(f"✅ Found {len(navigation_links['related'])} related posts")
                        break
                except Exception as e:
                    continue
            
            return navigation_links
            
        except Exception as e:
            self.logger.error(f"Error finding navigation links: {e}")
            return {'previous': None, 'next': None, 'related': []}
    
    def navigate_to_post(self, link_element, post_type="unknown"):
        """Navigate to a post link with natural behavior"""
        try:
            if not link_element:
                return False
                
            self.logger.info(f"🔗 Navigating to {post_type} post")
            
            # Get link URL for tracking
            href = link_element.get_attribute('href')
            if href:
                self.logger.info(f"📍 Post URL: {href}")
            
            # Scroll to link
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link_element)
            time.sleep(1)
            
            # Move mouse to link
            self.mouse.move_to_element(link_element)
            time.sleep(0.5)
            
            # Click the link
            link_element.click()
            self.logger.info(f"✅ Clicked {post_type} post link")
            
            # Wait for navigation
            time.sleep(3)
            
            # Verify navigation success
            current_url = self.driver.current_url
            if href and href in current_url:
                self.logger.info(f"✅ Successfully navigated to {post_type} post")
                return True
            else:
                self.logger.info(f"✅ Navigated to {post_type} post (URL verification skipped)")
                return True
                
        except Exception as e:
            self.logger.error(f"Error navigating to {post_type} post: {e}")
            return False
    
    def simulate_post_reading(self, duration_minutes=2):
        """Simulate reading a post with natural behavior"""
        try:
            self.logger.info(f"📖 Simulating post reading for {duration_minutes} minutes")
            
            # Use the existing natural article reading
            from advanced_website_robot import HumanLikeScroller
            scroller = HumanLikeScroller(self.driver, self.timing, self.mouse)
            
            # Simulate reading behavior
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while time.time() < end_time:
                # Random reading behavior
                behavior = random.choice(['scroll', 'pause', 're_read', 'scan'])
                
                if behavior == 'scroll':
                    scroller.reading_behavior_scroll()
                elif behavior == 'pause':
                    pause_duration = random.uniform(2, 8)
                    self.logger.info(f"📖 Reading pause: {pause_duration:.1f}s")
                    time.sleep(pause_duration)
                elif behavior == 're_read':
                    scroller.quick_scan_scroll()
                elif behavior == 'scan':
                    scroller.quick_scan_scroll()
                
                # Random delay between behaviors
                time.sleep(random.uniform(1, 3))
            
            self.logger.info("✅ Post reading simulation completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error simulating post reading: {e}")
            return False


class ArticleBrowser:
    """Advanced article browsing system with Previous/Next Post Navigation for AdSense RPM optimization"""
    def __init__(self, driver, timing_system, mouse_simulator, risk_monitor):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.risk_monitor = risk_monitor
        self.config = Configuration()
        self.patterns = DetectionPatterns()
        self.ad_clicker = AdClickingSystem(driver, timing_system, mouse_simulator)
        self.human_scroller = HumanLikeScroller(driver, timing_system, mouse_simulator)
        self.logger = logging.getLogger('advanced_website_robot')
        
        # Previous/Next Post Navigation System
        self.post_navigator = PostNavigator(driver, timing_system, mouse_simulator, risk_monitor)
        self.visited_posts = []  # Track visited posts to avoid loops
        self.min_posts_per_session = 3  # Minimum posts to visit per session
        self.max_posts_per_session = 7  # Maximum posts to visit per session
    
    def open_article_with_referer(self, article_url, referer_url=None):
        try:
            self.logger.info(f"Opening article: {article_url}")
            
            if referer_url:
                self.logger.info(f"Using referer: {referer_url}")
                
                # Navigate to referer first
                try:
                    self.driver.get(referer_url)
                    self.timing.wait_between_actions(2, 4)
                    
                    # Simulate some browsing on referer
                    self._simulate_referer_browsing()
                    
                    # Use improved navigation to maintain referer
                    navigation_success = self._navigate_with_referer(article_url, referer_url)
                    
                    if not navigation_success:
                        self.logger.warning("Navigation with referer failed, trying direct navigation")
                        self.driver.get(article_url)
                        
                except Exception as e:
                    self.logger.warning(f"Referer navigation failed: {e}, trying direct navigation")
                    self.driver.get(article_url)
            else:
                # Direct navigation without referer
                self.driver.get(article_url)
            
            self.risk_monitor.record_request()
            
            # Wait for page load with better error handling
            try:
                WebDriverWait(self.driver, 30).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                # Additional wait for dynamic content
                time.sleep(2)
                
            except TimeoutException:
                self.logger.warning("Page load timeout, but continuing...")
            except Exception as e:
                self.logger.warning(f"Page load check failed: {e}")
            
            # Check if we're actually on the target page
            current_url = self.driver.current_url
            if article_url in current_url or 'rexdl.biz.id' in current_url:
                self.logger.info("✅ Article loaded successfully")
                
                # Verify referer was sent (optional)
                if referer_url:
                    self._verify_referer_sent(referer_url)
                
                return True
            else:
                self.logger.error(f"❌ Failed to load article. Current URL: {current_url}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error opening article: {e}")
            # Try direct navigation as last resort
            try:
                self.logger.info("Attempting direct navigation as fallback")
                self.driver.get(article_url)
                time.sleep(3)
                
                current_url = self.driver.current_url
                if article_url in current_url or 'rexdl.biz.id' in current_url:
                    self.logger.info("✅ Direct navigation successful")
                    return True
                else:
                    self.logger.error(f"❌ Even direct navigation failed. Current URL: {current_url}")
                    return False
                    
            except Exception as e2:
                self.logger.error(f"Direct navigation also failed: {e2}")
                return False
    
    def _simulate_referer_browsing(self):
        """Simulate natural referer browsing (bandwidth optimized)"""
        try:
            self.logger.info("Simulating natural referer browsing (bandwidth optimized)")
            
            # Quick initial wait
            time.sleep(random.uniform(0.5, 1.5))
            
            # Light scroll behavior (minimal bandwidth usage)
            scroll_count = random.randint(1, 2)  # Reduced from 2-4
            for i in range(scroll_count):
                scroll_amount = random.randint(50, 150)  # Reduced from 100-250
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 1.5))  # Reduced from 2.0-4.0
            
            # Minimal mouse movement
            if random.random() < 0.4:  # 40% chance for mouse movement
                self.mouse.random_mouse_movement(random.uniform(0.5, 1.0))  # Reduced duration
            
            # Quick final pause
            time.sleep(random.uniform(1.0, 2.0))  # Reduced from 2.0-5.0
            
            # Check for ads on referer page (low chance)
            if random.random() < 0.1:  # 10% chance to check for ads on referer
                self.logger.info("🔍 Checking for Google AdSense ads on referer page...")
                clicked_ads = self.ad_clicker.click_ads(max_clicks=1, conservative=True)
                if clicked_ads:
                    self.logger.info(f"✅ Clicked {len(clicked_ads)} Google AdSense ads on referer page")
                else:
                    self.logger.info("ℹ️ No suitable Google AdSense ads found on referer page")
            
            self.logger.info("Referer browsing completed (bandwidth optimized)")
            
        except Exception as e:
            self.logger.warning(f"Error simulating referer browsing: {e}")
    
    def _natural_article_reading(self, duration_minutes=3):
        """Natural article reading behavior - seperti manusia benar-benar membaca"""
        try:
            self.logger.info(f"Starting natural article reading for {duration_minutes} minutes")
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            # Reading behavior states
            reading_state = "initial_scan"  # initial_scan, reading, re_reading, scanning, finishing
            last_scroll_position = 0
            reading_rhythm = 0  # 0-100, affects reading speed and pauses
            
            # Ad clicking integration
            last_ad_check = time.time()
            ad_check_interval = random.uniform(60, 180)  # Check for ads every 1-3 minutes
            
            while time.time() < end_time:
                current_scroll = self.driver.execute_script("return window.pageYOffset")
                page_height = self.driver.execute_script("return document.body.scrollHeight")
                viewport_height = self.driver.execute_script("return window.innerHeight")
                remaining_height = page_height - current_scroll - viewport_height
                
                # Check for ads periodically
                current_time = time.time()
                if current_time - last_ad_check > ad_check_interval:
                    self.logger.info("🔍 Checking for Google AdSense ads...")
                    clicked_ads = self.ad_clicker.click_ads(max_clicks=1, conservative=True)
                    if clicked_ads:
                        self.logger.info(f"✅ Clicked {len(clicked_ads)} Google AdSense ads")
                        # Post-click behavior is handled automatically in _click_ad_safely
                    else:
                        self.logger.info("ℹ️ No suitable Google AdSense ads found")
                    
                    last_ad_check = current_time
                    ad_check_interval = random.uniform(60, 180)  # Reset interval
                
                # Determine reading behavior based on state and content
                if reading_state == "initial_scan":
                    # Quick initial scan of the article
                    self._initial_article_scan()
                    reading_state = "reading"
                    reading_rhythm = random.randint(20, 35)  # Start slow, NO FAST READING
                    
                elif reading_state == "reading":
                    # Main reading behavior
                    scroll_result = self._natural_paragraph_reading(reading_rhythm)
                    if scroll_result == "finished":
                        reading_state = "finishing"
                    elif scroll_result == "re_read_needed":
                        reading_state = "re_reading"
                    elif scroll_result == "scanning":
                        reading_state = "scanning"
                    
                    # Adjust reading rhythm based on content complexity - NO FAST READING
                    reading_rhythm += random.randint(-3, 5)  # Reduced max increase
                    reading_rhythm = max(10, min(60, reading_rhythm))  # Reduced max rhythm
                    
                elif reading_state == "re_reading":
                    # Re-read previous content
                    self._re_read_previous_content()
                    reading_state = "reading"
                    
                elif reading_state == "scanning":
                    # Careful scanning behavior (NO FAST SCANNING)
                    self._careful_content_scan()
                    reading_state = "reading"
                    
                elif reading_state == "finishing":
                    # Final reading behavior
                    self._finish_reading_behavior()
                    break
                
                # Natural pause between reading actions
                pause_duration = self._calculate_natural_reading_pause(reading_rhythm)
                time.sleep(pause_duration)
                
                # Occasional mouse movement (like following text)
                if random.random() < 0.15:  # Reduced to 15% for more natural behavior
                    self._natural_mouse_tracking()
                
                # Check if we need to change reading state - don't finish too early
                if remaining_height < 50 and reading_state == "reading":  # Only finish when very close to bottom
                    reading_state = "finishing"
            
            self.logger.info("Natural article reading completed")
            return True
            
        except Exception as e:
            self.logger.warning(f"Error during natural article reading: {e}")
            return False
    
    def _initial_article_scan(self):
        """Initial scan of the article to understand structure"""
        try:
            self.logger.info("Performing initial article scan")
            
            # Get article structure
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Quick scan: scroll to see article structure
            scan_positions = [0.2, 0.4, 0.6, 0.8]  # Scan at 20%, 40%, 60%, 80% of article
            
            for position in scan_positions:
                target_scroll = int(page_height * position)
                self._human_like_scroll_to_position(target_scroll, duration=1.5)
                
                # Quick pause to "see" the content
                scan_pause = random.uniform(0.8, 2.0)
                time.sleep(scan_pause)
                
                # Occasional mouse movement during scan
                if random.random() < 0.3:
                    self._natural_mouse_tracking()
            
            # Return to top to start reading
            self._human_like_scroll_to_position(0, duration=2.0)
            time.sleep(random.uniform(1.0, 2.5))
            
        except Exception as e:
            self.logger.warning(f"Error during initial article scan: {e}")
    
    def _natural_paragraph_reading(self, reading_rhythm):
        """Read a paragraph naturally based on reading rhythm - NO FAST READING"""
        try:
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Calculate reading speed based on rhythm (0-100)
            # Higher rhythm = slightly faster reading, but NO FAST READING
            base_scroll_amount = random.randint(30, 80)  # Much smaller, more human-like scrolls
            rhythm_multiplier = 0.5 + (reading_rhythm / 100) * 0.3  # 0.5x to 0.8x (NO FAST)
            scroll_amount = int(base_scroll_amount * rhythm_multiplier)
            
            # Add natural variation with micro-adjustments
            variation = random.uniform(0.6, 1.1)  # Reduced max variation
            scroll_amount = int(scroll_amount * variation)
            
            # Add micro-adjustments like human reading
            if random.random() < 0.4:  # 40% chance for micro-adjustment
                micro_adjustment = random.randint(-15, 15)
                scroll_amount += micro_adjustment
            
            # Check if we're near the end - but don't stop too early
            remaining_height = page_height - current_scroll - viewport_height
            if remaining_height < 100:  # Only stop when very close to bottom
                # Ensure we scroll to the very bottom to read everything
                self.logger.info("Near bottom, ensuring complete reading to the end")
                self._ensure_complete_bottom_reading()
                return "finished"
            
            # Determine scroll behavior based on reading rhythm - NO FAST READING
            if reading_rhythm < 40:  # Slow, careful reading
                # Use line-by-line scrolling for careful reading
                lines_to_scroll = random.randint(1, 3)  # Fewer lines for more careful reading
                self._natural_line_by_line_scroll(lines_to_scroll)
                
                # Much longer reading pause for comprehension
                reading_pause = random.uniform(8.0, 15.0)  # Much longer pauses for understanding
                time.sleep(reading_pause)
                
                # Add comprehension pause for complex content
                if random.random() < 0.3:  # 30% chance for comprehension pause
                    comprehension_pause = random.uniform(5.0, 12.0)
                    self.logger.info(f"Comprehension pause: {comprehension_pause:.1f}s")
                    time.sleep(comprehension_pause)
                
                # Higher chance of re-reading
                if random.random() < 0.4:  # Increased re-read chance
                    return "re_read_needed"
                    
            else:  # Normal reading (NO FAST READING)
                # Use paragraph-based scrolling for normal reading
                paragraph_length = random.choice(["short", "medium", "long"])
                self._natural_paragraph_scroll(paragraph_length)
                
                # Normal reading pause - much longer for understanding
                reading_pause = random.uniform(6.0, 12.0)  # Much longer normal pauses
                time.sleep(reading_pause)
                
                # Add thinking pause for processing information
                if random.random() < 0.25:  # 25% chance for thinking pause
                    thinking_pause = random.uniform(4.0, 10.0)
                    self.logger.info(f"Thinking pause: {thinking_pause:.1f}s")
                    time.sleep(thinking_pause)
                
                # Occasional re-reading
                if random.random() < 0.25:  # Increased re-read chance
                    return "re_read_needed"
            
            return "reading"
            
        except Exception as e:
            self.logger.warning(f"Error during natural paragraph reading: {e}")
            return "reading"
    
    def _re_read_previous_content(self):
        """Re-read previous content like humans do"""
        try:
            self.logger.info("Re-reading previous content")
            
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            
            # Scroll back to re-read (like humans do when they miss something)
            re_read_amount = random.randint(150, 400)
            new_position = max(0, current_scroll - re_read_amount)
            
            self._human_like_scroll_to_position(new_position, duration=2.0)
            
            # Longer pause for re-reading
            re_read_pause = random.uniform(4.0, 10.0)
            time.sleep(re_read_pause)
            
            # Mouse movement during re-reading (like following text)
            self._natural_mouse_tracking()
            
        except Exception as e:
            self.logger.warning(f"Error during re-reading: {e}")
    
    def _careful_content_scan(self):
        """Careful scanning behavior - NO FAST SCANNING"""
        try:
            self.logger.info("Careful content scanning")
            
            # Moderate scroll for careful scanning
            scan_amount = random.randint(200, 350)  # Reduced from 300-600
            self._human_like_scroll_by_amount(scan_amount, duration=1.5)  # Slower duration
            
            # Longer pause for careful scanning
            scan_pause = random.uniform(2.0, 4.0)  # Longer pause
            time.sleep(scan_pause)
            
        except Exception as e:
            self.logger.warning(f"Error during careful content scan: {e}")
    
    def _finish_reading_behavior(self):
        """Final reading behavior when near the end - comprehensive reading"""
        try:
            self.logger.info("📖 Starting comprehensive finish reading behavior")
            
            # Get page dimensions
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            
            # Ensure we're at the very bottom
            bottom_position = page_height - viewport_height
            self.logger.info(f"Scrolling to absolute bottom: {bottom_position}")
            self._human_like_scroll_to_position(bottom_position, duration=4.0)
            
            # Comprehensive bottom reading
            self.logger.info("Reading bottom content comprehensively")
            bottom_reading_pause = random.uniform(15.0, 25.0)  # Very long pause for bottom reading
            time.sleep(bottom_reading_pause)
            
            # Scroll up to re-read conclusion section
            conclusion_scroll = random.randint(300, 600)
            conclusion_position = max(0, bottom_position - conclusion_scroll)
            self.logger.info(f"Re-reading conclusion section from position: {conclusion_position}")
            self._human_like_scroll_to_position(conclusion_position, duration=3.0)
            
            # Read conclusion thoroughly
            conclusion_pause = random.uniform(12.0, 20.0)  # Long pause for conclusion
            time.sleep(conclusion_pause)
            
            # Scroll back to bottom for final verification
            self.logger.info("Final verification - scrolling back to bottom")
            self._human_like_scroll_to_position(bottom_position, duration=2.0)
            
            # Final comprehensive reading pause
            final_verification_pause = random.uniform(8.0, 15.0)
            self.logger.info(f"Final verification reading pause: {final_verification_pause:.1f}s")
            time.sleep(final_verification_pause)
            
            # Verify we've read the entire article
            self._verify_complete_article_reading()
            
            self.logger.info("✅ Comprehensive finish reading behavior completed")
            
        except Exception as e:
            self.logger.warning(f"Error during finish reading behavior: {e}")
    
    def _human_like_scroll_to_position(self, target_position, duration=2.0):
        """Human-like scroll to specific position with natural patterns"""
        try:
            current_position = self.driver.execute_script("return window.pageYOffset")
            distance = target_position - current_position
            
            if abs(distance) < 30:  # Already close enough
                return True
            
            # Human-like scroll patterns
            scroll_direction = 1 if distance > 0 else -1
            abs_distance = abs(distance)
            
            # Calculate natural scroll behavior
            if abs_distance < 200:  # Small scroll - single smooth movement
                self._natural_small_scroll(distance, duration)
            elif abs_distance < 800:  # Medium scroll - with micro-pauses
                self._natural_medium_scroll(distance, duration)
            else:  # Large scroll - with multiple phases
                self._natural_large_scroll(distance, duration)
            
            return True
            
        except Exception as e:
            return False
    
    def _natural_small_scroll(self, distance, duration):
        """Natural small scroll behavior"""
        try:
            # Small scrolls are usually smooth with slight variations
            steps = random.randint(3, 8)
            step_size = distance / steps
            step_duration = duration / steps
            
            for step in range(steps):
                # Natural scroll with slight acceleration/deceleration
                progress = (step + 1) / steps
                
                # Ease-in-out curve for natural movement
                if progress < 0.5:
                    ease_factor = 2 * progress * progress
                else:
                    ease_factor = 1 - 2 * (1 - progress) * (1 - progress)
                
                new_position = self.driver.execute_script("return window.pageYOffset") + (step_size * ease_factor)
                self.driver.execute_script(f"window.scrollTo(0, {new_position});")
                
                # Natural timing variation
                delay = step_duration * random.uniform(0.8, 1.3)
                time.sleep(delay)
                
                # Occasional micro-pause (like reading a word)
                if random.random() < 0.15:
                    micro_pause = random.uniform(0.1, 0.3)
                    time.sleep(micro_pause)
            
        except Exception as e:
            pass
    
    def _natural_medium_scroll(self, distance, duration):
        """Natural medium scroll behavior with micro-pauses"""
        try:
            # Medium scrolls have natural pauses and variations
            phases = random.randint(2, 4)  # Multiple phases
            phase_distance = distance / phases
            
            for phase in range(phases):
                # Scroll phase
                phase_start = self.driver.execute_script("return window.pageYOffset")
                phase_end = phase_start + phase_distance
                
                # Natural scroll within phase
                self._natural_small_scroll(phase_distance, duration / phases)
                
                # Natural pause between phases (like reading)
                if phase < phases - 1:  # Don't pause after last phase
                    pause_duration = random.uniform(0.3, 1.2)
                    time.sleep(pause_duration)
                    
                    # Occasional hesitation (like re-reading)
                    if random.random() < 0.2:
                        hesitation = random.uniform(0.5, 1.5)
                        time.sleep(hesitation)
            
        except Exception as e:
            pass
    
    def _natural_large_scroll(self, distance, duration):
        """Natural large scroll behavior with multiple phases and pauses"""
        try:
            # Large scrolls are broken into natural reading phases
            phases = random.randint(3, 6)
            phase_distance = distance / phases
            
            for phase in range(phases):
                # Scroll phase
                self._natural_medium_scroll(phase_distance, duration / phases)
                
                # Longer pause between phases (like reading a section) - much longer
                if phase < phases - 1:  # Don't pause after last phase
                    pause_duration = random.uniform(3.0, 8.0)  # Much longer pauses
                    time.sleep(pause_duration)
                    
                    # Occasional longer pause (like getting distracted) - more frequent and longer
                    if random.random() < 0.4:  # Increased chance
                        distraction_pause = random.uniform(5.0, 12.0)  # Much longer distraction pause
                        time.sleep(distraction_pause)
                        self.logger.info(f"Distraction pause during scroll: {distraction_pause:.1f}s")
            
        except Exception as e:
            pass
    
    def _human_like_scroll_by_amount(self, scroll_amount, duration=1.5):
        """Human-like scroll by specific amount"""
        try:
            current_position = self.driver.execute_script("return window.pageYOffset")
            target_position = current_position + scroll_amount
            self._human_like_scroll_to_position(target_position, duration)
        except Exception as e:
            pass
    
    def _calculate_natural_reading_pause(self, reading_rhythm):
        """Calculate natural pause between reading actions - NO FAST READING"""
        # Base pause based on reading rhythm - NO FAST READING
        if reading_rhythm < 40:  # Slow reading
            base_pause = random.uniform(8.0, 15.0)  # Much longer pauses for comprehension
        else:  # Normal reading (NO FAST READING)
            base_pause = random.uniform(6.0, 12.0)  # Much longer normal pauses
        
        # Add occasional longer pauses (like getting distracted or thinking) - more frequent and longer
        if random.random() < 0.35:  # Increased chance for distraction/thinking pause
            distraction_pause = random.uniform(12.0, 30.0)  # Much longer distraction pauses
            base_pause += distraction_pause
            self.logger.info(f"Distraction/thinking pause: {distraction_pause:.1f}s")
        
        # Add comprehension pause for complex content - more frequent and longer
        if random.random() < 0.3:  # Increased chance for comprehension pause
            comprehension_pause = random.uniform(8.0, 20.0)  # Much longer comprehension pause
            base_pause += comprehension_pause
            self.logger.info(f"Comprehension pause: {comprehension_pause:.1f}s")
        
        return base_pause
    
    def _natural_mouse_tracking(self):
        """Natural mouse movement like following text"""
        try:
            # Shorter, more natural mouse movements
            duration = random.uniform(0.5, 1.5)
            self.mouse.random_mouse_movement(duration)
        except Exception as e:
            pass
    
    def _ensure_complete_bottom_reading(self):
        """Ensure article is read completely to the bottom"""
        try:
            self.logger.info("📖 Ensuring complete reading to the bottom of the article")
            
            # Get current position and page dimensions
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Scroll to the very bottom
            bottom_position = page_height - viewport_height
            self.logger.info(f"Scrolling to bottom position: {bottom_position}")
            self._human_like_scroll_to_position(bottom_position, duration=3.0)
            
            # Read the bottom content thoroughly
            self.logger.info("Reading bottom content thoroughly")
            bottom_reading_pause = random.uniform(10.0, 20.0)  # Long pause for bottom reading
            time.sleep(bottom_reading_pause)
            
            # Scroll up a bit to re-read some bottom content
            if random.random() < 0.7:  # 70% chance to re-read bottom
                re_read_scroll = random.randint(100, 300)
                re_read_position = bottom_position - re_read_scroll
                self.logger.info(f"Re-reading bottom content from position: {re_read_position}")
                self._human_like_scroll_to_position(re_read_position, duration=2.0)
                
                # Read the re-read content
                re_read_pause = random.uniform(8.0, 15.0)
                time.sleep(re_read_pause)
                
                # Scroll back to bottom
                self._human_like_scroll_to_position(bottom_position, duration=2.0)
            
            # Final bottom reading pause
            final_bottom_pause = random.uniform(5.0, 12.0)
            self.logger.info(f"Final bottom reading pause: {final_bottom_pause:.1f}s")
            time.sleep(final_bottom_pause)
            
            self.logger.info("✅ Complete bottom reading finished")
            
        except Exception as e:
            self.logger.warning(f"Error in complete bottom reading: {e}")
    
    def _verify_complete_article_reading(self):
        """Verify that the entire article has been read comprehensively"""
        try:
            self.logger.info("🔍 Verifying complete article reading")
            
            # Get current position and page dimensions
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Calculate reading coverage
            max_scroll_position = page_height - viewport_height
            reading_coverage = (current_scroll / max_scroll_position) * 100 if max_scroll_position > 0 else 100
            
            self.logger.info(f"📊 Reading coverage: {reading_coverage:.1f}%")
            
            # Ensure we've covered at least 95% of the article
            if reading_coverage < 95:
                self.logger.info(f"⚠️ Reading coverage below 95% ({reading_coverage:.1f}%), ensuring complete coverage")
                
                # Scroll to any missed sections
                missed_sections = []
                for i in range(0, int(max_scroll_position), 500):  # Check every 500px
                    if i > current_scroll - 200:  # If we haven't read this section
                        missed_sections.append(i)
                
                # Read missed sections
                for section_position in missed_sections[:3]:  # Limit to 3 sections
                    self.logger.info(f"Reading missed section at position: {section_position}")
                    self._human_like_scroll_to_position(section_position, duration=2.0)
                    
                    # Read the section
                    section_reading_pause = random.uniform(8.0, 15.0)
                    time.sleep(section_reading_pause)
                
                # Final scroll to bottom
                self._human_like_scroll_to_position(max_scroll_position, duration=2.0)
                final_verification_pause = random.uniform(5.0, 10.0)
                time.sleep(final_verification_pause)
            
            # Final comprehensive reading verification
            self.logger.info("📖 Performing final comprehensive reading verification")
            
            # Scroll through the entire article one more time (quick scan)
            self._comprehensive_article_scan()
            
            self.logger.info("✅ Complete article reading verification finished")
            
        except Exception as e:
            self.logger.warning(f"Error in complete article reading verification: {e}")
    
    def _comprehensive_article_scan(self):
        """Perform a comprehensive scan of the entire article"""
        try:
            self.logger.info("📖 Performing comprehensive article scan")
            
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            max_scroll_position = page_height - viewport_height
            
            # Scan in sections
            section_size = 400  # 400px sections
            num_sections = max(1, int(max_scroll_position / section_size))
            
            for section in range(num_sections):
                section_position = section * section_size
                self.logger.info(f"Scanning section {section + 1}/{num_sections} at position: {section_position}")
                
                # Scroll to section
                self._human_like_scroll_to_position(section_position, duration=1.5)
                
                # Brief reading pause
                section_pause = random.uniform(3.0, 6.0)
                time.sleep(section_pause)
            
            # Final scroll to bottom
            self._human_like_scroll_to_position(max_scroll_position, duration=2.0)
            final_scan_pause = random.uniform(5.0, 10.0)
            time.sleep(final_scan_pause)
            
            self.logger.info("✅ Comprehensive article scan completed")
            
        except Exception as e:
            self.logger.warning(f"Error in comprehensive article scan: {e}")
    
    def _natural_paragraph_scroll(self, paragraph_length="medium"):
        """Natural scroll behavior based on paragraph length"""
        try:
            # Get current scroll position
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Calculate scroll amount based on paragraph length - more human-like
            if paragraph_length == "short":
                # Short paragraphs - very small, precise scrolls
                scroll_amount = random.randint(25, 60)  # Much smaller for human-like reading
                phases = random.randint(2, 4)  # More phases for smoothness
            elif paragraph_length == "long":
                # Long paragraphs - moderate scrolls with more pauses
                scroll_amount = random.randint(80, 150)  # Reduced for more natural reading
                phases = random.randint(3, 6)  # More phases for smoothness
            else:  # medium
                # Medium paragraphs - balanced scrolls
                scroll_amount = random.randint(50, 100)  # Reduced for more natural reading
                phases = random.randint(2, 4)  # More phases for smoothness
            
            # Natural scroll with phases
            phase_amount = scroll_amount / phases
            
            for phase in range(phases):
                # Scroll phase
                self._human_like_scroll_by_amount(phase_amount, duration=1.0)
                
                # Natural pause between phases (like reading) - much longer
                if phase < phases - 1:
                    pause_duration = random.uniform(3.0, 8.0)  # Much longer pauses between phases
                    time.sleep(pause_duration)
                    
                    # Occasional micro-scroll adjustment (more frequent)
                    if random.random() < 0.6:  # Increased chance for micro-adjustment
                        micro_adjustment = random.randint(-8, 8)  # Smaller adjustments
                        self._human_like_scroll_by_amount(micro_adjustment, duration=1.2)  # Longer duration
            
            return True
            
        except Exception as e:
            return False
    
    def _natural_line_by_line_scroll(self, lines=3):
        """Natural line-by-line scrolling like reading"""
        try:
            # Line-by-line scrolling is very natural - smaller and more human-like
            line_height = random.randint(12, 20)  # Smaller line height for more natural reading
            
            for line in range(lines):
                # Scroll one line with micro-adjustments
                scroll_amount = line_height + random.randint(-2, 2)  # Small variation
                self._human_like_scroll_by_amount(scroll_amount, duration=0.8)  # Longer duration
                
                # Natural pause between lines - much longer for comprehension
                line_pause = random.uniform(2.0, 5.0)  # Much longer pauses
                time.sleep(line_pause)
                
                # Occasional longer pause (like reading a complex sentence) - more frequent and longer
                if random.random() < 0.4:  # Increased chance
                    reading_pause = random.uniform(4.0, 10.0)  # Much longer reading pause
                    self.logger.info(f"Complex sentence reading pause: {reading_pause:.1f}s")
                    time.sleep(reading_pause)
                
                # Occasional micro-scroll adjustment - more frequent
                if random.random() < 0.5:  # Increased chance for micro-adjustment
                    micro_adjustment = random.randint(-3, 3)
                    self._human_like_scroll_by_amount(micro_adjustment, duration=0.8)  # Longer duration
            
            return True
            
        except Exception as e:
            return False
    
    def _navigate_with_referer(self, target_url, referer_url):
        """Navigate to target URL while maintaining referer using multiple methods"""
        try:
            self.logger.info(f"Navigating to {target_url} with referer {referer_url}")
            
            # Method 1: Try using link click with proper referer context
            try:
                self.driver.execute_script(f"""
                    // Store referer in session storage first
                    sessionStorage.setItem('referer', '{referer_url}');
                    
                    // Create a link element with proper referer
                    var link = document.createElement('a');
                    link.href = '{target_url}';
                    link.target = '_self';
                    link.rel = 'noreferrer';
                    
                    // Add referer to link data
                    link.setAttribute('data-referer', '{referer_url}');
                    
                    // Add link to DOM and click it
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                """)
                
                # Wait for navigation
                time.sleep(3)
                
                # Check if navigation was successful
                current_url = self.driver.current_url
                if target_url in current_url or 'rexdl.biz.id' in current_url:
                    self.logger.info("✅ Navigation successful using link click method")
                    return True
                    
            except Exception as e:
                self.logger.warning(f"Link click navigation failed: {e}")
            
            # Method 2: Try using form submission with referer
            try:
                self.driver.execute_script(f"""
                    // Store referer in session storage
                    sessionStorage.setItem('referer', '{referer_url}');
                    
                    // Create a form to submit with referer
                    var form = document.createElement('form');
                    form.method = 'GET';
                    form.action = '{target_url}';
                    form.target = '_self';
                    
                    // Add hidden input for referer
                    var refererInput = document.createElement('input');
                    refererInput.type = 'hidden';
                    refererInput.name = 'referer';
                    refererInput.value = '{referer_url}';
                    form.appendChild(refererInput);
                    
                    // Add form to DOM and submit
                    document.body.appendChild(form);
                    form.submit();
                """)
                
                # Wait for navigation
                time.sleep(3)
                
                # Check if navigation was successful
                current_url = self.driver.current_url
                if target_url in current_url or 'rexdl.biz.id' in current_url:
                    self.logger.info("✅ Navigation successful using form method")
                    return True
                    
            except Exception as e:
                self.logger.warning(f"Form navigation failed: {e}")
            
            # Method 3: Try using window.location with referer
            try:
                self.driver.execute_script(f"""
                    // Store referer in session storage
                    sessionStorage.setItem('referer', '{referer_url}');
                    
                    // Use window.location to navigate with referer
                    window.location.href = '{target_url}';
                """)
                
                # Wait for navigation
                time.sleep(3)
                
                # Check if navigation was successful
                current_url = self.driver.current_url
                if target_url in current_url or 'rexdl.biz.id' in current_url:
                    self.logger.info("✅ Navigation successful using window.location method")
                    return True
                    
            except Exception as e:
                self.logger.warning(f"Window.location navigation failed: {e}")
            
            # Method 4: Direct navigation as last resort
            self.logger.warning("All JavaScript methods failed, using direct navigation")
            self.driver.get(target_url)
            time.sleep(3)
            
            # Check if direct navigation was successful
            current_url = self.driver.current_url
            if target_url in current_url or 'rexdl.biz.id' in current_url:
                self.logger.info("✅ Direct navigation successful")
                return True
            else:
                self.logger.error(f"❌ All navigation methods failed. Current URL: {current_url}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error in navigate with referer: {e}")
            # Last resort: direct navigation
            try:
                self.driver.get(target_url)
                time.sleep(3)
                return True
            except Exception as e2:
                self.logger.error(f"Even direct navigation failed: {e2}")
                return False
    
    def _set_referer_header(self, referer_url):
        """Set referer header for next request using multiple methods"""
        try:
            # Method 1: Use JavaScript to simulate navigation with referer
            self.driver.execute_script(f"""
                // Create a link element with referer
                var link = document.createElement('a');
                link.href = window.location.href;
                link.rel = 'noreferrer';
                
                // Set referer in history state
                if (window.history && window.history.replaceState) {{
                    window.history.replaceState({{referer: '{referer_url}'}}, '', window.location.href);
                }}
                
                // Set document referrer
                Object.defineProperty(document, 'referrer', {{
                    value: '{referer_url}',
                    writable: false
                }});
            """)
            
            # Method 2: Use browser navigation with referer
            self.driver.execute_script(f"""
                // Simulate coming from referer
                window.history.pushState({{referer: '{referer_url}'}}, '', window.location.href);
            """)
            
            # Method 3: Set referer in session storage
            self.driver.execute_script(f"""
                sessionStorage.setItem('referer', '{referer_url}');
            """)
            
            self.logger.info(f"Set referer header using multiple methods: {referer_url}")
            
        except Exception as e:
            self.logger.warning(f"Could not set referer header: {e}")
    
    def _verify_referer_sent(self, expected_referer):
        """Verify that referer was sent to the current page using multiple methods"""
        try:
            # Method 1: Check document.referrer
            actual_referer = self.driver.execute_script("return document.referrer;")
            
            # Method 2: Check history state
            history_referer = self.driver.execute_script("return window.history.state ? window.history.state.referer : null;")
            
            # Method 3: Check session storage
            storage_referer = self.driver.execute_script("return sessionStorage.getItem('referer');")
            
            # Method 4: Check if referer is in URL parameters or headers
            current_url = self.driver.current_url
            
            referer_found = False
            referer_source = ""
            
            if actual_referer and expected_referer in actual_referer:
                referer_found = True
                referer_source = "document.referrer"
            elif history_referer and expected_referer in history_referer:
                referer_found = True
                referer_source = "history.state"
            elif storage_referer and expected_referer in storage_referer:
                referer_found = True
                referer_source = "sessionStorage"
            elif expected_referer in current_url:
                referer_found = True
                referer_source = "URL"
            
            if referer_found:
                self.logger.info(f"✅ Referer successfully detected via {referer_source}: {expected_referer}")
            else:
                self.logger.warning(f"⚠️ Referer not detected. Expected: {expected_referer}")
                self.logger.warning(f"   document.referrer: {actual_referer}")
                self.logger.warning(f"   history.state: {history_referer}")
                self.logger.warning(f"   sessionStorage: {storage_referer}")
                
        except Exception as e:
            self.logger.warning(f"Could not verify referer: {e}")
    
    def browse_article_content(self, duration_minutes=None, enable_post_navigation=True):
        """Browse article content with natural reading behavior and post navigation for AdSense RPM optimization"""
        try:
            # Calculate reading duration based on article length if not specified
            if duration_minutes is None:
                duration_minutes = self._calculate_reading_duration()
            
            self.logger.info(f"Browsing article content for {duration_minutes:.1f} minutes (based on article length)")
            
            # Track current post
            current_url = self.driver.current_url
            if current_url not in self.visited_posts:
                self.visited_posts.append(current_url)
                self.logger.info(f"📝 Added initial post to visited list: {current_url}")
                self.logger.info(f"📊 Current visited posts count: {len(self.visited_posts)}")
            
            # Use natural article reading behavior instead of random actions
            success = self._natural_article_reading(duration_minutes)
            
            if success:
                self.logger.info("Natural article reading completed successfully")
                
                # Optional: Add some additional natural behaviors after reading
                if random.random() < 0.3:  # 30% chance for additional behaviors
                    self._post_reading_behaviors()
                
                # Enable post navigation for AdSense RPM optimization
                if enable_post_navigation:
                    self.logger.info("🔄 Starting post navigation for AdSense RPM optimization")
                    self.logger.info(f"📊 Target: {self.min_posts_per_session}-{self.max_posts_per_session} posts per session")
                    
                    navigation_success = self._navigate_to_other_posts()
                    if navigation_success:
                        self.logger.info("✅ Post navigation completed successfully")
                    else:
                        self.logger.info("ℹ️ Post navigation completed (no more posts found)")
                    
                    # Check if minimum posts requirement is met
                    if len(self.visited_posts) < self.min_posts_per_session:
                        self.logger.warning(f"⚠️ Only visited {len(self.visited_posts)} posts (minimum required: {self.min_posts_per_session})")
                        self.logger.info(f"📋 Visited posts URLs: {self.visited_posts}")
                    else:
                        self.logger.info(f"✅ Successfully visited {len(self.visited_posts)} posts (minimum: {self.min_posts_per_session})")
                        self.logger.info(f"📋 Visited posts URLs: {self.visited_posts}")
                
                return True
            else:
                self.logger.warning("Natural article reading failed, falling back to basic browsing")
                return self._fallback_browsing_behavior(duration_minutes)
            
        except Exception as e:
            self.logger.error(f"Error browsing article content: {e}")
            return False
    
    def _navigate_to_other_posts(self):
        """Navigate to other posts (previous, next, related) for AdSense RPM optimization"""
        try:
            self.logger.info("🔍 Searching for other posts to navigate to")
            self.logger.info(f"📊 Current visited posts count: {len(self.visited_posts)}")
            self.logger.info(f"📋 Current visited posts: {self.visited_posts}")
            
            # Find navigation links
            navigation_links = self.post_navigator.find_navigation_links()
            
            if not any([navigation_links['previous'], navigation_links['next'], navigation_links['related']]):
                self.logger.info("ℹ️ No navigation links found")
                return False
            
            # Decide which post to navigate to
            available_options = []
            
            if navigation_links['previous']:
                href = navigation_links['previous'].get_attribute('href')
                if href and href not in self.visited_posts:
                    available_options.append(('previous', navigation_links['previous']))
            
            if navigation_links['next']:
                href = navigation_links['next'].get_attribute('href')
                if href and href not in self.visited_posts:
                    available_options.append(('next', navigation_links['next']))
            
            if navigation_links['related']:
                for link in navigation_links['related']:
                    href = link.get_attribute('href')
                    if href and href not in self.visited_posts:
                        available_options.append(('related', link))
                        break  # Only take first related post
            
            if not available_options:
                self.logger.info("ℹ️ No new posts available to navigate to")
                return False
            
            # Choose a post to navigate to (prefer next > related > previous)
            chosen_post = None
            for post_type in ['next', 'related', 'previous']:
                for option_type, link in available_options:
                    if option_type == post_type:
                        chosen_post = (option_type, link)
                        break
                if chosen_post:
                    break
            
            if not chosen_post:
                chosen_post = available_options[0]  # Fallback to first available
            
            post_type, link_element = chosen_post
            
            # Navigate to the chosen post
            self.logger.info(f"🔗 Navigating to {post_type} post for AdSense RPM optimization")
            navigation_success = self.post_navigator.navigate_to_post(link_element, post_type)
            
            if navigation_success:
                # Track the new post URL immediately after successful navigation
                current_url = self.driver.current_url
                if current_url not in self.visited_posts:
                    self.visited_posts.append(current_url)
                    self.logger.info(f"📝 Added post to visited list: {current_url}")
                    self.logger.info(f"📊 Current visited posts count: {len(self.visited_posts)}")
                
                # Calculate reading duration based on article length
                reading_duration = self._calculate_reading_duration()
                self.logger.info(f"📖 Reading {post_type} post for {reading_duration:.1f} minutes (based on article length)")
                
                # Use natural article reading instead of simple simulation
                reading_success = self._natural_article_reading(reading_duration)
                
                if reading_success:
                    self.logger.info(f"✅ Successfully read {post_type} post")
                    
                    # Check for ads after reading each post
                    if random.random() < 0.3:  # 30% chance to check for ads after each post
                        self.logger.info("🔍 Checking for Google AdSense ads after post reading...")
                        clicked_ads = self.ad_clicker.click_ads(max_clicks=1, conservative=True)
                        if clicked_ads:
                            self.logger.info(f"✅ Clicked {len(clicked_ads)} Google AdSense ads after post reading")
                        else:
                            self.logger.info("ℹ️ No suitable Google AdSense ads found after post reading")
                    
                    # Check if we need to continue (minimum posts requirement)
                    if len(self.visited_posts) < self.min_posts_per_session:
                        self.logger.info(f"🔄 Need to read more posts (minimum: {self.min_posts_per_session}, current: {len(self.visited_posts)})")
                        return self._navigate_to_other_posts()
                    elif len(self.visited_posts) < self.max_posts_per_session:
                        # Optional: continue if more posts available
                        if random.random() < 0.6:  # 60% chance to continue
                            self.logger.info(f"🔄 Continuing to read more posts (current: {len(self.visited_posts)}/{self.max_posts_per_session})")
                            return self._navigate_to_other_posts()
                        else:
                            self.logger.info(f"ℹ️ Stopping after {len(self.visited_posts)} posts (user choice)")
                            return True
                    else:
                        self.logger.info(f"ℹ️ Reached maximum posts per session ({self.max_posts_per_session})")
                        return True
                else:
                    self.logger.warning(f"⚠️ Failed to read {post_type} post")
                    return False
            else:
                self.logger.warning(f"⚠️ Failed to navigate to {post_type} post")
                return False
                
        except Exception as e:
            self.logger.error(f"Error navigating to other posts: {e}")
            return False
    
    def _calculate_reading_duration(self):
        """Calculate reading duration based on article length (4-10 minutes)"""
        try:
            self.logger.info("📏 Analyzing article length to determine reading duration")
            
            # Get article text content
            article_text = self._get_article_text()
            
            if not article_text:
                # Fallback to default duration if no text found
                default_duration = random.uniform(4.0, 6.0)
                self.logger.info(f"📏 No article text found, using default duration: {default_duration:.1f} minutes")
                return default_duration
            
            # Calculate reading metrics
            word_count = len(article_text.split())
            char_count = len(article_text)
            
            # Average reading speed: 200-300 words per minute
            avg_reading_speed = random.uniform(200, 300)  # words per minute
            
            # Calculate base reading time
            base_reading_time = word_count / avg_reading_speed
            
            # Apply minimum and maximum constraints
            min_reading_time = 4.0  # 4 minutes minimum
            max_reading_time = 10.0  # 10 minutes maximum
            
            # Clamp the reading time
            reading_time = max(min_reading_time, min(max_reading_time, base_reading_time))
            
            # Add some natural variation (±10%)
            variation = random.uniform(0.9, 1.1)
            final_reading_time = reading_time * variation
            
            # Ensure it's within bounds after variation
            final_reading_time = max(min_reading_time, min(max_reading_time, final_reading_time))
            
            self.logger.info(f"📏 Article Analysis:")
            self.logger.info(f"   Word Count: {word_count}")
            self.logger.info(f"   Character Count: {char_count}")
            self.logger.info(f"   Reading Speed: {avg_reading_speed:.0f} words/min")
            self.logger.info(f"   Base Reading Time: {base_reading_time:.1f} minutes")
            self.logger.info(f"   Final Reading Time: {final_reading_time:.1f} minutes")
            
            return final_reading_time
            
        except Exception as e:
            self.logger.error(f"Error calculating reading duration: {e}")
            # Fallback to default duration
            default_duration = random.uniform(4.0, 6.0)
            self.logger.info(f"📏 Using fallback duration: {default_duration:.1f} minutes")
            return default_duration
    
    def _get_article_text(self):
        """Extract article text content for length analysis"""
        try:
            # Try multiple selectors to find article content
            article_selectors = [
                'article', 'main', '.post-content', '.entry-content', '.article-content',
                '.content', '.post-body', '.entry-body', '.article-body', '.post-text',
                '.entry-text', '.article-text', '.post', '.entry', '.single-post',
                '.blog-post', '.news-article', '.story-content', '.text-content'
            ]
            
            article_text = ""
            
            for selector in article_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        text = element.text.strip()
                        if len(text) > len(article_text):
                            article_text = text
                except:
                    continue
            
            # If no specific article content found, try to get body text
            if not article_text or len(article_text) < 100:
                try:
                    body_element = self.driver.find_element("tag name", "body")
                    article_text = body_element.text.strip()
                except:
                    pass
            
            # Clean up the text
            if article_text:
                # Remove extra whitespace and newlines
                article_text = ' '.join(article_text.split())
                
                # Limit text length for analysis (first 5000 characters)
                if len(article_text) > 5000:
                    article_text = article_text[:5000]
            
            if article_text and len(article_text) > 50:
                self.logger.info(f"📏 Extracted article text: {len(article_text)} characters")
                return article_text
            else:
                self.logger.warning("📏 Could not extract sufficient article text")
                return None
                
        except Exception as e:
            self.logger.error(f"Error extracting article text: {e}")
            return None
    
    def get_post_navigation_stats(self):
        """Get statistics about post navigation for AdSense RPM optimization"""
        try:
            stats = {
                'total_posts_visited': len(self.visited_posts),
                'min_posts_per_session': self.min_posts_per_session,
                'max_posts_per_session': self.max_posts_per_session,
                'posts_remaining': self.max_posts_per_session - len(self.visited_posts),
                'minimum_met': len(self.visited_posts) >= self.min_posts_per_session,
                'visited_urls': self.visited_posts.copy()
            }
            
            self.logger.info("📊 Post Navigation Statistics:")
            self.logger.info(f"   Total Posts Visited: {stats['total_posts_visited']}")
            self.logger.info(f"   Min Posts Required: {stats['min_posts_per_session']}")
            self.logger.info(f"   Max Posts Per Session: {stats['max_posts_per_session']}")
            self.logger.info(f"   Posts Remaining: {stats['posts_remaining']}")
            self.logger.info(f"   Minimum Requirement Met: {'✅ Yes' if stats['minimum_met'] else '❌ No'}")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting post navigation stats: {e}")
            return None
    
    def _post_reading_behaviors(self):
        """Additional natural behaviors after reading"""
        try:
            self.logger.info("Performing post-reading behaviors")
            
            # Check for ads after reading (higher chance)
            if random.random() < 0.4:  # 40% chance to check for ads after reading
                self.logger.info("🔍 Checking for Google AdSense ads after reading...")
                clicked_ads = self.ad_clicker.click_ads(max_clicks=1, conservative=True)
                if clicked_ads:
                    self.logger.info(f"✅ Clicked {len(clicked_ads)} Google AdSense ads after reading")
                else:
                    self.logger.info("ℹ️ No suitable Google AdSense ads found after reading")
            
            # Random post-reading actions
            actions = [
                'scroll_to_top', 'scroll_to_bottom', 'careful_scan', 
                'mouse_exploration', 'pause_and_think'
            ]
            
            selected_actions = random.sample(actions, random.randint(1, 3))
            
            for action in selected_actions:
                if action == 'scroll_to_top':
                    self._human_like_scroll_to_position(0, duration=2.0)
                    time.sleep(random.uniform(2.0, 4.0))
                    
                elif action == 'scroll_to_bottom':
                    page_height = self.driver.execute_script("return document.body.scrollHeight")
                    self._human_like_scroll_to_position(page_height, duration=2.0)
                    time.sleep(random.uniform(2.0, 4.0))
                    
                elif action == 'careful_scan':
                    self._careful_content_scan()
                    
                elif action == 'mouse_exploration':
                    self._natural_mouse_tracking()
                    
                elif action == 'pause_and_think':
                    thinking_pause = random.uniform(3.0, 8.0)
                    time.sleep(thinking_pause)
                    self.logger.info(f"Thinking pause: {thinking_pause:.1f}s")
                
                # Small pause between actions
                time.sleep(random.uniform(1.0, 2.5))
            
        except Exception as e:
            self.logger.warning(f"Error in post-reading behaviors: {e}")
    
    def _fallback_browsing_behavior(self, duration_minutes=5):
        """Fallback browsing behavior if natural reading fails"""
        try:
            self.logger.info("Using fallback browsing behavior")
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while time.time() < end_time:
                # Check risk before each action
                signals = self.risk_monitor.check_detection_signals()
                if not self.risk_monitor.handle_risk(signals):
                    self.logger.warning("Risk handling prevented action")
                    continue
                
                # Simple, safe actions
                action = random.choice(['scroll', 'mouse_move', 'pause'])
                
                if action == 'scroll':
                    # Simple scroll behavior
                    scroll_amount = random.randint(100, 300)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(2.0, 5.0))
                    
                elif action == 'mouse_move':
                    self.mouse.random_mouse_movement(random.uniform(0.5, 1.5))
                    
                elif action == 'pause':
                    pause_duration = random.uniform(3.0, 8.0)
                    time.sleep(pause_duration)
                
                # Wait between actions
                time.sleep(random.uniform(1.0, 3.0))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in fallback browsing behavior: {e}")
            return False
    
    def _try_click_random_link(self):
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
                self.mouse.move_to_element(random_link)
                self.timing.wait_between_actions(0.5, 1.5)
                
                # Click link
                random_link.click()
                self.risk_monitor.record_request()
                
                # Wait for page load
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                self.logger.info("Clicked random link successfully")
                
        except Exception as e:
            self.logger.warning(f"Error clicking random link: {e}")
    
    
    def _navigate_to_next_post(self):
        """Navigate to next post menggunakan multiple selector strategies"""
        try:
            # Try different selector strategies
            for selector in self.patterns.navigation_patterns['next']:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if self._is_valid_navigation_element(element, "next"):
                            if self._click_navigation_element(element, "next"):
                                return True
                                
                except Exception as e:
                    continue
            
            return False
            
        except Exception as e:
            return False
    
    def _navigate_to_previous_post(self):
        """Navigate to previous post menggunakan multiple selector strategies"""
        try:
            # Try different selector strategies
            for selector in self.patterns.navigation_patterns['previous']:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if self._is_valid_navigation_element(element, "previous"):
                            if self._click_navigation_element(element, "previous"):
                                return True
                                
                except Exception as e:
                    continue
            
            return False
            
        except Exception as e:
            return False
    
    def _is_valid_navigation_element(self, element, direction):
        """Validate navigation element"""
        try:
            # Check if element is visible and clickable
            if not element.is_displayed():
                return False
            
            # Check if element has valid href
            href = element.get_attribute('href')
            if not href or href == '#' or 'javascript:void(0)' in href:
                return False
            
            # Check if element is in viewport
            location = element.location
            if location['x'] < 0 or location['y'] < 0:
                return False
            
            # Check element size
            size = element.size
            if size['width'] < 10 or size['height'] < 10:
                return False
            
            return True
            
        except Exception as e:
            return False
    
    def _click_navigation_element(self, element, direction):
        """Click navigation element dengan human-like behavior"""
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            
            # Wait for element to be clickable
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable(element))
            
            # Add human-like delay
            delay = self.timing.human_like_delay("clicking")
            time.sleep(delay)
            
            # Use mouse simulator for human-like clicking
            if self.mouse.move_to_element(element):
                element.click()
                
                # Wait for page load
                time.sleep(self.timing.human_like_delay("navigation"))
                
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def _find_and_click_random_link(self, same_domain=True, max_attempts=5):
        """Find and click a random link on the page"""
        try:
            # Get current domain
            current_url = self.driver.current_url
            current_domain = urlparse(current_url).netloc
            
            # Find all link elements
            link_elements = self.driver.find_elements(By.TAG_NAME, "a")
            valid_links = []
            
            for element in link_elements:
                try:
                    href = element.get_attribute("href")
                    if not href or "javascript:void(0)" in href:
                        continue
                    
                    # Check if element is visible and displayed
                    if not element.is_displayed():
                        continue
                    
                    # Test if element is clickable
                    WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(element))
                    
                    # Check domain if required
                    if same_domain:
                        try:
                            element_domain = urlparse(href).netloc
                            if element_domain and element_domain != current_domain:
                                continue
                        except:
                            # Assume relative URL if parsing fails
                            pass
                    
                    valid_links.append(element)
                    
                except Exception as e:
                    continue
            
            if not valid_links:
                return False
            
            # Select random link
            random_link = random.choice(valid_links)
            
            # Click the link
            if self._click_navigation_element(random_link, "random"):
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    
    def open_rexdl_cloud_article(self):
        article_url = "https://rexdl.biz.id/cloud-migration-challenges-in-the-us-and-how-to-overcome-them/"
        referer_options = [
            "https://google.com", "https://bing.com",
            "https://reddit.com", "https://twitter.com", "https://linkedin.com",
            "https://github.com", "https://stackoverflow.com", "https://medium.com"
        ]
        
        referer_url = random.choice(referer_options)
        
        self.logger.info(f"Opening RexDL Cloud Migration article with referer: {referer_url}")
        
        # SIMPLE FLOW: Referer → Inject Link → Click Article
        success = False
        
        try:
            self.logger.info("🔄 Starting simple referer flow: Referer → Inject Link → Click Article")
            success = self._simple_referer_flow(article_url, referer_url)
            if success:
                self.logger.info("✅ Article opened successfully with simple referer flow")
        except Exception as e:
            self.logger.warning(f"Simple referer flow failed: {e}")
        
        # Fallback: Direct navigation
        if not success:
            try:
                self.logger.info("Trying direct navigation as fallback")
                self.driver.get(article_url)
                
                # Longer pause for direct navigation
                self.logger.info("Waiting for article page to load completely (direct navigation)")
                time.sleep(10)
                
                current_url = self.driver.current_url
                if article_url in current_url or 'rexdl.biz.id' in current_url:
                    success = True
                    self.logger.info("✅ Direct navigation successful")
                    
                    # Additional pause after successful direct navigation
                    self.logger.info("Additional pause for article stabilization (direct navigation)")
                    time.sleep(5)
                else:
                    self.logger.error(f"❌ Direct navigation failed. Current URL: {current_url}")
            except Exception as e:
                self.logger.error(f"Direct navigation failed: {e}")
        
        if success:
            # Enable post navigation for AdSense RPM optimization with dynamic reading duration
            browse_success = self.browse_article_content(duration_minutes=None, enable_post_navigation=True)
            if browse_success:
                self.logger.info("RexDL article browsing with post navigation completed successfully")
                self.logger.info(f"📊 Total posts visited: {len(self.visited_posts)}")
                return True
            else:
                self.logger.error("RexDL article browsing failed")
                return False
        else:
            self.logger.error("Failed to open RexDL article")
            return False
    
    def _simple_referer_flow(self, article_url, referer_url):
        """Simple referer flow: 1. Buka referer 2. Inject link artikel 3. Klik dan buka article"""
        try:
            self.logger.info(f"🔄 Starting simple referer flow: {referer_url} → {article_url}")
            
            # Step 1: Buka referer
            self.logger.info(f"📍 Step 1: Buka referer: {referer_url}")
            self.driver.get(referer_url)
            self.timing.wait_between_actions(1, 2)  # Reduced from 2-4 seconds
            
            # Step 2: Simulate browsing on referer (quick)
            self.logger.info("📍 Step 2: Simulating referer browsing (bandwidth optimized)")
            self._simulate_referer_browsing()
            
            # Step 3: Inject link artikel di referer
            self.logger.info(f"📍 Step 3: Inject link artikel di referer: {article_url}")
            link_injected = self._inject_article_link(article_url)
            
            if link_injected:
                # Step 4: Klik dan buka article URL dari referer
                self.logger.info("📍 Step 4: Klik dan buka article URL dari referer")
                click_success = self._click_injected_link()
                
                if click_success:
                    # Step 5: Verify we're on the article page with longer pause
                    self.logger.info("📍 Step 5: Waiting for article page to load completely")
                    time.sleep(8)  # Longer pause for article loading
                    
                    current_url = self.driver.current_url
                    if article_url in current_url or 'rexdl.biz.id' in current_url:
                        self.logger.info("✅ Simple referer flow completed successfully")
                        
                        # Additional pause after successful navigation
                        self.logger.info("📍 Additional pause for article stabilization")
                        time.sleep(5)
                        
                        return True
                    else:
                        self.logger.warning(f"⚠️ Click completed but not on target page: {current_url}")
                        return False
                else:
                    self.logger.warning("⚠️ Failed to click injected link")
                    return False
            else:
                self.logger.warning("⚠️ Failed to inject article link")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in simple referer flow: {e}")
            return False
    
    def _inject_article_link(self, article_url):
        """Inject article link into the current referer page"""
        try:
            self.logger.info(f"Injecting article link: {article_url}")
            
            # Inject a natural-looking link into the page
            self.driver.execute_script(f"""
                // Create a natural-looking link
                var link = document.createElement('a');
                link.href = '{article_url}';
                link.textContent = 'Cloud Migration Challenges in the US and How to Overcome Them';
                link.style.cssText = `
                    color: #1a73e8;
                    text-decoration: none;
                    font-size: 16px;
                    font-weight: 500;
                    line-height: 1.5;
                    margin: 10px 0;
                    display: block;
                    padding: 8px 12px;
                    border-radius: 4px;
                    transition: background-color 0.2s;
                `;
                link.id = 'injected-article-link';
                
                // Add hover effect
                link.addEventListener('mouseenter', function() {{
                    this.style.backgroundColor = '#f8f9fa';
                }});
                link.addEventListener('mouseleave', function() {{
                    this.style.backgroundColor = 'transparent';
                }});
                
                // Try to find a good place to inject the link
                var targetElement = null;
                
                // Try to find main content area
                var mainContent = document.querySelector('main') || 
                                 document.querySelector('#main') || 
                                 document.querySelector('.main-content') ||
                                 document.querySelector('article') ||
                                 document.querySelector('.content');
                
                if (mainContent) {{
                    targetElement = mainContent;
                }} else {{
                    // Fallback to body
                    targetElement = document.body;
                }}
                
                // Insert the link at the beginning of the target element
                if (targetElement) {{
                    targetElement.insertBefore(link, targetElement.firstChild);
                    console.log('Article link injected successfully');
                    return true;
                }} else {{
                    console.log('No suitable target element found');
                    return false;
                }}
            """)
            
            # Verify link was injected
            try:
                link_element = self.driver.find_element("id", "injected-article-link")
                if link_element:
                    self.logger.info("✅ Article link injected successfully")
                    return True
                else:
                    self.logger.warning("⚠️ Link injection verification failed")
                    return False
            except:
                self.logger.warning("⚠️ Could not verify link injection")
                return False
                
        except Exception as e:
            self.logger.error(f"Error injecting article link: {e}")
            return False
    
    def _click_injected_link(self):
        """Click the injected article link"""
        try:
            self.logger.info("Clicking injected article link")
            
            # Find the injected link
            link_element = self.driver.find_element("id", "injected-article-link")
            
            if link_element:
                # Scroll to the link first
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link_element)
                time.sleep(1)
                
                # Move mouse to link and click
                self.mouse.move_to_element(link_element)
                time.sleep(0.5)
                
                # Click the link
                link_element.click()
                self.logger.info("✅ Article link clicked successfully")
                
                # Wait for navigation to start
                time.sleep(3)
                
                return True
            else:
                self.logger.warning("⚠️ Injected link not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Error clicking injected link: {e}")
            return False


class AdvancedWebsiteRobot:
    """
    Main class mengikuti pattern cookie_robot.py namun dengan kompleksitas tinggi
    """
    
    def __init__(self, driver, process_advanced_features=True, random_behavior=True):
        self.driver = driver
        self.process_advanced_features = process_advanced_features
        self.random_behavior = random_behavior
        
        # Initialize components
        self.timing = TimingSystem()
        self.mouse = MouseMovementSimulator(driver)
        self.risk_monitor = RiskMonitor(driver)
        self.article_browser = ArticleBrowser(driver, self.timing, self.mouse, self.risk_monitor)
        
        logging.info(f'AdvancedWebsiteRobot initialized')
        logging.info(f'Advanced features processing: {self.process_advanced_features}')
        logging.info(f'Random behavior: {self.random_behavior}')
    
    def run_advanced_automation(self):
        """
        Main automation function mengikuti pattern cookie_robot.py
        """
        try:
            logging.info("Starting advanced automation")
            
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
            self.timing.wait_between_actions(2, 4)
            
            if self.process_advanced_features:
                # Run advanced article browsing
                success = self.article_browser.open_rexdl_cloud_article()
                
                if success:
                    logging.info("✅ Advanced automation completed successfully!")
                    
                    # Get comprehensive statistics
                    try:
                        risk_stats = self.risk_monitor.get_risk_statistics()
                        ad_stats = self.article_browser.ad_clicker.get_click_statistics()
                        
                        logging.info(f"📊 Risk Statistics:")
                        logging.info(f"   Current Risk Level: {risk_stats['current_risk_level']}")
                        logging.info(f"   Total Requests: {risk_stats['total_requests']}")
                        logging.info(f"   Requests Last Minute: {risk_stats['requests_last_minute']}")
                        logging.info(f"   Detection Events: {risk_stats['detection_events']}")
                        
                        logging.info(f"📊 Ad Clicking Statistics:")
                        logging.info(f"   Total Clicks: {ad_stats['total_clicks']}")
                        logging.info(f"   Recent Clicks: {ad_stats['recent_clicks']}")
                        logging.info(f"   Rate Limit Clicks (20min): {ad_stats['rate_limit_clicks']}/3")
                        logging.info(f"   Rate Limit Remaining: {ad_stats['rate_limit_remaining']}")
                        logging.info(f"   Click Rate: {ad_stats['click_rate']:.2f} clicks/min")
                        logging.info(f"   Average Interval: {ad_stats['average_click_interval']:.2f}s")
                        logging.info(f"   Ad Types Clicked: {ad_stats['ad_types_clicked']}")
                        
                        # Display post navigation statistics for AdSense RPM optimization
                        try:
                            post_stats = self.article_browser.get_post_navigation_stats()
                            if post_stats:
                                logging.info(f"📊 Post Navigation Statistics (AdSense RPM Optimization):")
                                logging.info(f"   Total Posts Visited: {post_stats['total_posts_visited']}")
                                logging.info(f"   Min Posts Required: {post_stats['min_posts_per_session']}")
                                logging.info(f"   Max Posts Per Session: {post_stats['max_posts_per_session']}")
                                logging.info(f"   Posts Remaining: {post_stats['posts_remaining']}")
                                logging.info(f"   Minimum Requirement Met: {'✅ Yes' if post_stats['minimum_met'] else '❌ No'}")
                                logging.info(f"   Estimated Page Views: {post_stats['total_posts_visited']}")
                        except Exception as e:
                            logging.warning(f"Could not get post navigation statistics: {e}")
                        
                    except Exception as e:
                        logging.warning(f"Could not get comprehensive statistics: {e}")
                else:
                    logging.error("❌ Advanced automation failed")
            else:
                logging.info("Skipping advanced features processing")
            
            # Keep browser open for inspection
            logging.info("⏳ Keeping browser open for 30 seconds...")
            time.sleep(30)
            
            logging.info("✅ Advanced automation completed!")
            
        except Exception as e:
            logging.error(f"Error in advanced automation: {e}", exc_info=True)
            
            # Keep browser open even on error
            logging.info("⏳ Keeping browser open for 15 seconds after error...")
            time.sleep(15)
    
    def run(self):
        """
        Main run function mengikuti pattern cookie_robot.py
        """
        self.run_advanced_automation()


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

logging.info('Advanced Website Robot started')
logging.info(f'inputparams: {inputparams}')
logging.info(f'process_advanced_features: {process_advanced_features}')
logging.info(f'random_behavior: {random_behavior}')

# Create and run robot (mengikuti pattern cookie_robot.py)
robot = AdvancedWebsiteRobot(
    driver=driver,
    process_advanced_features=process_advanced_features,
    random_behavior=random_behavior
)

robot.run()
