import logging
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_cookies(driver, path):
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver.add_cookie(cookie)
    logger.info(f"Cookies loaded: {cookies}")

def main():
    # Path to your WebDriver, assuming it's in the current directory
    service = Service('./chromedriver-linux64/chromedriver')
    driver = webdriver.Chrome(service=service)

    try:
        # Open WhatsApp Web
        driver.get('https://web.whatsapp.com')

        # Load cookies from a file
        load_cookies(driver, 'whatsapp_cookies.pkl')

        # Refresh the page to apply cookies
        driver.refresh()

        # Wait for the page to load and check if we are logged in
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-tab="3"]'))
            )
            logger.info("Logged in successfully using cookies!")
        except:
            logger.error("Failed to log in using cookies. Please check if the cookies are correct.")
            return

        # Prompt the user for recipient's name and message
        recipient_name = input("Enter the recipient's name: ")
        message = input("Enter the message: ")

        # Wait for the search box to be present
        logger.info("Waiting for the search box to be present...")
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.send_keys(recipient_name)
        search_box.send_keys(Keys.ENTER)

        # Wait for the chat to load
        logger.info("Waiting for the chat to load...")
        chat_loaded = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{recipient_name}"]'))
        )
        chat_loaded.click()

        # Wait for the message box to be present
        logger.info("Waiting for the message box to be present...")
        message_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]'))
        )
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        logger.info("Message sent successfully!")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

    finally:
        # Close the browser when done
        driver.quit()

if __name__ == "__main__":
    main()
