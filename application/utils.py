from datetime import datetime


def is_valid_iso_date(date_str) -> bool:
    '''
    Attempt to parse the string into a datetime object. Returns "True" if the date is valid.
    '''
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        return True
    except ValueError:
        return False
