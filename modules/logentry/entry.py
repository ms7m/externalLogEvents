

# Entry to logs

from modules.database.db import SpecifiedDatabase
from errors.all import *
from errors.eventLogger import *
from datetime import datetime
from helpers.status import failure, success


from loguru import logger
import traceback


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d")

class LogEntryInitalize(object):
    def __init__(self, specDatabaseObject):
        if isinstance(specDatabaseObject, SpecifiedDatabase) == True:
            self.specDatabase = specDatabaseObject
        else:
            raise ImproperParam(f"SpecDB Object is not a proper object. {type(specDatabaseObject)} was returned.")
        
        try:
            self.current_database_to_log = self.specDatabase.db
        except Exception as error:
            logger.error("Error accessing .db var for SpecDatabase. {error}")
            logger.debug(f"specDatabase Vars: {dir(self.specDatabase)} {type(self.specDatabase)}")
            raise ImproperParam(f"SpecDB object is corrupted.")

        self.provided_events = []


    @property
    def events(self):
        return [provEvents['eventName'] for provEvents in self.provided_events]

    def new_event(self, event_name, event_params=None):
        try:
            if event_name.upper() in [provEvents['eventName'] for provEvents in self.provided_events]:
                return failure("event is already added.")
            else:
                self.provided_events.append(
                    {
                        "eventName": event_name.upper(),
                        "eventParams": event_params
                    }
                )
                return success("event was added")

        except Exception as error:
            logger.error(f"Error on event addition block: {error}")
            logger.debug(f"{traceback.print_exc()}")
            raise EventAdditionFailure
    
    def log_event(self, event_name, provided_params, text):
        try:
            if event_name.upper() in self.events:
                
                for event in self.provided_events:
                    if event['eventName'] == event_name.upper():
                        current_event_params = event['eventParams']
                    else:
                        continue
        except Exception as error:
            logger.error(f"Error on log event grabber block: {error}")
            logger.debug(f"{traceback.print_exc()}")
            return failure(f"Unable to log event grab with {event_name}")


        try:
            # TODO: Actually Implement params
            current_time = datetime.now()
            timestamp = datetime.timestamp(current_time)

            posted = self.current_database_to_log.insert_one({
                "logEvent": event_name.upper(),
                "eventTimestamp": timestamp,
                "logMessage": str(text)
            })
            return success(f"Logged Event at {timestamp} with id of {posted.inserted_id}")
        except Exception as error:
            logger.error(f"Error on inserting log into DB. {error}")
            logger.debug(f"{traceback.print_exc()}")
            raise FailedToAddLogError


    def get_logs(self, event=0):
        if event == 0:
            try:
                return success("Found.", [log for log in self.current_database_to_log.find()])
            except Exception as error:
                logger.error(f"Error on trying to get all logs. {error}")
                logger.debug(f"{traceback.print_exc()}")
                return failure("Unable to get results.")