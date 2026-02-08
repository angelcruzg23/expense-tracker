from sqlalchemy.orm import Session
from typing import Optional
from backend import models, schemas


# ========== CRUD BANCOS ==========
def get_banco(db: Session, banco_id: int):
    return db.query(models.Banco).filter(models.Banco.id == banco_id).first()


def get_bancos(db: Session, activo: Optional[bool] = None):
    query = db.query(models.Banco)
    if activo is not None:
        query = query.filter(models.Banco.activo == (1 if activo else 0))
    return query.all()


def create_banco(db: Session, banco: schemas.BancoCreate):
    db_banco = models.Banco(**banco.model_dump())
    db.add(db_banco)
    db.commit()
    db.refresh(db_banco)
    return db_banco


def update_banco(db: Session, banco_id: int, banco: schemas.BancoUpdate):
    db_banco = get_banco(db, banco_id)
    if db_banco:
        update_data = banco.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_banco, key, value)
        db.commit()
        db.refresh(db_banco)
    return db_banco


def delete_banco(db: Session, banco_id: int):
    db_banco = get_banco(db, banco_id)
    if db_banco:
        db.delete(db_banco)
        db.commit()
        return True
    return False


# ========== CRUD MEDIOS DE PAGO ==========
def get_medio_pago(db: Session, medio_pago_id: int):
    return db.query(models.MedioPago).filter(models.MedioPago.id == medio_pago_id).first()


def get_medios_pago(db: Session, banco_id: Optional[int] = None, activo: Optional[bool] = None):
    query = db.query(models.MedioPago)
    if banco_id:
        query = query.filter(models.MedioPago.banco_id == banco_id)
    if activo is not None:
        query = query.filter(models.MedioPago.activo == (1 if activo else 0))
    return query.all()


def create_medio_pago(db: Session, medio_pago: schemas.MedioPagoCreate):
    db_medio_pago = models.MedioPago(**medio_pago.model_dump())
    db.add(db_medio_pago)
    db.commit()
    db.refresh(db_medio_pago)
    return db_medio_pago


def update_medio_pago(db: Session, medio_pago_id: int, medio_pago: schemas.MedioPagoUpdate):
    db_medio_pago = get_medio_pago(db, medio_pago_id)
    if db_medio_pago:
        update_data = medio_pago.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_medio_pago, key, value)
        db.commit()
        db.refresh(db_medio_pago)
    return db_medio_pago


def delete_medio_pago(db: Session, medio_pago_id: int):
    db_medio_pago = get_medio_pago(db, medio_pago_id)
    if db_medio_pago:
        db.delete(db_medio_pago)
        db.commit()
        return True
    return False


# ========== CRUD CUENTAS BANCARIAS ==========
def get_cuenta_bancaria(db: Session, cuenta_id: int):
    return db.query(models.CuentaBancaria).filter(models.CuentaBancaria.id == cuenta_id).first()


def get_cuentas_bancarias(db: Session, activa: Optional[bool] = None):
    query = db.query(models.CuentaBancaria)
    if activa is not None:
        query = query.filter(models.CuentaBancaria.activa == (1 if activa else 0))
    return query.all()


def create_cuenta_bancaria(db: Session, cuenta: schemas.CuentaBancariaCreate):
    db_cuenta = models.CuentaBancaria(**cuenta.model_dump())
    db.add(db_cuenta)
    db.commit()
    db.refresh(db_cuenta)
    return db_cuenta


def update_cuenta_bancaria(db: Session, cuenta_id: int, cuenta: schemas.CuentaBancariaUpdate):
    db_cuenta = get_cuenta_bancaria(db, cuenta_id)
    if db_cuenta:
        update_data = cuenta.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cuenta, key, value)
        db.commit()
        db.refresh(db_cuenta)
    return db_cuenta


def delete_cuenta_bancaria(db: Session, cuenta_id: int):
    db_cuenta = get_cuenta_bancaria(db, cuenta_id)
    if db_cuenta:
        db.delete(db_cuenta)
        db.commit()
        return True
    return False


# ========== CRUD INGRESOS ==========
def get_ingreso(db: Session, ingreso_id: int):
    return db.query(models.Ingreso).filter(models.Ingreso.id == ingreso_id).first()


def get_ingresos(db: Session, cuenta_bancaria_id: Optional[int] = None):
    query = db.query(models.Ingreso)
    if cuenta_bancaria_id:
        query = query.filter(models.Ingreso.cuenta_bancaria_id == cuenta_bancaria_id)
    return query.order_by(models.Ingreso.fecha.desc()).all()


def create_ingreso(db: Session, ingreso: schemas.IngresoCreate):
    # Crear el ingreso
    db_ingreso = models.Ingreso(**ingreso.model_dump())
    db.add(db_ingreso)

    # Actualizar saldo de la cuenta
    cuenta = get_cuenta_bancaria(db, ingreso.cuenta_bancaria_id)
    if cuenta:
        cuenta.saldo_total += ingreso.monto
        if ingreso.tipo == "ahorro":
            cuenta.saldo_ahorro += ingreso.monto
        else:
            cuenta.saldo_transaccional += ingreso.monto

    db.commit()
    db.refresh(db_ingreso)
    return db_ingreso


def delete_ingreso(db: Session, ingreso_id: int):
    db_ingreso = get_ingreso(db, ingreso_id)
    if db_ingreso:
        # Revertir saldo de la cuenta
        cuenta = get_cuenta_bancaria(db, db_ingreso.cuenta_bancaria_id)
        if cuenta:
            cuenta.saldo_total -= db_ingreso.monto
            if db_ingreso.tipo == "ahorro":
                cuenta.saldo_ahorro -= db_ingreso.monto
            else:
                cuenta.saldo_transaccional -= db_ingreso.monto

        db.delete(db_ingreso)
        db.commit()
        return True
    return False


# ========== CRUD TRANSFERENCIAS ==========
def get_transferencia(db: Session, transferencia_id: int):
    return db.query(models.Transferencia).filter(models.Transferencia.id == transferencia_id).first()


def get_transferencias(db: Session):
    return db.query(models.Transferencia).order_by(models.Transferencia.fecha.desc()).all()


def create_transferencia(db: Session, transferencia: schemas.TransferenciaCreate):
    # Validar que las cuentas sean diferentes
    if transferencia.cuenta_origen_id == transferencia.cuenta_destino_id:
        return None

    # Verificar saldo suficiente en cuenta origen
    cuenta_origen = get_cuenta_bancaria(db, transferencia.cuenta_origen_id)
    if not cuenta_origen or cuenta_origen.saldo_transaccional < transferencia.monto:
        return None

    # Crear transferencia
    db_transferencia = models.Transferencia(**transferencia.model_dump())
    db.add(db_transferencia)

    # Actualizar saldos
    cuenta_destino = get_cuenta_bancaria(db, transferencia.cuenta_destino_id)
    if cuenta_origen and cuenta_destino:
        cuenta_origen.saldo_transaccional -= transferencia.monto
        cuenta_origen.saldo_total -= transferencia.monto

        cuenta_destino.saldo_transaccional += transferencia.monto
        cuenta_destino.saldo_total += transferencia.monto

    db.commit()
    db.refresh(db_transferencia)
    return db_transferencia


def get_resumen_cuentas(db: Session):
    """Obtiene resumen de todas las cuentas"""
    cuentas = get_cuentas_bancarias(db, activa=True)

    total_general = sum(c.saldo_total for c in cuentas)
    total_ahorro = sum(c.saldo_ahorro for c in cuentas)
    total_transaccional = sum(c.saldo_transaccional for c in cuentas)

    return {
        "total_general": total_general,
        "total_ahorro": total_ahorro,
        "total_transaccional": total_transaccional,
        "cuentas": cuentas
    }
