from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


# Schemas para Categoría
class CategoriaBase(BaseModel):
    nombre: str
    presupuesto_mensual: float = 0.0
    color: str = "#3B82F6"
    icono: str = "💰"


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    presupuesto_mensual: Optional[float] = None
    color: Optional[str] = None
    icono: Optional[str] = None


class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


# Schemas para Subcategoría
class SubcategoriaBase(BaseModel):
    nombre: str
    categoria_id: int


class SubcategoriaCreate(SubcategoriaBase):
    pass


class SubcategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria_id: Optional[int] = None


class Subcategoria(SubcategoriaBase):
    id: int

    class Config:
        from_attributes = True


# Schemas para Gasto
class GastoBase(BaseModel):
    fecha: date
    monto: float = Field(gt=0, description="Monto debe ser mayor a 0")
    descripcion: str
    categoria_id: int
    subcategoria_id: Optional[int] = None
    medio_pago_id: Optional[int] = None
    banco_id: Optional[int] = None


class GastoCreate(GastoBase):
    pass


class GastoUpdate(BaseModel):
    fecha: Optional[date] = None
    monto: Optional[float] = Field(None, gt=0)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    subcategoria_id: Optional[int] = None
    medio_pago_id: Optional[int] = None
    banco_id: Optional[int] = None


class Gasto(GastoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Schemas extendidos con relaciones
class CategoriaConSubcategorias(Categoria):
    subcategorias: list[Subcategoria] = []

    class Config:
        from_attributes = True


class GastoDetallado(Gasto):
    categoria: Categoria
    subcategoria: Optional[Subcategoria] = None

    class Config:
        from_attributes = True


# Schemas para Banco
class BancoBase(BaseModel):
    nombre: str


class BancoCreate(BancoBase):
    pass


class BancoUpdate(BaseModel):
    nombre: Optional[str] = None
    activo: Optional[int] = None


class Banco(BancoBase):
    id: int
    activo: int = 1

    class Config:
        from_attributes = True


# Schemas para Medio de Pago
class MedioPagoBase(BaseModel):
    tipo: str  # "Débito" o "Crédito"
    nombre: str
    banco_id: int


class MedioPagoCreate(MedioPagoBase):
    pass


class MedioPagoUpdate(BaseModel):
    tipo: Optional[str] = None
    nombre: Optional[str] = None
    banco_id: Optional[int] = None
    activo: Optional[int] = None


class MedioPago(MedioPagoBase):
    id: int
    activo: int = 1

    class Config:
        from_attributes = True


# Schemas para Cuenta Bancaria
class CuentaBancariaBase(BaseModel):
    nombre: str
    banco_id: int
    saldo_total: float = 0.0
    saldo_ahorro: float = 0.0
    saldo_transaccional: float = 0.0


class CuentaBancariaCreate(CuentaBancariaBase):
    pass


class CuentaBancariaUpdate(BaseModel):
    nombre: Optional[str] = None
    banco_id: Optional[int] = None
    saldo_total: Optional[float] = None
    saldo_ahorro: Optional[float] = None
    saldo_transaccional: Optional[float] = None
    activa: Optional[int] = None


class CuentaBancaria(CuentaBancariaBase):
    id: int
    activa: int = 1

    class Config:
        from_attributes = True


# Schemas para Ingreso
class IngresoBase(BaseModel):
    nombre: str
    monto: float = Field(gt=0)
    fecha: date
    cuenta_bancaria_id: int
    tipo: str = "transaccional"  # "transaccional" o "ahorro"


class IngresoCreate(IngresoBase):
    pass


class IngresoUpdate(BaseModel):
    nombre: Optional[str] = None
    monto: Optional[float] = Field(None, gt=0)
    fecha: Optional[date] = None
    cuenta_bancaria_id: Optional[int] = None
    tipo: Optional[str] = None


class Ingreso(IngresoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Schemas para Transferencia
class TransferenciaBase(BaseModel):
    cuenta_origen_id: int
    cuenta_destino_id: int
    monto: float = Field(gt=0)
    fecha: date
    descripcion: Optional[str] = None


class TransferenciaCreate(TransferenciaBase):
    pass


class Transferencia(TransferenciaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
