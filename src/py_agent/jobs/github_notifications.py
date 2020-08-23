from github import Github
from todoist import TodoistAPI
import logging

from py_agent.credentials import get_credential

def github_notifications():
    gtoken = get_credential('github_token')
    todoist_token = get_credential('todoist_token')

    g = Github(gtoken)

    user = g.get_user()

    # all=False is broken
    # waiting for https://github.com/PyGithub/PyGithub/issues/1671
    notifications = user.get_notifications(all=False)

    requested_reviews = []
    assigned_issues = []
    added_notifications = []

    logging.info('Checking for new github notifications...')
    for n in notifications:
        if n.unread:
            if n.reason == 'review_requested':
                pr = n.get_pull_request()
                requested_reviews.append(pr)
                added_notifications.append(n)
            if n.reason == 'assign':
                issue = n.get_issue()
                assigned_issues.append(issue)
                added_notifications.append(n)

    if len(added_notifications) > 0:
        logging.info('Adding {} new tasks to todoist')
        todoist = TodoistAPI(todoist_token)
        todoist.sync()

        review_project = None
        issue_project = None

        for p in todoist.state['projects']:
            if p['name'].lower() == 'review requests':
                review_project = p
            if p['name'].lower() == 'issues':
                issue_project = p
        
        for r in requested_reviews:
            todoist.items.add(
                '{} [{} #{}]({})'.format(r.title, r.base.repo.full_name, r.number , r.html_url),
                project_id=review_project['id'],
                auto_reminder=True,
                due={"string": "next workday at 9am"},
                priority=4
            )

        for r in assigned_issues:
            todoist.items.add(
                '{} [#{}]({})'.format(r.title, r.number , r.html_url),
                project_id=issue_project['id'],
            )

        # todo close todos for prs/issues that are no longer active
        todoist.commit()    

        logging.info("Marking notifications as read")
        for n in added_notifications:
            n.mark_as_read()
    else:
        logging.info("No new notifications found")