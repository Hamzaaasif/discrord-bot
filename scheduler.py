from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger
import datetime
from google_sheet_script import read_google_sheet

def schedule_job():
    schedule_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"Scheduling the job at {schedule_time}")
    read_google_sheet()
    
    
if __name__ == "__main__":
    logger.info("Starting the scheduler")
    scheduler = BlockingScheduler()
    scheduler.add_job(schedule_job, 'interval', seconds=10)
    scheduler.start()
        
