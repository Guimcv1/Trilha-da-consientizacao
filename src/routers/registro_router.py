from fastapi import APIRouter, Depends
from schemas.registro_schema import RegistroCreate, RegistroResponse, RegistroMensagemResponse
from sqlalchemy.orm import Session
from services.registro_service import criar_registro, listar_registros, buscar_registro_por_id, atualizar_registro, deletar_registro
from dependencies import get_session

# Router para operações sobre registros de desempenho.
registro_router = APIRouter(prefix="/registro", tags=["registro"])


@registro_router.get("/read", response_model=list[RegistroResponse])
def listar_registros_endpoint(db: Session = Depends(get_session)):
    """Retorna todos os registros cadastrados."""
    return listar_registros(db)


@registro_router.get("/read/{registro_id}", response_model=RegistroResponse)
def buscar_registro_endpoint(registro_id: int, db: Session = Depends(get_session)):
    """Busca um registro pelo ID."""
    return buscar_registro_por_id(db, registro_id)


@registro_router.post("/create", response_model=RegistroMensagemResponse)
def criar_registro_endpoint(dados: RegistroCreate, db: Session = Depends(get_session)):
    """Cria um novo registro de acerto/erro."""
    return criar_registro(db, dados)


@registro_router.put("/update/{registro_id}", response_model=RegistroMensagemResponse)
def atualizar_registro_endpoint(registro_id: int, dados: RegistroCreate, db: Session = Depends(get_session)):
    """Atualiza um registro existente."""
    return atualizar_registro(db, registro_id, dados)


@registro_router.delete("/delete/{registro_id}")
def deletar_registro_endpoint(registro_id: int, db: Session = Depends(get_session)):
    """Deleta um registro pelo ID."""
    return deletar_registro(db, registro_id)
