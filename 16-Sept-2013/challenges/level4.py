__author__ = 'Gabriel Tremblay - initnull@gmail.com'

from tornado.web import RequestHandler
from tornado.escape import xhtml_escape

import base64
import config
import utils
import random
import sqlite3
import time


database = sqlite3.connect('db/level4.db')
database.execute(
    '''CREATE TABLE if not exists resets (token text, email text)''')


def create_token():
    """
    Creates a random reset token.
    :return: a password reset token
    """
    # Get a large random number http://docs.python.org/3.3/library/random.html
    seed_value = int(time.time() * 256)
    random.seed(seed_value)
    random_bits = random.getrandbits(128)
    token = base64.b64encode(str(random_bits).encode())
    print(seed_value)
    return token.decode()


def save_token(email, token):
    """
    Save the token with the email in the database
    :param email: user email
    :param token: Random token
    """
    cursor = database.cursor()
    cursor.execute("INSERT INTO resets VALUES (?, ?)", (token, email))
    database.commit()


def get_token_email(token):
    """
    Fetch the savec reset token entry from the database
    :param token: user supplied token
    :return: the reset entry
    """
    cursor = database.cursor()
    cursor.execute("SELECT * FROM resets WHERE token=?", (token, ))
    return cursor.fetchone()


class Level4Handler(RequestHandler):
    def get(self):
        show_code = self.get_argument("code", default=None)
        reset_token = self.get_argument("t", default=None)

        if config.level4_showcode and show_code:
            with open(__file__) as code:
                content = code.read()
                self.write("<pre>" + xhtml_escape(content) + "</pre>")
        elif reset_token:
            mail_entry = get_token_email(reset_token)

            if mail_entry:
                _, email = mail_entry
                if email == config.admin_email:
                    base_url = utils.get_cosmetic_url(self.request)
                    self.render("templates/success.html",
                        message=config.level4_message,
                        next_challenge=base_url + config.level1_link
                    )
                else:
                    self.render("templates/error.html",
                            message="HoHo! You did trigger the password reset "
                                    "function, but for the wrong user.")
            else:
                self.render("templates/error.html",
                            message="No such token!")
        else:
            self.render("templates/level.html", level="Level 4",
                        show_code=config.level4_showcode)

    def post(self):
        email = self.get_argument("email", default=None)
        if not email:
            self.send_error(400)
        elif email == config.admin_email:
            reset_token = create_token()
            save_token(email, reset_token)
            self.render("templates/error.html",
                        message="The reset link has been sent to the "
                                "admin's email.")
        else:
            reset_token = create_token()
            save_token(email, reset_token)
            base_url = utils.get_cosmetic_url(self.request)
            reset_link = base_url + config.level4_link + "?t=" + reset_token
            self.render("templates/resetlink.html", resetlink=reset_link)
