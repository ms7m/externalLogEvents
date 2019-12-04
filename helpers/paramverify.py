


def verify_params(param_list, request_object):
    param_verification = {}
    for param in param_list:
        param_verification[param] = False
    
    for param in param_list:
        current_param = request_object.get_param(param)
        if current_param:
            param_verification[param] = current_param
        else:
            param_verification[param] = False

    for param in param_verification:
        if param_verification[param] == False:
            return {
                "status": 1,
                "message": f"Invalid Params. {param} is missing."
            }
        else:
            continue
    return {
        'status': 0,
        'message': f"All params accounted for.",
        'paramsSupplied': param_list,
        'paramsProvided': param_verification
    }