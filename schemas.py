from typing import List, Optional

from pydantic import BaseModel
## Disciplina, Nota


class DisciplinaBase (BaseModel):
    name:str = None
    professor:Optional[str]  = None
    anotacao:Optional[str]  = None


class DisciplinaCreate(DisciplinaBase):
    pass

class Disciplina(DisciplinaBase):
    id:int
    class Config:
        orm_mode = True

class NotaBase (BaseModel):
    nome_av:str = None
    nota:str  = None
    id_disciplina:int  = None


class NotaCreate(NotaBase):
    pass


class Nota(NotaBase):
    id:int
    id_disciplina:int
    class Config:
        orm_mode = True