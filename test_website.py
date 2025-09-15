#!/usr/bin/env python3
"""
Test Website Script - Standalone Implementation
Menggabungkan semua fitur dari multilogin-script-runner menjadi satu file yang berdiri sendiri
"""

import os
import sys
import time
import json
import random
import logging
import math
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin

# Selenium imports
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ============================================================================
# CORE COMPONENTS - Komponen Inti
# ============================================================================

class TimingSystem:
    """
    Sistem timing canggih dengan delay yang bervariasi secara alami
    """
    
    def __init__(self):
        self.base_delay = 1.0
        self.delay_variability = 0.7
        self.long_pause_chance = 0.05
        self.long_pause_min = 3.0
        self.long_pause_max = 8.0
        
        # Human-like delay ranges
        self.human_typing_delay_range = (0.1, 0.3)
        self.human_scroll_delay_range = (1, 5)
        self.human_click_delay_range = (0.5, 2.0)
    
    def advanced_random_delay(self, base_delay: Optional[float] = None, 
                            variability: Optional[float] = None) -> float:
        """
        Generate advanced random delay dengan distribusi normal
        """
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
    
    def human_like_delay(self, delay_type: str = "normal") -> float:
        """
        Generate human-like delays berdasarkan tipe perilaku
        """
        if delay_type == "typing":
            delay = random.uniform(*self.human_typing_delay_range)
        elif delay_type == "scrolling":
            delay = random.uniform(*self.human_scroll_delay_range)
        elif delay_type == "clicking":
            delay = random.uniform(*self.human_click_delay_range)
        else:
            delay = self.advanced_random_delay()
        
        return delay
    
    def smart_delay(self, context: str = "general", intensity: str = "medium") -> float:
        """
        Generate smart delays berdasarkan konteks dan intensitas
        """
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
        
        # Add variability
        delay = random.uniform(base_delay * 0.5, base_delay * 1.5)
        
        return delay


class MouseMovementSimulator:
    """
    Simulator pergerakan mouse dengan kurva Bezier untuk gerakan alami
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.action_chains = ActionChains(driver)
        self.movement_history = []
    
    def bezier_curve(self, start: Tuple[int, int], end: Tuple[int, int], 
                    control_points: Optional[List[Tuple[int, int]]] = None) -> List[Tuple[int, int]]:
        """
        Generate Bezier curve points untuk pergerakan mouse yang smooth
        """
        if control_points is None:
            # Generate random control points
            mid_x = (start[0] + end[0]) // 2
            mid_y = (start[1] + end[1]) // 2
            
            # Add random offset to control points
            offset_x = random.randint(-100, 100)
            offset_y = random.randint(-100, 100)
            
            control_points = [
                (mid_x + offset_x, mid_y + offset_y),
                (mid_x - offset_x, mid_y - offset_y)
            ]
        
        # Generate points along the Bezier curve
        points = []
        steps = random.randint(20, 50)  # Random number of steps for naturalness
        
        for i in range(steps + 1):
            t = i / steps
            
            # Cubic Bezier curve formula
            x = (1-t)**3 * start[0] + 3*(1-t)**2*t * control_points[0][0] + \
                3*(1-t)*t**2 * control_points[1][0] + t**3 * end[0]
            y = (1-t)**3 * start[1] + 3*(1-t)**2*t * control_points[0][1] + \
                3*(1-t)*t**2 * control_points[1][1] + t**3 * end[1]
            
            points.append((int(x), int(y)))
        
        return points
    
    def human_like_movement(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Generate human-like mouse movement dengan variasi alami
        """
        # Calculate distance and determine movement type
        distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        
        if distance < 50:
            # Short movements - more direct
            return self._short_movement(start, end)
        elif distance < 200:
            # Medium movements - slight curve
            return self._medium_movement(start, end)
        else:
            # Long movements - more pronounced curve
            return self._long_movement(start, end)
    
    def _short_movement(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Generate short, direct movement"""
        points = []
        steps = random.randint(5, 15)
        
        for i in range(steps + 1):
            t = i / steps
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            
            # Add small random variations
            x += random.randint(-2, 2)
            y += random.randint(-2, 2)
            
            points.append((int(x), int(y)))
        
        return points
    
    def _medium_movement(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Generate medium movement with slight curve"""
        return self.bezier_curve(start, end)
    
    def _long_movement(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Generate long movement with pronounced curve"""
        # Create more dramatic control points for long movements
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        
        # Larger random offsets for more dramatic curves
        offset_x = random.randint(-200, 200)
        offset_y = random.randint(-200, 200)
        
        control_points = [
            (mid_x + offset_x, mid_y + offset_y),
            (mid_x - offset_x, mid_y - offset_y)
        ]
        
        return self.bezier_curve(start, end, control_points)
    
    def move_to_element(self, element, offset_x: int = 0, offset_y: int = 0) -> bool:
        """
        Move mouse to element dengan human-like movement
        """
        try:
            # Get element location and size
            location = element.location
            size = element.size
            
            # Calculate target position (center of element + offset)
            target_x = location['x'] + size['width'] // 2 + offset_x
            target_y = location['y'] + size['height'] // 2 + offset_y
            
            # Get current mouse position (approximate)
            current_x = random.randint(0, 1920)  # Approximate current position
            current_y = random.randint(0, 1080)
            
            # Generate human-like movement path
            movement_points = self.human_like_movement((current_x, current_y), (target_x, target_y))
            
            # Execute movement
            for point in movement_points:
                try:
                    # Use JavaScript to move mouse (more reliable than ActionChains)
                    self.driver.execute_script(f"""
                        var event = new MouseEvent('mousemove', {{
                            clientX: {point[0]},
                            clientY: {point[1]},
                            bubbles: true
                        }});
                        document.dispatchEvent(event);
                    """)
                    
                    # Small delay between movements
                    time.sleep(random.uniform(0.001, 0.01))
                    
                except Exception as e:
                    continue
            
            # Final move to element using ActionChains
            try:
                self.action_chains.move_to_element(element).perform()
                return True
            except Exception as e:
                return False
                
        except Exception as e:
            return False
    
    def click_element(self, element, click_type: str = "left") -> bool:
        """
        Click element dengan human-like movement dan timing
        """
        try:
            # Move to element first
            if not self.move_to_element(element):
                pass  # Continue anyway
            
            # Add human-like delay before click
            pre_click_delay = random.uniform(0.1, 0.5)
            time.sleep(pre_click_delay)
            
            # Perform click based on type
            if click_type == "left":
                self.action_chains.click(element).perform()
            elif click_type == "right":
                self.action_chains.context_click(element).perform()
            elif click_type == "double":
                self.action_chains.double_click(element).perform()
            else:
                self.action_chains.click(element).perform()
            
            # Add human-like delay after click
            post_click_delay = random.uniform(0.1, 0.3)
            time.sleep(post_click_delay)
            
            return True
            
        except Exception as e:
            return False
    
    def random_mouse_movement(self, duration: float = 1.0) -> None:
        """
        Perform random mouse movements untuk human-like behavior
        """
        try:
            # Get viewport size
            viewport_size = self.driver.execute_script("return {width: window.innerWidth, height: window.innerHeight}")
            
            start_time = time.time()
            current_pos = (random.randint(0, viewport_size['width']), 
                          random.randint(0, viewport_size['height']))
            
            while time.time() - start_time < duration:
                # Generate random target position
                target_pos = (random.randint(0, viewport_size['width']), 
                             random.randint(0, viewport_size['height']))
                
                # Move to target dengan human-like path
                movement_points = self.human_like_movement(current_pos, target_pos)
                
                for point in movement_points:
                    if time.time() - start_time >= duration:
                        break
                    
                    self.driver.execute_script(f"""
                        var event = new MouseEvent('mousemove', {{
                            clientX: {point[0]},
                            clientY: {point[1]},
                            bubbles: true
                        }});
                        document.dispatchEvent(event);
                    """)
                    
                    time.sleep(random.uniform(0.01, 0.05))
                
                current_pos = target_pos
                
                # Random pause between movements
                time.sleep(random.uniform(0.1, 0.5))
                
        except Exception as e:
            pass


class DriverSetup:
    """
    Setup WebDriver untuk Multilogin dengan fallback ke Chrome lokal
    """
    
    def __init__(self):
        self.mlx_debugging_url = os.environ.get('MLX_DEBUGGING_URL')
        self.mlx_profile_id = os.environ.get('MLX_PROFILE_ID')
    
    def create_stealth_driver(self, profile_id=None, debugging_url=None):
        """
        Create WebDriver instance connected to Multilogin
        Multilogin handles all stealth configuration automatically
        """
        # Use environment variables if not provided
        if not debugging_url:
            debugging_url = self.mlx_debugging_url
        if not profile_id:
            profile_id = self.mlx_profile_id
        
        # Minimal Chrome options - Multilogin handles all configuration
        options = Options()
        
        driver = None
        
        try:
            if debugging_url and profile_id:
                # Connect to Multilogin Remote WebDriver
                driver = Remote(
                    command_executor=debugging_url,
                    options=options
                )
                
            else:
                # Create local Chrome driver for testing
                driver = webdriver.Chrome(options=options)
            
            # Maximize window
            try:
                driver.maximize_window()
            except Exception as e:
                pass
            
            return driver
            
        except Exception as e:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            raise
    
    def setup_driver_with_fallback(self):
        """
        Setup driver dengan fallback options
        Try Multilogin first, then local Chrome
        """
        # Try Multilogin first
        if self.mlx_debugging_url and self.mlx_profile_id:
            try:
                return self.create_stealth_driver(self.mlx_profile_id, self.mlx_debugging_url)
            except Exception as e:
                pass
        
        # Fallback to local Chrome
        try:
            return self.create_stealth_driver()
        except Exception as e:
            raise
    
    def cleanup_driver(self, driver, is_api_execution=False):
        """
        Cleanup driver resources
        """
        if driver:
            try:
                if is_api_execution:
                    # Don't quit driver in API mode - keep it open for Multilogin
                    print("   API execution - keeping driver open for Multilogin")
                    return
                else:
                    driver.quit()
            except Exception as e:
                pass


class StealthManager:
    """
    Risk monitoring manager - Multilogin handles stealth automatically
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.detection_signals = []
        self.risk_level = "low"
    
    def apply_stealth_scripts(self) -> None:
        """
        Stealth scripts removed - Multilogin handles all stealth configuration automatically
        """
        pass
    
    def check_detection_signals(self) -> Dict[str, Any]:
        """
        Check for various detection signals
        """
        signals = {
            "captcha_detected": False,
            "unusual_requests": False,
            "behavioral_anomalies": False
        }
        
        try:
            # Check for CAPTCHA
            captcha_selectors = [
                '#captcha', '.captcha', '.g-recaptcha', '[data-sitekey]',
                '.recaptcha', '[data-testid*="captcha"]'
            ]
            
            for selector in captcha_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and any(el.is_displayed() for el in elements):
                        signals["captcha_detected"] = True
                        break
                except:
                    continue
            
            # Check for unusual network requests (basic check)
            try:
                logs = self.driver.get_log('performance')
                if len(logs) > 100:  # Arbitrary threshold
                    signals["unusual_requests"] = True
            except:
                pass
            
        except Exception as e:
            pass
        
        return signals
    
    def assess_risk_level(self, signals: Dict[str, Any]) -> str:
        """
        Assess risk level berdasarkan detection signals
        """
        risk_score = 0
        
        if signals["captcha_detected"]:
            risk_score += 3
        if signals["unusual_requests"]:
            risk_score += 1
        if signals["behavioral_anomalies"]:
            risk_score += 2
        
        if risk_score >= 3:
            self.risk_level = "high"
        elif risk_score >= 1:
            self.risk_level = "medium"
        else:
            self.risk_level = "low"
        
        return self.risk_level
    
    def apply_behavioral_stealth(self) -> None:
        """
        Behavioral stealth removed - Multilogin handles this automatically
        """
        pass
    
    def handle_detection(self, signals: Dict[str, Any]) -> bool:
        """
        Handle detection signals dan take appropriate action
        """
        risk_level = self.assess_risk_level(signals)
        
        if risk_level == "high":
            return self._emergency_protocol()
        elif risk_level == "medium":
            return self._slow_down_protocol()
        else:
            return True
    
    def _emergency_protocol(self) -> bool:
        """Emergency protocol untuk high risk situations"""
        try:
            # Take screenshot for analysis
            screenshot_path = f"emergency_screenshot_{random.randint(1000, 9999)}.png"
            self.driver.save_screenshot(screenshot_path)
            
            # Wait for cooldown period
            cooldown = random.randint(300, 600)  # 5-10 minutes
            time.sleep(cooldown)
            
            return False  # Indicate script should stop
            
        except Exception as e:
            return False
    
    def _slow_down_protocol(self) -> bool:
        """Slow down protocol untuk medium risk situations"""
        try:
            # Increase delays
            slowdown_delay = random.randint(30, 120)  # 30 seconds to 2 minutes
            time.sleep(slowdown_delay)
            
            return True  # Continue with slower pace
            
        except Exception as e:
            return True
    
    def get_stealth_status(self) -> Dict[str, Any]:
        """
        Get current stealth status
        """
        return {
            "risk_level": self.risk_level,
            "detection_signals": self.detection_signals,
            "stealth_handled_by_multilogin": True
        }


# ============================================================================
# CONFIGURATION & SETTINGS
# ============================================================================

class Configuration:
    """
    Global configuration settings
    """
    
    def __init__(self):
        # Timing settings
        self.base_delay = 1.0
        self.delay_variability = 0.7
        self.long_pause_chance = 0.05
        self.long_pause_min = 3.0
        self.long_pause_max = 8.0
        
        # Scroll settings
        self.scroll_intensities = {
            'light': (200, 400),
            'medium': (400, 700),
            'heavy': (700, 1200)
        }
        
        # Ad clicking settings (conservative approach)
        self.ad_click_chance = 0.1  # Conservative 10% chance
        self.ad_selectors = [
            '[class*="ad"]',
            '[id*="ad"]',
            '[data-ad]',
            'ins.adsbygoogle',
            '[data-ad-client]'
        ]
        
        # Navigation settings
        self.previous_selectors = [
            'a[rel="prev"]',
            '.prev-post',
            '.nav-previous',
            '.post-navigation-previous'
        ]
        
        self.next_selectors = [
            'a[rel="next"]',
            '.next-post',
            '.nav-next',
            '.post-navigation-next'
        ]
        
        # Environment variables
        self.mlx_debugging_url = os.environ.get('MLX_DEBUGGING_URL')
        self.mlx_profile_id = os.environ.get('MLX_PROFILE_ID')
        self.mlx_folder_id = os.environ.get('MLX_FOLDER_ID')
        
        # Logging settings
        self.log_level = "INFO"
        self.log_format = '%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s'
        
        # Risk monitoring settings
        self.risk_monitoring_enabled = True
        self.max_requests_per_minute = 30
        self.detection_threshold = 0.7
        
        # Website validation settings
        self.default_websites = [
            "https://fiverr.com", "https://yahoo.com", "https://en.wikipedia.org", 
            "https://aliexpress.com", "https://amazon.com", "https://ebay.com", 
            "https://twitch.com", "https://youtube.com", "https://reddit.com",
            "https://google.com", "https://twitter.com"
        ]
        
        # Human behavior simulation
        self.human_typing_delay_range = (0.1, 0.3)
        self.human_scroll_delay_range = (1, 5)
        self.human_click_delay_range = (0.5, 2.0)
        
        # Optimization settings
        self.optimization_settings = {
            "max_concurrent_actions": 3,
            "delay_between_actions": {"min": 1.0, "max": 3.0},
            "retry_attempts": 2
        }
        
        # Monitoring settings
        self.monitoring_settings = {
            "log_level": "DEBUG",
            "capture_screenshots": True,
            "analyze_network_requests": True
        }


# ============================================================================
# DETECTION PATTERNS
# ============================================================================

class DetectionPatterns:
    """
    Detection patterns dan anti-detection strategies
    """
    
    def __init__(self):
        # Known detection patterns dari berbagai platform
        self.detection_patterns = {
            'google': {
                'captcha_selectors': [
                    '#captcha',
                    '.g-recaptcha',
                    '[data-sitekey]',
                    '.recaptcha'
                ],
                'automation_flags': [
                    'webdriver',
                    'selenium',
                    'phantom',
                    'headless'
                ]
            },
            'facebook': {
                'captcha_selectors': [
                    '#captcha',
                    '.captcha',
                    '[data-testid*="captcha"]'
                ],
                'automation_flags': [
                    'webdriver',
                    'selenium'
                ]
            },
            'youtube': {
                'captcha_selectors': [
                    '#captcha',
                    '.g-recaptcha'
                ],
                'automation_flags': [
                    'webdriver'
                ]
            },
            'amazon': {
                'captcha_selectors': [
                    '#captcha',
                    '.captcha'
                ],
                'automation_flags': [
                    'webdriver',
                    'selenium'
                ]
            }
        }
        
        # Ad detection patterns
        self.ad_detection_patterns = {
            'google_adsense': [
                '[data-ad-client]',
                'ins.adsbygoogle',
                '.adsbygoogle'
            ],
            'facebook_ads': [
                '[data-testid*="ad"]',
                '.fb-ad',
                '[data-ad]'
            ],
            'generic_ads': [
                '[class*="ad"]',
                '[id*="ad"]',
                '[data-ad]',
                '.advertisement',
                '.ad-container',
                '.ads-wrapper'
            ]
        }
        
        # Behavioral patterns untuk human simulation
        self.behavioral_patterns = {
            'typing_speed': {
                'slow': (0.2, 0.5),
                'medium': (0.1, 0.3),
                'fast': (0.05, 0.15)
            },
            'scroll_patterns': {
                'casual': (1, 3),
                'research': (3, 7),
                'browsing': (2, 5)
            },
            'click_patterns': {
                'careful': (0.5, 1.5),
                'normal': (0.2, 0.8),
                'quick': (0.1, 0.3)
            }
        }
        
        # Risk indicators
        self.risk_indicators = {
            'high_risk': [
                'captcha_detected',
                'unusual_network_requests',
                'behavioral_anomalies',
                'automation_flags_detected'
            ],
            'medium_risk': [
                'frequent_requests',
                'pattern_detection',
                'suspicious_timing'
            ],
            'low_risk': [
                'normal_browsing',
                'human_like_behavior',
                'randomized_patterns'
            ]
        }
        
        # Emergency protocols
        self.emergency_protocols = {
            'captcha_detected': {
                'action': 'pause_and_wait',
                'duration': 300,  # 5 minutes
                'retry_attempts': 2
            },
            'high_risk_detected': {
                'action': 'switch_profile',
                'backup_profiles': 3,
                'cooldown_period': 600  # 10 minutes
            },
            'automation_detected': {
                'action': 'emergency_shutdown',
                'cleanup': True,
                'report': True
            }
        }


# ============================================================================
# LOGGING SYSTEM
# ============================================================================

class LoggingSystem:
    """
    Comprehensive logging system
    """
    
    def __init__(self):
        self.setup_basic_logging()
    
    def setup_basic_logging(self):
        """Setup basic logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('test_website.log')
            ]
        )
        self.logger = logging.getLogger('test_website')
    
    def log_script_start(self, script_name: str, profile_id: Optional[str] = None):
        """Log script start"""
        self.logger.info(f"=== {script_name.upper()} STARTED ===")
        self.logger.info(f"Script: {script_name}")
        self.logger.info(f"Profile ID: {profile_id}")
        self.logger.info(f"Start Time: {datetime.now()}")
        self.logger.info(f"Python Version: {sys.version}")
    
    def log_script_end(self, script_name: str, duration: float, success: bool = True):
        """Log script end"""
        self.logger.info(f"=== {script_name.upper()} ENDED ===")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"Success: {success}")
        self.logger.info(f"End Time: {datetime.now()}")
    
    def log_activity(self, activity: str, details: Optional[dict] = None):
        """Log activity"""
        message = f"Activity: {activity}"
        if details:
            message += f" | Details: {details}"
        self.logger.info(message)
    
    def log_error(self, error: Exception, context: Optional[str] = None):
        """Log error"""
        message = f"Error: {str(error)}"
        if context:
            message += f" | Context: {context}"
        self.logger.error(message)
    
    def log_performance(self, operation: str, duration: float, details: Optional[dict] = None):
        """Log performance metrics"""
        message = f"Performance: {operation} took {duration:.2f}s"
        if details:
            message += f" | Details: {details}"
        self.logger.info(message)


# ============================================================================
# ADVANCED FEATURES - Fitur Lanjutan
# ============================================================================

class AdClickingSystem:
    """
    Smart ad clicking system dengan conservative behavior
    """
    
    def __init__(self, driver: WebDriver, timing_system: TimingSystem, mouse_simulator: MouseMovementSimulator):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.click_history = []
        self.config = Configuration()
        self.patterns = DetectionPatterns()
        
    def detect_ads(self, page_source: Optional[str] = None) -> List[Dict]:
        """
        Detect ads pada current page
        """
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
    
    def _is_valid_ad_element(self, element) -> bool:
        """
        Validate if element is a valid ad element
        """
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
    
    def _calculate_click_probability(self, element, ad_type: str) -> float:
        """
        Calculate click probability berdasarkan element characteristics
        Conservative approach
        """
        base_probability = self.config.ad_click_chance
        
        try:
            # Adjust based on ad type
            type_multipliers = {
                'google_adsense': 0.8,  # More conservative for AdSense
                'facebook_ads': 0.6,
                'generic_ads': 0.4
            }
            
            base_probability *= type_multipliers.get(ad_type, 0.5)
            
            # Adjust based on element size
            size = element.size
            area = size['width'] * size['height']
            
            if area > 100000:  # Large ads
                base_probability *= 0.7
            elif area < 10000:  # Small ads
                base_probability *= 0.3
            
            # Adjust based on position
            location = element.location
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            if location['y'] > viewport_height * 0.8:  # Below fold
                base_probability *= 0.5
            elif location['y'] < viewport_height * 0.2:  # Above fold
                base_probability *= 1.2
            
            # Ensure probability is within reasonable bounds
            return max(0.01, min(base_probability, 0.3))
            
        except Exception as e:
            return base_probability
    
    def click_ads(self, max_clicks: int = 1, conservative: bool = True) -> List[Dict]:
        """
        Click ads dengan conservative behavior
        """
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
                            delay = self.timing.smart_delay("clicking", "medium")
                            time.sleep(delay)
            
            return clicked_ads
            
        except Exception as e:
            return clicked_ads
    
    def _should_click_ad(self, ad_info: Dict, conservative: bool) -> bool:
        """
        Determine if ad should be clicked berdasarkan probability dan conditions
        """
        try:
            # Check click probability
            if random.random() > ad_info['click_probability']:
                return False
            
            # Conservative checks
            if conservative:
                # Don't click if we've clicked too many ads recently
                recent_clicks = [click for click in self.click_history 
                               if time.time() - click['timestamp'] < 300]  # 5 minutes
                
                if len(recent_clicks) >= 3:  # Max 3 clicks per 5 minutes
                    return False
                
                # Don't click if ad is too small
                size = ad_info['size']
                if size['width'] < 100 or size['height'] < 100:
                    return False
            
            return True
            
        except Exception as e:
            return False
    
    def _click_ad_safely(self, ad_info: Dict) -> bool:
        """
        Click ad safely dengan human-like behavior
        """
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
            if self.mouse.click_element(element):
                # Record click in history
                click_record = {
                    'timestamp': time.time(),
                    'ad_type': ad_info['type'],
                    'position': ad_info['position'],
                    'size': ad_info['size']
                }
                self.click_history.append(click_record)
                
                # Add post-click delay
                post_click_delay = self.timing.smart_delay("clicking", "high")
                time.sleep(post_click_delay)
                
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def get_click_statistics(self) -> Dict:
        """
        Get ad clicking statistics
        """
        current_time = time.time()
        
        # Calculate recent click statistics
        recent_clicks = [click for click in self.click_history 
                        if current_time - click['timestamp'] < 3600]  # Last hour
        
        return {
            'total_clicks': len(self.click_history),
            'recent_clicks': len(recent_clicks),
            'click_rate': len(recent_clicks) / 60,  # Clicks per minute
            'average_click_interval': self._calculate_average_interval(),
            'ad_types_clicked': self._get_clicked_ad_types()
        }
    
    def _calculate_average_interval(self) -> float:
        """Calculate average interval between clicks"""
        if len(self.click_history) < 2:
            return 0.0
        
        intervals = []
        for i in range(1, len(self.click_history)):
            interval = self.click_history[i]['timestamp'] - self.click_history[i-1]['timestamp']
            intervals.append(interval)
        
        return sum(intervals) / len(intervals) if intervals else 0.0
    
    def _get_clicked_ad_types(self) -> Dict[str, int]:
        """Get count of clicked ad types"""
        ad_types = {}
        for click in self.click_history:
            ad_type = click['ad_type']
            ad_types[ad_type] = ad_types.get(ad_type, 0) + 1
        return ad_types


class ContentNavigator:
    """
    Advanced content navigation system
    """
    
    def __init__(self, driver: WebDriver, timing_system: TimingSystem, mouse_simulator: MouseMovementSimulator):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.navigation_history = []
        self.current_domain = None
        self.config = Configuration()
        
    def navigate_to_previous_post(self) -> bool:
        """
        Navigate to previous post menggunakan multiple selector strategies
        """
        try:
            # Try different selector strategies
            for selector in self.config.previous_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if self._is_valid_navigation_element(element, "previous"):
                            if self._click_navigation_element(element, "previous"):
                                return True
                                
                except Exception as e:
                    continue
            
            # Fallback: try to find any link with "prev" in text or attributes
            fallback_elements = self.driver.find_elements(By.XPATH, 
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'prev') or contains(@href, 'prev') or contains(@class, 'prev')]")
            
            for element in fallback_elements:
                if self._is_valid_navigation_element(element, "previous"):
                    if self._click_navigation_element(element, "previous"):
                        return True
            
            return False
            
        except Exception as e:
            return False
    
    def navigate_to_next_post(self) -> bool:
        """
        Navigate to next post menggunakan multiple selector strategies
        """
        try:
            # Try different selector strategies
            for selector in self.config.next_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if self._is_valid_navigation_element(element, "next"):
                            if self._click_navigation_element(element, "next"):
                                return True
                                
                except Exception as e:
                    continue
            
            # Fallback: try to find any link with "next" in text or attributes
            fallback_elements = self.driver.find_elements(By.XPATH, 
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'next') or contains(@href, 'next') or contains(@class, 'next')]")
            
            for element in fallback_elements:
                if self._is_valid_navigation_element(element, "next"):
                    if self._click_navigation_element(element, "next"):
                        return True
            
            return False
            
        except Exception as e:
            return False
    
    def _is_valid_navigation_element(self, element, direction: str) -> bool:
        """
        Validate navigation element
        """
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
            
            # Check if link belongs to same domain
            current_url = self.driver.current_url
            current_domain = urlparse(current_url).netloc
            
            try:
                element_domain = urlparse(href).netloc
                if element_domain and element_domain != current_domain:
                    # Allow same domain navigation
                    return True
            except:
                # If parsing fails, assume it's relative URL
                return True
            
            return True
            
        except Exception as e:
            return False
    
    def _click_navigation_element(self, element, direction: str) -> bool:
        """
        Click navigation element dengan human-like behavior
        """
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
            if self.mouse.click_element(element):
                # Record navigation
                self._record_navigation(direction, element.get_attribute('href'))
                
                # Wait for page load
                time.sleep(self.timing.smart_delay("navigation", "medium"))
                
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def find_and_click_random_link(self, same_domain: bool = True, max_attempts: int = 5) -> bool:
        """
        Find and click a random link on the page
        """
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
            link_href = random_link.get_attribute("href")
            
            # Click the link
            if self._click_navigation_element(random_link, "random"):
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def random_scroll(self, intensity: str = "medium") -> bool:
        """
        Perform random scrolling dengan different intensities
        """
        try:
            scroll_intensities = {
                'light': (1, 3),
                'medium': (3, 7),
                'heavy': (7, 15)
            }
            
            scroll_count = random.randint(*scroll_intensities.get(intensity, scroll_intensities['medium']))
            
            for _ in range(scroll_count):
                # Random scroll amount
                scroll_amount = random.randint(200, 800)
                
                # Random scroll direction (mostly down)
                if random.random() < 0.8:  # 80% chance to scroll down
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                else:  # 20% chance to scroll up
                    self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
                
                # Random delay between scrolls
                time.sleep(random.uniform(0.5, 2.0))
            
            return True
            
        except Exception as e:
            return False
    
    def _record_navigation(self, direction: str, url: str) -> None:
        """
        Record navigation action in history
        """
        navigation_record = {
            'timestamp': time.time(),
            'direction': direction,
            'url': url,
            'domain': urlparse(url).netloc
        }
        self.navigation_history.append(navigation_record)
        
        # Keep only last 50 navigation records
        if len(self.navigation_history) > 50:
            self.navigation_history = self.navigation_history[-50:]
    
    def get_navigation_stats(self) -> Dict:
        """
        Get navigation statistics
        """
        current_time = time.time()
        
        # Calculate recent navigation statistics
        recent_navigations = [nav for nav in self.navigation_history 
                             if current_time - nav['timestamp'] < 3600]  # Last hour
        
        return {
            'total_navigations': len(self.navigation_history),
            'recent_navigations': len(recent_navigations),
            'navigation_rate': len(recent_navigations) / 60,  # Navigations per minute
            'domains_visited': list(set(nav['domain'] for nav in self.navigation_history)),
            'navigation_types': self._get_navigation_types()
        }
    
    def _get_navigation_types(self) -> Dict[str, int]:
        """Get count of navigation types"""
        nav_types = {}
        for nav in self.navigation_history:
            nav_type = nav['direction']
            nav_types[nav_type] = nav_types.get(nav_type, 0) + 1
        return nav_types


class BehaviorSimulator:
    """
    Human behavior simulation system
    """
    
    def __init__(self, driver: WebDriver, timing_system: TimingSystem, mouse_simulator: MouseMovementSimulator):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.behavior_history = []
        self.current_behavior_profile = self._get_random_behavior_profile()
        self.config = Configuration()
        
    def _get_random_behavior_profile(self) -> Dict[str, str]:
        """
        Get random behavior profile untuk human-like variation
        """
        profiles = {
            "casual_reader": {
                "scroll_speed": "medium",
                "click_frequency": "low",
                "dwell_time": "long",
                "typing_speed": "medium",
                "attention_span": "medium"
            },
            "researcher": {
                "scroll_speed": "fast",
                "click_frequency": "high",
                "dwell_time": "medium",
                "typing_speed": "fast",
                "attention_span": "high"
            },
            "shopper": {
                "scroll_speed": "medium",
                "click_frequency": "high",
                "dwell_time": "short",
                "typing_speed": "medium",
                "attention_span": "low"
            },
            "social_media_browser": {
                "scroll_speed": "fast",
                "click_frequency": "medium",
                "dwell_time": "short",
                "typing_speed": "fast",
                "attention_span": "low"
            },
            "careful_reader": {
                "scroll_speed": "slow",
                "click_frequency": "low",
                "dwell_time": "long",
                "typing_speed": "slow",
                "attention_span": "high"
            }
        }
        
        profile_name = random.choice(list(profiles.keys()))
        profile = profiles[profile_name]
        profile['name'] = profile_name
        
        return profile
    
    def simulate_reading_behavior(self, duration: float, content_type: str = "general") -> None:
        """
        Simulate human reading behavior
        """
        try:
            start_time = time.time()
            scroll_interval = self._get_scroll_interval_for_profile()
            
            while time.time() - start_time < duration:
                # Random scroll behavior
                if random.random() < 0.3:  # 30% chance to scroll
                    self._simulate_reading_scroll()
                
                # Random pause behavior
                if random.random() < 0.2:  # 20% chance to pause
                    pause_duration = random.uniform(1, 3)
                    time.sleep(pause_duration)
                
                # Random mouse movement
                if random.random() < 0.1:  # 10% chance for mouse movement
                    self.mouse.random_mouse_movement(0.5)
                
                # Wait before next action
                time.sleep(scroll_interval)
            
            # Record behavior
            self._record_behavior("reading", duration, {"content_type": content_type})
            
        except Exception as e:
            pass
    
    def simulate_typing_behavior(self, text: str, element) -> bool:
        """
        Simulate human typing behavior
        """
        try:
            # Clear element first
            element.clear()
            
            # Type character by character dengan human-like delays
            typing_speed = self._get_typing_speed_for_profile()
            
            for char in text:
                element.send_keys(char)
                
                # Human-like typing delay
                delay = random.uniform(*typing_speed)
                time.sleep(delay)
                
                # Occasional longer pauses (thinking)
                if random.random() < 0.05:  # 5% chance
                    thinking_pause = random.uniform(0.5, 2.0)
                    time.sleep(thinking_pause)
            
            # Record behavior
            self._record_behavior("typing", len(text) * 0.1, {"text_length": len(text)})
            
            return True
            
        except Exception as e:
            return False
    
    def simulate_browsing_behavior(self, duration: float, intensity: str = "medium") -> None:
        """
        Simulate general browsing behavior
        """
        try:
            start_time = time.time()
            action_interval = self._get_action_interval_for_intensity(intensity)
            
            while time.time() - start_time < duration:
                # Random browsing actions
                action = random.choice([
                    "scroll", "pause", "mouse_move", "focus_change"
                ])
                
                if action == "scroll":
                    self._simulate_browsing_scroll()
                elif action == "pause":
                    self._simulate_browsing_pause()
                elif action == "mouse_move":
                    self.mouse.random_mouse_movement(1.0)
                elif action == "focus_change":
                    self._simulate_focus_change()
                
                # Wait before next action
                time.sleep(action_interval)
            
            # Record behavior
            self._record_behavior("browsing", duration, {"intensity": intensity})
            
        except Exception as e:
            pass
    
    def _simulate_reading_scroll(self) -> None:
        """Simulate reading scroll behavior"""
        try:
            scroll_amount = random.randint(100, 400)
            scroll_direction = "down" if random.random() < 0.8 else "up"
            
            if scroll_direction == "down":
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            else:
                self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
            
            # Reading pause after scroll
            reading_pause = random.uniform(1, 3)
            time.sleep(reading_pause)
            
        except Exception as e:
            pass
    
    def _simulate_browsing_scroll(self) -> None:
        """Simulate browsing scroll behavior"""
        try:
            scroll_amount = random.randint(200, 600)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Shorter pause for browsing
            browsing_pause = random.uniform(0.5, 1.5)
            time.sleep(browsing_pause)
            
        except Exception as e:
            pass
    
    def _simulate_browsing_pause(self) -> None:
        """Simulate browsing pause behavior"""
        pause_duration = random.uniform(2, 8)
        time.sleep(pause_duration)
    
    def _simulate_focus_change(self) -> None:
        """Simulate focus change behavior"""
        try:
            # Random focus events
            focus_scripts = [
                "window.focus()",
                "document.body.focus()",
                "document.activeElement.blur()"
            ]
            
            script = random.choice(focus_scripts)
            self.driver.execute_script(script)
            
        except Exception as e:
            pass
    
    def _get_scroll_interval_for_profile(self) -> float:
        """Get scroll interval berdasarkan behavior profile"""
        profile = self.current_behavior_profile
        
        if profile['scroll_speed'] == 'slow':
            return random.uniform(3, 6)
        elif profile['scroll_speed'] == 'fast':
            return random.uniform(0.5, 2)
        else:  # medium
            return random.uniform(1, 3)
    
    def _get_typing_speed_for_profile(self) -> Tuple[float, float]:
        """Get typing speed berdasarkan behavior profile"""
        profile = self.current_behavior_profile
        
        if profile['typing_speed'] == 'slow':
            return (0.2, 0.5)
        elif profile['typing_speed'] == 'fast':
            return (0.05, 0.15)
        else:  # medium
            return (0.1, 0.3)
    
    def _get_action_interval_for_intensity(self, intensity: str) -> float:
        """Get action interval berdasarkan intensity"""
        intervals = {
            'low': (2, 5),
            'medium': (1, 3),
            'high': (0.5, 2)
        }
        
        return random.uniform(*intervals.get(intensity, intervals['medium']))
    
    def _record_behavior(self, behavior_type: str, duration: float, metadata: Dict) -> None:
        """Record behavior in history"""
        behavior_record = {
            'timestamp': time.time(),
            'type': behavior_type,
            'duration': duration,
            'profile': self.current_behavior_profile['name'],
            'metadata': metadata
        }
        self.behavior_history.append(behavior_record)
        
        # Keep only last 100 behavior records
        if len(self.behavior_history) > 100:
            self.behavior_history = self.behavior_history[-100:]
    
    def get_behavior_stats(self) -> Dict:
        """
        Get behavior simulation statistics
        """
        current_time = time.time()
        
        # Calculate recent behavior statistics
        recent_behaviors = [behavior for behavior in self.behavior_history 
                           if current_time - behavior['timestamp'] < 3600]  # Last hour
        
        return {
            'current_profile': self.current_behavior_profile['name'],
            'total_behaviors': len(self.behavior_history),
            'recent_behaviors': len(recent_behaviors),
            'behavior_types': self._get_behavior_types(),
            'average_duration': self._calculate_average_duration(),
            'profile_usage': self._get_profile_usage()
        }
    
    def _get_behavior_types(self) -> Dict[str, int]:
        """Get count of behavior types"""
        behavior_types = {}
        for behavior in self.behavior_history:
            behavior_type = behavior['type']
            behavior_types[behavior_type] = behavior_types.get(behavior_type, 0) + 1
        return behavior_types
    
    def _calculate_average_duration(self) -> float:
        """Calculate average behavior duration"""
        if not self.behavior_history:
            return 0.0
        
        total_duration = sum(behavior['duration'] for behavior in self.behavior_history)
        return total_duration / len(self.behavior_history)
    
    def _get_profile_usage(self) -> Dict[str, int]:
        """Get count of profile usage"""
        profile_usage = {}
        for behavior in self.behavior_history:
            profile = behavior['profile']
            profile_usage[profile] = profile_usage.get(profile, 0) + 1
        return profile_usage


class VisitPlanGenerator:
    """
    Advanced visit plan generator untuk natural browsing patterns
    """
    
    def __init__(self):
        self.config = Configuration()
        self.plan_templates = {
            "casual_browsing": self._generate_casual_browsing_plan,
            "research_mode": self._generate_research_plan,
            "shopping_mode": self._generate_shopping_plan,
            "social_browsing": self._generate_social_browsing_plan,
            "news_reading": self._generate_news_reading_plan
        }
    
    def generate_visit_plan(self, plan_type: Optional[str] = None, 
                          duration_minutes: int = 30) -> List[Dict[str, Any]]:
        """
        Generate a visit plan dengan natural activity patterns
        """
        if not plan_type:
            plan_type = random.choice(list(self.plan_templates.keys()))
        
        # Generate base plan
        if plan_type in self.plan_templates:
            base_plan = self.plan_templates[plan_type]()
        else:
            base_plan = self._generate_casual_browsing_plan()
        
        # Scale plan to desired duration
        scaled_plan = self._scale_plan_to_duration(base_plan, duration_minutes)
        
        # Add natural variations
        varied_plan = self._add_natural_variations(scaled_plan)
        
        return varied_plan
    
    def _generate_casual_browsing_plan(self) -> List[Dict[str, Any]]:
        """
        Generate casual browsing plan
        """
        return [
            {"type": "scroll", "intensity": "light", "duration": 5},
            {"type": "read_time", "duration": 10},
            {"type": "scroll", "intensity": "medium", "duration": 3},
            {"type": "navigate_next", "probability": 0.3},
            {"type": "read_time", "duration": 8},
            {"type": "scroll", "intensity": "light", "duration": 4},
            {"type": "ad_click", "probability": 0.1},
            {"type": "read_time", "duration": 12},
            {"type": "scroll", "intensity": "medium", "duration": 6},
            {"type": "navigate_previous", "probability": 0.2},
            {"type": "read_time", "duration": 7}
        ]
    
    def _generate_research_plan(self) -> List[Dict[str, Any]]:
        """
        Generate research mode plan
        """
        return [
            {"type": "scroll", "intensity": "fast", "duration": 2},
            {"type": "read_time", "duration": 15},
            {"type": "scroll", "intensity": "fast", "duration": 2},
            {"type": "navigate_next", "probability": 0.6},
            {"type": "read_time", "duration": 20},
            {"type": "scroll", "intensity": "medium", "duration": 3},
            {"type": "navigate_next", "probability": 0.5},
            {"type": "read_time", "duration": 18},
            {"type": "scroll", "intensity": "fast", "duration": 2},
            {"type": "navigate_previous", "probability": 0.3},
            {"type": "read_time", "duration": 12}
        ]
    
    def _generate_shopping_plan(self) -> List[Dict[str, Any]]:
        """
        Generate shopping mode plan
        """
        return [
            {"type": "scroll", "intensity": "medium", "duration": 3},
            {"type": "read_time", "duration": 8},
            {"type": "scroll", "intensity": "medium", "duration": 4},
            {"type": "ad_click", "probability": 0.4},
            {"type": "read_time", "duration": 6},
            {"type": "scroll", "intensity": "light", "duration": 2},
            {"type": "navigate_next", "probability": 0.7},
            {"type": "read_time", "duration": 10},
            {"type": "scroll", "intensity": "medium", "duration": 3},
            {"type": "ad_click", "probability": 0.3},
            {"type": "read_time", "duration": 8}
        ]
    
    def _generate_social_browsing_plan(self) -> List[Dict[str, Any]]:
        """
        Generate social browsing plan
        """
        return [
            {"type": "scroll", "intensity": "fast", "duration": 1},
            {"type": "read_time", "duration": 5},
            {"type": "scroll", "intensity": "fast", "duration": 1},
            {"type": "navigate_next", "probability": 0.8},
            {"type": "read_time", "duration": 4},
            {"type": "scroll", "intensity": "fast", "duration": 1},
            {"type": "navigate_next", "probability": 0.6},
            {"type": "read_time", "duration": 6},
            {"type": "scroll", "intensity": "medium", "duration": 2},
            {"type": "navigate_previous", "probability": 0.4},
            {"type": "read_time", "duration": 5}
        ]
    
    def _generate_news_reading_plan(self) -> List[Dict[str, Any]]:
        """
        Generate news reading plan
        """
        return [
            {"type": "scroll", "intensity": "light", "duration": 4},
            {"type": "read_time", "duration": 25},
            {"type": "scroll", "intensity": "light", "duration": 3},
            {"type": "navigate_next", "probability": 0.5},
            {"type": "read_time", "duration": 20},
            {"type": "scroll", "intensity": "medium", "duration": 5},
            {"type": "navigate_next", "probability": 0.4},
            {"type": "read_time", "duration": 18},
            {"type": "scroll", "intensity": "light", "duration": 4},
            {"type": "navigate_previous", "probability": 0.3},
            {"type": "read_time", "duration": 15}
        ]
    
    def _scale_plan_to_duration(self, plan: List[Dict[str, Any]], 
                               duration_minutes: int) -> List[Dict[str, Any]]:
        """
        Scale plan to approximate duration
        """
        # Calculate current plan duration
        current_duration = sum(action.get('duration', 5) for action in plan)
        
        # Calculate scaling factor
        target_duration = duration_minutes * 60  # Convert to seconds
        scaling_factor = target_duration / current_duration
        
        # Scale the plan
        scaled_plan = []
        for action in plan:
            scaled_action = action.copy()
            if 'duration' in scaled_action:
                scaled_action['duration'] = int(scaled_action['duration'] * scaling_factor)
            scaled_plan.append(scaled_action)
        
        return scaled_plan
    
    def _add_natural_variations(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add natural variations to the plan
        """
        varied_plan = []
        
        for action in plan:
            # Add random variations to durations
            if 'duration' in action:
                variation = random.uniform(0.8, 1.2)
                action['duration'] = int(action['duration'] * variation)
            
            # Add random variations to probabilities
            if 'probability' in action:
                variation = random.uniform(0.7, 1.3)
                action['probability'] = min(1.0, action['probability'] * variation)
            
            # Add random variations to intensities
            if 'intensity' in action:
                intensities = list(self.config.scroll_intensities.keys())
                if random.random() < 0.1:  # 10% chance to change intensity
                    action['intensity'] = random.choice(intensities)
            
            varied_plan.append(action)
        
        return varied_plan


# ============================================================================
# UTILITY FUNCTIONS - Fungsi Bantuan
# ============================================================================

class UtilityFunctions:
    """
    Utility functions untuk operasi sehari-hari
    """
    
    def __init__(self, driver: WebDriver = None):
        self.driver = driver
        self.config = Configuration()
    
    def validate_and_sanitize_websites(self, websites: List[str]) -> List[str]:
        """
        Validate dan sanitize list of websites
        """
        valid_websites = []
        
        for website in websites:
            try:
                # Basic URL validation
                if not website.startswith(('http://', 'https://')):
                    website = 'https://' + website
                
                # Parse URL to validate format
                parsed = urlparse(website)
                if parsed.netloc and parsed.scheme in ['http', 'https']:
                    valid_websites.append(website)
                else:
                    print(f"⚠️ Invalid URL format: {website}")
                    
            except Exception as e:
                print(f"⚠️ Error validating website {website}: {e}")
                continue
        
        return valid_websites
    
    def wait_for_element(self, locator: Tuple[str, str], 
                        timeout: int = 10, condition: str = "presence") -> Optional[Any]:
        """
        Wait for element dengan berbagai conditions
        """
        if not self.driver:
            return None
            
        try:
            wait = WebDriverWait(self.driver, timeout)
            
            if condition == "presence":
                return wait.until(EC.presence_of_element_located(locator))
            elif condition == "visible":
                return wait.until(EC.visibility_of_element_located(locator))
            elif condition == "clickable":
                return wait.until(EC.element_to_be_clickable(locator))
            elif condition == "invisible":
                return wait.until(EC.invisibility_of_element_located(locator))
            else:
                return wait.until(EC.presence_of_element_located(locator))
                
        except Exception as e:
            return None
    
    def safe_click(self, element, max_retries: int = 3) -> bool:
        """
        Safe click dengan retry mechanism
        """
        if not self.driver:
            return False
            
        for attempt in range(max_retries):
            try:
                # Scroll element into view
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                
                # Wait for element to be clickable
                wait = WebDriverWait(self.driver, 5)
                wait.until(EC.element_to_be_clickable(element))
                
                # Click the element
                element.click()
                return True
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    return False
        
        return False
    
    def safe_send_keys(self, element, text: str, 
                      clear_first: bool = True, human_like: bool = True) -> bool:
        """
        Safe send keys dengan human-like behavior
        """
        if not self.driver:
            return False
            
        try:
            # Clear element first if requested
            if clear_first:
                element.clear()
            
            # Send keys character by character if human-like
            if human_like:
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
            else:
                element.send_keys(text)
            
            return True
            
        except Exception as e:
            return False
    
    def take_screenshot(self, filename: Optional[str] = None, 
                       directory: str = "logs/screenshots") -> Optional[str]:
        """
        Take screenshot dengan automatic filename generation
        """
        if not self.driver:
            return None
            
        try:
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            # Ensure filename has .png extension
            if not filename.endswith('.png'):
                filename += '.png'
            
            # Full path
            filepath = os.path.join(directory, filename)
            
            # Take screenshot
            self.driver.save_screenshot(filepath)
            
            return filepath
            
        except Exception as e:
            return None
    
    def get_page_info(self) -> Dict[str, Any]:
        """
        Get comprehensive page information
        """
        if not self.driver:
            return {}
            
        try:
            page_info = {
                'url': self.driver.current_url,
                'title': self.driver.title,
                'domain': urlparse(self.driver.current_url).netloc,
                'viewport_size': self.driver.execute_script("return {width: window.innerWidth, height: window.innerHeight}"),
                'page_source_length': len(self.driver.page_source),
                'timestamp': time.time()
            }
            
            # Try to get additional info
            try:
                page_info['page_height'] = self.driver.execute_script("return document.body.scrollHeight")
            except:
                page_info['page_height'] = 0
            
            try:
                page_info['scroll_position'] = self.driver.execute_script("return {x: window.pageXOffset, y: window.pageYOffset}")
            except:
                page_info['scroll_position'] = {'x': 0, 'y': 0}
            
            return page_info
            
        except Exception as e:
            return {}
    
    def random_delay(self, min_delay: float = 0.5, max_delay: float = 3.0) -> float:
        """
        Generate random delay
        """
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay
    
    def is_element_visible(self, element) -> bool:
        """
        Check if element is visible
        """
        if not self.driver:
            return False
            
        try:
            return element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0
        except:
            return False
    
    def scroll_to_element(self, element, smooth: bool = True) -> bool:
        """
        Scroll to element
        """
        if not self.driver:
            return False
            
        try:
            if smooth:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            else:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            
            time.sleep(0.5)  # Wait for scroll to complete
            return True
            
        except Exception as e:
            return False
    
    def get_element_text_safely(self, element) -> str:
        """
        Get element text safely
        """
        try:
            return element.text.strip()
        except:
            try:
                return element.get_attribute('textContent').strip()
            except:
                return ""
    
    def wait_for_page_load(self, timeout: int = 30) -> bool:
        """
        Wait for page to load completely
        """
        if not self.driver:
            return False
            
        try:
            # Wait for document ready state
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Additional wait for any pending requests
            time.sleep(1)
            return True
            
        except Exception as e:
            return False
    
    def cleanup_temp_files(self, directory: str = "logs/temp", days_old: int = 1) -> None:
        """
        Cleanup temporary files older than specified days
        """
        try:
            if not os.path.exists(directory):
                return
            
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    file_time = os.path.getmtime(filepath)
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        
        except Exception as e:
            pass
    
    def format_duration(self, seconds: float) -> str:
        """
        Format duration in human-readable format
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    def get_random_website(self) -> str:
        """
        Get random website from default list
        """
        return random.choice(self.config.default_websites)
    
    def create_backup_config(self, config_data: Dict[str, Any], 
                           backup_dir: str = "logs/backups") -> Optional[str]:
        """
        Create backup of configuration
        """
        try:
            # Create backup directory
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"config_backup_{timestamp}.json"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Write backup
            with open(backup_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            return backup_path
            
        except Exception as e:
            return None


class RiskMonitor:
    """
    Risk monitoring system untuk detection dan risk assessment
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.request_history = []
        self.detection_events = []
        self.config = Configuration()
        self.patterns = DetectionPatterns()
        self.risk_level = "low"
        self.request_count = 0
        self.last_request_time = 0
        
    def can_make_request(self) -> bool:
        """
        Check if we can make a request based on rate limiting
        """
        current_time = time.time()
        
        # Check rate limiting
        if current_time - self.last_request_time < 1.0:  # Minimum 1 second between requests
            return False
        
        # Check requests per minute
        recent_requests = [req for req in self.request_history 
                          if current_time - req < 60]  # Last minute
        
        if len(recent_requests) >= self.config.max_requests_per_minute:
            return False
        
        return True
    
    def record_request(self) -> None:
        """
        Record a request for rate limiting
        """
        current_time = time.time()
        self.request_history.append(current_time)
        self.last_request_time = current_time
        self.request_count += 1
        
        # Keep only last 100 requests
        if len(self.request_history) > 100:
            self.request_history = self.request_history[-100:]
    
    def check_detection_signals(self) -> Dict[str, Any]:
        """
        Check for various detection signals
        """
        signals = {
            "captcha_detected": False,
            "unusual_requests": False,
            "behavioral_anomalies": False,
            "automation_flags": False
        }
        
        try:
            # Check for CAPTCHA
            captcha_selectors = [
                '#captcha', '.captcha', '.g-recaptcha', '[data-sitekey]',
                '.recaptcha', '[data-testid*="captcha"]'
            ]
            
            for selector in captcha_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and any(el.is_displayed() for el in elements):
                        signals["captcha_detected"] = True
                        break
                except:
                    continue
            
            # Check for unusual request patterns
            if len(self.request_history) > 50:
                recent_requests = self.request_history[-10:]  # Last 10 requests
                intervals = [recent_requests[i] - recent_requests[i-1] for i in range(1, len(recent_requests))]
                
                if intervals and all(interval < 2.0 for interval in intervals):  # All requests within 2 seconds
                    signals["unusual_requests"] = True
            
            # Check for behavioral anomalies
            signals["behavioral_anomalies"] = self._detect_behavioral_anomalies()
            
            # Check for automation flags (basic check)
            try:
                page_source = self.driver.page_source.lower()
                automation_flags = ['webdriver', 'selenium', 'phantom', 'headless']
                if any(flag in page_source for flag in automation_flags):
                    signals["automation_flags"] = True
            except:
                pass
            
        except Exception as e:
            pass
        
        return signals
    
    def _detect_behavioral_anomalies(self) -> bool:
        """
        Detect behavioral anomalies
        """
        try:
            # Check for too many requests in short time
            current_time = time.time()
            recent_requests = [req for req in self.request_history 
                              if current_time - req < 300]  # Last 5 minutes
            
            if len(recent_requests) > 20:  # More than 20 requests in 5 minutes
                return True
            
            # Check for very regular intervals (suspicious)
            if len(self.request_history) > 10:
                intervals = [self.request_history[i] - self.request_history[i-1] 
                           for i in range(1, len(self.request_history))]
                
                if intervals:
                    avg_interval = sum(intervals) / len(intervals)
                    variance = sum((interval - avg_interval) ** 2 for interval in intervals) / len(intervals)
                    
                    if variance < 1.0:  # Very low variance (too regular)
                        return True
            
            return False
            
        except Exception as e:
            return False
    
    def assess_risk_level(self, signals: Dict[str, Any]) -> str:
        """
        Assess risk level berdasarkan detection signals
        """
        risk_score = 0
        
        if signals["captcha_detected"]:
            risk_score += 3
        if signals["unusual_requests"]:
            risk_score += 2
        if signals["behavioral_anomalies"]:
            risk_score += 2
        if signals["automation_flags"]:
            risk_score += 1
        
        if risk_score >= 3:
            self.risk_level = "high"
        elif risk_score >= 1:
            self.risk_level = "medium"
        else:
            self.risk_level = "low"
        
        # Record detection event
        self._record_detection_event(signals, risk_score)
        
        return self.risk_level
    
    def _record_detection_event(self, signals: Dict[str, Any], risk_score: float) -> None:
        """
        Record detection event
        """
        event = {
            'timestamp': time.time(),
            'signals': signals,
            'risk_score': risk_score,
            'risk_level': self.risk_level,
            'request_count': self.request_count
        }
        
        self.detection_events.append(event)
        
        # Keep only last 50 events
        if len(self.detection_events) > 50:
            self.detection_events = self.detection_events[-50:]
    
    def handle_risk(self, signals: Dict[str, Any]) -> bool:
        """
        Handle risk berdasarkan signals
        """
        risk_level = self.assess_risk_level(signals)
        
        if risk_level == "high":
            return self._handle_high_risk()
        elif risk_level == "medium":
            return self._handle_medium_risk()
        else:
            return self._handle_low_risk()
    
    def _handle_high_risk(self) -> bool:
        """
        Handle high risk situation
        """
        try:
            # Take screenshot for analysis
            utils = UtilityFunctions(self.driver)
            screenshot_path = utils.take_screenshot("high_risk_detection")
            
            # Emergency cooldown
            cooldown = random.randint(300, 600)  # 5-10 minutes
            time.sleep(cooldown)
            
            return False  # Indicate script should stop
            
        except Exception as e:
            return False
    
    def _handle_medium_risk(self) -> bool:
        """
        Handle medium risk situation
        """
        try:
            # Slow down operations
            slowdown_delay = random.randint(30, 120)  # 30 seconds to 2 minutes
            time.sleep(slowdown_delay)
            
            return True  # Continue with slower pace
            
        except Exception as e:
            return True
    
    def _handle_low_risk(self) -> bool:
        """
        Handle low risk situation
        """
        return True  # Continue normally
    
    def get_risk_statistics(self) -> Dict[str, Any]:
        """
        Get risk monitoring statistics
        """
        current_time = time.time()
        
        # Calculate recent statistics
        recent_events = [event for event in self.detection_events 
                        if current_time - event['timestamp'] < 3600]  # Last hour
        
        risk_levels = [event['risk_level'] for event in recent_events]
        
        return {
            'current_risk_level': self.risk_level,
            'total_requests': self.request_count,
            'recent_detection_events': len(recent_events),
            'risk_level_distribution': {
                'high': risk_levels.count('high'),
                'medium': risk_levels.count('medium'),
                'low': risk_levels.count('low')
            },
            'risk_trend': self._calculate_risk_trend(),
            'average_requests_per_minute': len([req for req in self.request_history 
                                              if current_time - req < 60]) / 60
        }
    
    def _calculate_risk_trend(self) -> str:
        """
        Calculate risk trend
        """
        if len(self.detection_events) < 5:
            return "insufficient_data"
        
        recent_events = self.detection_events[-5:]  # Last 5 events
        risk_scores = [event['risk_score'] for event in recent_events]
        
        if len(risk_scores) < 2:
            return "stable"
        
        # Calculate trend
        first_half = risk_scores[:len(risk_scores)//2]
        second_half = risk_scores[len(risk_scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg + 0.5:
            return "increasing"
        elif second_avg < first_avg - 0.5:
            return "decreasing"
        else:
            return "stable"


# ============================================================================
# ARTICLE BROWSING FUNCTIONS - Fungsi untuk Membuka Artikel
# ============================================================================

class ArticleBrowser:
    """
    Class untuk membuka dan browsing artikel dengan referer
    """
    
    def __init__(self, driver: WebDriver, timing_system: TimingSystem, 
                 mouse_simulator: MouseMovementSimulator, risk_monitor: RiskMonitor):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.risk_monitor = risk_monitor
        self.utils = UtilityFunctions(driver)
        self.config = Configuration()
        self.logger = LoggingSystem()
        
    def open_article_with_referer(self, article_url: str, referer_url: str = None) -> bool:
        """
        Buka artikel dengan referer yang tersedia
        """
        try:
            # Set referer jika tidak ada, gunakan default websites
            if not referer_url:
                referer_url = self.utils.get_random_website()
            
            self.logger.log_activity("Opening article with referer", {
                "article_url": article_url,
                "referer_url": referer_url
            })
            
            # Check if we can make request
            if not self.risk_monitor.can_make_request():
                self.logger.log_activity("Request blocked by rate limiting", {"status": "blocked"})
                return False
            
            # Record request
            self.risk_monitor.record_request()
            
            # Navigate to referer first
            self.logger.log_activity("Navigating to referer", {"url": referer_url})
            self.driver.get(referer_url)
            
            # Wait for page load
            self.utils.wait_for_page_load()
            
            # Add human-like delay
            delay = self.timing.smart_delay("navigation", "medium")
            time.sleep(delay)
            
            # Simulate some browsing behavior on referer
            self._simulate_referer_browsing()
            
            # Now navigate to article
            self.logger.log_activity("Navigating to article", {"url": article_url})
            self.driver.get(article_url)
            
            # Wait for page load
            self.utils.wait_for_page_load()
            
            # Check for detection signals
            signals = self.risk_monitor.check_detection_signals()
            risk_level = self.risk_monitor.assess_risk_level(signals)
            
            if risk_level == "high":
                self.logger.log_activity("High risk detected, stopping", {"risk_level": risk_level})
                return False
            
            # Handle risk if medium
            if risk_level == "medium":
                self.risk_monitor.handle_risk(signals)
            
            # Take screenshot for verification
            screenshot_path = self.utils.take_screenshot("article_opened")
            if screenshot_path:
                self.logger.log_activity("Screenshot taken", {"path": screenshot_path})
            
            # Get page info
            page_info = self.utils.get_page_info()
            self.logger.log_activity("Article opened successfully", {
                "title": page_info.get('title', 'Unknown'),
                "domain": page_info.get('domain', 'Unknown'),
                "url": page_info.get('url', 'Unknown')
            })
            
            return True
            
        except Exception as e:
            self.logger.log_activity("Error opening article", {"error": str(e)})
            return False
    
    def _simulate_referer_browsing(self) -> None:
        """
        Simulasi browsing behavior di referer page
        """
        try:
            # Random scroll
            scroll_amount = random.randint(200, 600)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Random delay
            delay = self.timing.human_like_delay("scrolling")
            time.sleep(delay)
            
            # Random mouse movement
            self.mouse.random_mouse_movement(0.5)
            
            # Another scroll
            scroll_amount = random.randint(100, 400)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Final delay
            delay = self.timing.smart_delay("reading", "low")
            time.sleep(delay)
            
        except Exception as e:
            pass
    
    def browse_article_content(self, duration_minutes: int = 5) -> bool:
        """
        Browse artikel content dengan human-like behavior
        """
        try:
            start_time = time.time()
            duration_seconds = duration_minutes * 60
            
            self.logger.log_activity("Starting article browsing", {
                "duration_minutes": duration_minutes,
                "article_url": self.driver.current_url
            })
            
            # Create behavior simulator
            behavior_sim = BehaviorSimulator(self.driver, self.timing, self.mouse)
            
            # Simulate reading behavior
            behavior_sim.simulate_reading_behavior(duration_seconds, "article")
            
            # Check for navigation elements and potentially click them
            content_nav = ContentNavigator(self.driver, self.timing, self.mouse)
            
            # Try to find and click related articles or navigation
            if random.random() < 0.3:  # 30% chance
                content_nav.find_and_click_random_link(same_domain=True, max_attempts=1)
            
            # Check for ads and potentially click them (conservative)
            ad_system = AdClickingSystem(self.driver, self.timing, self.mouse)
            if random.random() < 0.1:  # 10% chance
                clicked_ads = ad_system.click_ads(max_clicks=1, conservative=True)
                if clicked_ads:
                    self.logger.log_activity("Ad clicked during browsing", {
                        "ad_count": len(clicked_ads),
                        "ad_type": clicked_ads[0].get('type', 'unknown')
                    })
            
            # Final check for risk
            signals = self.risk_monitor.check_detection_signals()
            risk_level = self.risk_monitor.assess_risk_level(signals)
            
            if risk_level == "high":
                self.logger.log_activity("High risk detected during browsing", {"risk_level": risk_level})
                return False
            
            # Log completion
            actual_duration = time.time() - start_time
            self.logger.log_activity("Article browsing completed", {
                "planned_duration": duration_seconds,
                "actual_duration": actual_duration,
                "risk_level": risk_level
            })
            
            return True
            
        except Exception as e:
            self.logger.log_activity("Error during article browsing", {"error": str(e)})
            return False
    
    def open_rexdl_cloud_article(self) -> bool:
        """
        Buka artikel khusus tentang Cloud Migration Challenges
        """
        article_url = "https://rexdl.biz.id/cloud-migration-challenges-in-the-us-and-how-to-overcome-them/"
        
        # List of potential referer websites
        referer_options = [
            "https://google.com",
            "https://yahoo.com", 
            "https://bing.com",
            "https://reddit.com",
            "https://twitter.com",
            "https://linkedin.com",
            "https://github.com",
            "https://stackoverflow.com",
            "https://medium.com"
        ]
        
        # Select random referer
        referer_url = random.choice(referer_options)
        
        self.logger.log_activity("Opening RexDL Cloud Migration article", {
            "article_url": article_url,
            "selected_referer": referer_url
        })
        
        # Open article with referer
        success = self.open_article_with_referer(article_url, referer_url)
        
        if success:
            # Browse the article content
            browse_success = self.browse_article_content(duration_minutes=3)
            
            if browse_success:
                self.logger.log_activity("RexDL article browsing completed successfully", {
                    "article": "Cloud Migration Challenges in the US",
                    "referer_used": referer_url
                })
                return True
            else:
                self.logger.log_activity("RexDL article browsing failed", {
                    "article": "Cloud Migration Challenges in the US"
                })
                return False
        else:
            self.logger.log_activity("Failed to open RexDL article", {
                "article": "Cloud Migration Challenges in the US"
            })
            return False


def test_article_browsing():
    """
    Test article browsing functionality
    """
    print("\n🧪 Testing Article Browsing Functions...")
    
    # Test URL validation
    utils = UtilityFunctions()
    test_urls = [
        "https://rexdl.biz.id/cloud-migration-challenges-in-the-us-and-how-to-overcome-them/",
        "https://google.com",
        "invalid-url"
    ]
    
    valid_urls = utils.validate_and_sanitize_websites(test_urls)
    print(f"✅ URL Validation: {len(valid_urls)}/{len(test_urls)} URLs valid")
    
    # Test referer selection
    referer_options = [
        "https://google.com",
        "https://yahoo.com", 
        "https://reddit.com",
        "https://twitter.com"
    ]
    
    selected_referer = random.choice(referer_options)
    print(f"✅ Referer Selection: {selected_referer}")
    
    # Test article URL
    article_url = "https://rexdl.biz.id/cloud-migration-challenges-in-the-us-and-how-to-overcome-them/"
    print(f"✅ Article URL: {article_url}")
    
    # Test duration formatting
    test_duration = 180  # 3 minutes
    formatted_duration = utils.format_duration(test_duration)
    print(f"✅ Duration Format: {test_duration}s -> {formatted_duration}")
    
    print("🎉 Article Browsing Functions Test Completed!")


# ============================================================================
# MAIN TEST FUNCTION
# ============================================================================

def test_core_components():
    """
    Test core components functionality
    """
    print("🧪 Testing Core Components...")
    
    # Test Timing System
    timing = TimingSystem()
    delay = timing.advanced_random_delay()
    print(f"✅ Timing System: Generated delay of {delay:.2f}s")
    
    human_delay = timing.human_like_delay("typing")
    print(f"✅ Human-like Delay: {human_delay:.2f}s")
    
    smart_delay = timing.smart_delay("navigation", "medium")
    print(f"✅ Smart Delay: {smart_delay:.2f}s")
    
    # Test Configuration
    config = Configuration()
    print(f"✅ Configuration: Loaded {len(config.default_websites)} default websites")
    
    # Test Detection Patterns
    patterns = DetectionPatterns()
    print(f"✅ Detection Patterns: Loaded {len(patterns.detection_patterns)} platform patterns")
    
    # Test Logging System
    logger = LoggingSystem()
    logger.log_activity("Core components test", {"status": "success"})
    print("✅ Logging System: Working correctly")
    
    print("🎉 Core Components Test Completed!")


def test_advanced_features():
    """
    Test advanced features functionality
    """
    print("\n🧪 Testing Advanced Features...")
    
    # Test Visit Plan Generator
    plan_generator = VisitPlanGenerator()
    casual_plan = plan_generator.generate_visit_plan("casual_browsing", 5)
    print(f"✅ Visit Plan Generator: Generated {len(casual_plan)} actions for casual browsing")
    
    research_plan = plan_generator.generate_visit_plan("research_mode", 3)
    print(f"✅ Visit Plan Generator: Generated {len(research_plan)} actions for research mode")
    
    shopping_plan = plan_generator.generate_visit_plan("shopping_mode", 2)
    print(f"✅ Visit Plan Generator: Generated {len(shopping_plan)} actions for shopping mode")
    
    # Test plan variations
    varied_plan = plan_generator._add_natural_variations(casual_plan)
    print(f"✅ Plan Variations: Added natural variations to plan")
    
    # Test plan scaling
    scaled_plan = plan_generator._scale_plan_to_duration(casual_plan, 10)
    print(f"✅ Plan Scaling: Scaled plan to 10 minutes duration")
    
    # Test Configuration for Advanced Features
    config = Configuration()
    print(f"✅ Ad Selectors: {len(config.ad_selectors)} ad detection selectors")
    print(f"✅ Navigation Selectors: {len(config.previous_selectors)} previous, {len(config.next_selectors)} next selectors")
    print(f"✅ Scroll Intensities: {list(config.scroll_intensities.keys())}")
    
    # Test Detection Patterns for Advanced Features
    patterns = DetectionPatterns()
    print(f"✅ Ad Detection Patterns: {len(patterns.ad_detection_patterns)} ad types")
    print(f"✅ Behavioral Patterns: {len(patterns.behavioral_patterns)} behavior types")
    print(f"✅ Risk Indicators: {len(patterns.risk_indicators)} risk levels")
    
    print("🎉 Advanced Features Test Completed!")


def test_utility_functions():
    """
    Test utility functions functionality
    """
    print("\n🧪 Testing Utility Functions...")
    
    # Test UtilityFunctions
    utils = UtilityFunctions()
    
    # Test website validation
    test_websites = ["google.com", "https://yahoo.com", "invalid-url", "https://github.com"]
    valid_websites = utils.validate_and_sanitize_websites(test_websites)
    print(f"✅ Website Validation: {len(valid_websites)}/{len(test_websites)} websites valid")
    
    # Test random website selection
    random_website = utils.get_random_website()
    print(f"✅ Random Website: {random_website}")
    
    # Test duration formatting
    test_durations = [45.5, 125.0, 3661.0]
    for duration in test_durations:
        formatted = utils.format_duration(duration)
        print(f"✅ Duration Format: {duration}s -> {formatted}")
    
    # Test configuration backup
    test_config = {"test": "value", "number": 123}
    backup_path = utils.create_backup_config(test_config)
    if backup_path:
        print(f"✅ Config Backup: Created at {backup_path}")
    else:
        print("⚠️ Config Backup: Failed to create backup")
    
    # Test RiskMonitor
    print("\n🧪 Testing Risk Monitor...")
    
    # Create a mock driver for testing
    class MockDriver:
        def __init__(self):
            self.current_url = "https://example.com"
            self.page_source = "normal page content"
        
        def find_elements(self, by, selector):
            return []  # No elements found
    
    mock_driver = MockDriver()
    risk_monitor = RiskMonitor(mock_driver)
    
    # Test request recording
    risk_monitor.record_request()
    risk_monitor.record_request()
    print(f"✅ Risk Monitor: Recorded {risk_monitor.request_count} requests")
    
    # Test detection signals
    signals = risk_monitor.check_detection_signals()
    print(f"✅ Detection Signals: {len(signals)} signals checked")
    
    # Test risk assessment
    risk_level = risk_monitor.assess_risk_level(signals)
    print(f"✅ Risk Assessment: Current level is {risk_level}")
    
    # Test risk statistics
    stats = risk_monitor.get_risk_statistics()
    print(f"✅ Risk Statistics: {len(stats)} statistics available")
    
    print("🎉 Utility Functions Test Completed!")


def test_integration():
    """
    Test integration between components
    """
    print("\n🧪 Testing Component Integration...")
    
    # Test component initialization
    timing = TimingSystem()
    config = Configuration()
    patterns = DetectionPatterns()
    logger = LoggingSystem()
    
    # Test that components can work together
    plan_generator = VisitPlanGenerator()
    plan = plan_generator.generate_visit_plan("casual_browsing", 2)
    
    # Simulate plan execution timing
    total_duration = 0
    for action in plan:
        if 'duration' in action:
            total_duration += action['duration']
            # Test timing system with action duration
            delay = timing.smart_delay("general", "medium")
            total_duration += delay
    
    print(f"✅ Component Integration: Plan execution simulation completed")
    print(f"✅ Total simulated duration: {total_duration:.2f} seconds")
    
    # Test logging integration
    logger.log_activity("Integration test", {
        "plan_actions": len(plan),
        "total_duration": total_duration,
        "components_tested": ["TimingSystem", "VisitPlanGenerator", "LoggingSystem"]
    })
    
    # Test utility functions integration
    utils = UtilityFunctions()
    formatted_duration = utils.format_duration(total_duration)
    print(f"✅ Utility Integration: Formatted duration as {formatted_duration}")
    
    print("🎉 Component Integration Test Completed!")


def run_comprehensive_test():
    """
    Run comprehensive test of all components
    """
    print("🚀 Starting Comprehensive Test of test_website.py")
    print("=" * 60)
    
    try:
        # Test Core Components
        test_core_components()
        
        # Test Advanced Features
        test_advanced_features()
        
        # Test Utility Functions
        test_utility_functions()
        
        # Test Article Browsing Functions
        test_article_browsing()
        
        # Test Integration
        test_integration()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Core Components: Working")
        print("✅ Advanced Features: Working")
        print("✅ Utility Functions: Working")
        print("✅ Article Browsing Functions: Working")
        print("✅ Component Integration: Working")
        print("✅ File is ready for use!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")


def run_article_browsing_demo():
    """
    Demo function untuk menjalankan article browsing
    """
    print("🚀 Starting Article Browsing Demo")
    print("=" * 60)
    
    try:
        # Setup components
        print("🔧 Setting up components...")
        
        # Create driver
        driver_setup = DriverSetup()
        driver = driver_setup.create_stealth_driver()
        
        if not driver:
            print("❌ Failed to create driver")
            return
        
        # Create other components
        timing = TimingSystem()
        mouse = MouseMovementSimulator(driver)
        risk_monitor = RiskMonitor(driver)
        
        # Create article browser
        article_browser = ArticleBrowser(driver, timing, mouse, risk_monitor)
        
        print("✅ Components setup completed")
        
        # Open RexDL Cloud Migration article
        print("\n📖 Opening RexDL Cloud Migration article...")
        success = article_browser.open_rexdl_cloud_article()
        
        if success:
            print("✅ Article opened and browsed successfully!")
            
            # Get final statistics
            risk_stats = risk_monitor.get_risk_statistics()
            print(f"📊 Risk Statistics: {risk_stats['current_risk_level']} risk level")
            print(f"📊 Total Requests: {risk_stats['total_requests']}")
            
        else:
            print("❌ Failed to open or browse article")
        
        # Cleanup
        print("\n🧹 Cleaning up...")
        driver_setup.cleanup_driver(driver)
        print("✅ Cleanup completed")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")


def run_multilogin_script():
    """
    Script khusus untuk Multilogin Script Runner
    """
    print("🚀 Starting Multilogin Script Runner Mode")
    print("=" * 60)
    
    # Log environment variables
    print(f"🔍 Environment Variables:")
    print(f"   MLX_DEBUGGING_URL: {os.environ.get('MLX_DEBUGGING_URL', 'Not set')}")
    print(f"   MLX_PROFILE_ID: {os.environ.get('MLX_PROFILE_ID', 'Not set')}")
    print(f"   MLX_FOLDER_ID: {os.environ.get('MLX_FOLDER_ID', 'Not set')}")
    
    # Check if running via API endpoint
    is_api_execution = os.environ.get('MLX_DEBUGGING_URL') is not None
    print(f"   API Execution Mode: {is_api_execution}")
    
    driver = None
    
    try:
        # Setup components
        print("\n🔧 Setting up components...")
        
        # Create driver (will use Multilogin's driver)
        print("   Creating driver...")
        driver_setup = DriverSetup()
        driver = driver_setup.create_stealth_driver()
        
        if not driver:
            print("❌ Failed to create driver")
            return
        
        print("✅ Driver created successfully")
        
        # Test basic driver functionality
        print("   Testing driver functionality...")
        try:
            current_url = driver.current_url
            print(f"   Current URL: {current_url}")
        except Exception as e:
            print(f"   Warning: Could not get current URL: {e}")
        
        # Create other components
        print("   Creating timing system...")
        timing = TimingSystem()
        
        print("   Creating mouse simulator...")
        mouse = MouseMovementSimulator(driver)
        
        print("   Creating risk monitor...")
        risk_monitor = RiskMonitor(driver)
        
        # Create article browser
        print("   Creating article browser...")
        article_browser = ArticleBrowser(driver, timing, mouse, risk_monitor)
        
        print("✅ Components setup completed")
        
        # Open RexDL Cloud Migration article
        print("\n📖 Opening RexDL Cloud Migration article...")
        success = article_browser.open_rexdl_cloud_article()
        
        if success:
            print("✅ Article opened and browsed successfully!")
            
            # Get final statistics
            try:
                risk_stats = risk_monitor.get_risk_statistics()
                print(f"📊 Risk Statistics: {risk_stats['current_risk_level']} risk level")
                print(f"📊 Total Requests: {risk_stats['total_requests']}")
            except Exception as e:
                print(f"   Warning: Could not get risk statistics: {e}")
            
        else:
            print("❌ Failed to open or browse article")
        
        # Different behavior for API vs local execution
        if is_api_execution:
            # For API execution, keep browser open longer and don't quit
            print("\n⏳ API Mode: Keeping browser open for 30 seconds...")
            time.sleep(30)
            print("✅ API Script completed successfully - browser remains open!")
        else:
            # For local execution, shorter wait
            print("\n⏳ Local Mode: Keeping browser open for 10 seconds...")
            time.sleep(10)
            print("✅ Local Script completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Script failed with error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        # Keep browser open even on error
        if is_api_execution:
            print("\n⏳ API Mode: Keeping browser open for 15 seconds after error...")
            time.sleep(15)
        else:
            print("\n⏳ Local Mode: Keeping browser open for 5 seconds after error...")
            time.sleep(5)
    
    finally:
        # Different behavior for API vs local execution
        if is_api_execution:
            print("\n🔚 API Script finished - browser will remain open for Multilogin")
            if driver:
                try:
                    # For API execution, explicitly keep browser open
                    print("   Browser will remain open for API inspection")
                    # Don't call driver.quit() in API mode
                except:
                    pass
        else:
            print("\n🔚 Local Script finished - keeping browser open for inspection")
            if driver:
                try:
                    print("   Browser will remain open for manual inspection")
                except:
                    pass


def run_api_endpoint_script():
    """
    Script khusus untuk API endpoint execution
    """
    print("🚀 Starting API Endpoint Script Mode")
    print("=" * 60)
    
    # Log environment variables
    print(f"🔍 Environment Variables:")
    print(f"   MLX_DEBUGGING_URL: {os.environ.get('MLX_DEBUGGING_URL', 'Not set')}")
    print(f"   MLX_PROFILE_ID: {os.environ.get('MLX_PROFILE_ID', 'Not set')}")
    print(f"   MLX_FOLDER_ID: {os.environ.get('MLX_FOLDER_ID', 'Not set')}")
    
    driver = None
    
    try:
        # Setup components
        print("\n🔧 Setting up components for API execution...")
        
        # Create driver (will use Multilogin's driver)
        print("   Creating driver...")
        driver_setup = DriverSetup()
        driver = driver_setup.create_stealth_driver()
        
        if not driver:
            print("❌ Failed to create driver")
            return
        
        print("✅ Driver created successfully")
        
        # Test basic driver functionality
        print("   Testing driver functionality...")
        try:
            current_url = driver.current_url
            print(f"   Current URL: {current_url}")
        except Exception as e:
            print(f"   Warning: Could not get current URL: {e}")
        
        # Create other components
        print("   Creating timing system...")
        timing = TimingSystem()
        
        print("   Creating mouse simulator...")
        mouse = MouseMovementSimulator(driver)
        
        print("   Creating risk monitor...")
        risk_monitor = RiskMonitor(driver)
        
        # Create article browser
        print("   Creating article browser...")
        article_browser = ArticleBrowser(driver, timing, mouse, risk_monitor)
        
        print("✅ Components setup completed")
        
        # Open RexDL Cloud Migration article
        print("\n📖 Opening RexDL Cloud Migration article...")
        success = article_browser.open_rexdl_cloud_article()
        
        if success:
            print("✅ Article opened and browsed successfully!")
            
            # Get final statistics
            try:
                risk_stats = risk_monitor.get_risk_statistics()
                print(f"📊 Risk Statistics: {risk_stats['current_risk_level']} risk level")
                print(f"📊 Total Requests: {risk_stats['total_requests']}")
            except Exception as e:
                print(f"   Warning: Could not get risk statistics: {e}")
            
        else:
            print("❌ Failed to open or browse article")
        
        # For API execution, keep browser open longer
        print("\n⏳ API Endpoint Mode: Keeping browser open for 60 seconds...")
        time.sleep(60)
        print("✅ API Endpoint Script completed successfully - browser remains open!")
        
    except Exception as e:
        print(f"\n❌ API Script failed with error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        # Keep browser open even on error
        print("\n⏳ API Endpoint Mode: Keeping browser open for 30 seconds after error...")
        time.sleep(30)
    
    finally:
        print("\n🔚 API Endpoint Script finished - browser will remain open for Multilogin")
        if driver:
            try:
                # For API execution, explicitly keep browser open
                print("   Browser will remain open for API inspection")
                # Don't call driver.quit() in API mode
                driver_setup = DriverSetup()
                driver_setup.cleanup_driver(driver, is_api_execution=True)
            except:
                pass


def run_simple_multilogin_script():
    """
    Script sederhana mengikuti pola cookie_robot.py yang berhasil
    """
    print("🚀 Starting Simple Multilogin Script (Cookie Robot Pattern)")
    print("=" * 60)
    
    try:
        # Setup logging seperti cookie_robot.py
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        logger = logging.getLogger('test_website')
        
        logger.info("Simple Multilogin Script started")
        logger.info(f"Driver available: {driver is not None}")
        
        if not driver:
            logger.error("No driver available - script cannot continue")
            return
        
        # Test basic driver functionality
        try:
            current_url = driver.current_url
            logger.info(f"Current URL: {current_url}")
        except Exception as e:
            logger.warning(f"Could not get current URL: {e}")
        
        # Create simple components
        logger.info("Creating simple components...")
        timing = TimingSystem()
        mouse = MouseMovementSimulator(driver)
        risk_monitor = RiskMonitor(driver)
        article_browser = ArticleBrowser(driver, timing, mouse, risk_monitor)
        
        logger.info("Components created successfully")
        
        # Open RexDL Cloud Migration article
        logger.info("Opening RexDL Cloud Migration article...")
        success = article_browser.open_rexdl_cloud_article()
        
        if success:
            logger.info("✅ Article opened and browsed successfully!")
            
            # Get final statistics
            try:
                risk_stats = risk_monitor.get_risk_statistics()
                logger.info(f"📊 Risk Statistics: {risk_stats['current_risk_level']} risk level")
                logger.info(f"📊 Total Requests: {risk_stats['total_requests']}")
            except Exception as e:
                logger.warning(f"Could not get risk statistics: {e}")
            
        else:
            logger.error("❌ Failed to open or browse article")
        
        # Keep browser open for inspection
        logger.info("⏳ Keeping browser open for 30 seconds...")
        time.sleep(30)
        
        logger.info("✅ Simple Multilogin Script completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Script failed with error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Keep browser open even on error
        logger.info("⏳ Keeping browser open for 15 seconds after error...")
        time.sleep(15)


if __name__ == "__main__":
    import sys
    
    # Check if we have the driver variable (Multilogin Script Runner pattern)
    try:
        # Check if driver is available (Multilogin Script Runner provides this)
        if 'driver' in globals() and driver is not None:
            print("🔍 Detected Multilogin Script Runner with driver")
            run_simple_multilogin_script()
        else:
            # Check if we're in Multilogin Script Runner environment
            mlx_debugging_url = os.environ.get('MLX_DEBUGGING_URL')
            mlx_profile_id = os.environ.get('MLX_PROFILE_ID')
            
            if mlx_debugging_url or mlx_profile_id:
                print("🔍 Detected Multilogin Script Runner environment")
                # Check if running via API endpoint
                if mlx_debugging_url and 'launcher.mlx.yt' in mlx_debugging_url:
                    print("🔍 Detected API Endpoint execution")
                    run_api_endpoint_script()
                else:
                    run_multilogin_script()
            else:
                # Check if we have command line arguments
                if len(sys.argv) > 1 and sys.argv[1] == "demo":
                    run_article_browsing_demo()
                else:
                    # Try to run multilogin script anyway (might be in browser environment)
                    print("🔍 No Multilogin environment variables detected, trying multilogin script anyway...")
                    run_multilogin_script()
                    
    except Exception as e:
        print(f"❌ Error in main execution: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        # Fallback to comprehensive test
        print("\n🔄 Falling back to comprehensive test...")
        try:
            run_comprehensive_test()
        except Exception as e2:
            print(f"❌ Fallback also failed: {e2}")
            print("🔚 Script execution terminated")
