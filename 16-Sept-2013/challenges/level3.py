__author__ = 'Gabriel Tremblay - initnull@gmail.com'

from tornado.web import RequestHandler
from tornado.escape import xhtml_escape

import base64
import binascii
import config
import hashlib
import hmac
import utils

def create_token(email):
    """
    Creates a token and apply a hashmac so the user can't tamper it.
    :param email: User's email
    :return: a password reset token
    """
    token = base64.b64encode(email.encode())
    mac = hmac.new(config.level4_secret_key, token, hashlib.sha1)
    return token.decode() + "|" + str(mac.hexdigest())


def get_token_components(token):
    """
    Decode and split the user supplied token
    :param token: user supplied token
    :return: the mail and signature value
    """
    mail = None
    signature = None
    if not token or token == "":
        return mail, signature
    if "|" not in token:
        return mail, signature
    values = token.split("|")
    try:
        mail = base64.b64decode(values[0]).decode()
        signature = values[1]
    except binascii.Error:
        return mail, signature
    except UnicodeDecodeError:
        return mail, signature
    except Exception:
        return mail, signature
    return mail, signature


def validate_token(token):
    """
    Test if the token is valid and proceed to password reset
    :param token: user supplied token
    :return: True if token is valid, False if not.
    """
    mail, signature = get_token_components(token)
    if not mail or not signature:
        return False
    test_token = create_token(mail)
    if test_token != token:
        return False
    return True


class Level3Handler(RequestHandler):
    def get(self):
        show_code = self.get_argument("code", default=None)
        reset_token = self.get_argument("t", default=None)

        if config.level3_showcode and show_code:
            with open(__file__) as code:
                content = code.read()
                self.write("<pre>" + xhtml_escape(content) + "</pre>")
        elif reset_token:
            mail, signature = get_token_components(reset_token)
            if signature and not validate_token(reset_token):
                self.render("templates/error.html", message="Invalid data.")
            elif mail == config.admin_email:
                base_url = utils.get_cosmetic_url(self.request)
                self.render("templates/success.html",
                    message=config.level3_message,
                    next_challenge=base_url + config.level4_link
                )
            else:
                self.render("templates/error.html",
                            message="HoHo! You did trigger the password reset "
                                    "function, but for the wrong user.")
        else:
            self.render("templates/level.html", level="Level 3",
                        show_code=config.level3_showcode)

    def post(self):
        email = self.get_argument("email", default=None)
        if not email:
            self.send_error(400)
        elif email == config.admin_email:
            self.render("templates/error.html", message="Nice try ;)")
        else:
            reset_token = create_token(email)
            base_url = utils.get_cosmetic_url(self.request)
            reset_link = base_url + config.level3_link + "?t=" + reset_token
            self.render("templates/resetlink.html", resetlink=reset_link)