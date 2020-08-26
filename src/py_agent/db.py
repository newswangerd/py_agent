from sqlalchemy import create_engine, Column, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(types.Integer, primary_key=True)
    created = Column(types.DateTime)
    event_type = Column(types.String)

    # used to check if the event is a duplicate or not. This could be a
    # hash of the data or some unique ID from an API
    identifier = Column(types.String, unique=True)

    data = Column(types.PickleType)

    def __repr__(self):
        return f'{self.event_type}: {self.identifier}'

def init_db(filename=':memory:'):
    engine = create_engine('sqlite:///' + filename, echo=False)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return Session()

# session = init_db()
# testd = Event(created=datetime.now(), event_type='test', identifier='abc', data={'hello': 'world'})
# session.add(testd)
# e = session.query(Event).filter_by(identifier='abc', event_type='test').first()

# print (e.__dict__)
# print (e.data['hello'])