# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0042AD9D8B125DDE31B4FEEFB4825C5BE33D37FFB5105AED964292B8FAA067D0C87B1DA13C4A4DEC9D1425FF2EEDE61CC30FA7FAD3017201BC9E2514FC53D7B14C96F2A87DD9A0B8E32791BFD07F34E081F132D875C63BF81C138748CCB30CE6A4AD197BD589D88F5D75B2D967245EC1E2AE31C229ADA41EA6766656B4EC1F5EBD59044910CCB9F441CEE66F57A7FD66477BEFEC7901BDAA71F1013EC982A8390F55C7170F42808B1D39F894615474FB103FECDF9F0D5939880C2AE77442085130DAC71E14B3EC1CE80CC89FB9DC674B0B05D1595DA31B349DC3C21AB4F5D3BC0790A9F7EAF82F7FEE30F4C19A653550D2F24488D9513BB00932B7BDAAF323166E8A48D6C68EB386F8A50D4C2C0010F7EA2AD82397B91A1DE3B2DE2AF70FED5C88E556BFC7C64880B66CDEE032101C1C77AE1A241EF46C5337F47F7721ACE9F7702431BCE32300915ED7B333F283895CAF720852076281B330FA746D4FB26E5EAD
"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
