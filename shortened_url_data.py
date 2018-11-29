from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

# Default database connection instance. Initialize this before using this method.
shortenedUrlDb = SQLAlchemy();

# Indicates when we fail to insert an URL because it already exists.
INVALID_ID = -1;

# Database methods
class ShortenedUrl(shortenedUrlDb.Model):
    """
    This class abstracts a shortened url entry on the database.
    It contains the id, which is generated automatically by the database system,
    the base URL and the date when it was created.

    The id will be encoded by this server and sent to the user as the
    shortened URL id.
    """
    id = shortenedUrlDb.Column(shortenedUrlDb.Integer, primary_key=True);
    url = shortenedUrlDb.Column(shortenedUrlDb.String(80), index=True, unique=True, nullable=False);
    date = shortenedUrlDb.Column(shortenedUrlDb.DateTime, default=datetime.utcnow);

def get_shortened_url_by_id(id):
    """
    Gets the first shortened URL from the database with the
    parameter id, note that the id should be using the usual decimal numeral system.
    
    If there isn't an object with that id, it returns None.
    """
    return ShortenedUrl.query.filter_by(id = id).first();
    
def get_shortened_url_by_url(url_string):
    """
    Gets the first shortened URL from the database with the
    the url equals to the parameter string.
    
    If there isn't an object with that id, it returns None.
    """
    return ShortenedUrl.query.filter_by(url = url_string).first();
 
def publish_url(url_string):
    """
    It creates a new shortened url object and inserts it in the database.
    The database will generate its id, which will be returned by this method.
    
    If the URL is already on the database, it will return INVALID_ID.
    """
    try:
        urlEntry = ShortenedUrl(url = url_string);
        shortenedUrlDb.session.add(urlEntry);
        shortenedUrlDb.session.commit();    
        
    except exc.IntegrityError as e:
        # Repeated URLs aren't allowed, we return -1 to sign it to the caller.
        shortenedUrlDb.session().rollback();
        return INVALID_ID;
        
    return urlEntry.id;