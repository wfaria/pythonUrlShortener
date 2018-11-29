"""
Main server file. Contains the HTTP request handlers to
access and create shortened URLs.
"""

# Library imports.
from datetime import datetime
from flask import abort, Flask, jsonify, make_response, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException

# Local files imports.
from logger import Logger, LogType
from base_converter import BaseConverter
from shortened_url_data import *
from url_utils import validate_url

# Constants.
BASE_SYMBOLS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
SERVICE_URL = "http://127.0.0.1:8000";

# Initializing flask app with database configs.
app = Flask(__name__);
app.config.from_pyfile('config.py');

# This one is created on shortened_url_data.py.
shortenedUrlDb.init_app(app);

# Initializing local helper classes.
baseConverter = BaseConverter(BASE_SYMBOLS);
log = Logger("url_shorter");
   
def create_error_response(msg, code):
    """
    It creates a custom JSON response for exceptional cases.
    """
    return make_response(jsonify({'error': msg}), code);
          
@app.errorhandler(400)
def bad_request(error):
    """
    Default handler for bad request cases.
    """
    return create_error_response('Bad Request', 400);
       
@app.errorhandler(404)
def not_found(error):
    """
    Default handler for not found cases.
    """
    return create_error_response('Not Found', 404);

@app.errorhandler(500)
def bad_request(error):
    """
    Default handler for internal server error cases.
    """
    return create_error_response('Internal Server Error', 500);

@app.route('/shorten_url', methods=['POST'])
def reduce_url(): 
    """
    Route handler for POST request to shorten an URL.
    The user needs to send a JSON object with a valid url in
    a field called "url" to this one work property. If everything
    is OK it will return a JSON object containing an URL to the shortened url
    in our server.
    """   
    try:
        if (not request.json or not 'url' in request.json):
            abort(create_error_response("The POST message doesn't contain a JSON object with an 'url' string field.", 400));
        
        requestUrl = request.json['url'];

        # We only validate the URL's format.
        # We do not check the URL access here because it can be offline 
        # now but online in the future or vice-versa.
        validatedUrl = validate_url(requestUrl);
        if (validatedUrl is None):
            errorMsg = "The request url '{0}' field has an invalid URL format.".format(requestUrl);
            abort(create_error_response(errorMsg, 400));
        
        urlId = publish_url(validatedUrl);
        if (urlId == INVALID_ID):
            # The publish method failed because the URL is already on the database.
            # We will search for it and return its id.
            shortenedUrl = get_shortened_url_by_url(validatedUrl);
            if (shortenedUrl is None):
                # We didn't find what should exist there, return server failure.
                errorMsg = "Failed to find shortened_url for URL which should be stored on database. URL '{0}'".format(validatedUrl);
                log.write_message(LogType.ERROR, errorMsg);
                abort(500);
                
            urlId = shortenedUrl.id;
               
        ret = { "shortened_url" : "{0}/{1}".format(SERVICE_URL, baseConverter.encode(urlId)) };    
        return jsonify(ret), 201
        
    except HTTPException as e:
    # Expected error generated by abort method, throw it to the Flask manager.
        raise e;
    except Exception as e:
        log.write_message(LogType.ERROR, "Fatal error on POST request: {0}".format(e));
        abort(500);
    
@app.route('/<string:url_suffix>', methods=['GET'])
def get_shortened_url(url_suffix):
    """
    Route handler to GET request to access shortened urls.
    It will parse the suffix, try to get the correspondent url in our database
    and, if the url exists, redirect the user to it.
    """
    try:
        try:
            # Try to convert the suffix into a valid database ID.
            # We could also use a Redis cache here to make things faster.
            decimalId = baseConverter.decode(url_suffix);
        except ValueError:
            abort(create_error_response("The suffix ID contains an invalid format or character.", 400));
            
        # Get the URL reference using its ID.
        shortenedUrl = get_shortened_url_by_id(decimalId);
        if (shortenedUrl is None):
            abort(create_error_response("The requested shortened url isn't present in our database.", 404));
            
        return redirect(shortenedUrl.url);
    
    except HTTPException as e:
        # Expected error generated by abort method, throw it to the Flask manager.
        raise e;
    except Exception as e:
        log.write_message(LogType.ERROR, "Fatal error on GET request: {0}".format(e));
        abort(500);
 
if __name__ == "__main__":
    app.run(threaded=True);