# EVM Dashboard

Aplicación fullstack para gestionar **proyectos** y **actividades** y calcular automáticamente los indicadores de **Valor Ganado** (Earned Value Management, EVM). Permite ver de un vistazo si un proyecto va bien o mal en costo y cronograma.

Prueba técnica de Ingeniero de Desarrollo — Trycore Colombia.

## Qué hace

- API REST para crear, editar y eliminar proyectos y actividades.
- Cada actividad guarda: nombre, BAC (presupuesto total), % de avance planificado, % de avance real y AC (costo real). Los porcentajes van de 0 a 100.
- Calcula por actividad **y** consolidado por proyecto: PV, EV, CV, SV, CPI, SPI, EAC y VAC, con la interpretación de CPI y SPI.
- Dashboard con tabla de actividades, indicadores del proyecto, semáforo de CPI y SPI, y gráfica PV vs EV vs AC por actividad.
- Documentación OpenAPI (Swagger) en `/api-docs`.

### Fórmulas

| Indicador | Fórmula |
|---|---|
| PV (Valor planificado) | % planificado × BAC |
| EV (Valor ganado) | % completado × BAC |
| CV (Variación de costo) | EV − AC |
| SV (Variación de cronograma) | EV − PV |
| CPI | EV / AC |
| SPI | EV / PV |
| EAC | BAC / CPI |
| VAC | BAC − EAC |

### Decisiones de negocio

- **Consolidado del proyecto:** se suman BAC, PV, EV y AC de todas las actividades y los índices se recalculan sobre esos totales (no se promedian los índices).
- **División por cero:** si un indicador no se puede calcular (por ejemplo, CPI con AC = 0), el API devuelve `null` y la interpretación es "No calculable".
- **Dinero:** se usa `Decimal` (no `float`). Los montos se redondean a 2 decimales y los índices a 4.
- **Indicadores al vuelo:** no se guardan en la base de datos; se calculan en cada consulta a partir de los datos base.

## Stack

- Backend: Python + FastAPI + SQLAlchemy + Pydantic
- Base de datos: PostgreSQL 17
- Frontend: React + Vite (JavaScript) + Recharts
- Calidad: pytest, pytest-cov, ruff (Python) y ESLint (frontend)

## Arquitectura

El backend está en tres capas, cada una con una sola responsabilidad:

```
Petición HTTP → routers → servicios → cálculos (funciones puras)
                              ↓
                      modelos (PostgreSQL)
```

- `backend/app/routers/`: reciben la petición y devuelven la respuesta. No contienen lógica de negocio.
- `backend/app/servicios/`: buscan en la base de datos, llaman a los cálculos y arman la respuesta.
- `backend/app/calculos/`: las fórmulas EVM como funciones puras (sin base de datos ni web).
- `backend/app/modelos.py` y `backend/app/esquemas.py`: tablas y validación de entrada/salida.
- `database/init.sql`: script de inicialización de la base de datos.
- `frontend/`: dashboard en React. No calcula nada: muestra lo que devuelve el API.

## Requisitos

- Python 3.13
- Node.js 22 o superior (probado con 26) y npm
- PostgreSQL 17 (con `psql` disponible en la terminal)

## Cómo correr el proyecto

Los comandos están escritos para Windows (PowerShell). Se ejecutan desde la carpeta raíz del proyecto, salvo que se indique otra cosa.

### 1. Base de datos

Crea las bases de datos (el sistema te pedirá la contraseña del usuario `postgres`):

```bash
psql -U postgres -c "CREATE DATABASE evm_db;"
psql -U postgres -c "CREATE DATABASE evm_db_test;"
```

Ejecuta el script de inicialización sobre la base principal. Crea las tablas `proyectos` y `actividades` y se puede ejecutar más de una vez sin problema:

```bash
psql -U postgres -d evm_db -f database/init.sql
```

`evm_db_test` solo la usan las pruebas, que crean sus tablas por su cuenta con el mismo script.

### 2. Configuración

Copia la plantilla y escribe en `.env` la contraseña de tu usuario `postgres` (reemplaza `CHANGE_ME`). El archivo `.env` no se sube a Git.

```bash
copy .env.example .env
```

### 3. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

El API queda en http://127.0.0.1:8000 y la documentación en http://127.0.0.1:8000/api-docs.

> No hace falta "activar" el entorno virtual: se usa directamente el Python de `.venv`. Así se evita la política de ejecución de scripts de PowerShell.

### 4. Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173. El frontend reenvía las llamadas `/api/...` al backend en el puerto 8000, así que el backend debe estar corriendo.

## Pruebas y calidad

Backend (desde `backend/`). Necesita las bases de datos creadas y el `.env` listo:

```bash
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m ruff format --check .
```

`pytest` mide la cobertura de la capa de negocio y falla si baja del 80 %.

Frontend (desde `frontend/`):

```bash
npm run lint
npm run build
```

## Endpoints

La documentación completa, con esquemas y códigos de error, está en `/api-docs`.

| Método y ruta | Qué hace |
|---|---|
| `POST /proyectos` | Crea un proyecto |
| `GET /proyectos` | Lista los proyectos |
| `GET /proyectos/{id}` | Consulta un proyecto |
| `PUT /proyectos/{id}` | Edita un proyecto |
| `DELETE /proyectos/{id}` | Elimina un proyecto y sus actividades |
| `POST /proyectos/{id}/actividades` | Crea una actividad |
| `GET /proyectos/{id}/actividades` | Lista las actividades con sus indicadores |
| `PUT /actividades/{id}` | Edita una actividad |
| `DELETE /actividades/{id}` | Elimina una actividad |
| `GET /proyectos/{id}/indicadores` | Indicadores consolidados del proyecto |

## Flujo de trabajo (Gitflow)

- `main`: producción.
- `develop`: integración.
- `feature/*`: una rama por funcionalidad, que entra a `develop` mediante Pull Request.
- `release/*`: preparación de cada versión antes de pasar a `main`.
- Los commits son descriptivos y en imperativo.

El proceso de desarrollo con IA está documentado en `AI_PROCESS.md`.
