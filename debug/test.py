
from modules.database.db import SpecifiedDatabase
from modules.logentry.entry import LogEntryInitalize
from modules.eventManager.event import EventManager
from loguru import logger

import traceback

shared_db = SpecifiedDatabase("None")
shared_event = EventManager(shared_db)
shared_logs = LogEntryInitalize(shared_db, shared_event)

def run():
    try:
        shared_logs.log_event("VirtTest", "FIOJ")
    except Exception as error:
        logger.error("errof failure: {error}")
        traceback.print_exc()