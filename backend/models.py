from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    presupuesto_mensual = Column(Float, default=0.0)
    color = Column(String, default="#3B82F6")  # Tailwind blue-500 por defecto
    icono = Column(String, default="💰")  # Emoji por defecto

    subcategorias = relationship("Subcategoria", back_populates="categoria", cascade="all, delete-orphan")
    gastos = relationship("Gasto", back_populates="categoria")


class Subcategoria(Base):
    __tablename__ = "subcategorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="subcategorias")
    gastos = relationship("Gasto", back_populates="subcategoria")


class Banco(Base):
    __tablename__ = "bancos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    activo = Column(Integer, default=1)  # 1 = activo, 0 = inactivo

    cuentas = relationship("CuentaBancaria", back_populates="banco")
    gastos = relationship("Gasto", back_populates="banco")


class MedioPago(Base):
    __tablename__ = "medios_pago"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # "Débito" o "Crédito"
    nombre = Column(String, nullable=False)  # Ej: "Tarjeta Débito Bancolombia"
    banco_id = Column(Integer, ForeignKey("bancos.id"), nullable=False)
    activo = Column(Integer, default=1)

    banco = relationship("Banco")
    gastos = relationship("Gasto", back_populates="medio_pago")


class CuentaBancaria(Base):
    __tablename__ = "cuentas_bancarias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)  # Ej: "Cuenta Ahorro Principal"
    banco_id = Column(Integer, ForeignKey("bancos.id"), nullable=False)
    saldo_total = Column(Float, default=0.0)
    saldo_ahorro = Column(Float, default=0.0)  # No se toca
    saldo_transaccional = Column(Float, default=0.0)  # Disponible para gastos
    activa = Column(Integer, default=1)

    banco = relationship("Banco", back_populates="cuentas")
    ingresos = relationship("Ingreso", back_populates="cuenta")
    transferencias_origen = relationship("Transferencia", foreign_keys="Transferencia.cuenta_origen_id", back_populates="cuenta_origen")
    transferencias_destino = relationship("Transferencia", foreign_keys="Transferencia.cuenta_destino_id", back_populates="cuenta_destino")


class Ingreso(Base):
    __tablename__ = "ingresos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)  # Ej: "Salario", "Freelance"
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    cuenta_bancaria_id = Column(Integer, ForeignKey("cuentas_bancarias.id"), nullable=False)
    tipo = Column(String, default="transaccional")  # "transaccional" o "ahorro"
    created_at = Column(DateTime, default=datetime.utcnow)

    cuenta = relationship("CuentaBancaria", back_populates="ingresos")


class Transferencia(Base):
    __tablename__ = "transferencias"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_origen_id = Column(Integer, ForeignKey("cuentas_bancarias.id"), nullable=False)
    cuenta_destino_id = Column(Integer, ForeignKey("cuentas_bancarias.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cuenta_origen = relationship("CuentaBancaria", foreign_keys=[cuenta_origen_id], back_populates="transferencias_origen")
    cuenta_destino = relationship("CuentaBancaria", foreign_keys=[cuenta_destino_id], back_populates="transferencias_destino")


class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    monto = Column(Float, nullable=False)
    descripcion = Column(String, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    subcategoria_id = Column(Integer, ForeignKey("subcategorias.id"), nullable=True)
    medio_pago_id = Column(Integer, ForeignKey("medios_pago.id"), nullable=True)
    banco_id = Column(Integer, ForeignKey("bancos.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="gastos")
    subcategoria = relationship("Subcategoria", back_populates="gastos")
    medio_pago = relationship("MedioPago", back_populates="gastos")
    banco = relationship("Banco", back_populates="gastos")
