from loadData import load
import pandas as pd
from bs4 import BeautifulSoup
import time
import re
from initialSetup import setup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from deep_translator import GoogleTranslator
from selenium.webdriver.common.by import By

class insights:

    def job_data_preprocess():
        df = pd.read_csv("LinkedIn_Jobs.csv")
        df['Job Title'] = df['Job Title'].str.replace(r'\s*\(.*?[mMwW][^\)]*\)', '', regex=True)
        df['Job Link'] = "https://www.linkedin.com" + df['Job Link'].astype(str)
        #print(df['Location'][1])
        df['City'] = df['Location'].apply(lambda x: x.rsplit(' ', 1)[0] if ' ' in x else x).apply(lambda x:x.rsplit(',',1)[0] if ',' in x else x)
        #print(df['City'][1])
        df['Work_mode'] = df['Location'].apply(lambda x: x.rsplit(' ', 1)[1] if ' ' in x else None)
        df['Work_mode'] = df['Work_mode'].str.replace(r'[^\w\s]','',regex=True)
        #print(df['Work_mode'][1])
        df.drop('Location', axis=1,inplace=True)
        df['Work_mode'] = df['Work_mode'].str.replace('Germany', 'Not specified')
        return df

    def job_data_analysis(df):
        #calculate unique work mode types and the count, group by location
        df_city_workmode_counts = (df.groupby(['City', 'Work_mode'])
                                    .size()
                                    .reset_index(name='Count')
                                    .sort_values(['Count'], ascending=False))
        
        #find out the top 5 cities offering jobs
        top_Cities = df['City'].value_counts().sort_values(ascending=False).reset_index()
        top_Cities.columns = ['Cities','Job Count']

        #find out top 5 companies offering jobs
        top_companies = df['Company'].value_counts().sort_values(ascending=False).reset_index()
        top_companies.columns=['Company','Job Count']

        #find out number of jobs offered for workstudent and interns
        workstudent_jobs = df['Job Title'].where(df['Job Title'].str.contains("Werkstudent|Working Student")).reset_index(name='Workstudent Jobs')
        workstudent_jobs_df = workstudent_jobs['Workstudent Jobs'].dropna()
        count_ws = workstudent_jobs_df.size

        internship_jobs = df['Job Title'].where(df['Job Title'].str.contains("Intern|Internship|Praktikum|Trainee")).reset_index(name='Internship Jobs')
        internship_jobs_df = internship_jobs['Internship Jobs'].dropna()
        count_is = internship_jobs_df.size

        count_ft = df.shape[0]-count_ws-count_is
        data = {'Job Type':["Workstudent", "Internship","Full Time"],'Count':[count_ws,count_is,count_ft]}
        df_job_type_count = pd.DataFrame(data,index=[0,1,2])
        print(df_job_type_count)
        time.sleep(5)

def skill_text_analysis(driver, df):
    #open each job and find out the JD, check for skills required, store them in an array/list and find out top 5 required skills
    job_list_desc = []
    jobs = df['Job Link'].head()
    for job in jobs:
        #print(job)
        #load.visit_with_translation(driver, job)
        driver.get(job)
        time.sleep(8)  # Allow time for loading   
        see_more = driver.find_element(By.XPATH, "//button[contains(@class,'jobs-description')]")
        about_the_job = driver.find_element(By.XPATH, "//h2[text()='About the job']")
        driver.execute_script("arguments[0].scrollIntoView();", about_the_job)
        time.sleep(3)
        see_more.click()
        jobs_desc = extract_skills(driver)
        #translated_text = GoogleTranslator(source='auto', target='en').translate(jobs_desc)
        print(jobs_desc)
        job_list_desc.append(jobs_desc)

def translate_large_text(text, source='auto', target='en', chunk_size=4000):
    print("Translating...")
    translator = GoogleTranslator(source=source, target=target)
    translated_chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        print(chunk)
        translated = translator.translate(chunk)
        translated_chunks.append(translated)

    return " ".join(translated_chunks)

        
def extract_skills(driver):

    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_desc_element = soup.find("div", class_=re.compile('jobs-description__content'))
    job_desc_text = job_desc_element.get_text(separator="\n", strip=True)
    translated_text = translate_large_text(job_desc_text)
    translated_soup = BeautifulSoup(translated_text, 'html.parser')
    requirements = ["requirements", "what.*expect", "what.*bring", "what.*offer",
        "skills", ".*qualification.*", ".*your profile.*", ".*we are looking.*", 
        "Who you are", "Who we need", "we.*look.*for"]
     
    matching_keyword = re.compile("|".join(requirements), re.I)
    get_skills_points = translated_soup.find_all("span", text= matching_keyword)
    if get_skills_points:
        # Find next section or list after the heading
        content_block = get_skills_points.find_next(['ul', 'div', 'section'])

        if content_block:
            # If it's a list, extract list items
            if content_block.name == 'ul':
                return [li.get_text(strip=True) for li in content_block.find_all('li')]

            # If it's a div/section with <li> or <br>, get all list-like elements
            elif content_block.name in ['div', 'section']:
                list_items = content_block.find_all('li')
                if list_items:
                    return [li.get_text(strip=True) for li in list_items]
                else:
                    # fallback: split text by <br> or newline
                    raw_text = content_block.get_text(separator="\n").strip()
                    return [line.strip() for line in raw_text.split("\n") if len(line.strip()) > 3]
    
    return []



def main():

    chromedriver_path = 'D:/chromedriver-win64/chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    base_url = "https://www.linkedin.com/login"
    load_username, load_password, getjob = setup.load_env_file()
    setup.load_base_url(driver, base_url)
    setup.login(driver, load_username, load_password)
    time.sleep(5)
    df= insights.job_data_preprocess()   
    #insights.job_data_analysis(df)
    skill_text_analysis(driver,df)
    input("Press Enter to exit...")
    

if __name__ == "__main__":
    main() 