from sqlalchemy import Column , Integer , String, Text , DateTime , Float
from datetime import datetime
from .sessions import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer , primary_key=True, index=True)
    message_id = Column(String , unique=True , index=True , nullable=False)
    sender = Column(String, nullable=False)
    subject = Column(String)
    body = Column(Text)
    status = Column(String , default="new")
    created_at = Column(DateTime, default=datetime.utcnow)

    intent = Column(String , nullable=True)
    confidence = Column(Float, nullable=True)
    draft_response = Column(Text , nullable = True)
    