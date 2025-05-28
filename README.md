API de Gestión de Inventario
API REST para gestionar productos y pedidos, desarrollada con FastAPI y PostgreSQL, siguiendo Clean Architecture y principios de CQRS. Este proyecto incluye desarrollo backend, soporte para múltiples entornos (local y en la nube), y está inspirado en plataformas que conectan proveedores y comercios, como Harmony.
Tecnologías

FastAPI: Framework para la API REST.
PostgreSQL: Base de datos relacional (soporte para Supabase y PostgreSQL local).
SQLAlchemy: ORM para interactuar con la base de datos.
Pydantic: Validación de datos.
Pytest: Pruebas automatizadas (en proceso de implementación).
Docker: Contenerización (pendiente de implementar).
Sentry: Monitoreo de errores (pendiente de implementar).
Prometheus: Métricas de observabilidad (pendiente de implementar).

Instalación

Clona el repositorio:
git clone https://github.com/aramisjakolic/inventory-api.git
cd inventory-api


Crea un entorno virtual e instala las dependencias:
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt


Configura las variables de entorno en un archivo .env:
PORT=8000
ENVIRONMENT=development
DATABASE_URL_LOCAL=postgresql://postgres:[YOUR_LOCAL_PASSWORD]@localhost:5432/inventario
DATABASE_URL_SUPABASE=postgresql://[YOUR_SUPABASE_USER]:[YOUR_SUPABASE_PASSWORD]@[YOUR_SUPABASE_HOST]:5432/postgres?sslmode=require


Reemplaza [YOUR_LOCAL_PASSWORD] con la contraseña de tu usuario postgres local.
Reemplaza [YOUR_SUPABASE_USER], [YOUR_SUPABASE_PASSWORD], y [YOUR_SUPABASE_HOST] con las credenciales de tu base de datos Supabase.
Cambia ENVIRONMENT a production para usar Supabase, o mantén development para usar PostgreSQL local.


Ejecuta el servidor:
python -m src.main


Accede a la API:

Endpoint inicial: http://localhost:8000
Documentación Swagger: http://localhost:8000/docs
Documentación ReDoc: http://localhost:8000/redoc



Uso
La API permite gestionar productos con los siguientes endpoints:

POST /products: Crear un producto.
curl -X POST http://localhost:8000/products -H "Content-Type: application/json" -d '{"name": "Laptop", "price": 999.99, "stock": 10}'

Respuesta esperada:
{"id": 1, "name": "Laptop", "price": 999.99, "stock": 10}


GET /products: Listar todos los productos.
curl http://localhost:8000/products

Respuesta esperada:
[{"id": 1, "name": "Laptop", "price": 999.99, "stock": 10}]



Estructura del proyecto
inventario-api/
├── src/
│   ├── api/                  # Endpoints de FastAPI (product_routes.py)
│   ├── application/          # Casos de uso (product_service.py)
│   ├── domain/               # Entidades (product.py)
│   ├── infrastructure/       # Implementaciones (database.py, product_repository.py)
│   └── main.py               # Punto de entrada
├── tests/                    # Pruebas (pendiente de implementar)
├── requirements.txt          # Dependencias
├── .env                      # Variables de entorno (no en Git)
├── .gitignore                # Archivos ignorados
├── LICENSE                   # Licencia MIT
└── README.md                 # Documentación

Estado

Configuración inicial con FastAPI y PostgreSQL (Supabase y local) completada.
Entidad Product y conexión a base de datos implementadas.
Tabla products creada con columnas id, name, price, y stock.
Casos de uso (CreateProduct, GetAllProducts) implementados con CQRS.
Repositorio (SQLProductRepository) implementado para conectar con la base de datos.
Endpoints para crear y listar productos (POST /products, GET /products) disponibles.
Pendiente: Pruebas automatizadas con Pytest, contenerización con Docker, observabilidad con Sentry y Prometheus.

Autor

Aramis Jakolic
Email: ajkdwb@gmail.com
GitHub: https://github.com/DDAramis
Portafolio: aramisjakolic.com

Licencia
Este proyecto está licenciado bajo la Licencia MIT.
