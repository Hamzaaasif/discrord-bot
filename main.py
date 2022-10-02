from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger
import datetime
from google_sheet_script import read_google_sheet
from flask import Flask
from timeZone import get_hour

app = Flask(__name__)

@app.route('/')
def welcome():
    return "Server is running and scheduling..."

def schedule_job():
    schedule_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    logger.debug(f"Scheduling the job at {schedule_time}")
    read_google_sheet()
    
    
if __name__ == "__main__":
    logger.info("Starting the scheduler")
    scheduler = BlockingScheduler()
    scheduler.add_job(schedule_job, 'cron', hour=get_hour())
    scheduler.start()
    logger.info("Starting the flask server")
    app.run(host='0.0.0.0', port=8080)
        
