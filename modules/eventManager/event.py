# Event Manager

#from modules.database.db import SpecifiedDatabase
import hashlib


current_events = {
    0: "INFORMATION",
    1: "CRITICAL",
    2: "HANDLED ERROR"
}


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
        

"""
class EventManager(object):
    def __init__(self, database):
        self._current_specifiedDb = SpecifiedDatabase("None"):
        try:
            self._eventDb_raw = self._current_specifiedDb.current_db
            self.event_db = self._eventDb_raw.events

            try:
                raw_events = [index.to_dict() for index.event_db.list_indexes()]
                self.events = []
                for event in raw_events:
                    if event['level']
"""
                