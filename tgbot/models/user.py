from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=True)
    youtrackId = Column(Integer, nullable=True, unique=True)
    timettaId = Column(UUID, nullable=True, unique=True)
    telegramId = Column(Integer, nullable=True, unique=True)
    # telegramName = Column(String, nullable=True, unique=True)
    idAdmin = Column(Boolean, nullable=False, default=False)
    privateChatTelegramId = Column(Integer, nullable=True, unique=True)

    def __init__(self, fullname, youtrackId, timettaId, telegramId, isAdmin, privateChatTelegramId):
        self.telegramId = telegramId
        self.isAdmin = isAdmin
        self.privateChatTelegramId = privateChatTelegramId
        self.timettaId = timettaId
        self.youtrackId = youtrackId
        self.fullname = fullname