from fastapi import FastAPI
from api.api_v1 import api_router

app = FastAPI()

@app.get('/', status_code=200)
async def root():
    return {"message": "connection established"}

app.include_router(api_router)