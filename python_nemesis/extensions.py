from flask_keystone import FlaskKeystone
from flask_oslolog import OsloLog
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
log = OsloLog()
keystone = FlaskKeystone()
