from sqlalchemy.orm import Session
from models.model import Usuario
from fastapi import HTTPException

# Serviço de CRUD de usuários e suas estatísticas.

def criar_usuario(usuario_input, db):
    """Cria um novo usuário e retorna a entidade criada."""
    try:
        novo_usuario = Usuario(
            nome=usuario_input.nome,
            senha=usuario_input.senha,
            nivel=getattr(usuario_input, "nivel", 0),
        )
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return {"mensagem": "Usuário criado com sucesso.", "usuario": novo_usuario}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"O nome de usuário '{usuario_input.nome}' já está em uso.")


def listar_usuarios(db):
    """Retorna todos os usuários do banco."""
    try:
        return db.query(Usuario).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao listar usuários.")


def buscar_usuario(usuario_id, db):
    """Busca um usuário pelo ID. Levanta 404 se não existir."""
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail=f"Usuário com ID {usuario_id} não foi encontrado.")
        return usuario
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar usuário.")


def atualizar_progresso(usuario_id, dados, db):
    """Atualiza o progresso de acertos e erros de um usuário."""
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail=f"Não foi possível atualizar: Usuário com ID {usuario_id} não existe.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar usuário para atualização.")

    try:
        usuario.acerto_total = dados.acerto_total
        usuario.erro_total = dados.erro_total

        db.commit()
        db.refresh(usuario)
        return {"mensagem": "Progresso atualizado com sucesso.", "usuario": usuario}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível atualizar o progresso do usuário.") from exc


def deletar_usuario(usuario_id, db):
    """Deleta um usuário e trata falhas de integridade."""
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if not usuario:
            raise HTTPException(status_code=404, detail=f"Não foi possível deletar: Usuário com ID {usuario_id} não existe.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar usuário para exclusão.")

    try:
        db.delete(usuario)
        db.commit()
        return {"mensagem": "Usuário deletado com sucesso."}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível deletar o usuário porque ele está vinculado a registros.") from exc
