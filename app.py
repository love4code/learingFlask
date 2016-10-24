from flask import Flask, request, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
# The onluy requirement to the Flask class is constructor is the Pythons
# name variable.
#**********>>>
# TIP!!!!   >>>>>>>>
#**********>>>
# Python uses the this argument to determine the root pathof the application
# SO that later it can find resource files relative to the location of the
# application

# >>> current_app.name
# 'TestApp.app'
# >>> app_ctx.pop()
# >>> current_app.name

app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()

# >>> app.url_map
# Map([<Rule '/' (OPTIONS, GET, HEAD) -> index>,
#  <Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
#  <Rule '/user/<name>' (OPTIONS, GET, HEAD) -> user>])
