import urllib
from bs4 import BeautifulSoup
import json
from datetime import datetime



# functions for post_object values bs4
#
#
# get string of formatted date and time the posting was created
def getCreated (post_soup):
    p = post_soup.find_all(class_='postinginfo')[2]
    utc_date = p.find('time')['datetime']
    print utc_date
    print datetime.strptime(utc_date, '%Y-%m-%dT%H:%M:%S %z')
    # splitPSoup = p.find('time')['datetime'].split('T')      # element time, attribute datetime: '2016-05-06T13:42:50-0400'
    # return splitPSoup[0] + ' ' + splitPSoup[1]              # returns string with ' ' instead of 'T'

# get string of compensation rate for posting
def getComp (post_soup):
    p = post_soup.find(class_='attrgroup')
    return p.find_all('b')[0].text

# get string of employment type for posting
def getEmp (post_soup):
    p = post_soup.find(class_='attrgroup')
    return p.find_all('b')[1].text

# get array of meta details for posting
def getMeta (post_soup):
    metas = []
    ul = post_soup.find(class_='notices')
    for li in ul.find_all('li'):
        meta = li.text
        metas.append(meta)
    return metas

# get array of categories posting is under
def getCategories (post_soup):
    li = post_soup.find(class_='crumb category')
    return li.find('a').text.split('/')



# get document from listings page
web_page = urllib.urlopen('https://tallahassee.craigslist.org/search/jjj?employment_type=2').read()
soup = BeautifulSoup(web_page, 'lxml')

# run through each posting on listings page
for post in soup.find_all('a', class_ = 'hdrlnk')[:10]:

    link = post['href']                                 # url extension for specific posting page

    # get document from individual posting's page
    post_page = urllib.urlopen("https://tallahassee.craigslist.org" + link).read()      # open individual posting page
    post_soup = BeautifulSoup(post_page, 'lxml')                                        # souped posting page

    post_object = {                                                                     # object for post details
        'id': post_soup.find_all(class_='postinginfo')[1].text.split(': ', 1)[1],       # id is second appearance of class, read as 'posting id: #########'
        'uri': "https://tallahassee.craigslist.org" + link,
        'created': getCreated(post_soup),                                               # has a '-400' after time
        'description': post_soup.find(id='postingbody').text,
        'title': post_soup.find(id='titletextonly').text,
        # 'reply': {
        #     'text': getPhoneNum(post_soup)
        #     'email':
        # },
        'details': {
            'compensation': getComp(post_soup),
            'employment_type': getEmp(post_soup)
        },
        'meta': getMeta(post_soup),
        'categories': getCategories(post_soup)
    }

    # print json.dumps(post_object, sort_keys=True, indent=4, separators=(',', ': '))
