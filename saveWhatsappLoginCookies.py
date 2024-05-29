import logging
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def save_cookies(driver, path):
    try:
        cookies = driver.get_cookies()
        with open(path, 'wb') as file:
            pickle.dump(cookies, file)
        logger.info(f"Cookies saved: {cookies}")
    except Exception as e:
        logger.error(f"Failed to save cookies: {e}")

def main():
    chromedriver_path = 'C:/Users/Utilisateur/Desktop/Software_testing_environment/WhatsappAuto/chromedriver-win64/chromedriver.exe'
    service = Service(chromedriver_path)
    
    chrome_binary_path = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
    
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary_path
    options.add_argument('--start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        logger.info("Navigating to WhatsApp Web")
        driver.get('https://web.whatsapp.com')
        logger.info("Opened WhatsApp Web")

        logger.info("Please scan the QR code to log in.")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]'))
        )
        logger.info("QR code is displayed.")

        logger.info("Waiting for the main chat page to load.")
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-tab="3"]'))
        )
        logger.info("Logged in successfully, main chat page loaded.")

        input("Press Enter after logging in to save cookies...")

        save_cookies(driver, 'whatsapp_cookies.pkl')

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise

    finally:
        logger.info("Closing the browser")
        driver.quit()

if __name__ == "__main__":
    main()
