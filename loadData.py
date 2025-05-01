from initialSetup import setup
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class load:
        
    def get_jobs_listings(driver, getjob):
        job_icon = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//li-icon[@type='job']")))
        job_icon.click()
        #time.sleep(3)
        job_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword')]")))
        job_search.send_keys(getjob)
        job_search.send_keys(Keys.ENTER) 

    def load_job_data(driver):
        time.sleep(5)
        job_list = []
        for page in range (1,2):
            page+=1
            job_list_container = driver.find_elements(By.XPATH, "//li[contains(@class,'scaffold-layout__list-item')]")     
            n=0  
            for i in job_list_container:
                n+=1
                driver.execute_script("arguments[0].scrollIntoView();", job_list_container[n-1])
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            all_jobs = soup.find_all("div", class_=re.compile('display-flex job-card-container'))
            #print(len(all_jobs))
            for job in all_jobs:
                title = job.find("a", class_=re.compile('job-card-list__title--link')).find("strong").get_text(strip=True)
                company = job.find("div", class_=re.compile('artdeco-entity-lockup__subtitle')).find("span").get_text(strip=True)
                location = job.find("div", class_= re.compile('artdeco-entity-lockup__caption')).find("span").get_text(strip=True)
                job_link = job.find("a", class_=re.compile('job-card-list__title--link')).attrs["href"]
                job_list.append([title,company,location,job_link])
            xpath = f"//button[@aria-label='Page {page}']"
            next_page_button = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", next_page_button)  
            time.sleep(3)
        df = pd.DataFrame(job_list, columns=["Job Title", "Company", "Location", "Job Link"])
        df.head()
        df.to_csv("LinkedIn_Jobs.csv", index=False)
    
    def visit_with_translation(driver, url):
        # Open the original URL
        print("Into translation..")
        driver.get(url)
        time.sleep(3)
        print("Translating page to English...")
        translate_url = f"https://translate.google.com/translate?hl=en&sl=de&tl=en&u={url}"
        driver.get(translate_url)
        time.sleep(5)  # Allow time for translation   
        see_more = driver.find_element(By.XPATH, "//button[contains(@class,'jobs-description')]")
        see_more.click()
