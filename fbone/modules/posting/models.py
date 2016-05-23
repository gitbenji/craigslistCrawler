
from sqlalchemy import Column, Table

from fbone.modules.base import Base
from fbone.extensions import db

association_table = Table('association', Base.metadata,
    Column('posting_id', db.Integer, db.ForeignKey('postings.id')),
    Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)


class Posting(Base):
    __tablename__ = 'postings'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    uid = db.Column(db.String)
    uri = db.Column(db.String)
    created = db.Column(db.DateTime)
    description = db.Column(db.Text)
    title = db.Column(db.String)
    compensation = db.Column(db.String)
    employment_type = db.Column(db.String)
    meta = db.Column(db.String)
    categories = db.relationship('Category', secondary=association_table)
    # category_id = db.Column(db.Integer, db.ForeignKey(category.id))
    # categories = db.relationship('Category', lazy='dynamic')


class Category(Base):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, unique=True)
