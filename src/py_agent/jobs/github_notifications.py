from github import Github
from todoist import TodoistAPI
import logging
import json

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
                try:
                    pr = n.get_pull_request()
                    handler.publish('new_pr_review', f'pr_review-{pr.id}', pr._rawData)
                except:
                    logging.error(f'Could not retrieve pr at {n.subject.url}')
                added_notifications.append(n)

            if n.reason == 'subscribed':
                try:
                    if n.subject.type == 'PullRequest' and n.repository.full_name == 'pulp/pulp_ansible':
                        pr = n.get_pull_request()
                        handler.publish('new_pr_review', f'pr_review-{pr.id}', pr._rawData)
                except:
                    logging.error(f'Failed to retrieve mention {n.subject.type} at {n.subject.url}')

                added_notifications.append(n)

            elif n.reason == 'assign':
                try:
                    issue = n.get_issue()
                    handler.publish('new_issue_assigned', f'issue_assigned-{issue.id}', issue._rawData)
                except:
                    logging.error(f'Could not retrieve issue at {n.subject.url}')
                added_notifications.append(n)

            elif n.reason == 'mention':
                try:
                    if n.subject.type == 'Issue':
                        issue = n.get_issue()
                        handler.publish('new_github_at_mention', f'github_at_mention-{n.id}',
                            {'title': issue.title, 'url': issue.html_url, 'number': issue.number})
                    if n.subject.type == 'PullRequest':
                        pr = n.get_pull_request()
                        handler.publish('new_github_at_mention', f'github_at_mention-{n.id}',
                            {'title': pr.title, 'url': pr.html_url, 'number': pr.number})
                except:
                    logging.error(f'Failed to retrieve mention {n.subject.type} at {n.subject.url}')

                added_notifications.append(n)

    # if len(added_notifications) > 0:
    #     logging.info("Marking notifications as read")
    #     for n in added_notifications:
    #         n.mark_as_read()
    else:
        logging.info("No new notifications found")
