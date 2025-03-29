from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os

class setup:

    def load_env_file():
        load_dotenv("config.env")
        getusername = os.getenv("LINKEDIN_EMAIL")
        getpassword = os.getenv("LINKEDIN_PASSWORD")   
        getjob = os.getenv("JOB") 
        return getusername, getpassword, getjob

    def load_base_url(driver, base_url):
        """ options = webdriver.ChromeOptions()
        options.page_load_strategy = "none" """
        driver.get(base_url)
        driver.maximize_window()
        time.sleep(3)

    def login(driver, load_username, load_password):
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        username.send_keys(load_username)
        password.send_keys(load_password)
        sign_in_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        sign_in_btn.click()



