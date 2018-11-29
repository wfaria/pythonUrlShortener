from enum import Enum

class LogType(Enum):
    """
    Log type enumerator to let us handle log messages according to
    their severity.
    """
    INFO = 0
    ALERT = 1
    ERROR = 2    

class Logger:
    """
    Small class to simulate an object able to store log messages
    in another database like Elasticsearch.
    
    Here we just print the messages on the console.
    """
    def __init__(self, source):
        self.source = source;

    def write_message(self, type, message):
        # We could store this message in other place, like Elasticsearch.
        print("message type = '{0}', message = '{1}'".format(type, message));