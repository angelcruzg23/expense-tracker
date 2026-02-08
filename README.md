# Expense Tracker - Control de Gastos Domésticos

Aplicación web para controlar gastos del hogar, accesible desde móvil y desktop.

## Stack Tecnológico

- **Backend**: FastAPI + SQLite
- **Frontend**: HTML + Tailwind CSS + Alpine.js
- **Python**: 3.10+

## Instalación y Uso

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Ejecutar el servidor:**
```bash
python -m uvicorn backend.main:app --reload
```

3. **Acceder a la aplicación:**
   - **Aplicación Web**: http://localhost:8000
   - **API**: http://localhost:8000/api
   - **Documentación API**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

## Características de la Aplicación Web

### Dashboard Principal
- 📊 Resumen de presupuesto total, gastado y disponible
- 📅 Selector de mes y año para filtrar gastos
- 🎨 Diseño responsive (móvil y desktop)

### Registro de Gastos
- Formulario intuitivo para registrar gastos
- Selección de categoría y subcategoría
- Validación de datos en tiempo real

### Visualización
- 📈 Gráfico de barras comparando gastos vs presupuesto por categoría
- 📋 Tabla detallada de gastos por categoría
- Indicadores visuales de progreso (barras de progreso con colores)
- 🚨 Alertas visuales cuando se acerca al límite del presupuesto

### Gestión de Presupuestos
- Editar presupuesto mensual por categoría
- Ver diferencia entre presupuesto y gasto real
- Porcentaje de uso del presupuesto

### Lista de Gastos
- Tabla de gastos recientes
- Filtros por mes y año
- Eliminar gastos individuales
- Ver todos o limitar a 10 más recientes

## Endpoints Principales

### Categorías
- `GET /categorias` - Listar todas las categorías
- `POST /categorias` - Crear nueva categoría
- `PUT /categorias/{id}` - Actualizar categoría
- `DELETE /categorias/{id}` - Eliminar categoría

### Subcategorías
- `GET /subcategorias` - Listar subcategorías (filtrar por categoria_id opcional)
- `POST /subcategorias` - Crear subcategoría
- `PUT /subcategorias/{id}` - Actualizar subcategoría
- `DELETE /subcategorias/{id}` - Eliminar subcategoría

### Gastos
- `GET /gastos` - Listar gastos (filtros: categoria_id, mes, anio)
- `POST /gastos` - Registrar nuevo gasto
- `PUT /gastos/{id}` - Actualizar gasto
- `DELETE /gastos/{id}` - Eliminar gasto

### Resumen
- `GET /resumen?mes={mes}&anio={anio}` - Obtener resumen de gastos vs presupuesto

## Estructura del Proyecto

```
expense-tracker/
├── backend/
│   ├── __init__.py
│   ├── main.py          # Aplicación FastAPI y endpoints
│   ├── models.py        # Modelos SQLAlchemy
│   ├── database.py      # Configuración de base de datos
│   ├── crud.py          # Operaciones CRUD
│   └── schemas.py       # Schemas Pydantic
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css
│   │   └── js/
│   │       └── app.js   # Lógica Alpine.js
│   └── templates/
│       └── index.html   # Interfaz web principal
├── .gitignore
├── requirements.txt
├── CLAUDE.md
└── README.md
```

## Categorías Predefinidas

El sistema inicializa automáticamente las siguientes categorías:
- Alimentación
- Servicios
- Transporte
- Salud
- Educación
- Entretenimiento
- Hogar
- Impuestos
- Otros

## Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para manejo de base de datos
- **Pydantic**: Validación de datos
- **SQLite**: Base de datos local

### Frontend
- **HTML5**: Estructura semántica
- **Tailwind CSS**: Framework CSS utility-first
- **Alpine.js**: Framework JavaScript reactivo y ligero
- **Chart.js**: Gráficos interactivos

## Base de Datos

SQLite local (`expense_tracker.db`) se crea automáticamente al iniciar la aplicación.

## Desarrollo

La aplicación está diseñada para ser simple y directa:
- No requiere autenticación (MVP)
- Base de datos local (un solo usuario)
- Interfaz responsive para uso en móvil y desktop
- API RESTful bien documentada

## Próximas Funcionalidades

- [ ] Exportar datos a Excel/CSV
- [ ] Gráficos de tendencias mensuales
- [ ] Categorías y subcategorías personalizadas
- [ ] Notas y adjuntos para gastos
- [ ] Modo oscuro
- [ ] Multi-usuario con autenticación
