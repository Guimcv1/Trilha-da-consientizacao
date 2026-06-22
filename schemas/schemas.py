from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

# --- CATEGORIA ---
class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


# --- USUÁRIO ---
class UsuarioBase(BaseModel):
    nome: str

class UsuarioAuthSchema(UsuarioBase):
    senha: str

class UsuarioResponseSchema(UsuarioBase):
    id: int
    nivel: Optional[int] = None
    acerto_total: Optional[int] = None
    erro_total: Optional[int] = None

    class Config:
        from_attributes = True


# --- PERGUNTA ---
class PerguntaBase(BaseModel):
    pergunta: str
    alternativas: Optional[Dict[str, Any]] = None  
    resposta: Optional[str] = Field(None, max_length=1)
    feedback: Optional[str] = None

class PerguntaCreate(PerguntaBase):
    categoria: Optional[int] = None

class PerguntaResponse(PerguntaBase):
    id: int
    categoria: Optional[int] = None

    class Config:
        from_attributes = True


# --- REGISTRO ---
class RegistroBase(BaseModel):
    acerto_categoria: Optional[int] = None

class RegistroCreate(RegistroBase):
    categoria_id: Optional[int] = None
    user_id: Optional[int] = None

class RegistroResponse(RegistroBase):
    id: int
    categoria_id: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
