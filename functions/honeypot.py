import asyncio
import time
import os

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from functions.element_has_css_file import *

#PATH = "C:\chromedriver.exe"
#driver = webdriver.Chrome(PATH)
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
#wait = WebDriverWait(driver, 4)
driver.get('http://www.honeypot.is/')


async def honeypot(token):

    form_fill = driver.find_element(By.ID, "address")
    form_fill.send_keys(token)
    await asyncio.sleep(2)
    form_submit = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/form/div[2]/input")
    await asyncio.sleep(1)
    form_submit.submit()
    await asyncio.sleep(1)
    print(f"checking this token: {token}")

    try:
        print("is site loaded?")
        wait = WebDriverWait(driver, 15)
        succes_fail = wait.until(element_has_css_class((By.XPATH, '//*[@id="shitcoin"]/div/div'), "header"))
    except TimeoutException:
        print("To much time passed while loading")
    print("***"+ succes_fail.text+"***")

    try:
        checkheader = driver.find_element(By.CSS_SELECTOR, "div.header")
        answer = checkheader.text
        print(checkheader)
    except NoSuchElementException:
        print("no such element")

    return(answer)