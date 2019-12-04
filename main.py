# Load API

import falcon
from loguru import logger
from waitress import serve
from endpoints.logView import *
from endpoints.eventMgr import *
# import oswald

from modules.database.db import SpecifiedDatabase
from modules.logentry.entry import LogEntryInitalize
from modules.eventManager.event import EventManager

#logger.remove()
#logger.add("logs.log")


def add_log_endpoints(api, shared_resources):
    
    api.add_route("/logs/all/load", LoadLogs(shared_resources['sharedLog']))
    api.add_route("/logs/test/object", LoadLogsTest(shared_resources['sharedDb']))
    api.add_route("/logs/latest/one", LoadMostRecentLog(shared_resources['sharedLog']))
    api.add_route("/log", LogMessage(shared_resources['sharedLog']))
    return api

def add_event_endpoints(api, shared_resources):
    api.add_route("/events/all", CurrentEventsResource(shared_resources['sharedEvent']))
    api.add_route("/events/all/reload", EventLoadReloadResouce(shared_resources['sharedEvent']))
    api.add_route("/events/new", NewEventResouce(shared_resources['sharedEvent']))

    return api


def initalize():
    print("Loading LogEventAPI.")

    shared_db = SpecifiedDatabase("None")
    shared_event = EventManager(shared_db)
    shared_logs = LogEntryInitalize(shared_db, shared_event)

    shared_resources = {
        "sharedDb": shared_db,
        "sharedLog": shared_logs,
        "sharedEvent": shared_event
    }

    api = falcon.API()

    endpoints = [
        add_log_endpoints,
        add_event_endpoints
    ]

    for endpoint in endpoints:
        cur_endpoint = endpoint
        cur_endpoint(api, shared_resources)

    return api


serve(initalize())