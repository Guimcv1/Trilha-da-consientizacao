from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from passlib.hash import sha256_crypt as sha256
from main import Base

# Modelo de usuário com dados de autenticação e estatísticas.
class Usuario(Base):
    __tablename__ = 'Usuario'

    id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True)
    nome = Column('nome', String(255), nullable=False, unique=True)
    senha = Column('senha', String(255), nullable=False)
    nivel = Column('nivel', Integer)
    acerto_total = Column('acerto_total', Integer)
    erro_total = Column('erro_total', Integer)

    def __init__(self, nome, senha, nivel=0, acerto_total=0, erro_total=0):
        self.nome = nome
        self.senha = senha
        self.nivel = nivel
        self.acerto_total = acerto_total
        self.erro_total = erro_total

    def criptografar(self, senha):
        # Gera hash seguro para a senha antes de salvar no banco.
        self.senha = sha256.encrypt(senha)

    def verify(self, senha):
        # Verifica se a senha em texto corresponde ao hash armazenado.
        return sha256.verify(senha, self.senha)

# Modelo de pergunta com ligação opcional a uma categoria.
class Pergunta(Base):
    __tablename__ = 'Pergunta'

    id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True)
    categoria_id = Column('categoria', Integer, ForeignKey('Categoria.id'))
    pergunta = Column('pergunta', String(2000), nullable=False)
    alternativas = Column('alternativas', JSON)  # Armazena alternativas como JSON.
    resposta = Column('resposta', String(1))
    feedback = Column('feedback', String(2000))

# Modelo de categoria simples.
class Categoria(Base):
    __tablename__ = 'Categoria'

    id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True)
    nome = Column('nome', String(255), nullable=False)

# Modelo de registro que liga usuário e categoria com um resultado.
class Registro(Base):
    __tablename__ = 'Registro'

    id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True)
    categoria_id = Column('categoria_id', Integer, ForeignKey("Categoria.id"))
    user_id = Column('user_id', Integer, ForeignKey("Usuario.id"))
    acerto_categoria = Column('acerto_categoria', Integer)
