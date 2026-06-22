from fastapi import FastAPI
from routers.auth_router import router as auth_router

app = FastAPI()

@app.get('/')
async def init():
    return {'Mensagem':'Você esta na rota inicial, acesse o /docs para mais informações'}

app.include_router(auth_router)
