from fastapi import FastAPI

from config.otel_tracing import setup_tracing
from contextlib import asynccontextmanager
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup ---")
    yield 
    print("Shutdown ---")

app = FastAPI(title="Fintech Banking Support -- Agent API", lifespan=lifespan)
#FastAPIInstrumentor.instrument_app(app)
setup_tracing()

from app.routes.chat_routes import router
app.include_router(router, prefix="/api")
