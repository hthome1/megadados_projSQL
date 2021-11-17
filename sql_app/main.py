from os import SEEK_CUR
from typing   import List, Optional, Dict

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from . import crud, models, schemas
from .database import SessionLocal, engine

from pydantic import BaseModel, Field

import uuid

models.Base.metadata.create_all(bind=engine)

#---Informações do Projeto---#
tags_metadata = [
    {
        "name": "Alunos",
        "description": "Requests para a criação, edição e remoção de alunos"
    },
    {
        "name": "Disciplinas",
        "description": "Requests para a criação, edição e remoção de disciplinas"
    },
    {
        "name": "Notas",
        "description": "Requests para a criação, edição e remoção de notas"
    }
]

#---Descrição API---#
app = FastAPI(
    title="APS1 Megadados",
    description="API REST para controle de disciplinas",
    version="1.0.0",
    openapi_tags=tags_metadata    
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#----ALUNOS----#

#Todos#
@app.get("/aluno",tags=["Alunos"], name="Listar Alunos")
def todos_alunos(db: Session = Depends(get_db)):
    return crud.get_alunos(db=db)

#Criar#
@app.post("/aluno",tags=["Alunos"], name="Criar Aluno")
def criar_aluno(aluno: schemas.AlunoCreate,db: Session = Depends(get_db)):
    return crud.create_aluno(db=db,aluno=aluno)

#Atualizar#
@app.patch("/aluno",tags=["Alunos"], name="Criar Aluno")
def update_aluno(aluno_id: int,aluno: schemas.AlunoCreate,db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        return crud.update_aluno(db=db,aluno_id=aluno_id,aluno=aluno)
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#Deletar#
@app.delete("/aluno",tags=["Alunos"], name="Criar Aluno")
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        return crud.delete_aluno(db=db,aluno=aluno_check)
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#----DISCIPLINAS----#

#Todas#
@app.get("/disciplina",tags=["Disciplinas"], name="Listar Disciplinas")
def todas_disciplinas(aluno_id: int, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        return crud.get_disciplinas_aluno(db=db,aluno_id=aluno_id)
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#Criar#
@app.post("/disciplina",tags=["Disciplinas"], name="Criar disciplina")
def criar_disciplina(aluno_id: int, disciplina:schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        return crud.create_disciplina(db=db,aluno_id=aluno_id,disciplina=disciplina)
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#Atualizar#
@app.patch("/disciplina",tags=["Disciplinas"], name="Modificar disciplina")
def update_nota(aluno_id: int,disciplina_id: int, disciplina:schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        disciplina_check = crud.get_disciplina(db=db,id=disciplina_id)
        if disciplina_check:
            return crud.update_disciplina(db=db,disciplina_id=disciplina_id,disciplina=disciplina)
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#Deletar#
@app.delete("/disciplina",tags=["Disciplinas"], name="Deletar disciplina")
def delete_disciplina(aluno_id: int,disciplina_id: int, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        disciplina_check = crud.get_disciplina(db=db,id=disciplina_id)
        if disciplina_check:
            return crud.delete_disciplina(db=db,disciplina=disciplina_check)
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#----NOTAS----#

#Todas#
@app.get("/nota",tags=["Notas"], name="Listar Notas")
def todas_notas(aluno_id: int,disciplina_id: int, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        disciplina_check = crud.get_disciplina(db=db,id=disciplina_id)
        if disciplina_check:
            return crud.get_notas_disciplina(db=db,disciplina_id=disciplina_id)
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#Criar#
@app.post("/nota",tags=["Notas"], name="Criar Nota")
def criar_nota(aluno_id: int,disciplina_id: int, nota:schemas.NotaCreate, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        disciplina_check = crud.get_disciplina(db=db,id=disciplina_id)
        if disciplina_check:
            return crud.create_nota(db=db,disciplina_id=disciplina_id,nota=nota)
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#Atualizar#
@app.patch("/nota",tags=["Notas"], name="Modificar Nota")
def update_nota(aluno_id: int,disciplina_id: int,nota_id: int, nota:schemas.NotaCreate, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        disciplina_check = crud.get_disciplina(db=db,id=disciplina_id)
        if disciplina_check:
            nota_check = crud.get_nota(db=db,id=nota_id)
            if nota_check:
                return crud.update_nota(db=db,nota_id=nota_id,nota=nota)
            else:
                return HTTPException(status_code=404, detail="Nota não encontrada")
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#Deletar#
@app.delete("/nota",tags=["Notas"], name="Modificar Nota")
def delete_nota(aluno_id: int, disciplina_id: int, nota_id: int, db: Session = Depends(get_db)):
    aluno_check = crud.get_aluno(db=db,id=aluno_id)
    if aluno_check:
        disciplina_check = crud.get_disciplina(db=db,id=disciplina_id)
        if disciplina_check:
            nota_check = crud.get_nota(db=db,id=nota_id)
            if nota_check:
                return crud.delete_nota(db=db,nota=nota_check)
            else:
                return HTTPException(status_code=404, detail="Nota não encontrada")
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")