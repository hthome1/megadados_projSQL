from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref


from .database import Base ##Precisa criar o aquivo database com as conexões

class Disciplina(Base):
    __tablename__ = "disciplinas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index = True)
    professor = Column(String, unique = False)
    anotacao = Column(String)

    notas = relationship("Nota", cascade="all, delete-orphan")


class Nota(Base):
    __tablename__ = "nota"
    id = Column(Integer, primary_key=True, index=True)
    nome_av = Column(String,primary_key=True)
    nota = Column(Integer)
    id_disciplina = Column(Integer,ForeignKey("disciplinas.id"))

    disc = relationship("Disciplina", backref= backref("Nota", cascade="all, delete-orphan"))
