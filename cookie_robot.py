import os
import random
import time
import logging
import requests
import sys
import selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as Ac
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse
from urllib.parse import urljoin


def setup_logging():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s'))
    logging.getLogger(name='cookie_robot').addHandler(console_handler)


def validate_and_sanitize_websites(websites):
    sanitized_websites = []

    for website in websites:
        if not website.startswith(('http://', 'https://')):
            website = f'https://{website}'

        parsed = urlparse(website)

        # If the parsed URL does not contain a netloc (domain), it's invalid
        if not parsed.netloc:
            logging.error(f'Invalid website URL: {website}')
            continue

        # Try HTTPS first
        https_url = f'https://{parsed.netloc}{parsed.path}'
        try:
            response = requests.get(https_url, timeout=5, allow_redirects=True)
            if response.status_code in [200, 301, 302]:
                sanitized_websites.append(https_url)
                logging.info(f"Using HTTPS for {parsed.netloc}")
                continue  # Skip HTTP fallback if HTTPS works
            else:
                logging.warning(f'Unexpected status ({response.status_code}) for {https_url}, trying HTTP fallback.')
        except requests.RequestException:
            logging.warning(f'HTTPS failed for {https_url}. Trying HTTP instead.')

            # Fallback to HTTP if HTTPS fails
            http_url = f'http://{parsed.netloc}{parsed.path}'
            try:
                response = requests.get(http_url, timeout=5, allow_redirects=True)
                if response.status_code in [200, 301, 302]:
                    sanitized_websites.append(http_url)
                    logging.info(f"Using HTTP for {parsed.netloc}")
                    continue  # Use HTTP if successful
                else:
                    logging.error(f'HTTP fallback also returned unexpected status ({response.status_code}) for {http_url}')
            except requests.RequestException:
                logging.error(f'Both HTTPS and HTTP failed for {website}. Defaulting to HTTPS.')

        # Default to HTTPS if both fail
        sanitized_websites.append(https_url)
        logging.info(f'Defaulted to HTTPS for {parsed.netloc}')

    return sanitized_websites


class CookieRobot:

    def __init__(
            self,
            websites,
            driver,
            processCookieConsent=True,
            randomOrder=False,
            fractionMode=1.0,
    ):
        if randomOrder:
            random.shuffle(websites)

            if fractionMode != 1.0:
                part = int(len(websites) * fractionMode)
                websites = websites[:part]

        self.websites = websites
        self.driver = driver
        self.fractionMode = fractionMode
        self.processCookieConsent = processCookieConsent

        logging.info(f'CookieRobot initialized with websites: {self.websites}')
        logging.info(f'Cookies concent processing: {self.processCookieConsent}')

    def allow_cookies(self, site):
        logging.info(f'Accepting cookies for {site}')
        logging.info(f"Site value: {repr(site)}")

        max_retries = 3

        site_cookie_selectors = {
            'twitter': (By.XPATH, "(//button[@role='button' and contains(@class, 'css-175oi2r')])[1]"),
            'youtube': (By.XPATH, "//button[div[span[normalize-space(text())='Accept all']]]"),
            'amazon': (By.XPATH, "//input[@id='sp-cc-accept']"),
            'google': (By.ID, 'L2AGLb'),
            'ebay': (By.ID, 'gdpr-banner-accept'),
            'aliexpress': (By.XPATH, "//button[contains(@class, 'btn-accept')]"),
            'facebook': (By.CSS_SELECTOR,
                         "body > div._10.uiLayer._4-hy._3qw > div._59s7._9l2g > div > div > div > div > "
                         "div:nth-child(3) > div.x1exxf4d.x13fuv20.x178xt8z.x1l90r2v.x1pi30zi.x1swvt13 > div > "
                         "div:nth-child(2) > div.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf."
                         "xcfux6l.x1qhh985.xm0m39n.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu."
                         "x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg."
                         "x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.x9f619.x3nfvp2.xdt5ytf.xl56j7k.x1n2onr6.xh8yej3"),
            'fiverr': (By.XPATH, "//button[@id='onetrust-accept-btn-handler']"),
            'yahoo': (By.XPATH, "//button[@type='submit' and @name='agree' and @value='agree']"),
            'twitch': (By.XPATH, "//button[@data-a-target='consent-banner-accept']"),
            'instagram': (
                By.XPATH,
                "//button[contains(@class, '_a9--') and contains(@class, '_ap36') and contains(@class, '_a9_0')]")
        }

        try:
            if 'wikipedia' in site:
                logging.info("Skipping cookie handling for Wikipedia.")
                return

            for key, locator in site_cookie_selectors.items():
                if key in site:
                    if self._handle_cookie_button(locator, max_retries):
                        logging.info(f"Successfully handled cookies for {key}.")
                        return
                    else:
                        logging.error(f"Failed to click Allow Cookies button for {key} after {max_retries} attempts.")
                        return

            if 'reddit' in site:
                if self.reddit_click_accept_all_button(max_retries):
                    logging.info("Successfully clicked Reddit's 'Accept All' button.")
                    return
                else:
                    logging.error("Failed to click Reddit's 'Accept All' button after retries.")
                    return

            # Fallback to generic function for unknown sites
            if not self.generic_allow_cookies(max_retries):
                logging.warning(f"Failed to allow cookies for {site} after {max_retries} attempts.")
                return

            logging.error(f"Failed to click Allow Cookies button for {site} after {max_retries} attempts.")

        except Exception as e:
            logging.error(f"Error accepting cookies for {site}: {e}", exc_info=True)

    def _handle_cookie_button(self, locator, max_retries):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        retries = 0

        while retries < max_retries:
            try:
                logging.info(f"Checking presence of cookie button: {locator} (Attempt {retries + 1}/{max_retries})")

                if wait.until(EC.presence_of_element_located(locator)):
                    logging.info(f"Cookie button found for locator: {locator}. Proceeding to click.")

                    button = wait.until(EC.element_to_be_clickable(locator))

                    try:
                        # First try to move to the element and click
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                        Ac(driver).move_to_element(button).pause(1).click().perform()
                        time.sleep(2)

                    except selenium.common.exceptions.MoveTargetOutOfBoundsException as e:
                        logging.warning(f"MoveTargetOutOfBoundsException occurred: {e}. Retrying with direct click.")

                        # Retry clicking without moving if move_to_element fails
                        button.click()
                        time.sleep(2)

                    # Check if the button disappeared after clicking
                    if wait.until(EC.invisibility_of_element_located(locator)):
                        logging.info(f"Successfully clicked and dismissed the cookie button for locator: {locator}.")
                        return True
                    else:
                        logging.warning(f"Cookie button did not disappear after clicking: {locator}")

                else:
                    logging.warning(f"Cookie button not found for locator: {locator}.")
                    return False

            except Exception as e:
                retries += 1
                logging.warning(f"Retry {retries}/{max_retries} for locator {locator}: {e}")

                if retries < max_retries:
                    logging.info(f"Refreshing page for retry {retries}/{max_retries}...")
                    driver.refresh()
                    time.sleep(5)

        logging.error(f"Failed to find or click the cookie button after {max_retries} attempts for locator: {locator}.")
        return False

    def generic_allow_cookies(self, max_retries):
        """
        Tries to find and click the 'Allow Cookies' button using different language variations.
        Stops after reaching max_retries.
        """
        translations = [
            "Accept", "allow all cookies", "accept all cookies", "accept cookies",
            "alle akzeptieren", "alle cookies akzeptieren", "cookies akzeptieren",
            "accepter tous les cookies", "accepter les cookies", "tout accepter",
            "aceitar todos os cookies", "aceitar cookies", "permitir todos os cookies",
            "akceptuj wszystkie pliki cookies", "zaakceptuj cookies", "zgoda na cookies",
            "accetta tutti i cookie", "accetta cookie", "consenti tutti i cookie",
            "aceptar todas las cookies", "aceptar cookies", "permitir todas las cookies",
            "accepteren alle cookies", "alle cookies toestaan", "cookies accepteren",
            "accepta toate cookie-urile", "permite toate cookie-urile", "accepta cookie-uri"
        ]

        xpath_conditions = " or ".join([
            f"contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{translation.lower()}')"
            for translation in translations
        ])

        xpath = f"//button[.//span[{xpath_conditions}]] | //div[@role='button' and .//span[{xpath_conditions}]] | //button[{xpath_conditions}]"

        retries = 0

        while retries < max_retries:
            try:
                wait = WebDriverWait(self.driver, 10)
                button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

                try:
                    # First attempt: move to element and click
                    Ac(self.driver).move_to_element(button).click().perform()
                    logging.info(f"Clicked 'Allow Cookies' button on attempt {retries + 1} using move_to_element.")
                except selenium.common.exceptions.MoveTargetOutOfBoundsException as e:
                    logging.warning(f"MoveTargetOutOfBoundsException occurred: {e}. Retrying with direct click.")

                    # Retry with direct click if moving to element fails
                    button.click()
                    logging.info(f"Clicked 'Allow Cookies' button on attempt {retries + 1} using direct click.")

                time.sleep(2)

                # If the button disappears, assume successful acceptance
                if wait.until(EC.invisibility_of_element_located((By.XPATH, xpath))):
                    logging.info("Cookies accepted successfully.")
                    return True  # Stop further retries on success

            except Exception as e:
                retries += 1
                logging.warning(f"Generic cookie acceptance failed on attempt {retries}/{max_retries}: {e}")

                if retries < max_retries:
                    self.driver.refresh()
                    time.sleep(5)

            logging.info(f"Retrying generic cookie acceptance ({retries}/{max_retries})")

        logging.error(f"Failed to accept cookies after {max_retries} attempts.")
        return False  # Exhausted retries, cookies not accepted

    def reddit_click_accept_all_button(self, max_retries=2):
        retries = 0
        while retries < max_retries:
            try:
                # Locate the shadow host with explicit wait
                shadow_host = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "reddit-cookie-banner"))
                )
                logging.info("Found shadow host element: reddit-cookie-banner")

                shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", shadow_host)
                logging.info("Accessed shadow root of reddit-cookie-banner")

                accept_all_button = WebDriverWait(self.driver, 10).until(
                    lambda driver: shadow_root.find_element(By.CSS_SELECTOR, "#accept-all-cookies-button > button")
                )
                logging.info("Found 'Accept All' button inside shadow DOM")

                self.driver.execute_script("arguments[0].scrollIntoView(true);", accept_all_button)
                logging.info("Scrolled 'Accept All' button into view")

                Ac(self.driver).move_to_element(accept_all_button).click().perform()
                logging.info("Successfully clicked Reddit's 'Accept All' button.")
                return True

            except Exception as e:
                retries += 1
                logging.warning(f"Reddit button retry {retries}/{max_retries}: {e}")
                if retries < max_retries:
                    self.driver.refresh()
                    time.sleep(5)

        logging.error("Failed to click Reddit's 'Accept All' button after all retries.")
        return False  # Explicitly returning False on failure

    def automation(self):
        visited_domains = set()
        for website in self.websites:
            domain = urlparse(website).netloc
            logging.info(f'Visiting website: {website}')
            self.driver.get(website)
            logging.info('Site has loaded')
            try:
                self.driver.maximize_window()
                logging.info('Window maximized successfully')
            except Exception as e:
                logging.warning(f'Failed to maximize window: {e}')

            time.sleep(2)

            if self.processCookieConsent:
                if domain not in visited_domains:
                    self.allow_cookies(website)
                    visited_domains.add(domain)
            else:
                logging.info(
                    f'Skipping cookie consent processing for {website} as processCookieConsent is set to False.')

            self.gather_cookies(pages_per_site=3, scroll_range=(1, 5), sleep_range=(5, 10))

    def gather_cookies(self, pages_per_site=3, scroll_range=(1, 5), sleep_range=(5, 15)):
        """
        Args:
            pages_per_site (int): Number of successful page interactions to perform per site.
            scroll_range (tuple): Range of random scroll interactions (min, max).
            sleep_range (tuple): Range of random wait times between interactions (min, max).
        """

        start_time = time.time()
        timeout_seconds = 180  # 3 minutes timeout

        try:
            original_url = self.driver.current_url
            original_tab = self.driver.current_window_handle
            domain = original_url.split('//')[1].split('/')[0]
            logging.info(f"Starting cookie gathering on domain: {domain}")

            successful_interactions = 0
            failed_attempts = 0

            while successful_interactions < pages_per_site:

                if time.time() - start_time > timeout_seconds:
                    logging.warning(f"Timeout reached for {domain}. Moving to next site.")
                    break

                existing_tabs = self.driver.window_handles

                link_elements = self.driver.find_elements(By.TAG_NAME, "a")
                elements_with_domain = []

                for el in link_elements:
                    try:
                        href = el.get_attribute("href")
                        if not href or "javascript:void(0)" in href:
                            continue  # Skip invalid or non-functional links

                        # Check if the element is visible and displayed
                        if not el.is_displayed():
                            continue  # Skip hidden elements

                        # Test if the element is clickable
                        WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(el))

                        # Ensure the link belongs to the same domain
                        if domain in href:
                            elements_with_domain.append(el)
                    except Exception as filter_exception:
                        logging.debug(f"Skipping element during filtering: {filter_exception}")

                if not elements_with_domain:
                    logging.warning("No valid or clickable links found on the page with the same domain!")
                    break

                random_link = random.choice(elements_with_domain)
                link_href = random_link.get_attribute("href")
                logging.info(f"Attempting to click link: {link_href}")

                try:
                    logging.info("Scrolling the element into view.")
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                               random_link)

                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(random_link))

                    try:
                        Ac(self.driver).move_to_element(random_link).click().perform()
                        logging.info(f"Successfully clicked link: {link_href} using move_to_element.")
                    except selenium.common.exceptions.MoveTargetOutOfBoundsException as e:
                        logging.warning(f"MoveTargetOutOfBoundsException occurred: {e}. Retrying with direct click.")
                        random_link.click()
                        logging.info(f"Successfully clicked link: {link_href} using direct click.")

                    time.sleep(random.randint(sleep_range[0], sleep_range[1]))

                    # Detect new tabs
                    new_tabs = [tab for tab in self.driver.window_handles if tab not in existing_tabs]
                    if new_tabs:
                        # Switch to the new tab
                        new_tab = new_tabs[0]
                        logging.info(f"New tab detected: {new_tab}. Switching to it.")
                        self.driver.switch_to.window(new_tab)

                        logging.info(f"Scrolling in the new tab: {link_href}")
                        self.scroll_randomly(random.randint(scroll_range[0], scroll_range[1]))

                        # Close the new tab and return to the original
                        self.driver.close()
                        logging.info(f"Closed new tab: {new_tab}")
                        self.driver.switch_to.window(original_tab)
                        logging.info("Returned to the original tab.")
                    else:
                        logging.info("No new tab opened. Scrolling on the same page.")
                        self.scroll_randomly(random.randint(scroll_range[0], scroll_range[1]))

                    successful_interactions += 1
                    failed_attempts = 0  # Reset failed attempts on success
                    logging.info(f"Successful interactions: {successful_interactions}/{pages_per_site}")

                except Exception as e:
                    failed_attempts += 1
                    logging.warning(f"Failed to interact with link: {link_href}. Exception: {type(e).__name__}",
                                    exc_info=False)

                    # Return to the original page after 3 consecutive failures
                    if failed_attempts >= 3:
                        logging.warning("Three consecutive failures detected. Returning to the original page.")
                        self.driver.get(original_url)
                        time.sleep(random.randint(sleep_range[0], sleep_range[1]))
                        failed_attempts = 0

                    continue

                # Return to the original page if needed
                if self.driver.current_url != original_url:
                    logging.info("Returning to the original page.")
                    self.driver.get(original_url)
                    time.sleep(random.randint(sleep_range[0], sleep_range[1]))

            logging.info(f"Finished cookie gathering with {successful_interactions} successful interactions.")

        except Exception as e:
            if time.time() - start_time > timeout_seconds:
                logging.warning(f"Timeout reached while handling exception for {domain}. Moving to next site.")
            else:
                logging.error(f"Error during cookie gathering: {type(e).__name__}, {str(e)}", exc_info=True)

        finally:
            if time.time() - start_time > timeout_seconds:
                logging.warning(f"Timeout reached for {domain}. Exiting site.")
            logging.info("Finished cookie gathering.")

    def scroll_randomly(self, times):
        for _ in range(times):
            total_height = self.driver.execute_script(
                'return document.body.scrollHeight'
            )
            random_position = random.randint(0, total_height)
            self.driver.execute_script(
                f'window.scrollTo(0, {random_position});')
            time.sleep(random.randint(1, 5))

    def run(self):
        self.automation()


setup_logging()

inputparams = inputparams or {}
randomOrder = False
fractionMode = 1.0
processCookieConsent = True

websites = ["https://fiverr.com", "https://yahoo.com", "https://en.wikipedia.org", "https://aliexpress.com",
            "https://amazon.com", "https://ebay.com", "https://twitch.com", "https://youtube.com", "https://reddit.com",
            "https://google.com", "https://twitter.com"]



if 'websites' in inputparams:
    websites = inputparams['websites']

if 'randomOrder' in inputparams:
    randomOrder = inputparams['randomOrder']

if 'fractionMode' in inputparams:
    fractionMode = inputparams['fractionMode']

if 'processCookieConsent' in inputparams:
    processCookieConsent = inputparams['processCookieConsent']

logging.info('Cookie robot started')
logging.info(f'WEBSITES: {websites}')
logging.info(f'inputparams: {inputparams}')
logging.info(f'selenium version: {selenium.__version__}')
logging.info(f'randomOrder: {randomOrder}')
logging.info(f'fractionMode: {fractionMode}')

sanitized_websites = validate_and_sanitize_websites(websites)

bot = CookieRobot(
    websites=sanitized_websites,
    driver=driver,
    randomOrder=randomOrder,
    fractionMode=fractionMode,
    processCookieConsent=processCookieConsent
)

bot.run()