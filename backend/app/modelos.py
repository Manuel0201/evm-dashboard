"""Modelos: las tablas de la base de datos vistas como clases de Python."""

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_de_datos import Base
from app.constantes import DECIMALES, DIGITOS_DINERO, DIGITOS_PORCENTAJE, LONGITUD_NOMBRE


class Proyecto(Base):
    """Un proyecto agrupa actividades."""

    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(LONGITUD_NOMBRE))
    actividades: Mapped[list["Actividad"]] = relationship(
        back_populates="proyecto", cascade="all, delete-orphan", passive_deletes=True
    )


class Actividad(Base):
    """Una actividad guarda solo lo que escribe el usuario; los indicadores se calculan al vuelo."""

    __tablename__ = "actividades"

    id: Mapped[int] = mapped_column(primary_key=True)
    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyectos.id", ondelete="CASCADE"))
    nombre: Mapped[str] = mapped_column(String(LONGITUD_NOMBRE))
    presupuesto_total: Mapped[Decimal] = mapped_column(Numeric(DIGITOS_DINERO, DECIMALES))
    porcentaje_planificado: Mapped[Decimal] = mapped_column(Numeric(DIGITOS_PORCENTAJE, DECIMALES))
    porcentaje_real: Mapped[Decimal] = mapped_column(Numeric(DIGITOS_PORCENTAJE, DECIMALES))
    costo_real: Mapped[Decimal] = mapped_column(Numeric(DIGITOS_DINERO, DECIMALES))
    proyecto: Mapped[Proyecto] = relationship(back_populates="actividades")
