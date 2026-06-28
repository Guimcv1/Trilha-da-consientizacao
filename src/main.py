from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

# Cria a instância principal do FastAPI.
app = FastAPI()

# Configura o CORS para permitir chamadas de qualquer origem no ambiente de desenvolvimento.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega variáveis de ambiente a partir do arquivo .env.
load_dotenv()

# Lê as configurações de conexão do banco de dados.
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Se a porta estiver definida e for válida, adiciona ao host; caso contrário, usa apenas o host.
if db_port and str(db_port).strip().lower() != "none":
    try:
        int(db_port)
        host_part = f"{db_host}:{db_port}"
    except (TypeError, ValueError):
        host_part = db_host
else:
    host_part = db_host

# Monta a URL de conexão para PostgreSQL usando o driver psycopg2.
URL = f"postgresql+psycopg2://{db_user}:{db_password}@{host_part}/{db_name}"

# Cria o engine do SQLAlchemy para executar consultas no banco.
engine = create_engine(URL, echo=True)

# Cria a Base declarativa que será usada pelos modelos.
Base = declarative_base()

# Importa os routers após a configuração da Base para evitar problemas de importação circular.
from routers.auth_router import auth_router
from routers.usuario_router import usuario_router
from routers.categoria_router import categoria_router
from routers.pergunta_router import pergunta_router
from routers.registro_router import registro_router

# Registra os routers no aplicativo principal.
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(categoria_router)
app.include_router(pergunta_router)
app.include_router(registro_router)
