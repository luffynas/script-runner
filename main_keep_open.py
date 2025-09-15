#!/usr/bin/env python3
"""
Main Script for Multilogin Script Runner - Keep Browser Open Version
This version ensures the browser stays open for inspection
"""

import os
import sys
import time
import json
import random
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('main_keep_open')

# Global variables for Multilogin integration
inputparams = globals().get('inputparams', {})
driver = globals().get('driver', None)

def load_configuration() -> Dict[str, Any]:
    """Load configuration from various sources"""
    config = {
        'websites': ['https://google.com', 'https://yahoo.com', 'https://reddit.com'],
        'profile_id': 'd1dcd6cf-7d58-48ea-b5c4-c804e2e0cef8',
        'debugging_url': 'http://127.0.0.1:35000/d1dcd6cf-7d58-48ea-b5c4-c804e2e0cef8',
        'duration_minutes': 2,  # Very short duration for testing
        'keep_browser_open': True,  # Always keep browser open
        'wait_time': 120  # Wait 2 minutes before closing
    }
    
    # Override with input parameters
    if inputparams:
        config.update(inputparams)
    
    # Load from multilogin_config.json if exists
    config_file = 'multilogin_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            logger.warning(f"Could not load config file: {e}")
    
    return config

def simple_browse_website(driver, website: str):
    """Simple website browsing function"""
    try:
        logger.info(f"🌐 Visiting website: {website}")
        driver.get(website)
        
        # Wait for page to load
        time.sleep(5)
        
        # Get page title
        try:
            title = driver.title
            logger.info(f"📄 Page loaded: {title}")
        except:
            logger.info("📄 Page loaded (title not available)")
        
        # Simple scroll behavior
        try:
            logger.info("📜 Scrolling down...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(3)
            
            logger.info("📜 Scrolling up...")
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
        except Exception as e:
            logger.warning(f"Scroll failed: {e}")
        
        # Wait a bit more
        wait_time = random.uniform(3, 8)
        logger.info(f"⏳ Waiting {wait_time:.1f}s on page...")
        time.sleep(wait_time)
        
        logger.info(f"✅ Completed visit to {website}")
        
    except Exception as e:
        logger.error(f"❌ Error visiting website {website}: {e}")

def main():
    """Main execution function - keep browser open version"""
    global logger, driver
    
    logger.info("🚀 === Multilogin Script Runner - Keep Open Version ===")
    logger.info(f"⏰ Script started at: {datetime.now()}")
    
    start_time = time.time()
    success = False
    
    try:
        # Load configuration
        config = load_configuration()
        logger.info(f"⚙️ Configuration loaded successfully")
        
        # Check if driver is available
        if not driver:
            logger.error("❌ No driver available! Make sure Multilogin is running and profile is active.")
            logger.info("⏳ Waiting 60 seconds before exit to allow manual inspection...")
            time.sleep(60)
            return
        
        logger.info("✅ Driver is available, starting automation...")
        
        # Get websites to visit
        websites = config.get('websites', ['https://google.com'])
        logger.info(f"🌍 Will visit {len(websites)} websites")
        
        # Visit each website
        for i, website in enumerate(websites):
            try:
                logger.info(f"📊 Processing website {i+1}/{len(websites)}")
                simple_browse_website(driver, website)
                
                # Delay between websites
                if i < len(websites) - 1:  # Don't delay after last website
                    delay = random.uniform(5, 10)
                    logger.info(f"⏳ Waiting {delay:.1f}s before next website...")
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"❌ Error processing website {website}: {e}")
                continue
        
        success = True
        logger.info("🎉 Script execution completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error in main script: {e}")
        import traceback
        logger.error(f"📋 Traceback: {traceback.format_exc()}")
        success = False
        
    finally:
        # Log completion
        duration = time.time() - start_time
        logger.info(f"⏱️ Script execution finished in {duration:.2f} seconds")
        logger.info(f"✅ Success: {success}")
        
        # Always keep browser open for inspection
        if driver:
            wait_time = config.get('wait_time', 120)
            if success:
                logger.info(f"🎉 Script completed successfully! Keeping browser open for {wait_time} seconds for inspection...")
                logger.info("🔍 You can manually interact with the browser now!")
                logger.info("⏰ Browser will close automatically after the wait time.")
            else:
                logger.info(f"❌ Script failed! Keeping browser open for {wait_time} seconds for debugging...")
                logger.info("🔍 Please check the browser and logs for issues.")
            
            # Countdown timer
            for remaining in range(wait_time, 0, -10):
                logger.info(f"⏳ Browser will close in {remaining} seconds...")
                time.sleep(10)
            
            logger.info("🔚 Closing browser now...")
        else:
            logger.info("❌ No driver available, script will exit immediately")

if __name__ == "__main__":
    main()
