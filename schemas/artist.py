from pydantic import BaseModel

class ArtistCreate(BaseModel):
    name: str
    email: str | None = None


class ArtistOut(BaseModel):
    id: int
    name: str
    email: str | None

    class Config:
        from_attributes = True
