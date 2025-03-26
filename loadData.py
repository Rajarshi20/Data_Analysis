from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

chromedriver_path = 'D:/chromedriver-win64/chromedriver.exe'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

class load:
        
    def get_jobs_listings(getjob):
        job_icon = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//li-icon[@type='job']")))
        job_icon.click()
        #time.sleep(3)
        job_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword')]")))
        job_search.send_keys(getjob)
        job_search.send_keys(Keys.ENTER)    

def main():
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    load = load()
    load.get_jobs_listings(getjob)
    
    input("Press Enter to exit...")
    

if __name__ == "__main__":
    main()