
# Abstracted and higher level of the PyMongo object.
# Usually reserved for starting up for the first time



import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from errors.database import *
from loguru import logger
import traceback

class SpecifiedDatabase(object):
    def __init__(self, database_name, authentication_object=None):
        self._unverified_database_name = database_name
        self.authentication = authentication_object

        try:
            if isinstance(self._unverified_database_name, str) == True:
                # Load a MongoDB from auth settings
                try:
                    self._currentDatabase = MongoClient()
                    

                    try:
                        # Test connection to Mongo
                        # Do this by setting the default
                        # connection time to 1ms. (30s def)
                        # Raise error if failure.

                        try:
                            self._currentDatabase.serverSelectionTimeoutMS = 1
                            self._currentDatabase.server_info() # force connection on a request as the
                                                 # connect=True parameter of MongoClient seems
                                                 # to be useless here 
                            self._currentDatabase.serverSelectionTimeoutMS = 30000
                        except ServerSelectionTimeoutError:
                            raise ConnectionFaliureMongo
                        except Exception as error:
                            logger.error("Error other than a connection timeout for MongoConn Test: {error}")
                            logger.debug(f"{traceback.print_exc()}")
                            raise Exception(f"Unhandled Error: {error}")

                    except Exception as error:
                        logger.error("Error on outer block for MongoConn Test: {error}")
                        logger.debug(f"{traceback.print_exc()}")
                        raise ErrorCreationMongoDB
                
                    # TODO: Don't Forget to change this :)
                
                    self.current_db = self._currentDatabase.logEvents
                    self.db = self.current_db[f'{datetime.datetime.now().strftime("%Y-%m-%d")}']
                except Exception as error:
                    logger.error("Unable to initalize MongoDB into a class Var. {error}")
                    logger.debug(f"{traceback.print_exc()}")
                    raise ErrorCreationMongoDB

            else:
                logger.error(f"Improper Param supplied to to Db_name: {type(self._unverified_database_name)} was supplied.")
                raise ValueError("Improper Param supplied.")
        except Exception as error:
            logger.error(f"Error on Outerblock Initalize: SDB: {error}")
            logger.debug(f"{traceback.print_exc()}")
    
    
    def push_new_index(self, name="date"):
        try:
            self.db.create_index(name)
            logger.info("Attempted addition of index.")
        except Exception as error:
            raise IndexCreationError
    
    def verify_indexes(self, force=False):

        # Check if we cached this yet.

        if force == False:
            try:
                check = self.index_returned
                logger.debug("Cached!")

                if len(check) == 0:
                    pass
                else:
                    return check
            except AttributeError:
                pass
        else:
            pass

        
        try:
            raw_indexes = [index.to_dict() for index in self.db.list_indexes()]
        except Exception as error:
            logger.error(f"Unable to grab index for mongo: {error}")
            logger.debug(f"{traceback.print_exc()}")
            raise IndexGrabError

        try:

            current_index_name = self.current_db.name 
            current_default_index = {'_id_': {'v': 2, 'key': [('_id', 1)], 'ns': f'{current_index_name}.test'}}
            
            copiedIndexList = raw_indexes.copy()
            parsedIndexList = []

            for index in copiedIndexList:
                if index == current_default_index:
                    logger.debug("ignoring default index.")
                    continue
                else:
                    parsedIndexList.append(index)
            
            # Cache this for later. 
            # TODO: Use timestamp provided to determine if it's too old.
            
            self.index_returned = {
                'metadata': {
                    "timestamp": datetime.datetime.now()
                },
                'indexes': parsedIndexList
            }
            return self.index_returned
        except Exception as error:
            logger.error("Error on index list parse logic: {error}")
            logger.debug(f"{traceback.print_exc()}")
            raise Exception("Error on index list parse logic.")
                
        
                    