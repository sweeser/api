from pydantic import BaseModel

class TermBase(BaseModel):
    key: str
    description: str

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    description: str

class Term(TermBase):
    id: int

    class Config:
        orm_mode = True
