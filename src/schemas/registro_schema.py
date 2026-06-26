from pydantic import BaseModel
from typing import Optional

# Schema base para registro com campo de acerto/erro.
class RegistroBase(BaseModel):
    acerto_categoria: Optional[int] = None

# Schema usado para criação/atualização de registros.
class RegistroCreate(RegistroBase):
    categoria_id: Optional[int] = None
    user_id: Optional[int] = None

# Schema de resposta que expõe o ID, categoria e usuário.
class RegistroResponse(RegistroBase):
    id: int
    categoria_id: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


# Schema de resposta para endpoints que retornam mensagem e registro.
class RegistroMensagemResponse(BaseModel):
    mensagem: str
    registro: RegistroResponse
