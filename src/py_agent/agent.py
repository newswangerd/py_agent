import os
import schedule
import time
import logging

from py_agent.db import init_db
from py_agent.event_handler import EventHandler

logging.basicConfig(level=logging.INFO)


class Agent:
    def __init__(self):
        db_path = os.environ.get('PY_AGENT_DB_PATH')
        if not db_path:
            db_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
        
        self.db_session = init_db(db_path)
        self.handler = EventHandler(self.db_session)
        self.schedule = schedule
    
    def add_listener(self, fn, match):
        self.handler.subscribe(fn, match)
    
    def go(self):
        logging.info('Starting agent')
        while True:
            try:
                self.schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                logging.info('Shutting down')
                schedule.clear()
                exit()
            except Exception:
                logging.error("Job failed", exc_info=True)

