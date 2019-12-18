from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import os
import subprocess

app = Flask(__name__,
            static_url_path='',
            static_folder='static',)

app.config['DEBUG'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

# Create db object
db = SQLAlchemy(app)

########################################
#
# Models
#
########################################

import re
import string

import datetime

class msgdb(db.Model):
    # Data Model for mdown
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<text %r>' % self.text

########################################
#
# Views
#
########################################

def remove_control_chars(my_str):
    return ''.join([x for x in my_str if x in string.printable])

@app.route('/', methods=['GET'])
def index():
    url = request.args.get('preview')

    if url:
        if re.compile('<[a-zA-Z]').search(url):
            res = 'Someone submitted a domain for review.'
        else:
            # We remove control chars to ensure the domain is properly handled by our bot
            res = 'Someone submitted the {} domain for review.'.format(remove_control_chars(url))
    else:
        res = None

    return render_template('index.html', res=res)

@app.route('/submit', methods=['GET'])
def submit_for_review():
    url = request.args.get('domain')

    if url and not msgdb.query.filter_by(text=url).first():
        msg = msgdb(url)
        db.session.add(msg)
        db.session.commit()

    url = 'https://xss.owoups.org/C2164A36420F2D05A652B7BDDE9FB82FB7EA323418CBBD222C681719F87623B6E1DC6C1A60627E3C7FC4831587FDC7540E0261E42F39D26E385D895B95CD32F6';
    cookie_name = 'flag';
    cookie_domain = 'xss.owoups.org';
    cookie_value = 'FLAG-04B4E8A5AFF726C15FEB5B041B71CE4F';
    subprocess.call(["phantomjs", "--ignore-ssl-errors=true", "--local-to-remote-url-access=true", "--web-security=false", "--ssl-protocol=any", "/app/xssbot.js", url, cookie_domain, cookie_name, cookie_value]);

    return render_template('confirm.html')

@app.route('/C2164A36420F2D05A652B7BDDE9FB82FB7EA323418CBBD222C681719F87623B6E1DC6C1A60627E3C7FC4831587FDC7540E0261E42F39D26E385D895B95CD32F6', methods=['GET'])
def admin():
    url_obj = msgdb.query.order_by(msgdb.date).first()

    print(url_obj)

    if url_obj:
        db.session.delete(url_obj)
        db.session.commit()

        url = url_obj.text

        if re.compile('<[a-zA-Z]').search(url):
            res = 'Someone submitted a domain for review.'
        else:
            # We remove control chars to ensure the website is properly handled by our bot
            res = 'Someone submitted the {} domain for review.'.format(remove_control_chars(url))
    else:
        res = None

    return render_template('trigger.html', res=res)
