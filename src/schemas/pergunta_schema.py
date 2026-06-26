from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

# Schema base para pergunta.
class PerguntaBase(BaseModel):
    pergunta: str
    alternativas: Optional[Dict[str, Any]] = None
    resposta: Optional[str] = Field(None, max_length=1)
    feedback: Optional[str] = None

# Schema usado para criação/atualização de pergunta.
class PerguntaCreate(PerguntaBase):
    categoria: Optional[int] = None

# Schema de resposta que inclui o ID e a categoria associada.
class PerguntaResponse(PerguntaBase):
    id: int
    categoria: Optional[int] = None

    class Config:
        from_attributes = True


# Schema de resposta para endpoints que retornam mensagem e pergunta.
class PerguntaMensagemResponse(BaseModel):
    mensagem: str
    pergunta: PerguntaResponse
