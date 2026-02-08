# Expense Tracker - Control de Gastos Domésticos

## Objetivo
Aplicación web para controlar gastos del hogar, accesible desde móvil y desktop.

## Stack Tecnológico
- **Backend**: FastAPI + SQLite
- **Frontend**: HTML + Tailwind CSS + Alpine.js
- **Python**: 3.10+

## Estructura de Datos

### Categorías (basadas en plantilla Excel)
- Alimentación
- Servicios
- Transporte
- Salud
- Educación
- Entretenimiento
- Hogar
- Impuestos
- Otros

### Modelos de Base de Datos

**Categorías**
- id (PK)
- nombre
- presupuesto_mensual
- color (para gráficos)

**Subcategorías**
- id (PK)
- nombre
- categoria_id (FK)

**Gastos**
- id (PK)
- fecha
- monto
- descripcion
- categoria_id (FK)
- subcategoria_id (FK)
- created_at

## Funcionalidades MVP
1. Registrar gastos con categoría y subcategoría
2. Ver gastos del mes actual
3. Comparar gasto vs presupuesto por categoría
4. Gráfico de tendencias mensuales
5. Alertas cuando se acerca al límite del presupuesto

## Estructura de Carpetas
```
expense-tracker/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── crud.py
│   └── schemas.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       └── index.html
├── requirements.txt
├── CLAUDE.md
└── README.md
```

## Comandos de Desarrollo

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar servidor de desarrollo
```bash
python -m uvicorn backend.main:app --reload
```

### URLs de la Aplicación
- **App Web**: http://localhost:8000
- **API Info**: http://localhost:8000/api
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Arquitectura Backend

### Capa de Base de Datos (`backend/database.py`)
- SQLAlchemy con SQLite
- Base de datos: `expense_tracker.db` (creada automáticamente)
- Session management con dependency injection

### Modelos (`backend/models.py`)
- **Categoria**: Categorías principales con presupuesto y color
- **Subcategoria**: Subcategorías asociadas a categorías (relación 1:N)
- **Gasto**: Registros de gastos con fecha, monto y descripción
- Relaciones: Categoria 1:N Subcategoria, Categoria 1:N Gasto, Subcategoria 1:N Gasto

### Schemas (`backend/schemas.py`)
- Validación con Pydantic
- Schemas separados para Create, Update y Response
- `GastoDetallado`: incluye objetos de categoría y subcategoría completos
- `CategoriaConSubcategorias`: incluye lista de subcategorías

### CRUD (`backend/crud.py`)
- Operaciones de base de datos separadas de endpoints
- Filtros por mes/año para gastos
- `get_gastos_por_categoria_mes()`: agregación para resúmenes

### API Endpoints (`backend/main.py`)
- RESTful endpoints para Categorías, Subcategorías y Gastos
- Endpoint `/resumen`: calcula gastos vs presupuesto por categoría
- Las 9 categorías predefinidas se inicializan automáticamente en startup
- CORS habilitado para desarrollo frontend

## Arquitectura Frontend

### Templates (`frontend/templates/`)
- **index.html**: SPA (Single Page Application) principal
  - Usa Alpine.js para reactividad
  - Tailwind CSS para estilos (CDN)
  - Chart.js para gráficos

### JavaScript (`frontend/static/js/app.js`)
- **expenseTracker()**: Función Alpine.js principal con estado global
- **Estado**: gastos, categorías, subcategorías, resumen
- **Métodos CRUD**: crear/leer/eliminar gastos, actualizar presupuestos
- **Utilidades**: formateo de moneda y fechas
- Usa Fetch API para comunicarse con backend

### CSS (`frontend/static/css/custom.css`)
- Estilos personalizados y animaciones
- Optimizaciones para móvil
- Scrollbar customizado

### Integración Backend-Frontend
- FastAPI sirve archivos estáticos con `StaticFiles`
- Jinja2Templates para renderizar index.html
- Endpoint raíz (`/`) sirve la app web
- API REST en endpoints `/categorias`, `/gastos`, etc.

## Funcionalidades Implementadas

### MVP Completo ✅
1. ✅ Registrar gastos con categoría y subcategoría
2. ✅ Ver gastos del mes actual (filtrable por mes/año)
3. ✅ Comparar gasto vs presupuesto por categoría
4. ✅ Gráfico de barras (gastos vs presupuesto)
5. ✅ Alertas visuales cuando se acerca al límite del presupuesto (colores en barras de progreso)

### Características Adicionales
- Dashboard con resumen de totales
- Edición de presupuestos por categoría
- Eliminación de gastos
- Tabla de gastos recientes con paginación
- Diseño responsive (móvil y desktop)
- Indicadores visuales con colores por categoría

## Notas de Desarrollo
- Sin autenticación en MVP
- Base de datos SQLite local (`expense_tracker.db`)
- Las categorías iniciales se crean automáticamente al iniciar la app
- Los colores de categorías están en formato Tailwind CSS (hex)
- Alpine.js maneja la reactividad sin necesidad de build step
- CDNs para librerías (no hay bundle/build process)