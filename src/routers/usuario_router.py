from fastapi import APIRouter, Depends
from services.usuario_service import listar_usuarios, criar_usuario, buscar_usuario, atualizar_progresso, deletar_usuario
from dependencies import get_session
from sqlalchemy.orm import Session
from schemas.usuario_schema import UsuarioCreate, UsuarioUpdateProgresso, UsuarioMensagemResponse

# Router para operações de usuário.
usuario_router = APIRouter(prefix='/usuario', tags=['Usuario'])


@usuario_router.get('/read')
async def listar_usuarios_endpoint(db: Session = Depends(get_session)):
    """Retorna a lista de todos os usuários."""
    return listar_usuarios(db)


@usuario_router.get('/read/{usuario_id}')
async def buscar_usuario_endpoint(usuario_id: int, db: Session = Depends(get_session)):
    """Busca um usuário pelo ID."""
    return buscar_usuario(usuario_id, db)


@usuario_router.post('/create', response_model=UsuarioMensagemResponse)
async def criar_usuario_endpoint(usuario_input: UsuarioCreate, db: Session = Depends(get_session)):
    """Cria um usuário novo no banco."""
    return criar_usuario(usuario_input, db)


@usuario_router.put('/update/{usuario_id}', response_model=UsuarioMensagemResponse)
async def atualizar_progresso_endpoint(usuario_id: int, dados: UsuarioUpdateProgresso, db: Session = Depends(get_session)):
    """Atualiza o progresso de acertos/erros do usuário."""
    return atualizar_progresso(usuario_id, dados, db)


@usuario_router.delete('/delete/{usuario_id}')
async def deletar_usuario_endpoint(usuario_id: int, db: Session = Depends(get_session)):
    """Exclui um usuário pelo ID."""
    return deletar_usuario(usuario_id, db)
