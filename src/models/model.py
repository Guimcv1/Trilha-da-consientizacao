from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from passlib.hash import sha256_crypt as sha256
import os


load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(URL, echo=True)

class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = 'Usuario'

    id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True)
    nome = Column('nome', String(255), nullable=False, unique=True)
    senha = Column('senha', String(255), nullable=False)
    nivel = Column('nivel', Integer)
    acerto_total = Column('acerto_total', Integer)
    erro_total = Column('erro_total', Integer)

    def __init__(self, nome, senha, nivel = 0, acerto_total = 0, erro_total = 0):
         self.nome = nome
         self.senha = senha
         self.nivel = nivel
         self.acerto_total = acerto_total
         self.erro_total = erro_total         

    def criptografar(self,senha):
           self.senha = sha256.encrypt(senha)

    def verify(self,senha):
         resultado = sha256.verify(senha, self.senha)
         return resultado

class Perguta(Base):
     __tablename__ = 'Pergunta'

     id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True)
     categoria_id = Column('categoria', Integer, ForeignKey('Categoria.id'))
     pergunta = Column('pergunta', String(2000), nullable=False )
     alternativas = Column('alternativas', JSON)                                    #NOTE - vai ser um dicionario de listas = {[{}]}
     resposta = Column('resposta', String(1))
     feedback = Column('feedback', String(2000))

class Categoria(Base):
     __tablename__ = 'Categoria'
     
     id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True)
     nome = Column('nome', String(255), nullable=False)

class Registro(Base):
     __tablename__ = 'Registro'

     id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True)
     categoria_id = Column('categoria_id', Integer, ForeignKey("Categoria.id"))
     user_id = Column('user_id', Integer, ForeignKey("Usuario.id"))
     acerto_categoria = Column('acerto_categoria', Integer)
