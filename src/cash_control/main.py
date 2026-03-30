from fastapi import FastAPI
from cash_control.api.v1.routes.user_routes import router
from cash_control.core.database import Base, engine

app = FastAPI(title="Cash Control API", version="1.0.0")

# cria as tabelas automaticamente
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api/v1")