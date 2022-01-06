from selenium import webdriver
from bs4 import BeautifulSoup
import time

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

#open linkedin
driver.get("https://linkedin.com/uas/login")
  

time.sleep(5)
  

username = driver.find_element_by_id("username")
#enter your linkedin emailid in place of email
username.send_keys("devarsh1devarsh@gmail.com")  
  
pword = driver.find_element_by_id("password")
#enter your linkedin password in place of pass
pword.send_keys("pass")        

driver.find_element_by_xpath("//button[@type='submit']").click()

#now it will open all the categories one by one in form of for loop
for i in career_titles:
    print('\n'+i+'\n')
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
        
    #if no jobs are there for particular category
    if not job_titles:
        print("NO JOBS AVAILABLE")
    else:
        #printing the job details together of a particular category of job
        for j,k,l in zip(job_titles,company_names,location_list):
            print("Title:"+j+";"+"Company:"+k+";"+"Location:"+l)

    #program to get information of companies offering job
    print("\n\nCompanies")       
    for i in company_names:
        print("\n"+i)
        driver.get("https://www.linkedin.com/company/"+i)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        info_html = soup.find_all('div', {'class': 'org-top-card-summary-info-list__info-item'})
        info_data = []
        for data in info_html:
            info_data.append(data.text.strip())
        if not info_data:
            print("Company Data not available")
        else:
            print(info_data)







