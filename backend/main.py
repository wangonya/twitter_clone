from fastapi import FastAPI, Depends, Header, HTTPException
from .routes import users

app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
    if not x_token:
        raise HTTPException(status_code=400, detail="Token header is required")


app.include_router(
    users.router,
    prefix='/users',
)
