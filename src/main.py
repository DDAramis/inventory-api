import sys
import os
from pathlib import Path
import logging
import sentry_sdk
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from dotenv import load_dotenv
from src.infrastructure.database import init_db
from src.api.product_routes import router as product_router
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)
logger = logging.getLogger(__name__)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.handlers = [handler]

sys.path.append(str(Path(__file__).resolve().parent.parent))
try:
    load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
    logger.info("Environment variables loaded successfully")
except Exception as e:
    logger.error(f"Failed to load environment variables: {str(e)}")
    raise

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    environment=os.getenv("ENVIRONMENT", "development"),
)

REQUEST_COUNT = Counter('api_requests_total', 'Total number of API requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('api_request_latency_seconds', 'API request latency in seconds', ['method', 'endpoint'])

app = FastAPI(
    title="API de Gestión de Inventario",
    description="API REST para gestionar productos y pedidos con Clean Architecture",
    version="0.1.0",
)


@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    logger.info(f"Recording metrics for {method} {endpoint}")
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

    import time
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
    logger.info(f"Request latency for {method} {endpoint}: {duration} seconds")
    return response


@app.get("/metrics")
async def metrics():
    metrics_data = generate_latest(REGISTRY)
    logger.info("Serving Prometheus metrics")
    return PlainTextResponse(metrics_data)


try:
    app.include_router(product_router)
    logger.info("Product routes registered successfully")
except Exception as e:
    logger.error(f"Failed to register product routes: {str(e)}")
    raise

try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")


@app.get("/")
async def root():
    return {"message": "¡Bienvenido a la API de Gestión de Inventario!"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception in {request.method} {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
