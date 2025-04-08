# Job Scraping Project

This project is a Python-based web scraping tool that collects job listings data from the [Wuzzuf](https://wuzzuf.net) website. The scraper extracts essential job-related information such as job title, company name, location, required skills, salary, job responsibilities, and the posting date. The data is stored in a CSV file for further analysis.

## Features

- **Job Title**: Extracts the title of the job listing.
- **Company Name**: Extracts the name of the company hiring for the position.
- **Location**: Extracts the job location.
- **Skills**: Extracts the required skills for the job.
- **Salary**: Scrapes the salary information for the job (if available).
- **Requirements**: Extracts the job responsibilities and requirements (if available).
- **Date Posted**: Extracts the date the job was posted.

## Technologies Used

- **Python**: Programming language used for scripting.
- **BeautifulSoup**: Library used for parsing HTML and extracting data from the job listings page.
- **Selenium**: WebDriver used to handle dynamic content and JavaScript-driven elements (e.g., salary and job requirements).
- **Requests**: Used to make HTTP requests to retrieve web pages.
- **CSV**: Used to export scraped data into a CSV file for easy viewing and analysis.
- **WebDriver Manager**: Used to automatically handle and manage the appropriate ChromeDriver.

## Setup Instructions

### Requirements
1. Python 3.6 or higher
2. The following Python libraries:
   - `requests`
   - `beautifulsoup4`
   - `selenium`
   - `webdriver-manager`
   - `lxml`
   - `csv`
   
   You can install these libraries using `pip`:
   
   ```bash
   pip install requests beautifulsoup4 selenium webdriver-manager lxml
