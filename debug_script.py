#!/usr/bin/env python3
"""
Debug Script for Multilogin
===========================
Simple script to test basic functionality
"""

import os
import time
import logging
import sys
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('debug_script.log')
        ]
    )
    return logging.getLogger(__name__)

def main():
    """Main function"""
    logger = setup_logging()
    
    logger.info("=== Debug Script Started ===")
    logger.info(f"Current time: {datetime.now()}")
    logger.info(f"Python version: {sys.version}")
    
    # Get environment variables
    debugging_url = os.environ.get('MLX_DEBUGGING_URL')
    profile_id = os.environ.get('MLX_PROFILE_ID')
    folder_id = os.environ.get('MLX_FOLDER_ID')
    
    logger.info(f"Debugging URL: {debugging_url}")
    logger.info(f"Profile ID: {profile_id}")
    logger.info(f"Folder ID: {folder_id}")
    
    driver = None
    try:
        logger.info("Setting up WebDriver...")
        
        if debugging_url:
            # Connect to Multilogin debugging URL
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Remote(
                command_executor=debugging_url,
                options=chrome_options
            )
            
            logger.info(f"Connected to Multilogin debugging URL: {debugging_url}")
            
        else:
            # Create local Chrome driver for testing
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("Created local Chrome driver for testing")
        
        if not driver:
            logger.error("Failed to setup WebDriver")
            return
        
        # Test basic functionality
        logger.info("Testing basic functionality...")
        
        # Navigate to a simple website
        test_url = "https://www.google.com"
        logger.info(f"Navigating to: {test_url}")
        
        driver.get(test_url)
        time.sleep(3)
        
        # Get page title
        title = driver.title
        logger.info(f"Page title: {title}")
        
        # Take screenshot
        screenshot_path = f"debug_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        
        # Wait a bit more
        logger.info("Waiting 5 seconds...")
        time.sleep(5)
        
        logger.info("Basic functionality test completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in debug script: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise
    
    finally:
        # Cleanup
        if driver:
            try:
                logger.info("Closing WebDriver...")
                driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Error closing WebDriver: {e}")
        
        logger.info("=== Debug Script Finished ===")

if __name__ == "__main__":
    main()
