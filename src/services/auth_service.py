from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.model import Usuario

# Serviço de autenticação e criação de contas.

def login(db, credenciais):
    """Autentica um usuário usando nome e senha."""
    try:
        usuario = db.query(Usuario).filter(Usuario.nome == credenciais.nome).first()
    
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
        if not usuario.verify(credenciais.senha):
            raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
        
        return {"mensagem": "Usuário autenticado com sucesso!"}

    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao autenticar usuário")


def criar_conta(db, dados):
    """Cria um novo usuário e salva no banco."""
    try:
        usuario = db.query(Usuario).filter(Usuario.nome == dados.nome).first()
    
        if usuario:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
        novo_user = Usuario(nome=dados.nome, senha=dados.senha)
        novo_user.criptografar(dados.senha)
    
        db.add(novo_user)
        db.commit()
        db.refresh(novo_user)
    
        return {"mensagem": "Conta criada com sucesso."}
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar conta")


def dados(db, nome):
    """Retorna os dados do usuário solicitado pelo nome."""
    try:
        usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
        return usuario
    
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar dados do usuário")


def listar_nivel(db, nome):
    """Retorna o nível do usuário identificado pelo nome."""
    try:
        usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return {"mensagem": f"Nível do usuário {usuario.nome}", "nivel": usuario.nivel}
    
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar nível do usuário")


def deletar_user(db, nome):
    """Deleta o usuário identificado pelo nome."""
    try:
        usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado para exclusão")

    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar usuário para exclusão")

    try:
        db.delete(usuario)
        db.commit()
        return {"mensagem": "Usuário deletado com sucesso"}

    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível deletar o usuário devido a dependências de registros vinculados.")