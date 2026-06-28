from fastapi import APIRouter, Depends
from services.pergunta_service import criar_pergunta, listar_perguntas, buscar_pergunta, atualizar_pergunta, deletar_pergunta
from schemas.pergunta_schema import PerguntaCreate, PerguntaResponse, PerguntaMensagemResponse
from dependencies import get_session

# Router que agrupa os endpoints de pergunta.
pergunta_router = APIRouter(prefix="/pergunta", tags=["pergunta"])


@pergunta_router.get("/read", response_model=list[PerguntaResponse])
def listar_perguntas_endpoint(db = Depends(get_session)):
    """Retorna todas as perguntas do banco."""
    return listar_perguntas(db)


@pergunta_router.get("/read/{pergunta_id}", response_model=PerguntaResponse)
def buscar_pergunta_endpoint(pergunta_id: int, db = Depends(get_session)):
    """Busca uma pergunta específica por ID."""
    return buscar_pergunta(pergunta_id, db)


@pergunta_router.post("/create", response_model=PerguntaMensagemResponse, status_code=201)
def criar_pergunta_endpoint(pergunta_input: PerguntaCreate, db = Depends(get_session)):
    """Cria uma nova pergunta."""
    return criar_pergunta(pergunta_input, db)


@pergunta_router.put("/update/{pergunta_id}", response_model=PerguntaMensagemResponse)
def atualizar_pergunta_endpoint(pergunta_id: int, pergunta_input: PerguntaCreate, db = Depends(get_session)):
    """Atualiza os dados de uma pergunta existente."""
    return atualizar_pergunta(pergunta_id, pergunta_input, db)


@pergunta_router.delete("/delete/{pergunta_id}", response_model=PerguntaResponse)
def deletar_pergunta_endpoint(pergunta_id: int, db = Depends(get_session)):
    """Deleta uma pergunta por ID."""
    return deletar_pergunta(pergunta_id, db)
