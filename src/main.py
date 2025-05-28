import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from dotenv import load_dotenv
from src.infrastructure.database import init_db
from src.api.product_routes import router as product_router

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

init_db()

app = FastAPI(
    title = "API de Gestión de Inventario",
    description = "API REST para gestionar productos y pedidos con Clean Architecture",
    version = "0.1.0",
)


@app.get ("/")
async def root():
    return {"message": "¡Bienvenido a la API de Gestión de Inventario!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host= "0.0.0.0", port=port)