
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
