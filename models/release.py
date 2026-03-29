from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database_base import Base


class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", back_populates = "releases")

    def __repr__(self):
        return f"<Release id = {self.id}, name = {self.title}, artist = {self.artist.name}>"
