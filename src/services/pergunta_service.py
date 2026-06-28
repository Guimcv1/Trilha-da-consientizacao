from fastapi import HTTPException
from models.model import Pergunta, Categoria

# Serviço de CRUD para perguntas.

def criar_pergunta(pergunta_input, db):
    """Cria uma nova pergunta e valida a categoria informada."""
    try:
        categoria_id = pergunta_input.categoria
        if categoria_id in (None, 0, ""):
            categoria_id = None
        elif categoria_id is not None:
            categoria_existe = db.query(Categoria).filter(Categoria.id == categoria_id).first()
            if not categoria_existe:
                raise HTTPException(status_code=400, detail=f"Não foi possível criar a pergunta: A categoria com ID {categoria_id} não existe.")

        nova_pergunta = Pergunta(
            pergunta=pergunta_input.pergunta,
            alternativas=pergunta_input.alternativas,
            resposta=pergunta_input.resposta,
            feedback=pergunta_input.feedback,
            categoria_id=categoria_id,
        )
        db.add(nova_pergunta)
        db.commit()
        db.refresh(nova_pergunta)
        return {"mensagem": "Pergunta criada com sucesso.", "pergunta": nova_pergunta}
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível criar a pergunta. Verifique os dados informados.")


def listar_perguntas(db):
    """Lista todas as perguntas cadastradas."""
    try:
        return db.query(Pergunta).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao listar perguntas.")


def buscar_pergunta(pergunta_id, db):
    """Busca uma pergunta pelo ID e levanta 404 se não existir."""
    try:
        pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
        if not pergunta:
            raise HTTPException(status_code=404, detail=f"Pergunta com ID {pergunta_id} não foi encontrada.")
        return pergunta
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar pergunta.")


def atualizar_pergunta(pergunta_id, pergunta_input, db):
    """Atualiza os dados de uma pergunta existente."""
    try:
        pergunta_banco = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
        if not pergunta_banco:
            raise HTTPException(status_code=404, detail=f"Não foi possível atualizar: Pergunta com ID {pergunta_id} não existe.")

        categoria_id = pergunta_input.categoria
        if categoria_id in (None, 0, ""):
            categoria_id = None
        elif categoria_id is not None:
            categoria_existe = db.query(Categoria).filter(Categoria.id == categoria_id).first()
            if not categoria_existe:
                raise HTTPException(status_code=400, detail=f"Não foi possível atualizar: A categoria com ID {categoria_id} não existe.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar pergunta ou categoria para atualização.")

    try:
        pergunta_banco.pergunta = pergunta_input.pergunta
        pergunta_banco.alternativas = pergunta_input.alternativas
        pergunta_banco.resposta = pergunta_input.resposta
        pergunta_banco.feedback = pergunta_input.feedback
        pergunta_banco.categoria_id = categoria_id

        db.commit()
        db.refresh(pergunta_banco)
        return {"mensagem": "Pergunta atualizada com sucesso.", "pergunta": pergunta_banco}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível atualizar a pergunta. Verifique os dados informados.") from exc


def deletar_pergunta(pergunta_id, db):
    """Remove uma pergunta existente."""
    try:
        pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
        if not pergunta:
            raise HTTPException(status_code=404, detail=f"Não foi possível deletar: Pergunta com ID {pergunta_id} não existe.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar pergunta para exclusão.")

    try:
        db.delete(pergunta)
        db.commit()
        return {"mensagem": "Pergunta deletada com sucesso."}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível deletar a pergunta.") from exc
