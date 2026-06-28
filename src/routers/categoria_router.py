from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.categoria_service import criar_categoria, listar_categorias, buscar_categoria, atualizar_categoria, deletar_categoria
from schemas.categoria_schema import CategoriaCreate, CategoriaResponse, CategoriaMensagemResponse
from dependencies import get_session

# Router que agrupa os endpoints de categoria.
categoria_router = APIRouter(prefix="/categoria", tags=["Categoria"])


@categoria_router.get("/read", response_model=list[CategoriaResponse])
def listar_categorias_endpoint(db: Session = Depends(get_session)):
    """Retorna todas as categorias cadastradas."""
    return listar_categorias(db)


@categoria_router.get("/read/{categoria_id}", response_model=CategoriaResponse)
def buscar_categoria_endpoint(categoria_id: int, db: Session = Depends(get_session)):
    """Busca uma categoria pelo ID."""
    return buscar_categoria(categoria_id, db)


@categoria_router.post("/create", response_model=CategoriaMensagemResponse, status_code=201)
def criar_categoria_endpoint(categoria_input: CategoriaCreate, db: Session = Depends(get_session)):
    """Cria uma nova categoria."""
    return criar_categoria(categoria_input, db)


@categoria_router.put("/update/{categoria_id}", response_model=CategoriaMensagemResponse)
def atualizar_categoria_endpoint(categoria_id: int, categoria_input: CategoriaCreate, db: Session = Depends(get_session)):
    """Atualiza o nome de uma categoria existente."""
    return atualizar_categoria(categoria_id, categoria_input, db)


@categoria_router.delete("/delete/{categoria_id}", status_code=204)
def deletar_categoria_endpoint(categoria_id: int, db: Session = Depends(get_session)):
    """Deleta uma categoria pelo ID."""
    return deletar_categoria(categoria_id, db)
