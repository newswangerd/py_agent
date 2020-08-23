# py_agent

This is my personal automation project. It simply schedules a set of python jobs to run intermittently to do things for me like check the weather and add tasks to my todo list.

## Develop

Set up dev environment
- `pip install -r requirments.txt`
- `pip install -e .`

## Deploy

`ansible-playbook deploy.yaml -i inventory`