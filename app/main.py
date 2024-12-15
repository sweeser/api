from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

# Создаем таблицы при старте, если их нет
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Glossary API",
    description="Простое API для работы с глоссарием терминов",
    version="1.0.0"
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/terms", response_model=list[schemas.Term])
def read_terms(db: Session = Depends(get_db)):
    return crud.get_terms(db)

@app.get("/terms/{term_key}", response_model=schemas.Term)
def read_term(term_key: str, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_key(db, term_key)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term

@app.post("/terms", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_key(db, term.key)
    if db_term:
        raise HTTPException(status_code=400, detail="Term already exists")
    return crud.create_term(db, term)

@app.put("/terms/{term_key}", response_model=schemas.Term)
def update_term(term_key: str, update_data: schemas.TermUpdate, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_key(db, term_key)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return crud.update_term(db, db_term, update_data.description)

@app.delete("/terms/{term_key}")
def delete_term(term_key: str, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_key(db, term_key)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    crud.delete_term(db, db_term)
    return {"detail": "Term deleted"}
