import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

MAX_RETRIES = 3

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver

def safe_adsense_testing():
    retries = 0
    driver = None

    while retries < MAX_RETRIES:
        try:
            if not driver:
                driver = create_driver()

            # Safe navigation
            driver.get("https://www.google.com")
            time.sleep(random.uniform(2, 4))

            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )

            # Type like human
            search_terms = ["personal loans", "mortgage rates", "credit cards"]
            search_term = random.choice(search_terms)

            for char in search_term:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

            search_box.submit()
            time.sleep(random.uniform(3, 5))

            # Scroll
            for _ in range(3):
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(random.uniform(1, 2))

            # Adsense detection
            ads = driver.find_elements(By.CSS_SELECTOR, "[data-ad-client]")
            if ads:
                first_ad = ads[0]
                driver.execute_script("arguments[0].scrollIntoView();", first_ad)
                time.sleep(random.uniform(2, 4))

                if random.random() < 0.1:
                    try:
                        first_ad.click()
                        time.sleep(random.uniform(5, 8))
                        driver.back()
                    except Exception as e:
                        print(f"Ad click failed: {e}")

            # Browsing time
            time.sleep(random.uniform(10, 15))

            # Clean exit
            driver.quit()
            break  # selesai sukses

        except WebDriverException as e:
            print(f"Browser issue detected: {e}, retrying...")
            retries += 1
            try:
                driver.quit()
            except:
                pass
            driver = None
            time.sleep(3 * retries)  # backoff

        except Exception as e:
            print(f"Unexpected error: {e}")
            try:
                driver.quit()
            except:
                pass
            break

if __name__ == "__main__":
    safe_adsense_testing()
