from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from io import BytesIO
from datetime import datetime
import requests

def get_flat_date(date=None):
    # Get the current date
    if not date:
        date = datetime.now()

    # Format the date as YYYYMMDD
    flat_date = date.strftime('%Y%m%d')
    return flat_date

def get_flat_date_hour(date=None):
    # Get the current date
    if not date:
        date = datetime.utcnow()

    # Format the date as YYYYMMDD
    flat_date = date.strftime('%Y%m%d_%H')
    return flat_date

def get_flat_date_full(date=None):
    # Get the current date
    if not date:
        date = datetime.now()

    # Format the date as YYYYMMDD
    flat_date = date.strftime('%Y%m%d_%H%M')
    return flat_date

def get_readable_date(date=None):
    # Get the current date
    if not date:
        date = datetime.now()
    # Format the date as YYYYMMDD
    rdate = date.strftime('%d/%m/%Y')
    return rdate

def parse_flat_date_hour(flat_date_hour):
    # Parse the flat date string (YYYYMMDD_HH) back into a datetime object
    return datetime.strptime(flat_date_hour, '%Y%m%d_%H')