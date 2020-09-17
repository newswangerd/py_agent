import os
import argparse
from importlib import import_module

from py_agent.agent import Agent
from py_agent import jobs
from py_agent import listeners

def pars_args():
    parser = argparse.ArgumentParser(description='Test jobs and listeners.')
    parser.add_argument('--listener', '-l', type=str, dest='listener', help='Code that listens for events.')
    parser.add_argument('--job', '-j', type=str, dest='job', help='Job to execute.')
    parser.add_argument('--emit-type', '-t', type=str, dest='emit_type', help='Emits any events that match the givent type.')
    parser.add_argument('--emit-id', '-id', type=str, dest='emit_id', help='Emits any events that match the givent id.')
    parser.add_argument('-m', dest='memory_db', action='store_true', help='Use an in memory db.')
    parser.add_argument('--rm-db', '-r', dest='re_init_db', action='store_true', help='Remove drop the database before running anything.')
    parser.add_argument('--db-file', dest='db_file', type=str, help='Specify a database file to use.')

    return parser.parse_args()


#  Borrowed from django https://github.com/django/django/blob/master/django/utils/module_loading.py
def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path)

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        )


def main():
    args = pars_args()

    listener = args.listener
    job = args.job
    memory_db = args.memory_db
    re_init_db = args.re_init_db
    emit_type = args.emit_type
    emit_id = args.emit_id
    db_path = args.db_file

    if not db_path:
        db_path = os.path.join(os.path.dirname(__file__), 'test_data.sqlite')

    agent = None

    if re_init_db:
        if args.db_file:
            print ("--rm-db and --db-file are mutually exclusive to avoid accidental data loss. Ignore --rm-db")
        else:
            os.remove(db_path)

    if memory_db:
        agent = Agent(':memory:')
    else:
        agent = Agent(db_path)

    if listener:
        l_func = import_string(listener)
        agent.add_listener(l_func)

    events = []

    if job:
        j_func = import_string(job)
        j_func(handler=agent.handler)

    if emit_type:
        events.extend(agent.handler.query_events({'event_type': ('==', emit_type)}))

    if emit_id:
        events.extend(agent.handler.query_events({'identifier': ('==', emit_id)}))

    for e in events:
        agent.handler._emit_event(e)

if __name__ == '__main__':
    main()