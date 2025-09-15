#!/usr/bin/env python3
"""
Simple Debug Script
==================
Very simple script to test if browser stays open
"""

import os
import time
import sys
from datetime import datetime

print("=== Simple Debug Script Started ===")
print(f"Current time: {datetime.now()}")
print(f"Python version: {sys.version}")

# Get environment variables
debugging_url = os.environ.get('MLX_DEBUGGING_URL')
profile_id = os.environ.get('MLX_PROFILE_ID')
folder_id = os.environ.get('MLX_FOLDER_ID')

print(f"Debugging URL: {debugging_url}")
print(f"Profile ID: {profile_id}")
print(f"Folder ID: {folder_id}")

try:
    print("Importing selenium...")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    print("Selenium imported successfully")
    
    print("Setting up WebDriver...")
    
    if debugging_url:
        # Connect to Multilogin debugging URL
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Remote(
            command_executor=debugging_url,
            options=chrome_options
        )
        
        print(f"Connected to Multilogin debugging URL: {debugging_url}")
        
    else:
        # Create local Chrome driver for testing
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        print("Created local Chrome driver for testing")
    
    print("WebDriver setup completed")
    
    # Test basic functionality
    print("Testing basic functionality...")
    
    # Navigate to a simple website
    test_url = "https://www.google.com"
    print(f"Navigating to: {test_url}")
    
    driver.get(test_url)
    print("Navigation completed")
    
    time.sleep(3)
    print("Waited 3 seconds")
    
    # Get page title
    title = driver.title
    print(f"Page title: {title}")
    
    # Wait more
    print("Waiting 10 seconds...")
    time.sleep(10)
    
    print("Basic functionality test completed successfully!")
    
except Exception as e:
    print(f"ERROR in simple debug script: {e}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")
    raise

finally:
    # Cleanup
    try:
        if 'driver' in locals():
            print("Closing WebDriver...")
            driver.quit()
            print("WebDriver closed successfully")
    except Exception as e:
        print(f"Error closing WebDriver: {e}")
    
    print("=== Simple Debug Script Finished ===")
