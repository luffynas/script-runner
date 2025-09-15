#!/usr/bin/env python3
"""
Safe AdSense Testing Script for Multilogin X
Implements conservative behavior to avoid account restrictions.
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def safe_adsense_testing():
    """
    Safe AdSense testing with conservative behavior.
    """
    try:
        # Conservative Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Safe navigation to Google
        driver.get("https://www.google.com")
        time.sleep(random.uniform(2, 4))  # Random delay
        
        # Safe search behavior
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Type slowly like human
        search_terms = ["personal loans", "mortgage rates", "credit cards"]
        search_term = random.choice(search_terms)
        
        for char in search_term:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        
        time.sleep(random.uniform(1, 2))
        search_box.submit()
        
        # Wait for results
        time.sleep(random.uniform(3, 5))
        
        # Safe scrolling
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(random.uniform(1, 2))
        
        # Conservative AdSense interaction
        ads = driver.find_elements(By.CSS_SELECTOR, "[data-ad-client]")
        
        if ads:
            # Only interact with first ad, conservatively
            first_ad = ads[0]
            
            # Scroll to ad
            driver.execute_script("arguments[0].scrollIntoView();", first_ad)
            time.sleep(random.uniform(2, 4))
            
            # Conservative click probability (low)
            if random.random() < 0.1:  # 10% chance
                try:
                    first_ad.click()
                    time.sleep(random.uniform(5, 8))
                    driver.back()
                    time.sleep(random.uniform(2, 4))
                except:
                    pass  # Safe fail
        
        # Safe browsing time
        time.sleep(random.uniform(10, 15))
        
        # Clean exit
        driver.quit()
        
    except Exception as e:
        print(f"Safe AdSense testing error: {e}")
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    safe_adsense_testing()
