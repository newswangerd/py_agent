from todoist import TodoistAPI
from py_agent.credentials import get_credential

def add_pr_to_todoist(event=None, handler=None):
    todoist = TodoistAPI(get_credential('todoist_token'))
    todoist.sync()

    review_project = None

    for p in todoist.state['projects']:
        if p['name'].lower() == 'review requests':
            review_project = p
            break
    
    r = event.data
    todoist.items.add(
        '{} [{} #{}]({})'.format(r.title, r.base.repo.full_name, r.number , r.html_url),
        project_id=review_project['id'],
        auto_reminder=True,
        due={"string": "next workday at 9am"},
        priority=4
    )

    # todo close todos for prs/issues that are no longer active
    todoist.commit()   