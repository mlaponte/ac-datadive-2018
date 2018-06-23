import requests
from datamodel import Fields
from collections import OrderedDict


def get_complete_project_row(project_details):
    """
        Given a dictionary with the scraped information about a project, 
        this util method creates a ordered dictionary with values,
            if present in project_details else as None
            
        This can be useful to store consistent set of fields for all scraped projects
    """
    project_row = OrderedDict()
    for field in list(Fields):
        project_row[field] = project_details.get(field)
    return project_row


def download_project_documents(url):
    """
    Function to download PDF documents given a URL. Currently dumps files to
    $PWD.

    Copy-pasta from https://stackoverflow.com/a/16696317.
    """
    local_filename = url.split('/')[-1]
    print('Downloading {}'.format(url))
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename
