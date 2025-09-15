#!/usr/bin/env python3
"""
Debug Script with Output
========================
Debug script with better error handling and output to see what's happening
"""

import os
import time
import sys
from datetime import datetime

# Create a log file for debugging
log_file = f"/tmp/debug_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log_message(message):
    """Log message to file and print"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    try:
        with open(log_file, 'a') as f:
            f.write(log_entry + '\n')
    except:
        pass

log_message("=== Debug Script Started ===")
log_message(f"Current time: {datetime.now()}")
log_message(f"Python version: {sys.version}")
log_message(f"Log file: {log_file}")

# Get environment variables
debugging_url = os.environ.get('MLX_DEBUGGING_URL')
profile_id = os.environ.get('MLX_PROFILE_ID')
folder_id = os.environ.get('MLX_FOLDER_ID')

log_message(f"Debugging URL: {debugging_url}")
log_message(f"Profile ID: {profile_id}")
log_message(f"Folder ID: {folder_id}")

try:
    log_message("Importing selenium...")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    log_message("Selenium imported successfully")
    
    log_message("Setting up WebDriver...")
    
    if debugging_url:
        # Connect to Multilogin debugging URL
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        log_message(f"Connecting to: {debugging_url}")
        driver = webdriver.Remote(
            command_executor=debugging_url,
            options=chrome_options
        )
        
        log_message(f"Connected to Multilogin debugging URL: {debugging_url}")
        
    else:
        # Create local Chrome driver for testing
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        log_message("Created local Chrome driver for testing")
    
    log_message("WebDriver setup completed")
    
    # Test basic functionality
    log_message("Testing basic functionality...")
    
    # Navigate to a simple website
    test_url = "https://www.google.com"
    log_message(f"Navigating to: {test_url}")
    
    driver.get(test_url)
    log_message("Navigation completed")
    
    time.sleep(3)
    log_message("Waited 3 seconds")
    
    # Get page title
    title = driver.title
    log_message(f"Page title: {title}")
    
    # Get current URL
    current_url = driver.current_url
    log_message(f"Current URL: {current_url}")
    
    # Take screenshot
    try:
        screenshot_path = f"/tmp/debug_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        log_message(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        log_message(f"Screenshot failed: {e}")
    
    # Wait more
    log_message("Waiting 10 seconds...")
    time.sleep(10)
    
    log_message("Basic functionality test completed successfully!")
    
    # Keep browser open for manual inspection
    log_message("Keeping browser open for manual inspection...")
    log_message("Press Ctrl+C to stop or wait 60 seconds...")
    
    # Wait for 60 seconds or manual stop
    for i in range(60):
        time.sleep(1)
        if i % 10 == 0:
            log_message(f"Still running... {i}/60 seconds")
    
    log_message("60 seconds completed, closing browser...")
    
except Exception as e:
    log_message(f"ERROR in debug script: {e}")
    import traceback
    traceback_str = traceback.format_exc()
    log_message(f"Traceback: {traceback_str}")
    
    # Even if there's an error, try to keep browser open
    if 'driver' in locals():
        log_message("Error occurred but keeping browser open...")
        try:
            for i in range(30):
                time.sleep(1)
                if i % 5 == 0:
                    log_message(f"Error recovery... {i}/30 seconds")
        except KeyboardInterrupt:
            log_message("Manual stop requested")
        except Exception as cleanup_error:
            log_message(f"Cleanup error: {cleanup_error}")

finally:
    # Cleanup
    try:
        if 'driver' in locals():
            log_message("Closing WebDriver...")
            driver.quit()
            log_message("WebDriver closed successfully")
    except Exception as e:
        log_message(f"Error closing WebDriver: {e}")
    
    log_message("=== Debug Script Finished ===")
    log_message(f"Check log file for details: {log_file}")
