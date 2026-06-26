from pydantic import BaseModel

# Schema base para dados de usuário.
class UsuarioBase(BaseModel):
    nome: str

# Schema usado para criação de conta de usuário.
class UsuarioCreate(UsuarioBase):
    senha: str

# Schema de login com nome e senha.
class UsuarioLogin(UsuarioBase):
    senha: str

# Schema de resposta de usuário contendo dados expostos pela API.
class UsuarioResponse(UsuarioBase):
    id: int
    nivel: int
    acerto_total: int
    erro_total: int

    class Config:
        from_attributes = True


# Schema simples para respostas que retornam apenas mensagem.
class MensagemResponse(BaseModel):
    mensagem: str


# Schema que envolve mensagem e dados de usuário.
class UsuarioMensagemResponse(BaseModel):
    mensagem: str
    usuario: UsuarioResponse


# Schema usado para atualizar o progresso do usuário.
class UsuarioUpdateProgresso(BaseModel):
    acerto_total: int
    erro_total: int
