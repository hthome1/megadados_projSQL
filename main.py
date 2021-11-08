from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi  import FastAPI , HTTPException
from pydantic import BaseModel, Field
from typing   import List, Optional, Dict
import uuid


#---Models---#
class Nota(BaseModel):
    nota            :   int             = Field(..., example=5)

class Disciplina(BaseModel):
    disciplina      :   str             = Field(..., example="Engenharia")
    professor       :   Optional[str]   
    anotacao        :   Optional[str]
    notas           :   Optional[dict]

class DisciplinaEdit(BaseModel):
    professor       :   Optional[str]
    anotacao        :   Optional[str]
    notas           :   Optional[dict]

app = FastAPI()
aluno_test = "124c0fd0-40ac-11ec-b038-75bf62bc265c"
disciplina_test = "9c00d170-40cf-11ec-b4b8-e16d985e7810"
nota_test = "92e0c2a6-40db-11ec-aead-150824cd6f2e"

db = {
    aluno_test:{
        disciplina_test:{
            'disciplina':'Mega Dados',
            'professor' : None,
            'anotacao'  : None,
            'notas'     : {
                nota_test:{
                    'nota': 10
                }
            }
        }
    }
}

#---Informações do Projeto---#
tags_metadata = [
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

# ---Todas as disciplinas ---#
@app.get("/disciplina",tags=["Disciplinas"], name="Listar Disciplinas")
async def todas_disciplinas(aluno_id: str):
    if aluno_id in db:
        return db[aluno_id]
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

# ---Criar disciplina ---#
@app.post("/disciplina",tags=["Disciplinas"], name="Criar disciplina")
async def criar_disciplina(aluno_id: str,disciplina:Disciplina):
    if aluno_id in db:
        ID = str(uuid.uuid1())
        db[aluno_id][ID] = disciplina.dict()
        return db[aluno_id][ID]
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

#---Alterar disciplina ---#
@app.patch("/disciplina",tags=["Disciplinas"], name="Modificar disciplina")
async def update_disciplina(aluno_id: str,disciplina_id: str, disciplina: DisciplinaEdit):
    if aluno_id in db:
        if disciplina_id in db[aluno_id]:
            disciplina_antiga = db[aluno_id][disciplina_id]
            disciplina_antiga_model = Disciplina(**disciplina_antiga)
            update_data = disciplina.dict(exclude_unset=True)
            updated_disciplina = disciplina_antiga_model.copy(update=update_data)
            db[aluno_id][disciplina_id] = updated_disciplina.dict()
            return updated_disciplina
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

# #---Deletar disciplina ---#
@app.delete("/disciplina",tags=["Disciplinas"], name="Deletar disciplina")
async def delete_disciplina(aluno_id: str,disciplina_id: str):
    if aluno_id in db:
        if disciplina_id in db[aluno_id]:
            del db[aluno_id][disciplina_id]
            return db[aluno_id]
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

# ---Todas as Notas ---#
@app.get("/disciplinas/notas",tags=["Notas"], name="Listar Notas")
async def todas_notas(aluno_id: str,disciplina_id: str):
    if aluno_id in db:
        if disciplina_id in db[aluno_id]:
            if db[aluno_id][disciplina_id]["notas"]!=None:
                return db[aluno_id][disciplina_id]["notas"]
            else:
                return HTTPException(status_code=404, detail="Disciplina não possui notas cadastradas")
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

# ---Criar Nota ---#
@app.post("/disciplinas/notas",tags=["Notas"], name="Criar Nota")
async def criar_nota(aluno_id: str,disciplina_id: str,nota:Nota):
    if aluno_id in db:
        if disciplina_id in db[aluno_id]:
            if db[aluno_id][disciplina_id]["notas"]!=None:
                ID = str(uuid.uuid1())
                db[aluno_id][disciplina_id]["notas"][ID] = nota.dict()
                return db[aluno_id][disciplina_id]["notas"][ID]
            else:
                return HTTPException(status_code=404, detail="Disciplina não possui notas cadastradas")
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

# #---Alterar Nota ---#
@app.patch("/disciplinas/notas",tags=["Notas"], name="Modificar Nota")
async def update_nota(aluno_id: str,disciplina_id: str,nota_id: str,nota:Nota):
    if aluno_id in db:
        if disciplina_id in db[aluno_id]:
            if db[aluno_id][disciplina_id]["notas"]!=None and nota_id in db[aluno_id][disciplina_id]["notas"]:
                db[aluno_id][disciplina_id]["notas"][nota_id] = nota.dict(exclude_unset=True)
                return nota.dict(exclude_unset=True)
            else:
                return HTTPException(status_code=404, detail="Disciplina não possui Id_notas informado")
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")

# # #---Deletar Nota ---#
@app.delete("/disciplinas/notas",tags=["Notas"], name="Modificar Nota")
async def delete_nota(aluno_id: str,disciplina_id: str,nota_id: str):
    if aluno_id in db:
        if disciplina_id in db[aluno_id]:
            if db[aluno_id][disciplina_id]["notas"]!=None and nota_id in db[aluno_id][disciplina_id]["notas"]:
                del db[aluno_id][disciplina_id]["notas"][nota_id]
                return db[aluno_id][disciplina_id]["notas"]
            else:
                return HTTPException(status_code=404, detail="Disciplina não possui Id_notas informado")
        else:
            return HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        return HTTPException(status_code=404, detail="Aluno não encontrado")