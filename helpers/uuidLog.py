# Database and other operations for generating a unique ID for a log.


from datetime import datetime
from pymongo imprt MongoClient


# helpers

def check_date_mongo(provided_mongoClient):
    try:
        for 

class GenerateUUID(object):
    def __init__(self, provided_uuid=None):
        self._unverified_uuid = provided_uuid
        if self._unverified_uuid == None:
            try