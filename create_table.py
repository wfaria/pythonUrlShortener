"""
Small class to create the table necessary for this project.
"""

from flask import Flask
from shortened_url_data import shortenedUrlDb

app = Flask(__name__);
app.config.from_pyfile('config.py');
shortenedUrlDb.init_app(app);
shortenedUrlDb.create_all(app = app);