import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome in headless mode (optional)
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # run without opening a browser window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Fetch job listings page and parse it
def fetch_job_listings(page_num):
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    page_limit = int(soup.find("strong").text)

    if page_num > page_limit // 15:
        print("Pages ended, terminate.")
        return None

    # Extract job-related details
    job_titles = soup.find_all('h2', {"class": "css-m604qf"})
    company_names = soup.find_all('a', {'class': "css-17s97q8"})
    location_names = soup.find_all("span", {"class": "css-5wys0k"})
    job_skills = soup.find_all("div", {"class": "css-y4udm8"})
    posted_old = soup.find_all("div", {"class": "css-do6t5g"})
    posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
    posted = [*posted_new, *posted_old]

    return job_titles, company_names, location_names, job_skills, posted

# Process job data and store it into lists
def process_job_data(job_titles, company_names, location_names, job_skills, posted):
    job_title = []
    company_name = []
    location_name = []
    skills = []
    links = []
    date = []

    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text)
        links.append(job_titles[i].find("a").attrs['href'])
        company_name.append(company_names[i].text)
        location_name.append(location_names[i].text)
        skills.append(job_skills[i].text)
        date.append(posted[i].text)

    return job_title, company_name, location_name, skills, links, date

# Extract salary and requirements using Selenium
def get_salary_and_requirements(driver, link):
    driver.get(link)  # Navigate to the job listing page
    time.sleep(3)

    # Extract salary
    try:
        salary = driver.find_elements(By.CLASS_NAME, "css-4xky9y")
        get_salary = salary[3]
        salary_text = get_salary.text.strip()
    except:
        print("Salary not found")
        salary_text = "N/A"

    # Extract job requirements
    try:
        resp = [li.text for li in driver.find_element(By.CLASS_NAME, "css-1uobp1k").find_elements(By.TAG_NAME, "li")]
        if not resp:
            resp = [p.text for p in driver.find_element(By.CLASS_NAME, "css-1uobp1k").find_elements(By.TAG_NAME, "p")]
    except:
        print("Error in Responsibilities")
        resp = ["N/A"]

    return salary_text, resp

# Write the data to a CSV file
def write_to_csv(job_title, company_name, location_name, skills, links, salaries, requirments, date):
    file_list = [job_title, company_name, location_name, skills, links, salaries, requirments, date]
    exported = zip_longest(*file_list)

    with open("jobs.csv", "w", newline='', encoding='utf-8') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["Job Title", "Company Name", "Location", "Skills", "Links", "Salary", "Requirements", "Date"])
        wr.writerows(exported)

def main():
    page_num = 0
    job_title = []
    company_name = []
    location_name = []
    skills = []
    links = []
    salaries = []
    requirments = []
    date = []

    # Setup the driver for Selenium
    driver = setup_driver()

    while True:
        # Fetch job data
        job_data = fetch_job_listings(page_num)
        if not job_data:
            break

        job_titles, company_names, location_names, job_skills, posted = job_data

        # Process the job data and store in respective lists
        j_title, c_name, loc_name, skill, lks, dte = process_job_data(job_titles, company_names, location_names, job_skills, posted)

        # Append data to main lists
        job_title.extend(j_title)
        company_name.extend(c_name)
        location_name.extend(loc_name)
        skills.extend(skill)
        links.extend(lks)
        date.extend(dte)

        page_num += 1
        print("Page Switched")

    # Fetch additional data for each job link
    for link in links:
        salary, req = get_salary_and_requirements(driver, link)
        salaries.append(salary)
        requirments.append(req)

    # Close the driver once done
    driver.quit()

    # Write the collected data to a CSV file
    write_to_csv(job_title, company_name, location_name, skills, links, salaries, requirments, date)

if __name__ == "__main__":
    main()
