from py_agent.db import Event
from datetime import datetime
import operator


class InvalidMatchObect(Exception):
    def __init__(self, message):
        self.message = message


class EventHandler:
    listeners = []
    OPERATORS = {
        '==': operator.eq,
        '!=': operator.ne,
        '<': operator.lt,
        '>': operator.gt,
        'in': operator.contains
    }

    def __init__(self, db_session):
        self.db_session = db_session
    

    def subscribe(self, fn, log_match):
        self.listeners.append({'job': fn, 'match': log_match})

    def publish(self, event_type, identifier, data):
        # check if event exists
        if(self.db_session.query(Event).filter_by(identifier=identifier).scalar() is None):
            e = Event(
                created=datetime.now(), 
                event_type=event_type,
                identifier=identifier,
                data=data
            )
            self.db_session.add(e)
            self.db_session.commit()

            print(e)
            self._emit_event(e)

    def query(self, match):
        pass

    def _emit_event(self, event):
        for listener in self.listeners:
            if self._is_match(event, listener['match']):
                listener['job'](handler=self, event=event)

    def _is_match(self, event, match):
        if not self._is_valid_match_object(match):
            raise InvalidMatchObect(str(match) + ' is not a valid match object')

        matched = True
        # call a property so the object is initialized and can be loaded into a dict
        event.id
        event_dict = event.__dict__

        for key in match:
            val1 = event_dict[key]
            op, val2 = match[key]
            if not self.OPERATORS[op](val1, val2):
                matched = False
                break
        
        return matched
            
    # example match object
    # {
    #  'identifier': ('!=', '123'),
    #  'event_type': ('in', ['gh', 'gh_t']),
    #  'created': ('<', datetime.now())
    # }
    def _is_valid_match_object(self, match):
        keys = ['identifier', 'created', 'event_type']
        for key in match:
            if key not in keys:
                return False
            if match[key][0] not in self.OPERATORS:
                return False
        
        return True