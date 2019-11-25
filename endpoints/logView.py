# Log View Endpoint

from modules.database.db import SpecifiedDatabase
from modules.logentry.entry import LogEntryInitalize

class LoadAllLogs:
    def on_get(self, req, resp):
        jas = SpecifiedDatabase("ignore")
        crea = LogEntryInitalize(jas)
        logs = crea.get_logs()
        resp.media = logs


class LoadEvents:
    def on_get(self, req, resp):
        jas = 
class Endpoint:
    API_ENDS = [
        {
            "endpoint": "/logs/all/load",
            "endpointObj": LoadAllLogs()
        }
    ]