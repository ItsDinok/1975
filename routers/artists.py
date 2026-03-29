from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.artist import Artist
from schemas.artist import ArtistCreate, ArtistOut

router = APIRouter(prefix = "/artists", tags = ["artists"])

@router.post("/", response_model=ArtistOut)
def create_artist(data: ArtistCreate, db: Session = Depends(get_db)):
    artist = Artist(**data.dict())
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


@router.get("/", response_model = list[ArtistOut])
def list_artists(db: Session = Depends(get_db)):
    return db.query(Artist).all()
