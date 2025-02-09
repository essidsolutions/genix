from sqlalchemy import Column, String, Integer
from backend.app.database import Base

class OAuthCredentials(Base):
    __tablename__ = "oauth_credentials"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, index=True)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
