from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from schemas.usuario_schema import UsuarioCreate, UsuarioLogin, UsuarioResponse, MensagemResponse
from services.auth_service import login, criar_conta, dados, listar_nivel, deletar_user
from dependencies import get_session

# Router para autenticação e operação de usuário via Header.
auth_router = APIRouter(prefix="/auth", tags=["Autenticação e Usuários"])


@auth_router.post("/login", response_model=MensagemResponse, status_code=200)
def rota_login(credenciais: UsuarioLogin, db: Session = Depends(get_session)):
    """Autentica um usuário com nome e senha."""
    return login(db, credenciais)


@auth_router.post("/registro", response_model=UsuarioResponse, status_code=201)
def rota_criar_conta(dados: UsuarioCreate, db: Session = Depends(get_session)):
    """Cria uma nova conta de usuário."""
    return criar_conta(db, dados)


@auth_router.get("/meus-dados", response_model=UsuarioResponse, status_code=200)
def rota_dados(nome: Annotated[str | None, Header()] = None, db: Session = Depends(get_session)):
    """Retorna os dados do usuário baseado no Header 'nome'."""
    if not nome:
        raise HTTPException(status_code=400, detail="Header 'nome' não informado")
    return dados(db, nome)


@auth_router.get("/meu-nivel", status_code=200)
def rota_listar_nivel(nome: Annotated[str | None, Header()] = None, db: Session = Depends(get_session)):
    """Retorna o nível do usuário identificado pelo Header."""
    if not nome:
        raise HTTPException(status_code=400, detail="Header 'nome' não informado")
    return listar_nivel(db, nome)


@auth_router.delete("/deletar", status_code=204)
def rota_deletar_user(nome: Annotated[str | None, Header()] = None, db: Session = Depends(get_session)):
    """Deleta o usuário identificado pelo Header 'nome'."""
    if not nome:
        raise HTTPException(status_code=400, detail="Header 'nome' não informado")
    return deletar_user(db, nome)
