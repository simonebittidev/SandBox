from datetime import datetime

def get_flat_date(date=None):
    # Get the current date
    if not date:
        date = datetime.now()

    # Format the date as YYYYMMDD
    flat_date = date.strftime('%Y%m%d')
    return flat_date

def get_readable_date(date=None):
    # Get the current date
    if not date:
        date = datetime.now()
    # Format the date as YYYYMMDD
    rdate = date.strftime('%d/%m/%Y')
    return rdate