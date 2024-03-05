import uvicorn
from fastapi import FastAPI
# from database import MySQLDatabase


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "PARECE QUE O JOGO VIROU, NÃO É MESMO?!"}


@app.get("/teste")
async def teste():
    return {'teste': 'é só pra testar mesmo'}


if __name__ == "__main__":
    pass
