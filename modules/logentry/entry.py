

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
    def __init__(self, specDatabaseObject, sharedEventObject):
        self.sharedEventObject = sharedEventObject

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

        self.provided_events = [provEvents.to_dict['eventName'] for provEvents in self.sharedEventObject.eventMemory]


    @property
    def events(self):
        return [provEvents.to_dict['eventName'].upper() for provEvents in self.sharedEventObject.eventMemory]

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
    
    def log_event(self, event_name, text, provided_params=None):
        try:
            self.verified = False
            logger.debug(self.events)
            if event_name.upper() in self.events:
                
                for event in self.events:
                    if event.upper() == event_name.upper():
                        #current_event_params = event['eventParams']
                        self.verified = True
                        break
                    else:
                        continue
            else:
                logger.debug(f"Provided: {event_name.upper()} --> {self.events}")
                return failure("Event was not registered. Please register event.")
        except Exception as error:
            logger.error(f"Error on log event grabber block: {error}")
            logger.debug(f"{traceback.print_exc()}")
            return failure(f"Unable to log event grab with {event_name}")

        if self.verified == False:
            return failure(f"Event not registered. Please register event.")
        try:
            # TODO: Actually Implement params
            current_time = datetime.now()
            timestamp = datetime.timestamp(current_time)

            posted = self.current_database_to_log.insert_one({
                "eventName": event_name.upper(),
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
                return success("Found.", [{'id': str(log['_id']), 'event': log['eventName'], 'log': log['logMessage']} for log in self.current_database_to_log.find()])
            except Exception as error:
                logger.error(f"Error on trying to get all logs. {error}")
                logger.debug(f"{traceback.print_exc()}")
                return failure("Unable to get results.")