from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    published = Column(Boolean, default=True)
    scheduled_at = Column(DateTime, nullable=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    meta_title = Column(String)
    meta_description = Column(String)
