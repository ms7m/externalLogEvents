# Event Manager

from modules.database.db import SpecifiedDatabase
import hashlib
from loguru import logger
import traceback

current_events = {
    0: "INFORMATION",
    1: "CRITICAL",
    2: "HANDLED ERROR"
}


# Helpers
def verify_level(level):
    if level in [int(key) for key in current_events]:
        return True
    else:
        return False

def dict_to_event(dict_prov):
    return Event(dict_prov['eventName'], dict_prov['eventLevel'])


class Event(object):
    def __init__(self, event_name, event_level):

        __slots__ = ['event_name', 'event_level']

        self.event_name = event_name

        # Levels

        # Information - 0
        # Critical Errors - 1
        # Handled Errors - 2
        self._current_events = [int(key) for key in current_events]
        
        if isinstance(event_level, str) == True:
            try:
                self._unverified_level = int(event_level.strip())
            except ValueError:
                raise Exception(f"Did not supply a proper number from a string: {event_level}")
        else:
            if isinstance(event_level, int) == False:
                if isinstance(event_level, str) == True:
                    # ????
                    logger.debug("str escaped first check: stopping for safety.")
                    logger.debug(event_level)
                    raise Exception(f"SecError: Checks were escaped. {event_level}")
                else:
                    try:
                        self._unverified_level = int(event_level)
                    except ValueError:
                        raise Exception(f"Did not supply a proper number from a unknown type: {event_level}")

            else:
                self._unverified_level = int(event_level)

        if self._unverified_level in [0, 1, 2]:
            self.level = self._unverified_level
        else:
            raise Exception(f"Level provided {self._unverified_level} not valid.")

    @property
    def to_dict(self):
        if self.level:
            return {
                "eventName": self.event_name,
                "eventLevel": self.level
            }



class EventManager(object):
    def __init__(self, database):
        self._current_specifiedDb = database
        try:
            self._eventDb_raw = self._current_specifiedDb.current_db
            self.event_db = self._eventDb_raw.events

            self.eventMemory = []
            try:
                raw_events = [index for index in self.event_db.find()]
                self.events = []
                for event in raw_events:
                    logger.debug(event)
                    if verify_level(event['eventLevel']) == True:
                        self.eventMemory.append(
                            dict_to_event(event)
                        )
                    else:
                        logger.debug(f"warning: {event.get('eventName', '(NO EVENT NAME COULD BE FOUND)')} did not have a proper level.")
                        logger.debug(f"warning: {event.get('eventName', '(NO EVENT NAME COULD BE FOUND)')} level provided: {event.get('eventLevel', '(no level)')}")
                        continue
            except Exception as error:
                logger.error(f"error on loading events into eventMemory: {error}")
        except Exception as error:
            logger.error(f'complete failure on innerBlock for eventMemory: {error}')

    def reload_events(self):
        self.__init__(self._current_specifiedDb)
        return {
            "message": "action reloaded."
        }

    def add_event(self, event_object):
        try:
            logger.debug(f"new event action: {event_object.event_name}")
            try:
                action = self.event_db.insert_one(event_object.to_dict)
                logger.debug(f"new addition added: {event_object.event_name} with level {event_object.level} {current_events[event_object.level]} --> {action.inserted_id}")
                return True
            except Exception as error:
                logger.error(f"Unable to add event. {error}")
                try:
                    logger.debug(f"eventObject provided: {type(event_object)}")
                    return False
                except Exception as error:
                    logger.error("error on debugging event object.")
                    return False
        except Exception as error:
            logger.error(f"complete failure on either inner object: {error}")
            return False