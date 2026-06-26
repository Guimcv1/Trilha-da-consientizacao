from src.models.model import Registro
from fastapi import HTTPException

# Serviço de CRUD para registros de desempenho.

def criar_registro(db, dados):
    """Cria um registro de acerto/erro associado a usuário e categoria."""
    novo_registro = Registro(
        categoria_id=dados.categoria_id,
        user_id=dados.user_id,
        acerto_categoria=dados.acerto_categoria,
    )
    
    try:
        db.add(novo_registro)
        db.commit()
        db.refresh(novo_registro)
        return {
            "mensagem": "Registro criado com sucesso.",
            "registro": {
                "id": novo_registro.id,
                "categoria_id": novo_registro.categoria_id,
                "user_id": novo_registro.user_id,
                "acerto_categoria": novo_registro.acerto_categoria,
            },
        }
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Erro de integridade: Verifique se o user_id e a categoria_id existem.",
        )


def listar_registros(db):
    """Retorna todos os registros cadastrados."""
    return db.query(Registro).all()


def buscar_registro_por_id(db, registro_id):
    """Busca um registro pelo ID e levanta 404 se não existir."""
    registro = db.query(Registro).filter(Registro.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail=f"Registro com ID {registro_id} não encontrado.")
    return registro


def atualizar_registro(db, registro_id, dados):
    """Atualiza um registro existente com novos valores."""
    registro = buscar_registro_por_id(db, registro_id)
    
    registro.categoria_id = dados.categoria_id
    registro.user_id = dados.user_id
    registro.acerto_categoria = dados.acerto_categoria
    
    try:
        db.commit()
        db.refresh(registro)
        return {
            "mensagem": "Registro atualizado com sucesso.",
            "registro": {
                "id": registro.id,
                "categoria_id": registro.categoria_id,
                "user_id": registro.user_id,
                "acerto_categoria": registro.acerto_categoria,
            },
        }
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro de integridade ao atualizar: Verifique os IDs informados.")


def deletar_registro(db, registro_id):
    """Remove um registro existente do banco."""
    registro = buscar_registro_por_id(db, registro_id)
    
    try:
        db.delete(registro)
        db.commit()
        return {"mensagem": "Registro deletado com sucesso."}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível deletar o registro.") from exc
