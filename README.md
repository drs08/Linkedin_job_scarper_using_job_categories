# Linkedin_job_scarper_using_job_categories

**Requirements**

for windows open cmd and type the following

```
pip install selenium
```
```
pip install bs4
```
```
pip install mysql-connector-python
```
```
pip install requests
```
```
pip install PyMySQL
```
**Installing MYSQL Workbench**

Install your MYSQL Workbench from [here](https://dev.mysql.com/downloads/workbench/) and then connect the workbench.

**Installing chrome driver**

Install your chromedriver from [Chromedriver](https://chromedriver.chromium.org/downloads)

To check the version of your chrome [refer](https://www.businessinsider.com/guides/tech/what-version-of-google-chrome-do-i-have?IR=T)

**Working of the code**

The chromedriver will first open [career Guide](https://www.careerguide.com/career-options) and get all the career categories then it will open the [Linkedin](https://linkedin.com/uas/login) login page and will login through the account details you provide in the code. Then based on all the categories of job extraced from careerguide it will search on linkedin and will print the information off all jobs for the particular jobs avialable. Then it will search for details of each and every companies offering job and will print the details.

