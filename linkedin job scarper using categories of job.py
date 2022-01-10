from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pymysql
import mysql.connector
import requests

config = {
  'user': 'root',
  'password': 'devarsh98',
  'host': 'localhost',
  'database': 'atg',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

# create cursor to execute mysql commands
cursor = cnx.cursor()

#create tables
cursor.execute("CREATE TABLE JOB_CATEGORIES (Category VARCHAR(255))")
cursor.execute("CREATE TABLE JOB_SUBCATEGORIES (SubCategory VARCHAR(255))")
cursor.execute("CREATE TABLE STATES (Name VARCHAR(255))")
cursor.execute("CREATE TABLE JOB_DETAILS (Title VARCHAR(255), Company VARCHAR(255), Location VARCHAR(255))")
cursor.execute("CREATE TABLE COMPANY_DETAILS (Description VARCHAR(255), Location VARCHAR(255), Followers VARCHAR(255))")

#give the path of your chromedriver  
driver = webdriver.Chrome(r"C:\Users\devar\Downloads\chromedriver.exe")

#open careerguide to get all the categories of jobs
driver.get("https://www.careerguide.com/career-options")  

src = driver.page_source
soup = BeautifulSoup(src, 'lxml')

career_html = soup.find_all('h2', {'class': 'c-font-bold'})

#save all the job categories  
career_titles = []
  
for title in career_html:
    career_titles.append(title.text.strip())

src = driver.page_source
soup = BeautifulSoup(src, 'lxml')

#save all job subcategories
career_sub = []

for ultag in soup.find_all('ul', {'class': 'c-content-list-1'}):
    for litag in ultag.find_all('li'):
        career_sub.append(litag.text.strip())


# insert data to table like this one
for title in career_titles:
    value = title
    query = "INSERT INTO JOB_CATEGORIES (Category) VALUES (%s)"
    cursor.execute(query,(value,))
    cnx.commit()
for sub in career_sub:
    value = sub
    query = "INSERT INTO JOB_SUBCATEGORIES (SubCategory) VALUES (%s)"
    cursor.execute(query,(value,))
    cnx.commit()

#open linkedin
driver.get("https://linkedin.com/uas/login")
  

time.sleep(5)
  

username = driver.find_element_by_id("username")
#enter your linkedin emailid in place of email
username.send_keys("devarsh1devarsh@gmail.com")  
  
pword = driver.find_element_by_id("password")
#enter your linkedin password in place of pass
pword.send_keys("devarsh98")        

driver.find_element_by_xpath("//button[@type='submit']").click()

#now it will open all the categories one by one in form of for loop
for i in career_titles:
    '''print('\n'+i+'\n')'''
    driver.get("https://www.linkedin.com/jobs/search/?keywords="+i)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    #getting the job title
    jobs_html = soup.find_all('a', {'class': 'job-card-list__title'})
    job_titles = []
    for title in jobs_html:
        job_titles.append(title.text.strip())

    #getting the company name
        company_name_html = soup.find_all(
  'a', {'class': 'job-card-container__company-name'})
        company_names = []
    for name in company_name_html:
        company_names.append(name.text.strip())
    import re   # for removing the extra blank spaces

    #getting the location of job
    location_html = soup.find_all(
    'ul', {'class': 'job-card-container__metadata-wrapper'})
    location_list = []
    for loc in location_html:
        res = re.sub('\n\n +', ' ', loc.text.strip())
        location_list.append(res)

    for title,name,loc in zip(job_titles,company_names,location_list):
        value = title,name,loc
        query = "INSERT INTO JOB_DETAILS (Title,Company,Location) VALUES (%s,%s,%s)"
        cursor.executemany(query,(value,))
        cnx.commit()    


    #program to get information of companies offering job
    k=[]      
    for i in company_names:
        j=i.replace(' ','-')
        k.append(j)
    for i in k:    
        driver.get("https://www.linkedin.com/company/"+i)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        info_html = soup.find_all('div', {'class': 'org-top-card-summary-info-list__info-item'})
        info_data = []
        for data in info_html:
            info_data.append(data.text.strip())
        finfo_data = [info_data[i * 3:(i + 1) * 3] for i in range((len(info_data) + 2) // 3 )]

        for info in finfo_data:
            value = info
            query = "INSERT INTO COMPANY_DETAILS (Description,Location,Followers) VALUES (%s,%s,%s)"
            cursor.executemany(query,(value,))
            cnx.commit()
      


#close the database  
cnx.close()
