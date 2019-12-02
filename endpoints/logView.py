# Log View Endpoint

from modules.database.db import SpecifiedDatabase
from modules.logentry.entry import LogEntryInitalize
from loguru import logger
from helpers.status import failure

logger.remove()
logger.add("logs.log")


sharedSpecDB = SpecifiedDatabase("None")
sharedLog = LogEntryInitalize(sharedSpecDB)

class LoadLogsTest:
    def on_get(self, req, resp):
        resp.media = {
            "object": str(sharedSpecDB)
        }
class LoadMostRecentLog:
    def on_get(self, req, resp):
        check_for_force_flag = req.get_param("flag", default=None)
        
        if check_for_force_flag == None:
            current_logs = sharedLog.get_logs()

            # TODO: Func to only get one.

            resp.media = current_logs['output'][-1]

class LoadLogs:
    def on_get(self, req, resp):
        try:
            current_logs = sharedLog.get_logs()
            if len(current_logs['output']) > 10:
                
                # Check for force flag
                check_for_force_flag = req.get_param("flag", default=None)
                
                if check_for_force_flag != None:
                    specified_flag = check_for_force_flag

                    # Switch Cases

                    current_statements = {
                        "show-all": current_logs,
                        "none": failure("Too many logs to show, please specify correct flag, or use pages endpoint.")
                    }

                    resp.media = current_statements.get(specified_flag, failure("Invalid Flag. Please use correct flag."))
                else:
                    resp.media = failure("Too Many logs to show, please specify correct flags, or use pages endpoint.")
            else:
                resp.media = current_logs
        except Exception as error:
            logger.error(f"Error on LoadLogs: {error}")
            resp.media = failure("Something fucked up.")
class LoadEvents:
    def on_get(self, req, resp):
        resp.media = {
            "events": sharedLog.events
        }


def initalize(api_object):
    api_object.add_route("/logs/all/load", LoadLogs)
    api_object.add_route("/logs/events/all", LoadEvents)
    api_object.add_route("/logs/all/load/test", LoadLogsTest)
    return api_object