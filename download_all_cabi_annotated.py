''' Input = (1) link containing multiple zip files.
	Downloads the zipped CaBi data from s3 and stores locally.
	Output = zip files downloaded from s3.
'''

### download_all_cabi.py

from splinter import Browser
import os
import urllib.request
import shutil
import zipfile


def get_links():
    ### You'll need to find a chrome browser or firefox browser to launch this function
    browser = Browser('chrome')
    browser.visit('https://s3.amazonaws.com/capitalbikeshare-data/index.html')

    links = browser.find_by_css('#tbody-content a')
    ###links = [link for link in links if link['href']]
	
	# iterates through links, opens them, and gets any .zip content
    zip_links = [] # instantiating empty list
    for link in links: # iterates through links
        link_text = link['href'] # grab actual link string
        with urllib.request.urlopen(link_text) as response: # open the link and get what's inside
            subtype = response.info().get_content_subtype()
            if subtype == 'zip': # if it's a zip file, append it to the list
                zip_links.append(link_text)

    return zip_links # return list of zip files


def download_links(links):

    download_dir = '../cabi_data' # set the download directory to this locally
    if not os.path.exists(download_dir): # if directory doesn't exist, create it
        os.mkdir(download_dir)
	# grabs file name from the end of the link and creates a path component
    for link in links: # iterates through the zip links list returned above
        file_name = os.path.join(download_dir, link.split('/')[-1]) # grabs file name from end of link and creates a local path component
        print(file_name)
        ### save file to disk
        with urllib.request.urlopen(link) as response, open(file_name, 'wb') as out_file:
			# shutil useful for files and collections of files (copying and removal)
            shutil.copyfileobj(response, out_file) # copies file from link and writes new file locally
        with zipfile.ZipFile(file_name, "r") as zip_ref: # unzips the .zips to return csvs, puts in download_dir
            zip_ref.extractall(download_dir)

links = get_links()
download_links(links)