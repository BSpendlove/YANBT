def valdiate_required_fields(fields, data):
    if not data:
        return False

    for entry in fields:
        if not entry in data:
            return False, entry

    return True, None
