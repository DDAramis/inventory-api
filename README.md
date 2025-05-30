API de Gestión de Inventario
API REST para gestionar productos y pedidos, desarrollada con FastAPI y PostgreSQL, siguiendo Clean Architecture y principios de CQRS. Este proyecto está diseñado para conectar proveedores y comercios, inspirado en plataformas como Harmony. Incluye soporte para múltiples entornos (local y en la nube), pruebas automatizadas, contenerización, y observabilidad, lo que lo hace ideal para demostrar habilidades de desarrollo backend profesional.
Características

Gestión de productos: Crea y lista productos con endpoints REST.
Clean Architecture: Código organizado en capas (dominio, aplicación, infraestructura).
CQRS: Separación de comandos (crear) y consultas (listar).
Soporte multi-entorno: Compatible con PostgreSQL local y Supabase.
Pruebas automatizadas: Tests unitarios con Pytest.
Contenerización: Docker y Docker Compose para despliegue.
Observabilidad: Monitoreo de errores con Sentry y métricas con Prometheus.

Tecnologías

FastAPI: Framework para la API REST.
PostgreSQL: Base de datos relacional (soporte para Supabase y PostgreSQL local).
SQLAlchemy: ORM para interactuar con la base de datos.
Pydantic: Validación de datos.
Pytest: Pruebas automatizadas.
Docker: Contenerización.
Sentry: Monitoreo de errores.
Prometheus: Métricas de observabilidad.

Instalación
Opción 1: Instalación manual

Clona el repositorio:
git clone https://github.com/DDAramis/inventory-api.git
cd inventory-api


Crea un entorno virtual e instala las dependencias:
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt


Configura las variables de entorno en un archivo .env:
ENVIRONMENT=development
DATABASE_URL_LOCAL=postgresql://postgres:[YOUR_LOCAL_PASSWORD]@localhost:xxxx/inventario
DATABASE_URL_SUPABASE=postgresql://[YOUR_SUPABASE_USER]:[YOUR_SUPABASE_PASSWORD]@[YOUR_SUPABASE_HOST]:xxxx/postgres?sslmode=require
PORT=8000
SENTRY_DSN=https://your-sentry-dsn@oYOUR_ORG_ID.ingest.us.sentry.io/YOUR_PROJECT_ID


Reemplaza [YOUR_LOCAL_PASSWORD] con la contraseña de tu usuario postgres local.
Reemplaza [YOUR_SUPABASE_USER], [YOUR_SUPABASE_PASSWORD], y [YOUR_SUPABASE_HOST] con las credenciales de tu base de datos Supabase.
Reemplaza SENTRY_DSN con el DSN de tu proyecto en Sentry.
Cambia ENVIRONMENT a production para usar Supabase, o mantén development para usar PostgreSQL local.


Ejecuta el servidor:
python -m src.main



Opción 2: Usar Docker

Asegúrate de tener Docker y Docker Compose instalados:
docker --version
docker-compose --version


Configura las variables de entorno en un archivo .env:
ENVIRONMENT=development
DATABASE_URL_LOCAL=postgresql://postgres:[YOUR_LOCAL_PASSWORD]@localhost:xxx/inventario
DATABASE_URL_SUPABASE=postgresql://[YOUR_SUPABASE_USER]:[YOUR_SUPABASE_PASSWORD]@[YOUR_SUPABASE_HOST]:xxxx/postgres?sslmode=require
PORT=8000
SENTRY_DSN=https://your-sentry-dsn@oYOUR_ORG_ID.ingest.us.sentry.io/YOUR_PROJECT_ID


Reemplaza los valores como se indica en la instalación manual.


Construye y ejecuta los contenedores:
docker-compose up --build


Para detener los contenedores:
docker-compose down


Para eliminar los datos de la base de datos:
docker-compose down -v



Accede a la API

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


Probar error para Sentry:
curl -X POST http://localhost:8000/products -H "Content-Type: application/json" -d '{"name": "Laptop", "price": -10, "stock": 10}'

Respuesta esperada:
{"detail":[{"type":"greater_than","loc":["body","price"],"msg":"Input should be greater than 0","input":-10.0,"ctx":{"gt":0}}]}

Verifica en tu panel de Sentry que el error se haya registrado.


Observabilidad
Monitoreo de errores con Sentry
Sentry captura errores y excepciones en la API. Si ocurre un error (como enviar un precio inválido), puedes verlo en tu panel de Sentry con detalles como el stack trace y la solicitud que lo causó.
Métricas con Prometheus
Prometheus recopila métricas sobre el rendimiento y uso de la API. Las métricas disponibles incluyen:

api_requests_total: Número total de solicitudes, etiquetado por método HTTP y endpoint.
api_request_latency_seconds: Latencia de las solicitudes en segundos, etiquetado por método HTTP y endpoint.

Acceder a Prometheus

Asegúrate de que los contenedores estén corriendo (ver Opción 2: Usar Docker).

Abre tu navegador y visita: http://localhost:9090

Consulta las métricas:

Número de solicitudes:
Consulta: api_requests_total{method="POST", endpoint="/products"}
Esto muestra cuántas solicitudes POST se han hecho al endpoint /products.


Latencia (percentil 95):
Consulta: histogram_quantile(0.95, sum(rate(api_request_latency_seconds_bucket{method="POST", endpoint="/products"}[5m])) by (le))
Esto muestra el percentil 95 de la latencia de las solicitudes POST a /products, útil para detectar cuellos de botella.


Tasa de solicitudes por segundo:
Consulta: rate(api_requests_total{method="POST", endpoint="/products"}[5m])
Esto muestra la tasa de solicitudes por segundo en los últimos 5 minutos.





Estas métricas te permiten monitorear el rendimiento y detectar problemas como picos de latencia o errores frecuentes.
Pruebas
El proyecto incluye pruebas automatizadas con Pytest. Para ejecutar las pruebas:

Asegúrate de que el entorno virtual está activado:
source venv/bin/activate  # En Windows: venv\Scripts\activate


Ejecuta las pruebas:
pytest tests/test_product_routes.py -v



Las pruebas cubren:

Verificación de rutas disponibles.
Creación de productos.
Listado de productos.
Validación de datos (por ejemplo, precios inválidos).

Estructura del proyecto
inventario-api/
├── src/
│   ├── api/                  # Endpoints de FastAPI (product_routes.py)
│   ├── application/          # Casos de uso (product_service.py)
│   ├── domain/               # Entidades (product.py)
│   ├── infrastructure/       # Implementaciones (database.py, product_repository.py)
│   └── main.py               # Punto de entrada
├── tests/                    # Pruebas (test_product_routes.py, conftest.py)
├── requirements.txt          # Dependencias
├── requirements.in           # Dependencias base (opcional, para pip-tools)
├── .env                      # Variables de entorno (no en Git)
├── .gitignore                # Archivos ignorados
├── pytest.ini                # Configuración de Pytest
├── Dockerfile                # Archivo para construir la imagen Docker
├── docker-compose.yml        # Configuración de Docker Compose
├── prometheus.yml            # Configuración de Prometheus
├── LICENSE                   # Licencia MIT
└── README.md                 # Documentación

Estado

Configuración inicial con FastAPI y PostgreSQL (Supabase y local) completada.
Entidad Product y conexión a base de datos implementadas.
Tabla products creada con columnas id, name, price, y stock.
Casos de uso (CreateProduct, GetAllProducts) implementados con CQRS.
Repositorio (SQLProductRepository) implementado para conectar con la base de datos.
Endpoints para crear y listar productos (POST /products, GET /products) disponibles.
Pruebas automatizadas con Pytest implementadas y funcionando.
Contenerización con Docker y Docker Compose implementada y funcionando.
Monitoreo de errores con Sentry implementado y funcionando.
Métricas de observabilidad con Prometheus implementadas y funcionando.

Contribución

Fork el repositorio y clónalo localmente:
git clone https://github.com/YOUR_USERNAME/inventory-api.git
cd inventory-api


Crea una rama para tu contribución:
git checkout -b feature/nueva-funcionalidad


Haz tus cambios y commitea:
git add .
git commit -m "Add nueva funcionalidad"


Sube tus cambios a tu fork:
git push origin feature/nueva-funcionalidad


Crea un Pull Request desde tu fork al repositorio principal, describiendo tus cambios.


Notas:

Sigue las convenciones de código existentes (PEP 8 para Python).
Añade pruebas para cualquier nueva funcionalidad.
Asegúrate de que todas las pruebas pasen antes de enviar tu PR (pytest tests/).

Autor

Aramis Jakolic
Email: ajkdwb@gmail.com
GitHub: https://github.com/DDAramis
Portafolio: aramisjakolic.com

Licencia
Este proyecto está licenciado bajo la Licencia MIT.
