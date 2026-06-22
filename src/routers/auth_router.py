from fastapi import APIRouter, Header, Depends
from typing import Annotated
from models.model import Usuario
from dependencies import Session as ses


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.get('/login')
async def login(nome:str, senha:str, session = Depends(ses)):
    usuario = session.query(Usuario).filter(Usuario.nome == nome).first()
    if usuario:
        if usuario.verify(senha) == True:
            return {'mensagem':'usuario autenticado'}
        else:
            return {'Mensagem':'Usuario ou Senha incorretos'}
    else:
        return {'mensagem': 'Usuario não encontrado'}

@router.post('/criar_conta')
async def criar_conta(nome:str, senha:str, session = Depends(ses)):
    usuario = session.query(Usuario).filter(Usuario.nome == nome).first()
    if usuario:
        return {'mensagem':'Usuario já criado'}        
    else:
        novo_user = Usuario(nome=nome, senha=senha)
        novo_user.criptografar(senha)
        session.add(novo_user)
        session.commit()
        return {'mensagem':'Usuario criado com sucesso!'}
    

@router.get("/listar_dados")
async def dados(nome : Annotated[str | None, Header()] = None, session = Depends(ses)) :
    user = session.query(Usuario).filter(Usuario.nome == nome).first()
    if user:
        usuario = session.query(Usuario).filter(Usuario.nome == nome).first()
        user_dados = {
                      "id":usuario.id,
                      'nome':usuario.nome,
                      'nivel':usuario.nivel,
                      'acerto_total':usuario.acerto_total,
                      'erro_total':usuario.erro_total
                      }
        return user_dados
    else:
        return {'mensagem': 'Usuario não encontrado'}

@router.get('/nivel')
async def listar_nivel(nome:str, session = Depends(ses)):
    usuario = session.query(Usuario).filter(Usuario.nome == nome).first()
    if not usuario:
        return {'mensagem': 'Usuário não encontrado'}
    nivel = usuario.nivel    
    return nivel

@router.delete('/deletar_usuario')
async def deletar_user(nome:str, session = Depends(ses)):
    usuario = session.query(Usuario).filter(Usuario.nome == nome).first()
    session.delete(usuario)
    session.commit()
    return {'mensagem':'Usuario excluido com sucesso'}
