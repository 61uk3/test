from fastapi import FastAPI
from routers import ItemRouter
from routers import UserRouter
from routers import AuthRouter


app = FastAPI()

app.include_router(ItemRouter.router, prefix='/items')
# app.include_router(UserRouter.router, prefix='/user')
app.include_router(AuthRouter.router)
