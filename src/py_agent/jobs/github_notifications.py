from github import Github
from todoist import TodoistAPI
import logging

from py_agent.credentials import get_credential

def github_notifications(handler=None, event=None):
    gtoken = get_credential('github_token')

    g = Github(gtoken)
    user = g.get_user()

    # all=False is broken
    # waiting for https://github.com/PyGithub/PyGithub/issues/1671
    notifications = user.get_notifications(all=False)

    added_notifications = []

    logging.info('Checking for new github notifications...')
    for n in notifications:
        if n.unread:
            if n.reason == 'review_requested':
                pr = n.get_pull_request()
                handler.publish('new_pr_review', f'pr_review: {pr.id}', pr)
                added_notifications.append(n)

            if n.reason == 'assign':
                issue = n.get_issue()
                handler.publish('new_issue_assigned', f'issue_assigned: {issue.id}', issue)
                added_notifications.append(n)

    if len(added_notifications) > 0:
        logging.info("Marking notifications as read")
        for n in added_notifications:
            n.mark_as_read()
    else:
        logging.info("No new notifications found")