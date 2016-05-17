from urllib import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

import session


# get string of date created
def getCreated(post_soup):
    p = post_soup.find_all(class_='postinginfo')[2]
    # element time, attribute datetime: '2016-05-06T13:42:50-0400'
    utc_date = p.find('time')['datetime'][:19]
    # took out timezone because of sqlite
    return datetime.strptime(utc_date, '%Y-%m-%dT%H:%M:%S')


# get string of compensation rate for posting
def getComp(post_soup):
    p = post_soup.find(class_='attrgroup')
    return p.find_all('b')[0].text


# get string of employment type for posting
def getEmp(post_soup):
    p = post_soup.find(class_='attrgroup')
    return p.find_all('b')[1].text


# get string of meta details for posting
def getMeta(post_soup):
    metas = ""
    ul = post_soup.find(class_='notices')
    for li in ul.find_all('li'):
        meta = li.text
        # comma separated string of meta details
        metas = metas + meta + ", "
    return metas


# get array of categories that posting is under
def getCategories(post_soup):
    li = post_soup.find(class_='crumb category')
    return li.find('a').text.split('/')


# get document from listings page
url = 'https://tallahassee.craigslist.org/search/jjj?employment_type=2'
web_page = urlopen(url).read()
soup = BeautifulSoup(web_page, 'lxml')

# run through each posting on listings page
for post in soup.find_all('a', class_='hdrlnk')[:10]:

    # url extension for specific posting page
    link = post['href']

    # get document from individual posting's page
    # open individual posting page
    post_page = urlopen("https://tallahassee.craigslist.org" + link).read()
    # souped posting page
    post_soup = BeautifulSoup(post_page, 'lxml')

    # variables for the data - to be sent through the model
    # id is second appearance of class, read as 'posting id: #########'
    uid = post_soup.find_all(class_='postinginfo')[1].text.split(': ', 1)[1]
    uri = "https://tallahassee.craigslist.org" + link
    created = getCreated(post_soup)
    description = post_soup.find(id='postingbody').text
    title = post_soup.find(id='titletextonly').text
    compensation = getComp(post_soup)
    employment_type = getEmp(post_soup)
    meta = getMeta(post_soup)

    from model import Posting
    # individual posting instance through the model
    posting = Posting(
        uid=uid,
        uri=uri,
        created=created,
        description=description,
        title=title,
        compensation=compensation,
        employment_type=employment_type,
        meta=meta
    )

    from model import Category

    categories = getCategories(post_soup)
    for category_name in categories:

        category = session.getFromDb(Category, name=category_name)
        if not category:
            category = Category(name=category_name)
            session.addToDb(category)

        # send categories to session
        posting.categories.append(category)

    # send posting to session
    session.addToDb(posting)

# call session.py to close
session.closeConnection()
