# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Flask-Script Manager
"""

import os
import sqlalchemy

from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand

from fbone import create_app
from fbone.extensions import db
from fbone.utils import PROJECT_PATH, MALE
from fbone.modules.posting import Posting, Category

from urllib import urlopen
from bs4 import BeautifulSoup

from script import getCreated, getComp, getEmp, getMeta, getCategories

app = create_app()
manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)


@manager.command
def initdb():
    """Init/reset database."""

    try:
        db.drop_all()
    except sqlalchemy.exc.OperationalError:
        URI = app.config['SQLALCHEMY_DATABASE_URI'][:app.config['SQLALCHEMY_DATABASE_URI'].rfind('/')]
        engine = sqlalchemy.create_engine(URI)
        engine.execute("CREATE DATABASE fbone")

    db.create_all()

    # code from original script.py
    #
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

        # go through each category for individual posting
        categories = getCategories(post_soup)
        for category_name in categories:

            category = Category().first(name=category_name)
            if not category:
                category = Category(name=category_name)
                # save category using base.py method save
                Category().save(category)

        # save posting using base.py method save
        Posting().save(posting)


@manager.command
def tests():
    """Run the tests."""
    import pytest
    cmd = pytest.main([os.path.join(PROJECT_PATH, 'tests'), '--verbose'])
    return cmd


if __name__ == "__main__":
    manager.run()
