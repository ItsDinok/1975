# main.py
from database import engine, SessionLocal
from database_base import Base
from models import artist, release
from models.artist import Artist
from models.release import Release
from fastapi import FastAPI
from routers import artists

Base.metadata.create_all(bind = engine)
app = FastAPI()
app.include_router(artists.router)

db = SessionLocal()

artist = Artist(name = "Blakey", email = "blakey@blakey.com")
db.add(artist)
db.commit()
db.refresh(artist)

release = Release(title = "Hit single", artist_id = artist.id)
db.add(release)
db.commit()

print(artist.releases)

print(db.query(Artist).all())
