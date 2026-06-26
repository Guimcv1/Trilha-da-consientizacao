from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.model import Usuario

# Serviço de autenticação e criação de contas.

def login(db, credenciais):
    """Autentica um usuário usando nome e senha."""
    usuario = db.query(Usuario).filter(Usuario.nome == credenciais.nome).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if not usuario.verify(credenciais.senha):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
        
    return {"mensagem": "Usuário autenticado com sucesso!"}


def criar_conta(db, dados):
    """Cria um novo usuário e salva no banco."""
    usuario = db.query(Usuario).filter(Usuario.nome == dados.nome).first()
    
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
        
    novo_user = Usuario(nome=dados.nome, senha=dados.senha)
    novo_user.criptografar(dados.senha)
    
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    
    return {"mensagem": "Conta criada com sucesso."}


def dados(db, nome):
    """Retorna os dados do usuário solicitado pelo nome."""
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario


def listar_nivel(db, nome):
    """Retorna o nível do usuário identificado pelo nome."""
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    return {"mensagem": f"Nível do usuário {usuario.nome}", "nivel": usuario.nivel}


def deletar_user(db, nome):
    """Deleta o usuário identificado pelo nome."""
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para exclusão")
        
    db.delete(usuario)
    db.commit()
    return {"mensagem": "Usuário deletado com sucesso"}
