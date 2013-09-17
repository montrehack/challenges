__author__ = 'Gabriel Tremblay - initnull@gmail.com'

from tornado.web import RequestHandler
from tornado.escape import xhtml_escape

import base64
import binascii
import config
import utils

def create_token(email):
    """
    Creates a password reset token
    :param email: User's email
    :return: a password reset token
    """
    token = base64.b64encode(email.encode())
    return token.decode()


def get_token_components(token):
    """
    Decode and split the user supplied token
    :param token: user supplied token
    :return: the reset mail
    """
    if not token or token == "":
        return None

    try:
        mail = base64.b64decode(token)
    except binascii.Error:
        return None
    except UnicodeDecodeError:
        return None
    return mail.decode()


class Level1Handler(RequestHandler):
    def get(self):
        show_code = self.get_argument("code", default=None)
        reset_token = self.get_argument("t", default=None)

        if config.level1_showcode and show_code:
            with open(__file__) as code:
                content = code.read()
                self.write("<pre>" + xhtml_escape(content) + "</pre>")
        elif reset_token:
            mail = get_token_components(reset_token)
            if mail == config.admin_email:
                base_url = utils.get_cosmetic_url(self.request)
                self.render("templates/success.html",
                    message=config.level1_message,
                    next_challenge=base_url + config.level2_link
                )
            else:
                self.render("templates/error.html",
                            message="HoHo! You did trigger the password reset "
                                    "function, but for the wrong user.")
        else:
            self.render("templates/level.html", level="Level 1",
                        show_code=config.level1_showcode)

    def post(self):
        email = self.get_argument("email", default=None)
        if not email:
            self.send_error(400)
        elif email == config.admin_email:
            self.render("templates/error.html", message="Nice try ;)")
        else:
            reset_token = create_token(email)
            base_url = utils.get_cosmetic_url(self.request)
            reset_link = base_url + config.level1_link + "?t=" + reset_token
            self.render("templates/resetlink.html", resetlink=reset_link)