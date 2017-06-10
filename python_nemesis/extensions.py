from flask_oslolog import OsloLog
from flask_sqlalchemy import SQLAlchemy
from flask_keystone import FlaskKeystone


db = SQLAlchemy()
log = OsloLog()
keystone = FlaskKeystone()
