from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


user_project = Table(
    'users_projects',
    Base.metadata,
    Column('project_id', ForeignKey('projects.id', primary_key=True)),
    Column('user_id', ForeignKey('users.id', primary_key=True)),
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=True)
    youtrackId = Column(Integer, nullable=True, unique=True)
    timettaId = Column(String, nullable=True, unique=True)
    telegramId = Column(Integer, nullable=True, unique=True)
    idAdmin = Column(Boolean, nullable=False, default=False)
    privateChatTelegramId = Column(Integer, nullable=True, unique=True)
    projects = relationship('Project', secondary=user_project, back_populates='users')

    def __init__(self, fullname, youtrackId, timettaId, telegramId, isAdmin, privateChatTelegramId):
        self.telegramId = telegramId
        self.isAdmin = isAdmin
        self.privateChatTelegramId = privateChatTelegramId
        self.timettaId = timettaId
        self.youtrackId = youtrackId
        self.fullname = fullname

    def __str__(self):
        return f'User({self.id}, "{self.fullname}")'


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    youtrackId = Column(String, nullable=False)
    users = relationship('User', secondary=user_project, back_populates='projects')

    def __init__(self, name, youtrackId):
        self.name = name
        self.youtrackId = youtrackId
