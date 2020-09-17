import os
import time
import logging

from py_agent.db import init_db
from py_agent.event_handler import EventHandler
from py_agent.scheduler import SafeScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s.%(funcName)s(): %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class Agent:
    def __init__(self, db_path=None):
        if not db_path:
            db_path = os.environ.get('PY_AGENT_DB_PATH')
        if not db_path:
            db_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
        
        self.db_session = init_db(db_path)
        self.handler = EventHandler(self.db_session)
        self.schedule = SafeScheduler()
    
    def add_listener(self, fn, match=None):
        self.handler.subscribe(fn, match)
    
    def go(self):
        logging.info('Starting agent')
        while True:
            self.schedule.run_pending()
            time.sleep(1)

