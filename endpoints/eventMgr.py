# Event manager

print("Initalizing Event Manager")

from modules.eventManager.event import EventManager, Event
from helpers.status import success, failure
from helpers.paramverify import verify_params

class CurrentEventsResource:
    def __init__(self, eventMgr):
        self.eventMgr = eventMgr

    def on_get(self, req, resp):
        resp.media = {
            "events": [event.to_dict for event in self.eventMgr.eventMemory]
        }

class NewEventResouce:
    def __init__(self, eventMgr):
        self.eventMgr = eventMgr

    def on_get(self, req, resp):
        resp.media = failure("endpoint not supported.")

    def on_post(self, req, resp):
        params = ['eventName', 'eventLevel']
        param_check = verify_params(params, req)
        if param_check['status'] == 0:
            try:
                params = param_check['paramsProvided']
                try:
                    cur_event = Event(params['eventName'], params['eventLevel'])
                    resp.media = {
                        "result": self.eventMgr.add_event(cur_event)
                    }
                except Exception as error:
                    resp.media = failure("invalid event configuration.")
            except Exception as error:
                resp.media = failure("complete failure")
        else:
            resp.media = param_check
class EventLoadReloadResouce:
    def __init__(self, eventMgr):
        self.eventMgr = eventMgr

    def on_get(self, req, resp):
        resp.media = self.eventMgr.reload_events()
