from fastapi import FastAPI
from app.routes.chat_routes import router


app = FastAPI(title="Fintech Banking Support -- Agent API")


app.include_router(router, prefix="/api")
