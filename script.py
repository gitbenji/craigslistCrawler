import urllib
from bs4 import BeautifulSoup
from datetime import datetime

import model
import session

# get string of date created
def getCreated (post_soup):
    p = post_soup.find_all(class_='postinginfo')[2]
    utc_date = p.find('time')['datetime'][:19]              # element time, attribute datetime: '2016-05-06T13:42:50-0400'
    return datetime.strptime(utc_date, '%Y-%m-%dT%H:%M:%S')

# get string of compensation rate for posting
def getComp (post_soup):
    p = post_soup.find(class_='attrgroup')
    return p.find_all('b')[0].text

# get string of employment type for posting
def getEmp (post_soup):
    p = post_soup.find(class_='attrgroup')
    return p.find_all('b')[1].text

# get string of meta details for posting
def getMeta (post_soup):
    metas = ""
    ul = post_soup.find(class_='notices')
    for li in ul.find_all('li'):
        meta = li.text
        metas = metas + meta + ", "
    return metas

# get string of categories with '/' that posting is under
def getCategories (post_soup):
    li = post_soup.find(class_='crumb category')
    return li.find('a').text

# get document from listings page
web_page = urllib.urlopen('https://tallahassee.craigslist.org/search/jjj?employment_type=2').read()
soup = BeautifulSoup(web_page, 'lxml')

# run through each posting on listings page
for post in soup.find_all('a', class_ = 'hdrlnk')[:10]:

    link = post['href']             # url extension for specific posting page

    # get document from individual posting's page
    post_page = urllib.urlopen("https://tallahassee.craigslist.org" + link).read()      # open individual posting page
    post_soup = BeautifulSoup(post_page, 'lxml')                                        # souped posting page


    id = post_soup.find_all(class_='postinginfo')[1].text.split(': ', 1)[1]             # id is second appearance of class, read as 'posting id: #########'
    uri = "https://tallahassee.craigslist.org" + link
    created = getCreated(post_soup)
    description = post_soup.find(id='postingbody').text
    title = post_soup.find(id='titletextonly').text
    compensation = getComp(post_soup)
    employment_type = getEmp(post_soup)
    meta = getMeta(post_soup)
    categories = getCategories(post_soup)

    posting = model.Posting(id = id, uri = uri, created = created, description = description, title = title, compensation = compensation, employment_type = employment_type, meta = meta, categories = categories)

    session.addPost(posting)

# call session.py to commit
session.commitAll()

# call session.py to close
session.closeConnection()
