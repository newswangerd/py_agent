# PyAgent

This is my personal automation project. It simply schedules a set of python jobs to run intermittently to do things for me like check the weather and add tasks to my todo list.

## Architecture

There are two key concepts in py_agent

- Agents are jobs that run periodically and publish events when something happens. An example of this is a job that checks github notifications every 10 minutes and publishes events whenever new issues are assigned to the user.
- Listeners listen to events and perform some action when the event is issued. An example of this is a listener that watches events for new pull requests on github and adds them as tasks in Todoist.

This model allows for separation of concerns between scripts that fetch data and scripts that act on data. Because of this, adding new logic to perform actions on incoming data doesn't require changing the core agent script. Additionally, since actions are performed on event propagation, events can be saved to a database and use to deduplicate new incoming events so that listeners are only triggered when something changes as well as saved for later analyses.

## Example Agent

In this example `my_job` runs ever 2 seconds and emits an event of type `my_event_type` with a unique identifier of `123`. `my_listener` subscribes to all events that match the `my_event_type` event type and prints `event.data['payload']`.

```python
from py_agent.agent import Agent
from py_agent.utils import listen_for

agent = Agent()

def my_job(handler=None):
    print('running my job')
    handler.publish('my_event_type', '123', {'payload': 'hello world'})

@listen_for({'event_type': ('==', 'my_event_type')})
def my_listener(handler=None, event=None):
    print('running my listener')
    print(event.data['payload'])

agent.schedule.every(2).seconds.do(my_job, handler=agent.handler)

agent.add_listener(my_listener)

agent.go()
```

This is what this example looks like when it's run. Note that my listener only runs once. This is because events are de duplicated based on their `identifier`. Since `my_job` always emits events with `identifier=123`, it will only create one event.

```console
2020-08-27 23:03:19.480 INFO agent.go(): Starting agent
2020-08-27 23:03:21.484 INFO __init__.run(): Running job Every 2 seconds do my_job(handler=<py_agent.event_handler.EventHandler object at 0x1069348b0>) (last run: [never], next run: 2020-08-27 23:03:21)
running my job
2020-08-27 23:03:21.498 INFO event_handler.publish(): New event -> my_event_type: 123
running my listener
hello world
2020-08-27 23:03:23.500 INFO __init__.run(): Running job Every 2 seconds do my_job(handler=<py_agent.event_handler.EventHandler object at 0x1069348b0>) (last run: 2020-08-27 23:03:21, next run: 2020-08-27 23:03:23)
running my job
2020-08-27 23:03:25.504 INFO __init__.run(): Running job Every 2 seconds do my_job(handler=<py_agent.event_handler.EventHandler object at 0x1069348b0>) (last run: 2020-08-27 23:03:23, next run: 2020-08-27 23:03:25)
running my job
```

## Writing new agents

py_agent comes with an `agent-test` cli tool that can be used for developing new jobs and listeners.

example.py
```python
def my_job(handler=None):
    print('running my job')
    handler.publish('my_event_type', '123', {'payload': 'hello world'})

@listen_for({'event_type': ('==', 'my_event_type')})
def my_listener(handler=None, event=None):
    print('running my listener')
    print(event.data['payload'])
```

`agent-test` can persist events between runs. This allows for jobs to be created first, followed by listeners. This is handy in instances where jobs take a long time to run, or make large API request. To test the functions in `example.py`:

- `agent-test -j example.my_job` -> run a single job.
- `agent-test -j example.my_job -l example.my_listener` -> run a job and a listener.
- `agent-test -l example.my_listener -t my_event_type` -> run a listener and re-emit any events of type `my_event_type` from a previous run without using a job.
- `agent-test -r -j example.my_job` -> drop the database before running a job so that new events aren't de duplicated.
- `agent-test -m -j example.my_job -l example.my_listener` -> run a job and a listener using an in memory database so that events aren't saved between runs.

## Develop

Set up dev environment

- `pip install -r requirments.txt`
- `pip install -e .`

## Deploy

`ansible-playbook deploy.yaml -i inventory`