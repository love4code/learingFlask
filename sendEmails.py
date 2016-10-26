from TestApp import app
from flask_mail import Message
from flask import render_template
from flask_mail import Mail

msg = Message('test subject', sender='lover4code@code.com', recipients=[
    'groversbusiness@gmail.com'])

msg.body = 'text body'

msg.html = '<b>HTML</b> body'

with app.app.app_context():
    app.mail.send(msg)

# Create a function to send emails

def send_email(to, subject, template, **kwargs):
    """Send emails"""


    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, \
                  sender=app.config['FLASKY_MAIL_SENDER'], \
                  recipients=[to])
    # Plain Text Body
    msg.body = render_template(template + '.txt', **kwargs)
    # Rich text Body
    msg.html = render_template(template + '.html', **kwargs)
    # Needs to be executed with an activated application context
    mail.send(msg)