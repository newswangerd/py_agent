from py_agent.agent import Agent

from py_agent.jobs import github_notifications, todoist_reading_list
from py_agent.listeners import (
    add_issue_to_todoist,
    add_pr_to_todoist,
    add_article_to_dropbox,
    add_mention_to_todoist
)

import logging

logging.info("PyAgent is a GO")

agent = Agent()

agent.schedule.every(10).minutes.do(github_notifications, handler=agent.handler)
agent.schedule.every(30).minutes.do(todoist_reading_list, handler=agent.handler)

# Github
agent.add_listener(add_issue_to_todoist)
agent.add_listener(add_pr_to_todoist)
agent.add_listener(add_mention_to_todoist)

agent.add_listener(add_article_to_dropbox)

agent.go()