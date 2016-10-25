from flask import Flask, request, render_template, redirect, url_for, session
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
# Two Hours of hell thanks to wtf undocumented updates
# Basically have to re learn the plugin From Scratch
# Expect more frustration to come.
from wtforms import StringField, SubmitField
from wtforms import validators
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

app = Flask(__name__)
# The app.config dictionary is a general purpose place to store config vars
# used by the framework
# The configuration object also has methods to import values from files
# or the environment
app.config['SECRET_KEY'] = 'Hard to guess string'

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

# In Flask-WTF each form is respresented by a class that inherrits from
# the class Form
# The fields in the form are defined as class variables and, each class
# variable is assigned an object associated with the field type.
# The first argument to the field is the label that will be used when
# rendering it.


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
    # validate() Returns True is the data has been accepted
    # by all the field Validators
    if form.validate():
        # variable data is stored in the user session as session['name']
        session['name'] = form.name.data
        # POST/REDIRECT/GET Best Practice to prevent form re submission
        # url_for() generates a route using the URL map, this ensures that
        # any changes made in routes will automatically be available
        return redirect(url_for('index'))
    # name variable is now accessed though the user session session['name']
    # using session.get() gettr
    # using get to request distionary keys prevent exceptions for keys not
    # found because get returns a default value of None for a missing key
    return render_template('index.html', form=form,name=session.get('name'))

# dynamic variables nthe url
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()

# >>> app.url_map
# Map([<Rule '/' (OPTIONS, GET, HEAD) -> index>,
#  <Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
#  <Rule '/user/<name>' (OPTIONS, GET, HEAD) -> user>])
