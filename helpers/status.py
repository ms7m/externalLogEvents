# Status Helpers


def success(custom_message, extra_provs=None):

    if extra_provs == None:
        return {
            "status": 0,
            "message": custom_message
        }
    else:
        return {
            "status": 0,
            "message": custom_message,
            "output": extra_provs
        }


def failure(custom_message, raiseCustomError=False):
    return {
        "status": 1,
        "message": custom_message
    }