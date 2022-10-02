import moment
import datetime
from loguru import logger

def get_hour():
    logger.info("Getting the time zone")
    now = datetime.datetime.now()
    local_now = now.astimezone()
    local_tz = local_now.tzinfo
    local_tzname = local_tz.tzname(local_now)
    logger.debug(f"machine time zone: {local_tzname}")

    machine_time = moment.utcnow().timezone(local_tzname).date
    logger.debug(f"machine time: {machine_time}")
    local_time = moment.utcnow().timezone("CET").date
    logger.debug(f"local time in CET: {local_time}")

    machine_time_zone = int(machine_time.strftime("%z"))
    local_time_zone = int(local_time.strftime("%z"))

    hour_diff = (machine_time_zone - local_time_zone)/100
    logger.debug(f"hour difference: {hour_diff}")
    hour_to_run_cron = 3
    new_time = hour_to_run_cron + hour_diff

    if(new_time == 24):
        new_time = 0
    elif(new_time > 24):
        new_time -= 24
    elif(new_time < 0):
        new_time = 24 + new_time
    logger.info(f"Hour to run cron: {int(new_time)}")
    return int(new_time)
