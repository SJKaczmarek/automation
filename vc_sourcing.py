# coding: utf-8
#--------------------------------------------------------------------------------------#
# To Download python from here : https://www.python.org/downloads/
# Go into terminal as admin and run this command : easy_install pip
# Then run following commands to install dependencies
# pip install beautifulsoup4
# pip install selenium
# Download chrome driver from here https://sites.google.com/a/chromium.org/chromedriver/downloads
# Put driver executable path in $PATH environment variable
# To run this file : python vc_sourcing.py
#--------------------------------------------------------------------------------------#

import selenium
import re
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import sys
# Here you can select all the filters. And provide the same name which is shown on web page.
##------------------------------- SELECT OPTIONS ----------------------------------------##
industries = 'Artificial Intelligence'              # Default All
regions = 'USA'                 # Default All
specific_company = ''           # Default ''
investor_type = 'All'           # Default All
investor_status = 'Active'      # Default All
investor_stage = 'Seed'         # Default All
date_from = ''                  # Default ''
date_to = ''                    # Default ''
firstname = ''                  # Default ''
lastname = ''                   # Default ''
city = ''                       # Default ''
state = 'California'            # Default All
zipcode = ''                    # Default ''

##------------------------------------- END ---------------------------------------------##
reload(sys)
sys.setdefaultencoding('utf8')
url = ""
# Open investor.csv file to write results
writer = csv.writer(open("investors_california_AI.csv","wb"), delimiter=',',quoting=csv.QUOTE_ALL)
headers = ['VENTURE','DESIGNATION','FIRSTNAME','LASTNAME','EMAIL']
writer.writerow(headers)
# Function which scrapes investor names and emails from page
def scrape(soup):
    # Find the Investor name using its id
    span = soup.find('span',id = 'ctl00_LeftColumnContentPlaceholder_txtInvestoryCompanyName')
    # Get the investor name from span text
    name = str(span.text).encode('utf-8').strip()
    print name
    # Write Investor name in csv file
    writer.writerow([name])
    # Find Div which contains investor details from webpage
    div = soup.find('div',id = 'ctl00_LeftColumnContentPlaceholder_UpdatePanel1')
    # Find the table which has all the investor names and emails
    table = div.find_all('table')[1]
    tds = table.find_all('td')
    details = []
    details.append(' ')
    cnt = 0
    for td in tds[1:]:
        if cnt == 3:
            writer.writerow(details)
            details = []
            details.append(' ')
            cnt = 0
        # Finding Investor positions and their names from appropriate span tags of webpage
        span = td.find('span')
        if span:
            val = str(span.text)
            if ',' in val:
                fname,lname = val.split(',')
                details.append(lname.strip())
                details.append(fname.strip())
            elif 'N/A' in val:
                details.append(' ')
            else:
                details.append(val.strip())
            cnt = cnt + 1
        # Finding email value from img tag of webpage
        img = td.find('img')
        if img:
            if 'onclick' in img.attrs:
                email = img.attrs['onclick']
                email = re.findall("'(.*?)'",email)
                details.append(str(email[0]))
                cnt = cnt + 1

# Initialize chrome driver
driver = webdriver.Chrome()
# Open login page 
driver.get(url)
# Find username and password field from login page
username = driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_tbEmailAddress")
password = driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_tbPassword")
# Fill up those fields by sending these key strokes
username.send_keys("")
password.send_keys("")
# Click on Submit button
driver.find_element_by_name("ctl00$LeftColumnContentPlaceholder$btnLogon").click()

# Find selection tag to select necessary option : 'venture investors'
Select(driver.find_element_by_id('ctl00_LeftColumnContentPlaceholder_drpSearchType')).select_by_value('1')
# Selcting all filters
#-------------------------- Start filters ------------------------------------------#

Select(driver.find_element_by_id('ctl00_LeftColumnContentPlaceholder_theInvestorSearchOptions_lstIndustry')).select_by_visible_text(industries)
Select(driver.find_element_by_id('ctl00_LeftColumnContentPlaceholder_theInvestorSearchOptions_lstRegion')).select_by_visible_text(regions)
Select(driver.find_element_by_id('ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_ddlInvestorType')).select_by_visible_text(investor_type)
Select(driver.find_element_by_id('ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_ddlStatus')).select_by_visible_text(investor_status)
Select(driver.find_element_by_id('ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_ddlStage')).select_by_visible_text(investor_stage)
Select(driver.find_element_by_id('ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_ddlState')).select_by_visible_text(state)
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_theInvestorSearchOptions_txtCompany").send_keys(specific_company)
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_txtDateMin").send_keys(date_from)
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_txtDateMax").send_keys(date_to)
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_txtFirstName").send_keys(firstname)
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_txtLastName").send_keys(lastname)
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_txtCity").send_keys(city)
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_theInvestorAdvancedSearchOptions_txtZipcode").send_keys(zipcode)

#-------------------------- End filters ------------------------------------------#
# Find search button from webpage and click on it
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_btnSubmit").click()
# Wait for results to finish loading
wait = WebDriverWait(driver, 10)
# Get the source code of current web page and parse it into html using BeautifulSoup
soup = BeautifulSoup(driver.page_source,'html.parser')
# Find the pagetable from webpage using table id
table = soup.find('table', id = 'ctl00_SingleColumnContentPlaceholder_grd1')
values = []
# Store all venture Investors result in values list [15 records per each page]
for td in table.find_all('td'):
    a = td.find('a')
    if a:
        # if 'SearchResultInvestorDetail' in a.attrs['href']:
        if 'SearchResult' in a.attrs['href']:
             values.append(a.text)
# Click on the first Investor name
driver.find_element_by_link_text(values[0]).click()
# wait = 2
while True:
    try:
        # Get the source code of current web page and parse it into html using BeautifulSoup
        invest = BeautifulSoup(driver.page_source,'html.parser')
        # Call scrape function
        scrape(invest)
        # Find Next button and click on that to view and scrape the next page
        elem = driver.find_element_by_link_text('NEXT >')
        if elem.is_enabled():
            # click on next button
            elem.click()
            # wait = wait - 1
        else:
            break
    except NoSuchElementException:
        break
driver.quit()
