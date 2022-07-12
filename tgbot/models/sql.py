from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


user_project = Table(
    'users_projects',
    Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, name='id')
    fullname = Column(String, nullable=True, name='fullname')
    youtrackId = Column(Integer, nullable=True, unique=True, name='youtrack_id')
    timettaId = Column(String, nullable=True, unique=True, name='timetta_id')
    telegramId = Column(Integer, nullable=True, unique=True, name='telegram_id')
    isAdmin = Column(Boolean, nullable=True, name='is_admin')
    privateChatTelegramId = Column(Integer, nullable=True, unique=True, name='private_chat_telegram_id')
    projects = relationship('Project', secondary=user_project, back_populates='users')

    def __init__(self, fullname, youtrack_id, timetta_id, telegram_id, is_admin, private_chat_telegram_id):
        self.telegramId = telegram_id
        self.isAdmin = is_admin
        self.privateChatTelegramId = private_chat_telegram_id
        self.timettaId = timetta_id
        self.youtrackId = youtrack_id
        self.fullname = fullname

    def to_string(self):
        return f'User({self.id}, ' \
               f'"{self.fullname}", ' \
               f'{self.youtrackId}, ' \
               f'{self.timettaId}, ' \
               f'{self.telegramId}, ' \
               f'{self.isAdmin}, ' \
               f'{self.privateChatTelegramId})'

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, name='id')
    name = Column(String, nullable=False, name='name')
    youtrackId = Column(String, nullable=False, name='youtrack_id')
    users = relationship('User', secondary=user_project, back_populates='projects')

    def __init__(self, name, youtrackId):
        self.name = name
        self.youtrackId = youtrackId

    def to_string(self):
        return f'Project({self.id}, "{self.name}", {self.youtrackId})'

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()
