import schedule
import time
import logging

from py_agent.jobs import github_notifications

logging.basicConfig(level=logging.INFO)

logging.info('Starting scheduler')
schedule.every(10).minutes.do(github_notifications)

while True:
    try:
        schedule.run_pending()
        time.sleep(100)
    except KeyboardInterrupt:
        logging.info('Shutting down')
        schedule.clear()
        exit()
    except Exception:
        logging.error("Job failed", exc_info=True)
