from typing import List, Optional

from pydantic import BaseModel

#----Alunos----#

class AlunoBase (BaseModel):
    nome:str = None

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id:int
    class Config:
        orm_mode = True

#----Disciplinas----#

class DisciplinaBase (BaseModel):
    nome:str = None
    professor:Optional[str]  = None
    anotacao:Optional[str]  = None


class DisciplinaCreate(DisciplinaBase):
    pass

class Disciplina(DisciplinaBase):
    aluno_id:int
    id:int
    class Config:
        orm_mode = True

#----Notas----#

class NotaBase (BaseModel):
    nome:str = None
    nota:str  = None

class NotaCreate(NotaBase):
    pass

class Nota(NotaBase):
    disciplina_id:int
    id:int
    class Config:
        orm_mode = True