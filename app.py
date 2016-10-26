from flask import Flask, request, render_template, redirect, \
                                        url_for, \
    session, flash
from flask_script import Manager, Shell

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
# When working in a virtual enviornment make sure to be in the activated
# state when using pip install to install packages
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message



# Two Hours of hell thanks to wtf undocumented updates
# Basically have to re learn the plugin From Scratch
# Expect more frustration to come.
from wtforms import StringField, SubmitField
from wtforms import validators
import os
# The only requirement to the Flask class is constructor is the Pythons
# name variable.
#**********>>>
# TIP!!!!   >>>>>>>>
#**********>>>
# Python uses the this argument to determine the root path of the
# application
# SO that later it can find resource files relative to the location of the
# application

# >>> current_app.name
# 'TestApp.app'
# >>> app_ctx.pop()
# >>> current_app.name
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'data.sqlite')
# This setting enables automatic commits of databse changes at the end of
#  every request
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# The app.config dictionary is a general purpose place to store config vars
# used by the framework
# The configuration object also has methods to import values from files
# or the environment
app.config['SECRET_KEY'] = 'Hard to guess string'

# +-----------------------------------------------------------------------+
#               MAIL SERVER CONFIGURATIONS
# +-----------------------------------------------------------------------+
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'markagrover85@gmail.com' # should be set
# in envoirnment as os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = 'installs' # should be set
# in envoirnment as os.environ.get('MAIL_PASSWORD')
# +-----------------------------------------------------------------------+
#               MAIL ADMIN CONFIGURATIONS
# +-----------------------------------------------------------------------+
app.config['FLASKY_ADMIN'] = 'groversbusiness@gmail.com' # should be set
# in envoirnment as os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = 'demo-subject-prefix'

app.config['FLASKY_MAIL_SENDER'] = 'markagrover85@gmail.com' # should be set
# in envoirnment as os.environ.get('FLASKY_ADMIN')

# adding Manager we are able to run command line arguments to get our
# server up and running.
manager = Manager(app)
# Pass our app object through Bootstrap to make our app a bootstrap app.
bootstrap = Bootstrap(app)
# Moment allows for date time to be displayed in the client timezone
# Look into Unicode Requirements on strings if having troubles
moment = Moment(app)
# Error handlers return a response, like view functions.
# They aslo return the numeric status code that corresponds to the error.
db = SQLAlchemy(app)
# In Flask-WTF each form is represented by a class that inherits from
# the class Form
# The fields in the form are defined as class variables and, each class
# variable is assigned an object associated with the field type.
# The first argument to the field is the label that will be used when
# rendering it.

# To expose the database migrate commands, Flask Migrate exposes a
# 'MigrateCommand' class that is attached to Flask_Script's manager object.

# Before database migrations can be maintained, it is necessary to create
# a migration repository with the 'init' command
# [$]> python app.py db init
# this command create a migrations folder, where all themigration scripts
#  will be stored.
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
# [$]> python app.py db migrate -m "Initial Migration"
# creates an automatic migration script

# [$]> python app.py db upgrade
# For a first migration this is effectively equivalent to call
# db.create_all()
# however, in successive migrations the upgrade command applies updates
# to the tables without effecting their contents

# Initialize Flask Mail
mail = Mail(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # allows us to add filters
    # because the query is not automatically executed (lazy='dynamic')
    users = db.relationship('User', backref='role', lazy='dynamic')
    # >> > str(user_role.users)
    # 'SELECT users.id AS users_id, users.username AS users_username,
    # users.role_id AS users_role_id \nFROM users \nWHERE ? = users.role_id'

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username




class NameForm(Form):
    name = StringField('What is your name?',[validators.DataRequired()])
    submit = SubmitField('Submit')

# +-----------------------------------------------------------------------+
# |                                                                       |
# |                   Optional Validator Arguments are                    |
# |                                                                       |
# +-----------------------------------------------------------------------+
# | StringField                Text Field
# |
# |...........................+...........................................|
# |TextAreaField               multiple line Text Field
# |
# |...........................+...........................................|
# |PasswordField               Password TextField
# |
# |...........................+...........................................|
# |HiddenField                 hidden TextField
# |
# |...........................+...........................................|
# |DateField                   TextField That accepts a datetime.datetime
# |                            value in a given format
# |...........................+...........................................|
# |DateTimeField               Text Field that accepts a datetime.datetime
# |                            value in a given format
# |...........................+...........................................|
# |IntegerField                Text Field that accepts an integer value
# |
# |...........................+...........................................|
# |DecimalField                text field that accepts a decimal.Decimal
# |                            Value
# |...........................+...........................................|
# |FloatField                  Text Field That Accepts a floating point
# |                             number
# |...........................+...........................................|
# |BooleanField                Checkbox with True and False Values
# |
# |...........................+...........................................|
# |RadioField                  List of Radio Buttons
# |
# |...........................+...........................................|
# |SelectField                 Drop-Down list of choices
# |
# |...........................+...........................................|
# |SelectMultipleField         Drop-Down list of choices
# |                            with multiple selection.
# |...........................+...........................................|
# |FileField                   File upload field
# |
# |...........................+...........................................|
# |SubmitField                 Form submission button
# |
# |...........................+...........................................|
# |FormField                   Embed a form as a field in a container form
# |
# |...........................+...........................................|
# |FieldList                   List of fields of a given type
# |
# |...........................+...........................................|

# +-----------------------------------------------------------------------+
# |
# | WTForms Built In Validators
# |...........................+...........................................|
# |Email                       Validates an Email Address
# |
# |...........................+...........................................|
# |EqualTo                     Compares the values of two fields:
# |                            Useful when request a double password fields
# |...........................+...........................................|
# |IPAddress                   Validates an IPv4 network address
# |
# |...........................+...........................................|
# |Length                      Validates the length of the string entered
# |
# |...........................+...........................................|
# |NumberRange                 Validates that the value entered is
# |                            within the numeric range
# |...........................+...........................................|
# |Optional                    Allows an Empty Input On the Field
# |                             Skipping additional Validators
# |...........................+...........................................|
# |Required                    Validate that the field contains Data
# |
# |...........................+...........................................|
# |Regex                       Validates against a regex
# |
# |...........................+...........................................|
# |URL                         Validates a URL
# |
# |...........................+...........................................|
# |AnyOf                       Validates that the input is one of a list
# |                            of possible values
# |...........................+...........................................|
# |NoneOf                      Validates that the input is none of a list
# |                            of possible values
# |...........................+...........................................|
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Because Index page has a form we need to  Register  the view function
# as a handler for GET and POST request in the URL map
# When Methods is not given then the view function is registered to handle
# get request only
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            # Expanding Index to send Admin an email each time their is a
            #  new user
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],
                           'NEW USER',
                           'mail/new_user',
                           user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get(
        'name'),known=session.get('known',False))

# dynamic variables nthe url
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# Create a function to send emails

def send_email(to, subject, template, **kwargs):
    """Send emails"""


    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    # Plain Text Body
    msg.body = render_template(template + '.txt', **kwargs)
    # Rich text Body
    msg.html = render_template(template + '.html', **kwargs)
    # Needs to be executed with an activated application context
    mail.send(msg)

# The Flask_Script Shell command can be comfigured to automatically
# import certian objects

# To add objects to the import list the shell command needs to b registered
# with a make_context callback function

def make_shell_context():
    """Make a shell context"""

    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

# >>> app.url_map
# Map([<Rule '/' (OPTIONS, GET, HEAD) -> index>,
#  <Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
#  <Rule '/user/<name>' (OPTIONS, GET, HEAD) -> user>])
