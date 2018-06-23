import time
import unicodecsv
import requests
import logging
import random

from selenium import webdriver
from datamodel import Fields
from bs4 import BeautifulSoup
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import NoSuchElementException
from scraperutils import write_csv

# Disable selenium DEBUG level logging
LOGGER.setLevel(logging.WARNING)

# Disable requests and urllib3 DEBUG level logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Create logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_doc_links(page_soup):
    doc_links=[]
    doc = page_soup.find('p',{'id':'ctl00_MainContent_documentLink'}).find('a').get('href')
    doc_link = "http://www.cao-ombudsman.org/cases/" + doc.split("'")[1]
    doc_links.append(doc_link)
    return doc_links
def parse_pdf_links(doc_links):
    for url in doc_links:
        res = requests.get(url)
        if res.status_code != 200:
            logger.info("%s is broken".format(url))
            continue    
        #get doc page data
        try:
            doc_soup = BeautifulSoup(res.text, 'html.parser')
        except: 
            doc_soup = ""
            continue
        try:
            pdf_links = doc_soup.findAll('a')
            pdf_links_list = ['http://www.cao-ombudsman.org/cases/document-links/' + link.get('href') for link in pdf_links[1:]]
            pdf_links_comma_seperated = ", ".join(pdf_links_list)
        except:
            pdf_links_comma_seperated = ""
    return pdf_links_comma_seperated

def get_page_source(url):
    logger.info("Starting chrome driver")
    driver = webdriver.Chrome()
    logger.info("Going to {link}".format(link = url))
    driver.get(url)
    logger.info("Waiting for page to load")
    time.sleep(3)
    logger.info("Clicking the search button")
    button = driver.find_element_by_id('ctl00_MainContent_btnSearch').click()
    time.sleep(2)
    logger.info("Getting the page source")
    s = driver.page_source
    logger.info("Closing the driver")
    driver.close()
    return s

def get_project_links(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    links = soup.find("div", {"id": "results"}).findAll('a')
    project_links = []
    logger.info('Getting the project links')
    for i in links:
        linkspart = 'http://www.cao-ombudsman.org' + i.get('href')
        project_links.append(linkspart)
    logger.info("Found {number_of_projects} links".format(number_of_projects = len(project_links)))
    return project_links

##########################################

def parse_project_info(page_soup, tag_name):
    try:
        project_info = page_soup.findAll(tag_name)
    except: 
        project_info = ""
    
    return project_info

def parse_project_project_id(tag_name, id_name, project_info):
    try:
        project, project_id = project_info[1].find(tag_name,{'id': id_name}).get_text().rsplit(' ', 1)
    except: 
        project, project_id = ""
    
    return project, project_id

def parse_country(tag_name, id_name, project_info):
    try:
        country = project_info[1].find(tag_name,{'id':id_name}).get_text()
    except: 
        country = ""
    
    return country

def parse_environmental_category(tag_name, id_name, project_info):
    try:
        environmental_category = project_info[1].find(tag_name,{'id':id_name}).get_text()
    except:
        environmental_category = ""
    
    return environmental_category
        
def parse_project_type(tag_name, id_name, project_info):
    try:
        project_type = project_info[1].find(tag_name,{'id':id_name}).get_text()
    except:
        project_type = ""
    
    return project_type

def parse_sector(tag_name, id_name, project_info):
    try: 
        sector = project_info[1].find(tag_name,{'id':id_name}).get_text()
    except: 
        sector = ""
    
    return sector

def parse_financial_institution(tag_name, id_name, project_info):
    try:
        financial_institution = project_info[1].find(tag_name,{'id':id_name}).get_text()
    except: 
        financial_institution = ""
    
    return financial_institution

def parse_project_company(tag_name, id_name, project_info):
    try:
        project_company = project_info[1].find(tag_name,{'id':id_name}).get_text()
    except: 
        project_company = ""
    
    return project_company

def parse_project_loan(tag_name, id_name, project_info):
    try: 
        project_loan = project_info[1].find(tag_name,{'id':id_name}).get_text()
    except: 
        project_loan = ""
    
    return project_loan

def parse_date(tag_name, id_name, project_info):
    try:
        date_filed = project_info[0].find(tag_name,{'id':id_name}).get_text()
        year = date_filed[-4:]
    except:
        date_filed = ""
        year = ""
    
    return year, date_filed

def parse_issues(tag_name, id_name, project_info):
    try:
        issues = project_info[0].find(tag_name,{'id':id_name}).get_text()
    except:
        issues = ""
    
    return issues

def parse_case_status(tag_name, id_name, project_info):
    try:
        case_status = project_info[0].find(tag_name,{'id':id_name}).get_text()
    except:
        case_status = ""
    
    return case_status

def parse_project_information(page_soup, url):   

    project_info = parse_project_info(page_soup, 'dl') 
    
    case_id = ''.join([i for i in url if i.isdigit()])
    
    project, project_id = parse_project_project_id('dd', 'ctl00_MainContent_ctrlProjectName', project_info)

    country = parse_country('dd', 'ctl00_MainContent_ctrlProjectCountries', project_info)
    
    environmental_category = parse_environmental_category('dd', 'ctl00_MainContent_ctrlEnvironmentCategory', project_info)
 
    project_type = parse_project_type('dd', 'ctl00_MainContent_ctrlDepartment', project_info)

    sector = parse_sector('dd', 'ctl00_MainContent_ctrlSector', project_info)

    financial_institution = parse_financial_institution('dd', 'ctl00_MainContent_ctrlInstitution', project_info)
        
    project_company = parse_project_company('dd', 'ctl00_MainContent_ctrlCompany', project_info)

    project_loan = parse_project_loan('dd', 'ctl00_MainContent_ctrlCommitment', project_info)

    year, date_filed = parse_date('dd', 'ctl00_MainContent_ctrlDateFilled', project_info)

    issues = parse_issues('dd', 'ctl00_MainContent_ctrlConcerns', project_info)

    case_status = parse_case_status('dd', 'ctl00_MainContent_ctrlCaseStatus', project_info)
    
    return url, case_id, project, project_id, country, environmental_category, project_type, sector, \
            financial_institution, project_company, project_loan, year,date_filed ,issues, case_status
    

def parse_last_completed_stage(tag_name, soup):
    # Completed Stages
    try:
        #completed_stages = soup.findAll("span", {"class":"completed"})
        completed_stages = [i.get_text() for i in soup.findAll(tag_name, {"class": "completed"})]
        last_completed_stage = completed_stages[-1]
    except IndexError:
        closed_stage = [i.get_text() for i in soup.findAll(tag_name, {"class": "closed"})]
        last_completed_stage = closed_stage
    
    return last_completed_stage

def parse_active_stage(tag_name, soup):
    # Active Stage
    try: 
        active_stage = [i.get_text() for i in soup.findAll(tag_name, {"class":"inprocess"})]
        if active_stage == []:
            active_stage = None
        else:
            active_stage = active_stage[0]
    except NoSuchElementException:
        active_stage = None
    
    return active_stage

def get_eligibility_start_date(active_stage):
    # Eligibility Start Date
    if active_stage in ('Eligibility: In Process', 'Eligible: In Process'):
        eligibility_start_date = 'Completed'
    else: 
        eligibility_start_date = None
    
    return eligibility_start_date

def get_eligibility_end_date(last_completed_stage):
    # Eligibility End Date
    if last_completed_stage in ('Eligibility: Completed', 'Eligible: Completed'):
        eligibility_end_date = 'Completed'
    else: 
        eligibility_end_date = None
    
    return eligibility_end_date

def get_dr_start_date(active_stage, last_completed_stage):
    # dr Start Date
    if active_stage in ('Assessment Period: In Process', 'Facilitating Settlement: Active'):
        dr_start_date = 'Completed'
    elif last_completed_stage == 'Assessment Period: Completed':
        dr_start_date = 'Completed'
    else: 
        dr_start_date = None 
    
    return dr_start_date

def get_dr_end_date(last_completed_stage):
    # dr End Date
    if last_completed_stage == 'Facilitating Settlement: Completed':
        dr_end_date = 'Completed'
    else: 
        dr_end_date = None
    
    return dr_end_date

def get_monitoring_start_date(active_stage):
    # Monitoring Start Date
    if active_stage in ('Monitoring/Close Out: In Process', 'Monitoring: In Process'):
        monitoring_start_date = 'Completed'
    else: 
        monitoring_start_date = None  
    
    return monitoring_start_date

def get_monitoring_end_date(last_completed_stage):
    # Monitoring End Date
    if last_completed_stage == 'Monitoring/Close Out: Completed':
        monitoring_end_date = 'Completed'
    else: 
        monitoring_end_date = None
    
    return monitoring_end_date

def get_cr_start_date(active_stage, last_completed_stage):
    # CR Start Date
    if active_stage in ('Under Appraisal: In Process', 'Under Audit: In Process'):
        cr_start_date = 'Completed'
    elif last_completed_stage == 'Under Appraisal: Completed':
        cr_start_date = 'Completed'
    else: 
        cr_start_date = None
    
    return cr_start_date

def get_cr_end_date(last_completed_stage):
    # CR End Date
    if last_completed_stage == 'Under Audit: Compelted':
        cr_end_date = 'Completed'
    else: 
        cr_end_date = None
        
    return cr_end_date

def get_date_closed(last_completed_stage):
    # Date Closed
    if last_completed_stage == 'Monitoring: Completed':
        date_closed = 'Completed'
    else: 
        date_closed = None
    
    return date_closed

def parse_project_tracker(soup):

    last_completed_stage = parse_last_completed_stage("span", soup)
 
    active_stage = parse_active_stage("span", soup)
    
    eligibility_start_date = get_eligibility_start_date(active_stage)

    eligibility_end_date = get_eligibility_end_date(last_completed_stage)

    dr_start_date = get_dr_start_date(active_stage, last_completed_stage)

    dr_end_date = get_dr_end_date(last_completed_stage)

    monitoring_start_date = get_monitoring_start_date(active_stage)

    monitoring_end_date = get_monitoring_end_date(last_completed_stage)

    cr_start_date = get_cr_start_date(active_stage, last_completed_stage)
 
    cr_end_date = get_cr_end_date(last_completed_stage)

    date_closed = get_date_closed(last_completed_stage)
    
    return last_completed_stage, active_stage, eligibility_start_date, eligibility_end_date, dr_start_date, dr_end_date, monitoring_start_date, \
           monitoring_end_date, cr_start_date, cr_end_date, date_closed
    
def process_project_urls(list_of_project_links):
    processed_project_dicts = []
    # Starting to iterate over the project links and parse the required fields
    for l in list_of_project_links:
        project_dict = {}
        time.sleep(random.choice(range(5,10)))
        res = requests.get(l)
        if res.status_code != 200:
            logger.info("%s is broken".format(l))
            continue 
        else:
            #get page data
            try:
                page_soup = BeautifulSoup(res.text, 'html.parser')
            except: 
                page_soup = ""
                continue  

            # Parsing project information
            url, case_id, project, project_id, country, environmental_category, project_type, sector, \
                financial_institution, project_company, project_loan, year, date_filed ,issues, case_status = parse_project_information(page_soup, l)

            # Parsing the case tracker
            last_completed_stage, active_stage, eligibility_start_date, eligibility_end_date, dr_start_date, dr_end_date, monitoring_start_date, \
               monitoring_end_date, cr_start_date, cr_end_date, date_closed = parse_project_tracker(page_soup)

            # Getting the pdf links
            document_links = get_doc_links(page_soup)
            pdf_links = parse_pdf_links(document_links)

            registration_end_date = None
            registration_start_date = date_filed


            project_dict[Fields.IAM.name] = 'CAO'
            project_dict[Fields.IAM_ID.name] = 21
            project_dict[Fields.YEAR.name] = year
            project_dict[Fields.COUNTRY.name] = country
            project_dict[Fields.PROJECT_NAME.name] = project
            project_dict[Fields.PROJECT_ID.name] = case_id
            project_dict[Fields.PROJECT_NUMBER.name] = project_id
            project_dict[Fields.RELATED_PROJECT_NUMBER.name] = None
            project_dict[Fields.PROJECT_TYPE.name] = project_type
            project_dict[Fields.PROJECT_LOAN_AMOUNT.name] = project_loan
            project_dict[Fields.SECTOR.name] = sector
            project_dict[Fields.ISSUES.name] = issues
            project_dict[Fields.FILERS.name] = None
            project_dict[Fields.FILING_DATE.name] = date_filed
            project_dict[Fields.ENVIRONMENTAL_CATEGORY.name] = environmental_category
            project_dict[Fields.COMPLAINT_STATUS.name] = case_status
            project_dict[Fields.REGISTRATION_START_DATE.name] = registration_start_date
            project_dict[Fields.REGISTRATION_END_DATE.name] = registration_end_date
            project_dict[Fields.ELIGIBILITY_START_DATE.name] = eligibility_start_date
            project_dict[Fields.ELIGIBILITY_END_DATE.name] = eligibility_end_date
            project_dict[Fields.DISPUTE_RESOLUTION_START_DATE.name] = dr_start_date
            project_dict[Fields.DISPUTE_RESOLUTION_END_DATE.name] = dr_end_date
            project_dict[Fields.COMPLIANCE_REVIEW_START_DATE.name] = cr_start_date
            project_dict[Fields.COMPLIANCE_REVIEW_END_DATE.name] = cr_end_date
            project_dict[Fields.MONITORING_START_DATE.name] = monitoring_start_date
            project_dict[Fields.MONITORING_END_DATE.name] = monitoring_end_date
            project_dict[Fields.IS_COMPLIANCE_REPORT_ISSUED.name] = None
            project_dict[Fields.DATE_CLOSED.name] = date_closed
            project_dict[Fields.DOCUMENTS.name] = pdf_links
            project_dict[Fields.HYPERLINK.name] = l


            #writer.writerow(row_data)
            processed_project_dicts.append(project_dict)
            logger.info("Completed project {current_project_number}".format(current_project_number = list_of_project_links.index(l)))
    return processed_project_dicts




if __name__ == "__main__":
    
    base_url = 'http://www.cao-ombudsman.org/cases/default.aspx'
   
    s = get_page_source(base_url)
    
    project_links = get_project_links(s)
    
    processed_project_dicts = process_project_urls(project_links)

    write_csv('cao', processed_project_dicts)
    
   