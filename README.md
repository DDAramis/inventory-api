API de Gestión de Inventario
API REST para gestionar productos y pedidos, desarrollada con FastAPI, PostgreSQL, y siguiendo Clean Architecture y principios de CQRS. Este proyecto es en desarrollo backend, pruebas automatizadas, contenedores Docker, y observabilidad con Sentry y Prometheus. Está inspirado en plataformas que conectan proveedores y comercios, como Harmony.
Tecnologías

FastAPI: Framework para la API REST.
PostgreSQL: Base de datos relacional (usando Supabase).
SQLAlchemy: ORM para interactuar con la base de datos.
Pydantic: Validación de datos.
Pytest: Pruebas automatizadas.
Docker: Contenerización (pendiente de implementar).
Sentry: Monitoreo de errores (pendiente de implementar).
Prometheus: Métricas de observabilidad (pendiente de implementar).

Instalación

Clona el repositorio:git clone https://github.com/aramisjakolic/inventory-api.git
cd inventory-api


Crea un entorno virtual e instala las dependencias:python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt


Configura las variables de entorno en un archivo .env:PORT=8000
ENVIRONMENT=development
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@[db-host].supabase.co:5432/postgres

Reemplaza [YOUR-PASSWORD] y [db-host] con las credenciales de tu base de datos Supabase.
Ejecuta el servidor:python src/main.py


Accede a la API:
Endpoint inicial: http://localhost:8000
Documentación Swagger: http://localhost:8000/docs
Documentación ReDoc: http://localhost:8000/redoc



Estructura del proyecto
inventario-api/
├── src/
│   ├── api/                  # Endpoints de FastAPI
│   ├── application/          # Casos de uso
│   ├── domain/               # Entidades (ej. Product)
│   ├── infrastructure/       # Implementaciones (ej. base de datos)
│   └── main.py               # Punto de entrada
├── tests/                    # Pruebas
├── requirements.txt          # Dependencias
├── .env                      # Variables de entorno (no en Git)
├── .gitignore                # Archivos ignorados
├── LICENSE                   # Licencia MIT
└── README.md                 # Documentación

Estado

Configuración inicial con FastAPI y PostgreSQL (Supabase) completada.
Entidad Product y conexión a base de datos implementadas.
Tabla products creada con columnas id, name, price, y stock.
Pendiente: Casos de uso, endpoints, CQRS, pruebas automatizadas, Docker, Sentry, Prometheus.

Autor
Aramis JakolicEmail: ajkdwb@gmail.com.com GitHub: https://github.com/DDAramis  Portafolio: aramisjakolic.com
Licencia
Este proyecto está licenciado bajo la Licencia MIT.
