from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from backend import schemas, crud_financiero
from backend.database import get_db

router = APIRouter()


# ========== ENDPOINTS BANCOS ==========
@router.get("/bancos", response_model=list[schemas.Banco])
def listar_bancos(activo: Optional[bool] = None, db: Session = Depends(get_db)):
    return crud_financiero.get_bancos(db, activo=activo)


@router.post("/bancos", response_model=schemas.Banco, status_code=201)
def crear_banco(banco: schemas.BancoCreate, db: Session = Depends(get_db)):
    return crud_financiero.create_banco(db, banco)


@router.put("/bancos/{banco_id}", response_model=schemas.Banco)
def actualizar_banco(banco_id: int, banco: schemas.BancoUpdate, db: Session = Depends(get_db)):
    db_banco = crud_financiero.update_banco(db, banco_id, banco)
    if not db_banco:
        raise HTTPException(status_code=404, detail="Banco no encontrado")
    return db_banco


@router.delete("/bancos/{banco_id}", status_code=204)
def eliminar_banco(banco_id: int, db: Session = Depends(get_db)):
    if not crud_financiero.delete_banco(db, banco_id):
        raise HTTPException(status_code=404, detail="Banco no encontrado")


# ========== ENDPOINTS MEDIOS DE PAGO ==========
@router.get("/medios-pago", response_model=list[schemas.MedioPago])
def listar_medios_pago(
    banco_id: Optional[int] = None,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return crud_financiero.get_medios_pago(db, banco_id=banco_id, activo=activo)


@router.post("/medios-pago", response_model=schemas.MedioPago, status_code=201)
def crear_medio_pago(medio_pago: schemas.MedioPagoCreate, db: Session = Depends(get_db)):
    return crud_financiero.create_medio_pago(db, medio_pago)


@router.put("/medios-pago/{medio_pago_id}", response_model=schemas.MedioPago)
def actualizar_medio_pago(
    medio_pago_id: int,
    medio_pago: schemas.MedioPagoUpdate,
    db: Session = Depends(get_db)
):
    db_medio_pago = crud_financiero.update_medio_pago(db, medio_pago_id, medio_pago)
    if not db_medio_pago:
        raise HTTPException(status_code=404, detail="Medio de pago no encontrado")
    return db_medio_pago


@router.delete("/medios-pago/{medio_pago_id}", status_code=204)
def eliminar_medio_pago(medio_pago_id: int, db: Session = Depends(get_db)):
    if not crud_financiero.delete_medio_pago(db, medio_pago_id):
        raise HTTPException(status_code=404, detail="Medio de pago no encontrado")


# ========== ENDPOINTS CUENTAS BANCARIAS ==========
@router.get("/cuentas-bancarias", response_model=list[schemas.CuentaBancaria])
def listar_cuentas_bancarias(activa: Optional[bool] = None, db: Session = Depends(get_db)):
    return crud_financiero.get_cuentas_bancarias(db, activa=activa)


@router.get("/cuentas-bancarias/resumen")
def obtener_resumen_cuentas(db: Session = Depends(get_db)):
    return crud_financiero.get_resumen_cuentas(db)


@router.post("/cuentas-bancarias", response_model=schemas.CuentaBancaria, status_code=201)
def crear_cuenta_bancaria(cuenta: schemas.CuentaBancariaCreate, db: Session = Depends(get_db)):
    return crud_financiero.create_cuenta_bancaria(db, cuenta)


@router.put("/cuentas-bancarias/{cuenta_id}", response_model=schemas.CuentaBancaria)
def actualizar_cuenta_bancaria(
    cuenta_id: int,
    cuenta: schemas.CuentaBancariaUpdate,
    db: Session = Depends(get_db)
):
    db_cuenta = crud_financiero.update_cuenta_bancaria(db, cuenta_id, cuenta)
    if not db_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    return db_cuenta


@router.delete("/cuentas-bancarias/{cuenta_id}", status_code=204)
def eliminar_cuenta_bancaria(cuenta_id: int, db: Session = Depends(get_db)):
    if not crud_financiero.delete_cuenta_bancaria(db, cuenta_id):
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")


# ========== ENDPOINTS INGRESOS ==========
@router.get("/ingresos", response_model=list[schemas.Ingreso])
def listar_ingresos(cuenta_bancaria_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud_financiero.get_ingresos(db, cuenta_bancaria_id=cuenta_bancaria_id)


@router.post("/ingresos", response_model=schemas.Ingreso, status_code=201)
def crear_ingreso(ingreso: schemas.IngresoCreate, db: Session = Depends(get_db)):
    # Verificar que la cuenta existe
    cuenta = crud_financiero.get_cuenta_bancaria(db, ingreso.cuenta_bancaria_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")

    return crud_financiero.create_ingreso(db, ingreso)


@router.delete("/ingresos/{ingreso_id}", status_code=204)
def eliminar_ingreso(ingreso_id: int, db: Session = Depends(get_db)):
    if not crud_financiero.delete_ingreso(db, ingreso_id):
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")


# ========== ENDPOINTS TRANSFERENCIAS ==========
@router.get("/transferencias", response_model=list[schemas.Transferencia])
def listar_transferencias(db: Session = Depends(get_db)):
    return crud_financiero.get_transferencias(db)


@router.post("/transferencias", response_model=schemas.Transferencia, status_code=201)
def crear_transferencia(transferencia: schemas.TransferenciaCreate, db: Session = Depends(get_db)):
    db_transferencia = crud_financiero.create_transferencia(db, transferencia)

    if not db_transferencia:
        raise HTTPException(
            status_code=400,
            detail="No se puede realizar la transferencia. Verifica que las cuentas sean diferentes y que haya saldo suficiente."
        )

    return db_transferencia
