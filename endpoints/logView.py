# Log View Endpoint

from modules.database.db import SpecifiedDatabase
from modules.logentry.entry import LogEntryInitalize
from loguru import logger

logger.remove()
logger.add("logs.log")


sharedSpecDB = SpecifiedDatabase("None")
sharedLog = LogEntryInitalize(sharedSpecDB)

class LoadLogsTest:
    def on_get(req, resp):
        resp.media = {
            "object": str(sharedSpecDB)
        }

class LoadLogs:
    def on_get(req, resp):
        resp.media = sharedLog.get_logs()

class LoadEvents:
    def on_get(req, resp):
        resp.media = {
            "events": sharedLog.events
        }

        
class Endpoint:
    API_ENDS = [
        {
            "endpoint": "/logs/all/load",
            "endpointObj": LoadLogsTest
        }
    ]