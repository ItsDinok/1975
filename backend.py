from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://admin:password@localhost:5432/label_db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Artist(Base):
    def __repr__(self):
        return f"<Artist id={self.id} name={self.name}>"

    __tablename__ = "artists"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    email = Column(String)


class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = False)
    artist_id = Column(Integer)
    release_date = Column(Date)


Base.metadata.create_all(engine)

# Insert and query

Session = sessionmaker(bind = engine)
session = Session()

# Create
artist = Artist(name = "Test Artist", email = "test@email.com")
session.add(artist)
session.commit()

# Read
artists = session.query(Artist).all()
print(artists)

