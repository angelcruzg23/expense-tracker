# 💰 Expense Tracker - Control de Gastos

Aplicación web completa para gestionar gastos personales, presupuestos, ingresos y cuentas bancarias. Accesible desde cualquier dispositivo.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

🌐 **Demo en vivo**: https://expense-tracker-r2r2.onrender.com/

---

## ✨ Características

### 📊 Gestión de Gastos
- ✅ Registro rápido de gastos con categorías y subcategorías
- ✅ Asociación de gastos a medios de pago (débito/crédito)
- ✅ Vista mensual con filtros por fecha
- ✅ Eliminación de gastos con confirmación

### 🏷️ Categorías Personalizables
- ✅ 9 categorías predefinidas con iconos emoji
- ✅ Crear categorías personalizadas
- ✅ Asignar colores e iconos personalizados
- ✅ Gestión completa de subcategorías

### 💳 Presupuestos Mensuales
- ✅ Configurar presupuesto por categoría
- ✅ Vista comparativa: Presupuesto vs Gastado
- ✅ Indicadores de progreso con semáforo (verde/amarillo/rojo)
- ✅ Gráficos interactivos con Chart.js

### 🏦 Gestión Bancaria Completa
- ✅ Crear y gestionar bancos
- ✅ Medios de pago (tarjetas débito/crédito)
- ✅ **Cuentas bancarias** con saldos separados:
  - Saldo Transaccional (dinero del día a día)
  - Saldo Ahorros (dinero ahorrado)
- ✅ Vista de resumen consolidado de todas las cuentas
- ✅ Actualización en tiempo real de saldos

### 💵 Registro de Ingresos
- ✅ Registrar ingresos por categoría:
  - Salario, Freelance, Inversiones, Negocio, Bonificación, Otro
- ✅ Asociar ingresos a cuentas bancarias específicas
- ✅ Actualización automática de saldos al registrar ingresos
- ✅ Vista mensual de ingresos totales
- ✅ Lista de ingresos recientes con paginación

### 📱 Diseño Responsive
- ✅ Adaptable para móvil, tablet y desktop
- ✅ Interfaz moderna con Tailwind CSS
- ✅ Componentes interactivos con Alpine.js
- ✅ **Configurado para funcionar en producción (Render)**

---

## 🚀 Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos ligera
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

### Frontend
- **HTML5 + Tailwind CSS**: Interfaz moderna y responsive
- **Alpine.js**: Reactividad sin build step
- **Chart.js**: Gráficos interactivos
- **Fetch API**: Comunicación con backend
- **Configuración dinámica**: Usa `window.location.origin` para detectar automáticamente la URL de la API

---

## 📦 Instalación Local

### Prerequisitos
- Python 3.11 o superior
- pip

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/expense-tracker.git
   cd expense-tracker
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Abrir en el navegador**
   - **Aplicación Web**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

---

## 🌐 Despliegue en Render

**¡Despliega tu propia instancia gratis en Render.com!**

📖 **Guía completa de despliegue**: [DEPLOY.md](./DEPLOY.md)

### Resumen rápido:
1. Push tu código a GitHub
2. Ve a [Render Dashboard](https://dashboard.render.com/)
3. Conecta tu repositorio
4. Render detectará automáticamente `render.yaml`
5. ¡Tu app estará en línea en minutos!

**Configuración ya incluida:**
- ✅ `render.yaml` con configuración de servicio
- ✅ `requirements.txt` actualizado
- ✅ Frontend configurado con `window.location.origin`
- ✅ CORS habilitado para todas las origins

---

## 📁 Estructura del Proyecto

```
expense-tracker/
├── backend/
│   ├── __init__.py
│   ├── main.py                   # App FastAPI + endpoints
│   ├── models.py                 # Modelos de BD
│   ├── schemas.py                # Esquemas Pydantic
│   ├── crud.py                   # CRUD básico
│   ├── crud_financiero.py        # CRUD módulos financieros
│   ├── endpoints_financiero.py   # Endpoints ingresos/cuentas
│   └── database.py               # Config SQLAlchemy
├── frontend/
│   ├── static/
│   │   └── js/
│   │       └── app.js            # Lógica Alpine.js
│   └── templates/
│       └── index.html            # Página principal (SPA)
├── requirements.txt              # Dependencias Python
├── render.yaml                   # Config para Render
├── .gitignore
├── README.md                     # Este archivo
├── DEPLOY.md                     # Guía de despliegue
└── CLAUDE.md                     # Especificaciones técnicas
```

---

## 🎯 Guía de Uso

### 1️⃣ Configuración Inicial

1. **Configurar Bancos**
   - Click en "🏦 Bancos"
   - Agregar bancos (ej: Bancolombia, Nequi, etc.)

2. **Crear Cuentas Bancarias**
   - Click en "🏦 Cuentas Bancarias"
   - Crear cuentas con saldos iniciales (transaccional y ahorros)

3. **Configurar Categorías**
   - Click en "Categorías"
   - Personalizar iconos, colores y nombres
   - Crear categorías adicionales si es necesario

4. **Establecer Presupuestos**
   - Click en "Presupuestos"
   - Asignar presupuesto mensual a cada categoría

### 2️⃣ Uso Diario

1. **Registrar Gastos**
   - Formulario siempre visible en la página principal
   - Seleccionar fecha, monto, categoría
   - Opcional: medio de pago y banco
   - Click en "Registrar Gasto"

2. **Registrar Ingresos**
   - Click en "💵 Ingresos"
   - Completar formulario de ingreso
   - Seleccionar cuenta bancaria destino
   - El saldo se actualiza automáticamente

3. **Monitorear Finanzas**
   - Ver gráficos: Click en "Ver Gráficos"
   - Revisar tabla "Presupuesto vs Gastos" (expandible)
   - Verificar saldos en "Cuentas Bancarias"

---

## 🔧 API Endpoints

### Categorías
```
GET    /categorias          # Listar categorías
POST   /categorias          # Crear categoría
PUT    /categorias/{id}     # Actualizar categoría
DELETE /categorias/{id}     # Eliminar categoría
```

### Gastos
```
GET    /gastos?mes=&anio=   # Listar gastos filtrados
POST   /gastos              # Crear gasto
DELETE /gastos/{id}         # Eliminar gasto
```

### Resumen
```
GET /resumen?mes=&anio=     # Resumen mensual
```

### Financiero
```
GET    /bancos              # Listar bancos
POST   /bancos              # Crear banco
GET    /medios-pago         # Listar medios de pago
POST   /medios-pago         # Crear medio de pago
GET    /cuentas-bancarias   # Listar cuentas
POST   /cuentas-bancarias   # Crear cuenta
PUT    /cuentas-bancarias/{id}  # Actualizar saldos
GET    /ingresos?mes=&anio= # Listar ingresos
POST   /ingresos            # Crear ingreso
```

Documentación completa en: `http://localhost:8000/docs`

---

## 🗃️ Base de Datos

SQLite con las siguientes tablas:

- `categorias` - Categorías de gastos con iconos y colores
- `subcategorias` - Subcategorías por categoría
- `gastos` - Registro de gastos
- `bancos` - Bancos disponibles
- `medios_pago` - Tarjetas débito/crédito
- `cuentas_bancarias` - Cuentas con saldos (transaccional/ahorros)
- `ingresos` - Registro de ingresos
- `transferencias` - Movimientos entre cuentas (futuro)

La base de datos se crea automáticamente al iniciar la aplicación.

---

## 🐛 Solución de Problemas

### Error: "Error al cargar las categorías" en móvil

**Causa**: Problema de CORS o configuración de API URL

**Solución**:
1. Verifica la consola del navegador (F12)
2. Debe mostrar: `🔧 API URL configurada: https://tu-url.onrender.com`
3. Si muestra `http://localhost:8000`, limpia caché del navegador
4. Verifica que estés usando HTTPS (no HTTP)

### La aplicación se tarda en cargar en Render

**Causa**: Plan gratuito de Render se duerme tras 15 min de inactividad

**Solución**: Espera 30-60 segundos la primera vez. Es normal.

### Cambios no se reflejan después de redesplegar

**Solución**:
1. Limpia caché del navegador (Ctrl+Shift+Delete)
2. Abre en ventana de incógnito
3. En Render, ve a "Manual Deploy" → "Clear build cache & deploy"

---

## 🤝 Contribuir

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

---

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- Tailwind CSS por el sistema de diseño moderno
- Alpine.js por la reactividad simple y poderosa
- Chart.js por los gráficos interactivos
- Render por el hosting gratuito

---

## 📞 Soporte

Si encuentras bugs o tienes sugerencias:
1. Abre un [Issue](https://github.com/tu-usuario/expense-tracker/issues)
2. Describe el problema con detalles
3. Incluye capturas de pantalla si es relevante

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**
