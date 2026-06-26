from pydantic import BaseModel

# Schema base para categoria com apenas o nome.
class CategoriaBase(BaseModel):
    nome: str

# Schema usado para criação/atualização de categoria.
class CategoriaCreate(CategoriaBase):
    pass

# Schema de resposta que inclui o ID da categoria.
class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


# Schema de resposta que envolve mensagem e categoria criada/atualizada.
class CategoriaMensagemResponse(BaseModel):
    mensagem: str
    categoria: CategoriaResponse
