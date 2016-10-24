from flask import Flask, request, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
# The onluy requirement to the Flask class is constructor is the Pythons
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
# adding Manager we are able to run command line arguments to get our
# server up and running.
manager = Manager(app)
# Pass our app object through Bootstrap to make our app a bootstrap app.
bootstrap = Bootstrap(app)

# Error handlers return a response, like view functions.
# They aslo return the numeric status code that corresponds to the error.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')

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
