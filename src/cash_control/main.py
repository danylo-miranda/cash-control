from fastapi import FastAPI
from cash_control.api.v1.routes.user_routes import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")