from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import time


def setup(driver, base_url):
    """ options = webdriver.ChromeOptions()
    options.page_load_strategy = "none" """
    driver.get(base_url)
    #time.sleep(10)

def main():
    chromedriver_path = 'D:/chromedriver-win64/chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.linkedin.com/login"
    setup(driver, base_url)

if __name__ == "__main__":
    main()