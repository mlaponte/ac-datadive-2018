import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

import scraperutils
from datamodel import Fields


def get_page_content(url):
    """
        Given a url, this would return the html content of the page parsed by BeautifulSoup
    """
    page = requests.get(url)
    page_content = BeautifulSoup(page.content, 'html.parser')
    return page_content, page.status_code


def get_project_table(html):
    """
        Grab the table with project information
    """
    maindiv = html.find("div", {"id": "consultationsList"})
    table= maindiv.find_all('table')
    df = pd.read_html(str(table), header=0)
    df = df[0]
    return df


def get_project_urls(html):
    """
    Retrieve the urls from the onclick js function
    """
    maindiv = html.find("div", {"id": "consultationsList"})
    trs = maindiv.find_all('tr')
    urls = []
    for i in trs:
        if i.get('onclick'):
            url = i.get('onclick').split(',')[0].replace("window.open('/"'',"").strip('\'').strip()
            url = 'http://' + url
            urls.append(url)
    return urls


def get_project_documents(page):
    """
    Retrieve URLS for each complaint.
    """

    docs = page.find("div", {"class": "box complaints-box white-background"})

	#Not all pages have document sections. Not all pages with document sections have document links.
    if docs:
        links = docs.find_all('a')
        if links:
            document_links = []
            for l in links:
                url = l['href']	
                document_links.append('www.eib.org' + url)
            return ','.join(document_links)
        else:
            return None
    else:
        return None


def scrape(html):
    ## GET PROJECT TABLE
    df = get_project_table(html)
    ## GET URLS
    urls = get_project_urls(html)
    df['urls'] = urls

    ## Limit to E type
    df = df[df.Type == 'E']

    def clean(x):
        return x.replace(':','').strip()

    ## Store the project specific data
    ## Only grabbing Filer/ID right now - but should be expanded
    project_data = []
    count404 = 0
    url404 = []

	## Iterate over urls - controlling for 404 errors
    count = 0
    for idx, url in zip(df.index,df.urls):
        page, sc = get_page_content(url)
        if sc != 404:
            main_section = page.find('div',{'id':'consultations'})
            project_id = main_section.find('strong',text='Reference').next_sibling
            filer = main_section.find('strong',text='Complainant').next_sibling
            #Scrape and DL project docs. Just dumps the files to the same
            #directory for now.
            documents = get_project_documents(page)
            if documents:
                cleaned_id = project_id.replace('/', '_').replace(': ', '')
                scraperutils.check_make_directory(cleaned_id)
                for doc in documents.split(','):
                    filepath = scraperutils.download_project_documents('http://' + doc,
                                                                       cleaned_id)
            project_data.append([idx, clean(project_id), clean(filer), documents])
        else:
            count404 += 1
            url404.append(url)
            project_data.append([idx, None, None, None])
        count += 1
        if count % 25 ==0:
            print count

    print('Number of 404 Responses', count404)

    ## Merge into DF and return 
    project_data = pd.DataFrame(project_data,columns=['idx','project id','Filer(s)', 'documents'])
    project_data.index = project_data.idx
    project_data = project_data.drop('idx',axis=1)
    df = pd.concat([df, project_data],axis=1)
    df = df.reset_index(drop=True)
    return df, {'url404':url404, 'count404':count404}


def run():
    """
    Run all the things.

    Returns
    ------

    output_data : list
                    List of OrderedDicts
    """
    base_url = "http://www.eib.org/about/accountability/complaints/cases/index.htm"
    html, sc = get_page_content(base_url)

    df, info = scrape(html)
    df['IAM'] = 'EIB'
    df['IAM ID'] = 29
    df['registration_start_date'] = df['Received Date'] ## This is in the AC code but may not be what they actually want. 
    df['year'] = [i[-4:] for i in df['Received Date']]


    data_model_conforming = {
	'Received Date'          :'FILING_DATE'             ,
	'Case Name'              :'PROJECT_NAME'            ,
	'Country/Territory'      :'COUNTRY'                 ,
	'project id'             :'PROJECT_ID'              ,
	'urls'                   :'HYPERLINK'               ,
	'Filer(s)'               :'FILERS'                  ,
	'IAM'                    :'IAM'                     ,
	'IAM ID'                 :'IAM_ID'                  ,
	'registration_start_date':'REGISTRATION_START_DATE' ,
	'Current Status'         :'COMPLAINT_STATUS'        ,  
	'year'                   :'YEAR'                    ,
	'documents'              :'DOCUMENTS'
    }
    output_df = df.copy()
    output_df = output_df.rename(columns = data_model_conforming)

    output_data = []
    for ix, r in output_df.iterrows():
       temp = scraperutils.get_complete_project_row(r) 
       output_data.append(temp)

    return output_data
        

if __name__ == '__main__':
    formatted_data = run()
    scraperutils.write_csv('eib', formatted_data)
