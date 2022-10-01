from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import datetime
import json
from loguru import logger
import time
from discord import start

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = './google-keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
json_file= open('keys.json')
input_data = json.load(json_file)

# The ID spreadsheet.
SPREADSHEET_ID = input_data['google_sheet_Id']

def update_send_status(sheet, status,row_number):
    logger.debug(f"Updating status of send message: {status}")
    range_name = "Sheet1!I{}:I{}".format(
        row_number, row_number+1)
    staus = [[status]]
    logger.info(f"Updating status")
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption="USER_ENTERED", body={"values": staus}).execute()
    logger.info("Sheet status updated successfully..")

def update_last_message_time(sheet, row_number):
    range_name = "Sheet1!G{}:G{}".format(
        row_number, row_number+1)
    curr_date_time = [[str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))]]
    logger.info(f"Updating last message time at google sheet")
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption="USER_ENTERED", body={"values": curr_date_time}).execute()
    update_send_status(sheet,'SUCCESS',row_number)
    logger.info("Sheet time updated successfully..")

def read_google_sheet():
    logger.info("Reading from google sheet")
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    google_sheet = sheet.values().get(spreadsheetId=SPREADSHEET_ID, 
                                      range="Sheet1!A:H").execute()
    sheet_data = google_sheet.get('values', [])
    sheet_data.pop(0)
    row_number = 1
    for data in sheet_data:
        row_number = row_number + 1
        isActive = data[4]
        logger.debug(f"Checking acitve status: {isActive}")
        if(isActive=='TRUE'):
            remaining_hours = int(data[-1])
            if(remaining_hours < 1):
                logger.debug(f"Sending message to {data[0]} channel")
                res_status = start(data[2], data[3])
                logger.debug(f"channel ID : {data[2]}, channel Message: {data[3]}")
                logger.debug(f"Message status from discord: {res_status}")
                if(res_status == 200):
                    update_last_message_time(sheet, row_number)
                else:
                    update_send_status(sheet,'FAILED',row_number)
                logger.info("Waiting 20 secs before sending another message...")
                time.sleep(20)
            else:
                logger.info("No message need to send, watching")
        else:
            logger.info(f"Ignoring non active channels: {data[2]}")
            