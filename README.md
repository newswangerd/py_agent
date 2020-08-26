# py_agent

This is my personal automation project. It simply schedules a set of python jobs to run intermittently to do things for me like check the weather and add tasks to my todo list.

## Architecture

There are two key concepts in py_agent

- Agents are jobs that run periodically and publish events when something happens. An example of this is a job that checks github notifications every 10 minutes and publishes events whenever new issues are assigned to the user.
- Listeners listen to events and perform some action when the event is issued. An example of this is a listener that watches events for new pull requests on github and adds them as tasks in Todoist.

This model allows for separation of concerns between scripts that fetch data and scripts that act on data. Because of this, adding new logic to perform actions on incoming data doesn't require changing the core agent script. Additionally, since actions are performed on event propagation, events can be saved to a database and use to deduplicate new incoming events so that listeners are only triggered when something changes as well as saved for later analyses.

Here's an example detailing how to set up agents and listeners:

```
from py_agent.agent import Agent

from py_agent.jobs import github_notifications
from py_agent.listeners import add_issue_to_todoist, add_pr_to_todoist

agent = Agent()
task = agent.create_partial(github_notifications)

agent.schedule.every(10).seconds.do(task)

agent.add_listener(add_issue_to_todoist, {'event_type': ('==', 'new_issue_assigned')})
agent.add_listener(add_pr_to_todoist, {'event_type': ('==', 'new_pr_review')})

agent.go()
```

## Develop

Set up dev environment

- `pip install -r requirments.txt`
- `pip install -e .`

## Deploy

`ansible-playbook deploy.yaml -i inventory`