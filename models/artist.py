# models/artist.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database_base import Base

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False)

    releases = relationship("Release", back_populates = "artist")

    def __repr__(self):
        return f"<Artist id = {self.id} name = {self.name}>"
