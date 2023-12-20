from sqlalchemy import Column, Date, ForeignKey,  String,  Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    id         = Column(String, primary_key=True)
    username   = Column(String(25), unique=True)
    password   = Column(String(255))
    office     = Column(String(25))
    is_staff   = Column(Boolean, default = False)
    create_at  = Column(String(50))
    logs       = relationship('Log', cascade = "all, delete", back_populates = 'user')
    activities = relationship('Activity', cascade = "all, delete", back_populates = 'user')

    def __repr__(self):
        return f"<User {self.username}>"
    

class Log(Base):
    __tablename__ = 'logs'

    id        = Column(String, primary_key=True)
    photo_id  = Column(String, nullable = True)
    persent   = Column(String, nullable = True)
    create_at = Column(String, nullable = True)
    user_id   = Column(String, ForeignKey('users.id'))
    user      = relationship('User', back_populates = 'logs')

    def __repr__(self):
        return f"<Log {self.id}>"


class Activity(Base):
    __tablename__ = 'activities'

    id        = Column(String, primary_key=True)
    create_at = Column(String, nullable = True)
    user_id   = Column(String, ForeignKey('users.id'))
    user      = relationship('User', back_populates = 'activities')

    def __repr__(self):
        return f"<Activity {self.id}>"