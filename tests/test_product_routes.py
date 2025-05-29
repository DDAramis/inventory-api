import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.infrastructure.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from pathlib import Path
import os

# Cargar variables de entorno
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Configurar el cliente de prueba
client = TestClient(app)

# Verificar que las rutas están disponibles
def test_routes_available():
    # Obtener todas las rutas disponibles en la aplicación
    routes = [route.path for route in app.routes]
    print(f"Available routes: {routes}")
    assert "/products/" in routes, "Route /products/ not found in app routes"
    assert "/" in routes, "Root route / not found in app routes"

# Fixture para limpiar y preparar la base de datos antes de cada prueba
@pytest.fixture
def db_session():
    # Verificar que DATABASE_URL esté configurada
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    database_url = os.getenv("DATABASE_URL_LOCAL") if ENVIRONMENT == "development" else os.getenv("DATABASE_URL_SUPABASE")
    if not database_url:
        raise ValueError(f"DATABASE_URL for {ENVIRONMENT} not found. Ensure DATABASE_URL_LOCAL or DATABASE_URL_SUPABASE is set in .env")
    
    try:
        # Crear las tablas
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        yield db
    except Exception as e:
        pytest.fail(f"Failed to set up database: {str(e)}")
    finally:
        db.close()
        # Limpiar la base de datos después de cada prueba
        Base.metadata.drop_all(bind=engine)

# Prueba para crear un producto
def test_create_product(db_session: Session):
    product_data = {
        "name": "Laptop",
        "price": 999.99,
        "stock": 10
    }
    response = client.post("/products", json=product_data)
    print(f"Create product response: {response.json()}")
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "stock": 10
    }

    # Verificar que el producto se guardó en la base de datos
    response = client.get("/products")
    print(f"Get all products response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "stock": 10
    }]

# Prueba para listar productos vacíos
def test_get_all_products_empty(db_session: Session):
    response = client.get("/products")
    print(f"Get all products empty response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == []

# Prueba para manejar errores de validación al crear un producto
def test_create_product_invalid_price(db_session: Session):
    product_data = {
        "name": "Laptop",
        "price": -10.0,  # Precio inválido
        "stock": 10
    }
    response = client.post("/products", json=product_data)
    print(f"Invalid price response: {response.json()}")
    assert response.status_code == 422  # Pydantic validation error
    assert "Input should be greater than 0" in response.json()["detail"][0]["msg"]