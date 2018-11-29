"""
This file contains some configuration parameters
to access the database using the Sqlalchemy library.
"""

# Relative path SQLite database.
SQLALCHEMY_DATABASE_URI = "sqlite:///urls.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False