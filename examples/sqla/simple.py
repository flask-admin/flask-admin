from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext import admin, wtf
from flask.ext.admin.contrib import sqlamodel
from flask.ext.admin.contrib.sqlamodel import filters

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Create models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, backref='posts')

    def __unicode__(self):
        return self.title


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# Customized Post model admin
class PostAdmin(sqlamodel.ModelView):
    # Visible columns in the list view
    #list_columns = ('title', 'user')
    excluded_list_columns = ['text']

    # List of columns that can be sorted. For 'user' column, use User.username as
    # a column.
    sortable_columns = ('title', ('user', User.username), 'date')

    # Rename 'title' columns to 'Post Title' in list view
    rename_columns = dict(title='Post Title')

    searchable_columns = ('title', User.username)

    column_filters = ('user',
                      'title',
                      'date',
                      filters.FilterLike(Post.title, 'Fixed Title', options=(('test1', 'Test 1'), ('test2', 'Test 2'))))

    # Pass arguments to WTForms. In this case, change label for text field to
    # be 'Big Text' and add required() validator.
    form_args = dict(
                    text=dict(label='Big Text', validators=[wtf.required()])
                )

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(PostAdmin, self).__init__(Post, session)

if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'Simple Models')

    # Add views
    admin.add_view(sqlamodel.ModelView(User, db.session))
    admin.add_view(PostAdmin(db.session))

    # Create DB
    db.create_all()

    # Start app
    app.debug = True
    app.run('0.0.0.0', 8000)
