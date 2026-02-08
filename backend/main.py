from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from pathlib import Path

from backend import models, schemas, crud
from backend.database import engine, get_db
from backend.endpoints_financiero import router as financiero_router

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="API para control de gastos domésticos",
    version="1.0.0"
)

# Incluir routers
app.include_router(financiero_router, tags=["Financiero"])

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos y templates
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))


# Inicializar categorías y bancos predefinidos
@app.on_event("startup")
def startup_event():
    from backend import crud_financiero

    db = next(get_db())

    # Inicializar categorías
    categorias_iniciales = [
        {"nombre": "Alimentación", "color": "#10B981", "presupuesto_mensual": 0.0, "icono": "🍔"},
        {"nombre": "Servicios", "color": "#3B82F6", "presupuesto_mensual": 0.0, "icono": "💡"},
        {"nombre": "Transporte", "color": "#F59E0B", "presupuesto_mensual": 0.0, "icono": "🚗"},
        {"nombre": "Salud", "color": "#EF4444", "presupuesto_mensual": 0.0, "icono": "❤️"},
        {"nombre": "Educación", "color": "#8B5CF6", "presupuesto_mensual": 0.0, "icono": "📚"},
        {"nombre": "Entretenimiento", "color": "#EC4899", "presupuesto_mensual": 0.0, "icono": "🎬"},
        {"nombre": "Hogar", "color": "#06B6D4", "presupuesto_mensual": 0.0, "icono": "🏠"},
        {"nombre": "Impuestos", "color": "#64748B", "presupuesto_mensual": 0.0, "icono": "📄"},
        {"nombre": "Otros", "color": "#9CA3AF", "presupuesto_mensual": 0.0, "icono": "💰"},
    ]

    for cat_data in categorias_iniciales:
        if not crud.get_categoria_by_nombre(db, cat_data["nombre"]):
            crud.create_categoria(db, schemas.CategoriaCreate(**cat_data))

    # Inicializar bancos
    bancos_iniciales = ["Bancolombia", "Nequi", "Banco Falabella", "Davivienda", "BBVA"]

    for banco_nombre in bancos_iniciales:
        bancos_existentes = crud_financiero.get_bancos(db)
        if not any(b.nombre == banco_nombre for b in bancos_existentes):
            crud_financiero.create_banco(db, schemas.BancoCreate(nombre=banco_nombre))


# Endpoints raíz
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Servir la aplicación web"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api")
def api_root():
    """Información de la API"""
    return {
        "message": "Expense Tracker API",
        "version": "1.0.0",
        "endpoints": {
            "categorias": "/categorias",
            "subcategorias": "/subcategorias",
            "gastos": "/gastos",
            "resumen": "/resumen"
        }
    }


# ========== ENDPOINTS CATEGORÍAS ==========
@app.get("/categorias", response_model=list[schemas.CategoriaConSubcategorias])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categorias(db, skip=skip, limit=limit)


@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaConSubcategorias)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.get_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@app.post("/categorias", response_model=schemas.Categoria, status_code=201)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria_by_nombre(db, categoria.nombre)
    if db_categoria:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    return crud.create_categoria(db, categoria)


@app.put("/categorias/{categoria_id}", response_model=schemas.Categoria)
def actualizar_categoria(
    categoria_id: int,
    categoria: schemas.CategoriaUpdate,
    db: Session = Depends(get_db)
):
    db_categoria = crud.update_categoria(db, categoria_id, categoria)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria


@app.delete("/categorias/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    if not crud.delete_categoria(db, categoria_id):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")


# ========== ENDPOINTS SUBCATEGORÍAS ==========
@app.get("/subcategorias", response_model=list[schemas.Subcategoria])
def listar_subcategorias(
    categoria_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_subcategorias(db, categoria_id=categoria_id, skip=skip, limit=limit)


@app.get("/subcategorias/{subcategoria_id}", response_model=schemas.Subcategoria)
def obtener_subcategoria(subcategoria_id: int, db: Session = Depends(get_db)):
    subcategoria = crud.get_subcategoria(db, subcategoria_id)
    if not subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    return subcategoria


@app.post("/subcategorias", response_model=schemas.Subcategoria, status_code=201)
def crear_subcategoria(subcategoria: schemas.SubcategoriaCreate, db: Session = Depends(get_db)):
    # Verificar que la categoría existe
    if not crud.get_categoria(db, subcategoria.categoria_id):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return crud.create_subcategoria(db, subcategoria)


@app.put("/subcategorias/{subcategoria_id}", response_model=schemas.Subcategoria)
def actualizar_subcategoria(
    subcategoria_id: int,
    subcategoria: schemas.SubcategoriaUpdate,
    db: Session = Depends(get_db)
):
    db_subcategoria = crud.update_subcategoria(db, subcategoria_id, subcategoria)
    if not db_subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    return db_subcategoria


@app.delete("/subcategorias/{subcategoria_id}", status_code=204)
def eliminar_subcategoria(subcategoria_id: int, db: Session = Depends(get_db)):
    if not crud.delete_subcategoria(db, subcategoria_id):
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")


# ========== ENDPOINTS GASTOS ==========
@app.get("/gastos", response_model=list[schemas.GastoDetallado])
def listar_gastos(
    categoria_id: Optional[int] = None,
    mes: Optional[int] = Query(None, ge=1, le=12),
    anio: Optional[int] = Query(None, ge=2000),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_gastos(db, categoria_id=categoria_id, mes=mes, anio=anio, skip=skip, limit=limit)


@app.get("/gastos/{gasto_id}", response_model=schemas.GastoDetallado)
def obtener_gasto(gasto_id: int, db: Session = Depends(get_db)):
    gasto = crud.get_gasto(db, gasto_id)
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return gasto


@app.post("/gastos", response_model=schemas.Gasto, status_code=201)
def crear_gasto(gasto: schemas.GastoCreate, db: Session = Depends(get_db)):
    # Verificar que la categoría existe
    if not crud.get_categoria(db, gasto.categoria_id):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Verificar subcategoría si se proporciona
    if gasto.subcategoria_id and not crud.get_subcategoria(db, gasto.subcategoria_id):
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")

    return crud.create_gasto(db, gasto)


@app.put("/gastos/{gasto_id}", response_model=schemas.Gasto)
def actualizar_gasto(
    gasto_id: int,
    gasto: schemas.GastoUpdate,
    db: Session = Depends(get_db)
):
    db_gasto = crud.update_gasto(db, gasto_id, gasto)
    if not db_gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return db_gasto


@app.delete("/gastos/{gasto_id}", status_code=204)
def eliminar_gasto(gasto_id: int, db: Session = Depends(get_db)):
    if not crud.delete_gasto(db, gasto_id):
        raise HTTPException(status_code=404, detail="Gasto no encontrado")


# ========== ENDPOINT RESUMEN ==========
@app.get("/resumen")
def obtener_resumen(
    mes: int = Query(..., ge=1, le=12),
    anio: int = Query(..., ge=2000),
    db: Session = Depends(get_db)
):
    """Obtiene resumen de gastos vs presupuesto por categoría"""
    resumen = crud.get_gastos_por_categoria_mes(db, mes, anio)

    resultado = []
    total_presupuesto = 0.0
    total_gastado = 0.0

    for nombre, presupuesto, color, gastado in resumen:
        gastado = gastado or 0.0
        total_presupuesto += presupuesto
        total_gastado += gastado

        resultado.append({
            "categoria": nombre,
            "presupuesto_mensual": presupuesto,
            "total_gastado": gastado,
            "diferencia": presupuesto - gastado,
            "porcentaje_usado": (gastado / presupuesto * 100) if presupuesto > 0 else 0,
            "color": color
        })

    return {
        "mes": mes,
        "anio": anio,
        "categorias": resultado,
        "totales": {
            "presupuesto_total": total_presupuesto,
            "gastado_total": total_gastado,
            "diferencia_total": total_presupuesto - total_gastado
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
