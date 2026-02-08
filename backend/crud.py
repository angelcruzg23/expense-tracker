from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from typing import Optional
from datetime import date
from backend import models, schemas


# CRUD para Categorías
def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()


def get_categoria_by_nombre(db: Session, nombre: str):
    return db.query(models.Categoria).filter(models.Categoria.nombre == nombre).first()


def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()


def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def update_categoria(db: Session, categoria_id: int, categoria: schemas.CategoriaUpdate):
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        update_data = categoria.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_categoria, key, value)
        db.commit()
        db.refresh(db_categoria)
    return db_categoria


def delete_categoria(db: Session, categoria_id: int):
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
        return True
    return False


# CRUD para Subcategorías
def get_subcategoria(db: Session, subcategoria_id: int):
    return db.query(models.Subcategoria).filter(models.Subcategoria.id == subcategoria_id).first()


def get_subcategorias(db: Session, categoria_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Subcategoria)
    if categoria_id:
        query = query.filter(models.Subcategoria.categoria_id == categoria_id)
    return query.offset(skip).limit(limit).all()


def create_subcategoria(db: Session, subcategoria: schemas.SubcategoriaCreate):
    db_subcategoria = models.Subcategoria(**subcategoria.model_dump())
    db.add(db_subcategoria)
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria


def update_subcategoria(db: Session, subcategoria_id: int, subcategoria: schemas.SubcategoriaUpdate):
    db_subcategoria = get_subcategoria(db, subcategoria_id)
    if db_subcategoria:
        update_data = subcategoria.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_subcategoria, key, value)
        db.commit()
        db.refresh(db_subcategoria)
    return db_subcategoria


def delete_subcategoria(db: Session, subcategoria_id: int):
    db_subcategoria = get_subcategoria(db, subcategoria_id)
    if db_subcategoria:
        db.delete(db_subcategoria)
        db.commit()
        return True
    return False


# CRUD para Gastos
def get_gasto(db: Session, gasto_id: int):
    return db.query(models.Gasto).filter(models.Gasto.id == gasto_id).first()


def get_gastos(
    db: Session,
    categoria_id: Optional[int] = None,
    mes: Optional[int] = None,
    anio: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Gasto)

    if categoria_id:
        query = query.filter(models.Gasto.categoria_id == categoria_id)

    if mes:
        query = query.filter(extract('month', models.Gasto.fecha) == mes)

    if anio:
        query = query.filter(extract('year', models.Gasto.fecha) == anio)

    return query.order_by(models.Gasto.fecha.desc()).offset(skip).limit(limit).all()


def create_gasto(db: Session, gasto: schemas.GastoCreate):
    db_gasto = models.Gasto(**gasto.model_dump())
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto


def update_gasto(db: Session, gasto_id: int, gasto: schemas.GastoUpdate):
    db_gasto = get_gasto(db, gasto_id)
    if db_gasto:
        update_data = gasto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_gasto, key, value)
        db.commit()
        db.refresh(db_gasto)
    return db_gasto


def delete_gasto(db: Session, gasto_id: int):
    db_gasto = get_gasto(db, gasto_id)
    if db_gasto:
        db.delete(db_gasto)
        db.commit()
        return True
    return False


def get_gastos_por_categoria_mes(db: Session, mes: int, anio: int):
    """Obtiene el total de gastos por categoría en un mes específico
    Incluye TODAS las categorías, incluso las que no tienen gastos"""

    # Subconsulta para obtener gastos del mes
    gastos_mes = db.query(
        models.Gasto.categoria_id,
        func.sum(models.Gasto.monto).label('total_gastado')
    ).filter(
        extract('month', models.Gasto.fecha) == mes,
        extract('year', models.Gasto.fecha) == anio
    ).group_by(
        models.Gasto.categoria_id
    ).subquery()

    # LEFT JOIN para incluir todas las categorías
    return db.query(
        models.Categoria.nombre,
        models.Categoria.presupuesto_mensual,
        models.Categoria.color,
        func.coalesce(gastos_mes.c.total_gastado, 0).label('total_gastado')
    ).outerjoin(
        gastos_mes, models.Categoria.id == gastos_mes.c.categoria_id
    ).order_by(
        models.Categoria.id
    ).all()
