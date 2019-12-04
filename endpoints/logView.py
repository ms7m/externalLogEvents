# Log View Endpoint

from modules.database.db import SpecifiedDatabase
from modules.logentry.entry import LogEntryInitalize
from loguru import logger
from helpers.status import failure
from helpers.paramverify import verify_params
import traceback


logger.remove()
logger.add("logs.log")


class LoadLogsTest:
    def __init__(self, sharedSpecDB):
        self.sharedSpecDB = sharedSpecDB

    def on_get(self, req, resp):
        resp.media = {
            "object": str(self.sharedSpecDB)
        }
class LoadMostRecentLog:
    def __init__(self, sharedLog):
        self.sharedLog = sharedLog

    def on_get(self, req, resp):
        check_for_force_flag = req.get_param("flag", default=None)
        
        if check_for_force_flag == None:
            current_logs = self.sharedLog.get_logs()

            # TODO: Func to only get one.

            resp.media = current_logs['output'][-1]


class LogMessage:
    def __init__(self, sharedLog):
        self.sharedLog = sharedLog

    def on_post(self, req, resp):
        try:
            params_required = [
                "eventName",
                "logMessage"
            ]

            current_verification = verify_params(params_required, req)
            if current_verification['status'] == 0:
                try:
                    result = self.sharedLog.log_event(
                        current_verification['paramsProvided']['eventName'],
                        current_verification['paramsProvided']['logMessage']
                    )
                    resp.media = result
                except Exception as error:
                    logger.debug(error)
                    logger.debug(f"{traceback.print_exc()}")
                    resp.media = {
                        "status": "failure"
                    }
        except Exception as error:
            logger.debug(error)
            logger.debug(f"{traceback.print_exc()}")
            resp.media = {
                "status": "complete failure"
            }


class LoadLogs:
    def __init__(self, sharedLog):
        self.sharedLog = sharedLog


    def on_get(self, req, resp):
        try:
            current_logs = self.sharedLog.get_logs()
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

