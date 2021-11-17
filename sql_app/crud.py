from sqlalchemy.orm import Session

from . import models, schemas

#----GET----#

#ALL#

def get_alunos(db: Session,  skip: int = 0):
    return db.query(models.Aluno).offset(skip).all()

def get_disciplinas(db: Session,  skip: int = 0):
    return db.query(models.Disciplina).offset(skip).all()

def get_notas(db: Session,  skip: int = 0):
    return db.query(models.Nota).offset(skip).all()

#SELECTED#

def get_aluno(db: Session, id:int):
    return db.query(models.Aluno).filter(models.Aluno.id == id).first()

def get_disciplina(db: Session, id:int):
    return db.query(models.Disciplina).filter(models.Disciplina.id == id).first()

def get_nota(db: Session, id:int):
    return db.query(models.Nota).filter(models.Nota.id == id).first()

#ALL SELECTED#

def get_disciplinas_aluno(db: Session, aluno_id:int , skip: int = 0):
    return db.query(models.Disciplina).filter(models.Disciplina.aluno_id == aluno_id).offset(skip).all()

def get_notas_disciplina(db: Session, disciplina_id:int , skip: int = 0):
    return db.query(models.Nota).filter(models.Nota.disciplina_id == disciplina_id).offset(skip).all()

#----CREATE----#
def create_aluno(db: Session, aluno: schemas.AlunoCreate):
    db_aluno = models.Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def create_disciplina(db: Session, aluno_id: int, disciplina: schemas.DisciplinaCreate):
    db_disciplina = models.Disciplina(aluno_id=aluno_id, **disciplina.dict())
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

def create_nota(db: Session, disciplina_id: int, nota: schemas.NotaCreate):
    db_nota = models.Nota(disciplina_id=disciplina_id, **nota.dict())
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota

#----UPDATE----#

def update_aluno(db: Session, aluno_id: int, aluno: schemas.AlunoCreate):
    db.query(
        models.Aluno
        ).filter(
            models.Aluno.id == aluno_id
            ).update({
                models.Aluno.nome: aluno.nome
                })
    db.commit()
    return "Aluno Atualizado!"

def update_disciplina(db: Session, disciplina_id: int, disciplina: schemas.DisciplinaCreate):
    db.query(
        models.Disciplina
        ).filter(
            models.Disciplina.id == disciplina_id
            ).update({
                models.Disciplina.nome: disciplina.nome, 
                models.Disciplina.professor: disciplina.professor,
                models.Disciplina.anotacao: disciplina.anotacao
                })
    db.commit()
    return "Disciplina Atualizada!"

def update_nota(db: Session, nota_id: int, nota: schemas.NotaCreate):
    db.query(
        models.Nota
        ).filter(
            models.Nota.id == nota_id
            ).update({
                models.Nota.nome: nota.nome,
                models.Nota.nota: nota.nota,
                })
    db.commit()
    return "Nota Atualizada!"

#----DELETE----#

def delete_aluno(db: Session,  aluno: schemas.Aluno):
    db.delete(aluno)
    db.commit()
    return "Aluno deletado!"

def delete_disciplina(db: Session,  disciplina: schemas.Disciplina):
    db.delete(disciplina)
    db.commit()
    return "Disciplina deletada!"

def delete_nota(db: Session,  nota: schemas.Nota):
    db.delete(nota)
    db.commit()
    return "Nota deletada!"