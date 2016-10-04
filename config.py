import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# OPENID_PROVIDERS = [
#     {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
#     {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
#     {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
#     {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
#     {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
#
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

MY_TOKEN = "ZTYyMzNjMmUtZmMzZC00MjZjLTkwODItZTA1NmMzMTg2MzM5YTJiM2NiZjgtN2Yz"
SPARK_PPL = "https://api.ciscospark.com/v1/people"
SPARK_ROOMS = "https://api.ciscospark.com/v1/rooms"
SPARK_MSG = "https://api.ciscospark.com/v1/messages"
