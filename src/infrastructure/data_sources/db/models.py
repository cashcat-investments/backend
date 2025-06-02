from sqlalchemy import Column, DateTime, String, UUID
from src.infrastructure.data_sources.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_pic = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"email=\"{self.email}\", " \
               f"first_name=\"{self.first_name}\", " \
               f"last_name=\"{self.last_name}\", " \
               f"profile_pic=\"{self.profile_pic}\", " \
               f"created_at={self.created_at}, " \
               f"updated_at={self.updated_at})>"