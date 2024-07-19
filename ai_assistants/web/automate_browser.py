from pickle import STOP
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import os, sys

def autoWebpage(input_str):
    """
    Automates the process of interacting with a mortgage webpage.

    This function uses Selenium WebDriver to perform the following steps:
    1. Open a Chrome browser and navigate to the specified base URL.
    2. Wait for the page to load and locate an anchor tag.
    3. Find and click the link that contains the partial text 'Mortgage'.
    4. Wait for the mortgage page to load and locate the relevant input fields.
    5. Enter a mortgage amount, loan period, and interest rate into the respective fields.
    6. Scroll to the bottom of the page.

    Args:
        input_str (dict): A dictionary containing the key 'base_url' with the URL of the webpage to be automated.

    Raises:
        Exception: If an error occurs during the automation process, it is caught and printed.

    Note:
        This function requires ChromeDriver and the necessary Selenium dependencies to be installed.
    """
    try:
        base_url = input_str.get('base_url')
        if not base_url:
            raise ValueError("The input dictionary must contain a 'base_url' key with a valid URL.")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.maximize_window()
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        time.sleep(4)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Mortgage')
        link.click()
        time.sleep(6)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        time.sleep(6)
        mortgage_amount = driver.execute_script("""return document.querySelector('os-tab').querySelector('article').querySelector('os-panel').querySelector('os-input[data-quantity-type="principle-loan"]').shadowRoot.querySelector('input')""")
        mortgage_amount.send_keys(350000)
        mortgage_amount.send_keys(Keys.ENTER)
        mortgage_period = driver.execute_script("""return document.querySelector('os-tab').querySelector('article').querySelector('os-panel').querySelector('os-input[data-quantity-type="loan-period"]').shadowRoot.querySelector('input')""")
        mortgage_period.send_keys(360)
        mortgage_period.send_keys(Keys.ENTER)
        mortgage_rate = driver.execute_script("""return document.querySelector('os-tab').querySelector('article').querySelector('os-panel').querySelector('os-input[data-quantity-type="interest-rate"]').shadowRoot.querySelector('input')""")
        mortgage_rate.send_keys(1.6)
        mortgage_rate.send_keys(Keys.ENTER)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(20)
        return f'Website is automated.'
    except Exception as e:
        print(e)
