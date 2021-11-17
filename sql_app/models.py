from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref


from .database import Base ##Precisa criar o aquivo database com as conexões

class Aluno(Base):
    __tablename__ = "aluno"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), index = True)
    children_disciplina = relationship("Disciplina", cascade="all, delete-orphan")

class Disciplina(Base):
    __tablename__ = "disciplina"
    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer,ForeignKey("aluno.id"))
    nome = Column(String(50), unique=True, index = True)
    professor = Column(String(50),index = True)
    anotacao = Column(String(50),index = True)
    children_nota = relationship("Nota", cascade="all, delete-orphan")
    # aluno = relationship("aluno", backref= backref("disciplina", cascade="all, delete-orphan"))

class Nota(Base):
    __tablename__ = "nota"
    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer,ForeignKey("disciplina.id"))
    nome = Column(String(50),unique=True, index = True)
    nota = Column(Integer,index = True)
    # disciplina = relationship("disciplina", backref= backref("nota", cascade="all, delete-orphan"))
