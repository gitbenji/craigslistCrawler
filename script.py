import urllib
from bs4 import BeautifulSoup
import json
from daytime import daytime

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Firefox()
#
# # functions for post_object values
# #
# #
# # open browser to posting page with Selenium
# def open_browser (link):
#     driver.get("https://tallahassee.craigslist.org" + link)
#
# # click the reply button
# def click_reply ():
#     try:
#         reply_btn = driver.find_element_by_class_name('reply_button')
#         reply_btn.click()
#         return True
#     except:
#         return False
#         pass
#
# # wait until popup loads with info and print info
# def get_reply_info (button_exists):
#     if button_exists:
#         isLoaded = False
#         while not isLoaded:
#             div = driver.find_element_by_class_name('returnemail')
#             if div.get_attribute('style') == 'display: block;':
#                 isLoaded = True
#                 email = driver.find_element_by_class_name('mailapp').text
#                 reply = {
#                     'email': email
#                 }
#                 return reply
#     else:
#         reply = {
#             'text': 'N/A',
#             'email': 'N/A'
#         }



# functions for post_object values bs4
#
#
# get string of formatted date and time the posting was created
def getCreated (post_soup):
    p = post_soup.find_all(class_='postinginfo')[2]
    splitPSoup = p.find('time')['datetime'].split('T')      # element time, attribute datetime: '2016-05-06T13:42:50-0400'
    return splitPSoup[0] + ' ' + splitPSoup[1]              # returns string with ' ' instead of 'T'

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


    # # SELENIUM run through
    # open_browser(link)
    # button_exists = click_reply()
    # post_object = {
    #     'reply': get_reply_info(button_exists)
    # }


    # BS4 run through
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

    print json.dumps(post_object, sort_keys=True, indent=4, separators=(',', ': '))
