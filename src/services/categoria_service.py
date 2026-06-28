from fastapi import HTTPException
from models.model import Categoria

# Serviço de CRUD para categorias.

def criar_categoria(categoria_input, db):
    """Cria uma nova categoria e salva no banco."""
    try:
        nova_categoria = Categoria(nome=categoria_input.nome)
        db.add(nova_categoria)
        db.commit()
        db.refresh(nova_categoria)
        return {"mensagem": "Categoria criada com sucesso.", "categoria": nova_categoria}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"A categoria '{categoria_input.nome}' já está cadastrada.")


def listar_categorias(db):
    """Lista todas as categorias cadastradas."""
    try:
        return db.query(Categoria).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao listar categorias.")


def buscar_categoria(categoria_id, db):
    """Busca uma categoria pelo ID e levanta 404 se não existir."""
    try:
        categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail=f"Categoria com ID {categoria_id} não foi encontrada.")
        return categoria
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar categoria.")

def atualizar_categoria(categoria_id, categoria_input, db):
    """Atualiza o nome de uma categoria existente."""
    try:
        categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail=f"Não foi possível atualizar: Categoria com ID {categoria_id} não existe.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar categoria para atualização.")

    try:
        categoria.nome = categoria_input.nome
        db.commit()
        db.refresh(categoria)
        return {"mensagem": "Categoria atualizada com sucesso.", "categoria": categoria}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Não foi possível atualizar: O nome '{categoria_input.nome}' já está em uso por outra categoria.")


def deletar_categoria(categoria_id, db):
    """Remove uma categoria e trata dependências de registros."""
    try:
        categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail=f"Não foi possível deletar: Categoria com ID {categoria_id} não existe.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar categoria para exclusão.")

    try:
        db.delete(categoria)
        db.commit()
        return {"mensagem": "Categoria deletada com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível deletar a categoria porque ela está vinculada a registros.") 
