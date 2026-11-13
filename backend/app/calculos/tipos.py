"""Formas de los datos que entran y salen de los cálculos EVM."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class InterpretacionCosto(StrEnum):
    """Lectura del CPI: qué tan bien va el proyecto en costos."""

    BAJO_PRESUPUESTO = "Bajo presupuesto"
    EN_PRESUPUESTO = "En presupuesto"
    SOBRE_PRESUPUESTO = "Sobre presupuesto"
    NO_CALCULABLE = "No calculable"


class InterpretacionCronograma(StrEnum):
    """Lectura del SPI: qué tan bien va el proyecto en tiempo."""

    ADELANTADO = "Adelantado"
    EN_TIEMPO = "En tiempo"
    ATRASADO = "Atrasado"
    NO_CALCULABLE = "No calculable"


@dataclass(frozen=True)
class DatosActividad:
    """Lo que el líder de proyecto escribe para una actividad."""

    presupuesto_total: Decimal
    porcentaje_planificado: Decimal
    porcentaje_real: Decimal
    costo_real: Decimal


@dataclass(frozen=True)
class Montos:
    """Los cuatro montos en dinero que alimentan los indicadores: BAC, PV, EV y AC."""

    presupuesto_total: Decimal
    valor_planificado: Decimal
    valor_ganado: Decimal
    costo_real: Decimal


@dataclass(frozen=True)
class Indicadores:
    """Resultado EVM de una actividad o de un proyecto. None significa 'no calculable'."""

    valor_planificado: Decimal
    valor_ganado: Decimal
    variacion_costo: Decimal
    variacion_cronograma: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    interpretacion_costo: InterpretacionCosto
    interpretacion_cronograma: InterpretacionCronograma
