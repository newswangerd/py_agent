from todoist import TodoistAPI
from py_agent.credentials import get_credential
from py_agent.utils import listen_for
from py_agent.my_utils import todoist as t_utils

@listen_for({'event_type': ('==', 'new_github_at_mention')})
def add_mention_to_todoist(event=None, handler=None):
    todoist = TodoistAPI(get_credential('todoist_token'))
    todoist.sync()

    mention_project = t_utils.get_project_by_name(todoist, 'GH Mentions')

    r = event.data
    todoist.items.add(
        '{} [#{}]({})'.format(r['title'], r['number'] , r['url']),
        project_id=mention_project['id'],
        auto_reminder=True,
        due={"string": "next workday at 9am"},
        priority=4
    )

    # todo close todos for prs/issues that are no longer active
    todoist.commit()