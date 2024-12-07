from datetime import datetime

def get_flat_date():
    # Get the current date
    current_date = datetime.now()
    # Format the date as YYYYMMDD
    flat_date = current_date.strftime('%Y%m%d')
    return flat_date

def get_readable_date():
    # Get the current date
    current_date = datetime.now()
    # Format the date as YYYYMMDD
    rdate = current_date.strftime('%d/%m/%Y')
    return rdate