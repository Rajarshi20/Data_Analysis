from initialSetup import setup
from loadData import load
from job_data_insights import insights
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def main():

    chromedriver_path = 'D:/chromedriver-win64/chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    base_url = "https://www.linkedin.com/login"
    load_username, load_password, getjob = setup.load_env_file()
    setup.load_base_url(driver, base_url)
    setup.login(driver, load_username, load_password)
    load.get_jobs_listings(driver, getjob)
    load.load_job_data(driver)
    #print("Closing driver..")
    #driver.close()
    df = insights.job_data_preprocess()
    insights.job_data_analysis(df)
    insights.skill_text_analysis(driver, df)
    
    input("Press Enter to exit...")
    

if __name__ == "__main__":
    main()