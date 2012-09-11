# -*- coding: utf-8 -*-

import sys
import os

sys.path.pop(0)
sys.path.insert(0, os.getcwd())

from flask import Flask

import peewee

from flask.ext import admin
from flask.ext.admin.contrib import peeweemodel


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'

db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField(max_length=80)
    email = peewee.CharField(max_length=120)

    def __unicode__(self):
        return self.username


class UserInfo(BaseModel):
    key = peewee.CharField(max_length=64)
    value = peewee.CharField(max_length=64)

    user = peewee.ForeignKeyField(User)

    def __unicode__(self):
        return '%s - %s' % (self.key, self.value)


class Post(BaseModel):
    title = peewee.CharField(max_length=120)
    text = peewee.TextField(null=False)
    date = peewee.DateTimeField()

    user = peewee.ForeignKeyField(User)

    def __unicode__(self):
        return self.title


class UserAdmin(peeweemodel.ModelView):
    inline_models = (UserInfo,)


class PostAdmin(peeweemodel.ModelView):
    # Visible columns in the list view
    #list_columns = ('title', 'user')
    excluded_list_columns = ['text']

    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    sortable_columns = ('title', ('user', User.email), 'date')

    # Full text search
    searchable_columns = ('title', User.username)

    # Column filters
    column_filters = ('title',
                      'date',
                      User.username)


@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    admin = admin.Admin(app, 'Peewee Models')

    admin.add_view(UserAdmin(User))
    admin.add_view(PostAdmin(Post))

    try:
        User.create_table()
        UserInfo.create_table()
        Post.create_table()
    except:
        pass

    app.debug = True
    app.run('0.0.0.0', 8000)
