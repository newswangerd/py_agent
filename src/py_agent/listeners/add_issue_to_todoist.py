from todoist import TodoistAPI
from py_agent.credentials import get_credential
from py_agent.utils import listen_for

@listen_for({'event_type': ('==', 'new_issue_assigned')})
def add_issue_to_todoist(event=None, handler=None):
    todoist = TodoistAPI(get_credential('todoist_token'))
    todoist.sync()

    issue_project = None

    for p in todoist.state['projects']:
        if p['name'].lower() == 'issues':
            issue_project = p
            break
    
    r = event.data
    todoist.items.add(
        '{} [#{}]({})'.format(r['title'], r['number'] , r['html_url']),
        project_id=issue_project['id'],
    )

    # todo close todos for prs/issues that are no longer active
    todoist.commit()