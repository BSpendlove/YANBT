def bad_json_response():
    return {
        "error": True,
        "reason": "Data must be valid JSON."
    }

def bad_token_response():
    return {
        "error": True,
        "reason": "Bad Token provided."
    }

def bad_auth_response():
    return {
        "error": True,
        "reason": "Bad Authentication provided."
    }

def error_response(error):
    return {
        "error": True,
        "reason": "Try/Except catched an Exception.",
        "exception_string": str(error)
    }

def message_response(data):
    return {
        "error": True,
        "reason": data
    }

def data_response(data):
    return {
        "error": False,
        "data": data
    }

def missing_field_response(field):
    return {
        "error": True,
        "reason": "Missing required field.",
        "missing_field": field
    }
