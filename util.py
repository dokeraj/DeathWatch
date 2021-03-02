def safeCast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def safeCastBool(val, default=False):
    try:
        return str(val).lower() in ['true', '1', 'y', 'yes']
    except Exception as e:
        return default
