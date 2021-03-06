from todoist import TodoistAPI
from py_agent.credentials import get_credential
from py_agent.utils import listen_for
from py_agent.my_utils import todoist as t_utils


@listen_for({'event_type': ('==', 'new_pr_review')})
def add_pr_to_todoist(event=None, handler=None):
    todoist = TodoistAPI(get_credential('todoist_token'))
    todoist.sync()

    # review_project = t_utils.get_project_by_name(todoist, 'review requests')

    r = event.data
    title = 'PR'

    if r['base']['repo']['full_name'] == 'pulp/pulp_ansible':
        title = 'Pulp Ansible PR'

    todoist.items.add(
        '{} - {} [{} #{}]({})'.format(title, r['title'], r['base']['repo']['full_name'], r['number'], r['html_url']),
        # project_id=review_project['id'],
        # auto_reminder=True,
        # due={"string": "next workday at 9am"},
        # priority=4
    )

    # todo close todos for prs/issues that are no longer active
    todoist.commit()
