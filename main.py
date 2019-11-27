# Load API

import falcon
from loguru import logger
from waitress import serve
from endpoints.logView import *
# import oswald

from modules.database.db import SpecifiedDatabase
from modules.logentry.entry import LogEntryInitalize

#logger.remove()
#logger.add("logs.log")

api = falcon.API()

api.add_route("/logs/all/load", LoadLogs)
api.add_route("/logs/events/all", LoadEvents)
api.add_route("/logs/all/load/test", LoadLogsTest)
serve(api)