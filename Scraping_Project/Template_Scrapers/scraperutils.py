import os
import requests
import pandas as pd
from datamodel import Fields
from collections import OrderedDict


def _get_data(path, project_id):
    """Private function to get the absolute path to the downloaded file."""
    cwd = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(cwd, 'pdf', project_id, path)


def check_make_directory(project_id):
    """Check to see if the `pdf/$PROJECT_ID` dir exists. If not, make it."""
    cwd = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(cwd, 'pdf', project_id)):
        os.makedirs(os.path.join(cwd, 'pdf', project_id))


def get_complete_project_row(project_details):
    """
    Given a dictionary with the scraped information about a project, 
    this util method creates a ordered dictionary with values,
    if present in project_details else as None
            
    This can be useful to store consistent set of fields for all scraped projects
    """
    project_row = OrderedDict()
    for field in list(Fields):
        project_row[field.name] = project_details.get(field.name)
    return project_row


def write_csv(scraper_name, data):
    """
    Function to write out the list of OrderedDicts to a CSV using Pandas. Writes
    to a file with scraper name and timestamp in the title.

    Inputs
    ------

    scraper_name : str.
                    Name of the scraper, i.e., the webiste. Example is 'eib'.

    data : list.
            List of OrderedDicts
    """
    date = str(datetime.now())
    pd.DataFrame(data).to_csv('{}_scrape_{}.csv'.format(scraper_name, date),
                              encoding='utf-8', index=False)  


def download_project_documents(url, project_id):
    """
    Function to download PDF documents given a URL. Currently creates a `pdf`
    directory in PWD and then subdirs for each project ID.

    Copy-pasta from https://stackoverflow.com/a/16696317.
    """
    filename = url.split('/')[-1]
    local_filename = _get_data(filename, project_id)
    print('Downloading {}'.format(url))
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename
