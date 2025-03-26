from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import time
from dotenv import load_dotenv
import os

chromedriver_path = 'D:/chromedriver-win64/chromedriver.exe'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

class setup:

    def load_env_file():
        load_dotenv("config.env")
        getusername = os.getenv("LINKEDIN_EMAIL")
        getpassword = os.getenv("LINKEDIN_PASSWORD")   
        getjob = os.getenv("JOB") 
        return getusername, getpassword, getjob

    def load_base_url(base_url):
        """ options = webdriver.ChromeOptions()
        options.page_load_strategy = "none" """
        driver.get(base_url)
        driver.maximize_window()
        time.sleep(3)

    def login(load_username, load_password):
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        username.send_keys(load_username)
        password.send_keys(load_password)
        sign_in_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        sign_in_btn.click()

    def get_jobs_listings(getjob):
        job_icon = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//li-icon[@type='job']")))
        job_icon.click()
        #time.sleep(3)
        job_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword')]")))
        job_search.send_keys(getjob)
        job_search.send_keys(Keys.ENTER)


def main():
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    setup = setup()
    base_url = "https://www.linkedin.com/login"
    load_username, load_password, getjob = load_env_file()
    setup.load_base_url(base_url)
    setup.login(load_username, load_password)
    setup.get_jobs_listings(getjob)
    
    input("Press Enter to exit...")
    

if __name__ == "__main__":
    main()