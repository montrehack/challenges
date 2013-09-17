__author__ = 'Gabriel Tremblay - initnull@gmail.com'

# Daemon settings
listen_port = 1337 
external_ip = "127.0.0.1"
admin_email = "admin@montrehack.ca"

# Easyness settings
level1_showcode=False
level2_showcode=True
level3_showcode=True
level4_showcode=True

# "Secret" links as variable so the levels can print their code without
# leaking the next level path.
level1_link = r"/b4d463e5-8f93-448c-af83-02eb2ba23873/"
level2_link = r"/64096cb9-80c9-4994-99c4-45251ec38b4c/"
level3_link = r"/70d684e8-f6c4-4081-b18c-4a71dda11816/"
level4_link = r"/0dbc7c23-01a4-498c-a4c4-02f0ed7ccb55/"

level4_secret_key = b"58ac401c-fc81-4e3e-9b1c-464e93cfaddb"

# Level messages
level1_message = "Base64 is not a strong _encryption_ algorithm!"
level2_message = "Make sure you don't use a weak key for your hmac!"
level3_message = "Even if you use strong and proven algorithms, make sure the implementation is right!"
level4_message = "PRNGs can be evil! (Under Windows, python's random.seed() is always based on system time!"
