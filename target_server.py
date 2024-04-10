from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


@app.post("/task1")
async def root(r: Request):
    user_data = await r.json()
    print(f'task1 : {user_data}')
    return user_data


@app.post("/task2")
async def root(r: Request):
    user_data = await r.json()
    print(f'task2 : {user_data}')
    return user_data