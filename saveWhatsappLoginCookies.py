import logging
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_cookies(driver, path):
    cookies = driver.get_cookies()
    with open(path, 'wb') as file:
        pickle.dump(cookies, file)
    logger.info(f"Cookies saved: {cookies}")

def main():
    # Path to your WebDriver, assuming it's in the current directory
    service = Service('./chromedriver-linux64/chromedriver')
    driver = webdriver.Chrome(service=service)

    try:
        # Open WhatsApp Web
        driver.get('https://web.whatsapp.com')

        # Wait for the QR code to be displayed
        logger.info("Please scan the QR code to log in.")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]'))
        )
        logger.info("QR code is displayed.")

        # Wait for the main chat page to load
        logger.info("Waiting for the main chat page to load.")
        main_chat_page = WebDriverWait(driver, 120).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, '//div[@data-tab="3"]')),
                EC.presence_of_element_located((By.XPATH, '//span[@data-testid="menu"]')),
                EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
            )
        )
        logger.info("Logged in successfully, main chat page loaded.")

        input("Press Enter after logging in to save cookies...")

        # Ensure all necessary cookies are loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[@data-testid="menu"]'))
        )

        # Save cookies to a file
        save_cookies(driver, 'whatsapp_cookies.pkl')

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

    finally:
        # Close the browser when done
        driver.quit()

if __name__ == "__main__":
    main()
