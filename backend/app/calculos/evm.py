"""Fórmulas de Valor Ganado (EVM). Cada indicador es una función pequeña e independiente."""

from decimal import ROUND_HALF_UP, Decimal

from app.calculos.tipos import (
    DatosActividad,
    Indicadores,
    InterpretacionCosto,
    InterpretacionCronograma,
    Montos,
)

CERO = Decimal("0")
PORCENTAJE_TOTAL = Decimal("100")
INDICE_NEUTRO = Decimal("1")
PASO_DINERO = Decimal("0.01")
PASO_INDICE = Decimal("0.0001")


def dividir_o_nulo(numerador: Decimal, denominador: Decimal) -> Decimal | None:
    """Divide; si el denominador es cero devuelve None (no hay dato, no se inventa un número)."""
    if denominador == CERO:
        return None
    return numerador / denominador


def redondear(valor: Decimal | None, paso: Decimal) -> Decimal | None:
    """Redondea al paso indicado (0.01 para dinero, 0.0001 para índices). Conserva None."""
    if valor is None:
        return None
    return valor.quantize(paso, rounding=ROUND_HALF_UP)


def calcular_valor_planificado(
    porcentaje_planificado: Decimal, presupuesto_total: Decimal
) -> Decimal:
    """PV = % planificado x BAC."""
    return porcentaje_planificado * presupuesto_total / PORCENTAJE_TOTAL


def calcular_valor_ganado(porcentaje_real: Decimal, presupuesto_total: Decimal) -> Decimal:
    """EV = % completado x BAC."""
    return porcentaje_real * presupuesto_total / PORCENTAJE_TOTAL


def calcular_variacion_costo(valor_ganado: Decimal, costo_real: Decimal) -> Decimal:
    """CV = EV - AC."""
    return valor_ganado - costo_real


def calcular_variacion_cronograma(valor_ganado: Decimal, valor_planificado: Decimal) -> Decimal:
    """SV = EV - PV."""
    return valor_ganado - valor_planificado


def calcular_cpi(valor_ganado: Decimal, costo_real: Decimal) -> Decimal | None:
    """CPI = EV / AC. None si AC es cero."""
    return dividir_o_nulo(valor_ganado, costo_real)


def calcular_spi(valor_ganado: Decimal, valor_planificado: Decimal) -> Decimal | None:
    """SPI = EV / PV. None si PV es cero."""
    return dividir_o_nulo(valor_ganado, valor_planificado)


def calcular_eac(presupuesto_total: Decimal, cpi: Decimal | None) -> Decimal | None:
    """EAC = BAC / CPI. None si el CPI no existe o es cero."""
    if cpi is None:
        return None
    return dividir_o_nulo(presupuesto_total, cpi)


def calcular_vac(presupuesto_total: Decimal, eac: Decimal | None) -> Decimal | None:
    """VAC = BAC - EAC. None si el EAC no existe."""
    if eac is None:
        return None
    return presupuesto_total - eac


def interpretar_costo(cpi: Decimal | None) -> InterpretacionCosto:
    """CPI mayor a 1: bajo presupuesto. Menor a 1: sobre presupuesto."""
    if cpi is None:
        return InterpretacionCosto.NO_CALCULABLE
    if cpi > INDICE_NEUTRO:
        return InterpretacionCosto.BAJO_PRESUPUESTO
    if cpi < INDICE_NEUTRO:
        return InterpretacionCosto.SOBRE_PRESUPUESTO
    return InterpretacionCosto.EN_PRESUPUESTO


def interpretar_cronograma(spi: Decimal | None) -> InterpretacionCronograma:
    """SPI mayor a 1: adelantado. Menor a 1: atrasado."""
    if spi is None:
        return InterpretacionCronograma.NO_CALCULABLE
    if spi > INDICE_NEUTRO:
        return InterpretacionCronograma.ADELANTADO
    if spi < INDICE_NEUTRO:
        return InterpretacionCronograma.ATRASADO
    return InterpretacionCronograma.EN_TIEMPO


def calcular_montos_actividad(datos: DatosActividad) -> Montos:
    """Convierte los porcentajes de una actividad en los montos BAC, PV, EV y AC."""
    return Montos(
        presupuesto_total=datos.presupuesto_total,
        valor_planificado=calcular_valor_planificado(
            datos.porcentaje_planificado, datos.presupuesto_total
        ),
        valor_ganado=calcular_valor_ganado(datos.porcentaje_real, datos.presupuesto_total),
        costo_real=datos.costo_real,
    )


def consolidar_montos(lista_montos: list[Montos]) -> Montos:
    """Suma los montos de varias actividades. Sin actividades, todo es cero."""
    return Montos(
        presupuesto_total=sum((m.presupuesto_total for m in lista_montos), CERO),
        valor_planificado=sum((m.valor_planificado for m in lista_montos), CERO),
        valor_ganado=sum((m.valor_ganado for m in lista_montos), CERO),
        costo_real=sum((m.costo_real for m in lista_montos), CERO),
    )


def calcular_indicadores(montos: Montos) -> Indicadores:
    """Calcula todos los indicadores desde BAC, PV, EV y AC (sirve para actividad y proyecto)."""
    cpi = calcular_cpi(montos.valor_ganado, montos.costo_real)
    spi = calcular_spi(montos.valor_ganado, montos.valor_planificado)
    eac = calcular_eac(montos.presupuesto_total, cpi)
    vac = calcular_vac(montos.presupuesto_total, eac)
    cpi_redondeado = redondear(cpi, PASO_INDICE)
    spi_redondeado = redondear(spi, PASO_INDICE)

    return Indicadores(
        valor_planificado=redondear(montos.valor_planificado, PASO_DINERO),
        valor_ganado=redondear(montos.valor_ganado, PASO_DINERO),
        variacion_costo=redondear(
            calcular_variacion_costo(montos.valor_ganado, montos.costo_real), PASO_DINERO
        ),
        variacion_cronograma=redondear(
            calcular_variacion_cronograma(montos.valor_ganado, montos.valor_planificado),
            PASO_DINERO,
        ),
        cpi=cpi_redondeado,
        spi=spi_redondeado,
        eac=redondear(eac, PASO_DINERO),
        vac=redondear(vac, PASO_DINERO),
        interpretacion_costo=interpretar_costo(cpi_redondeado),
        interpretacion_cronograma=interpretar_cronograma(spi_redondeado),
    )


def calcular_indicadores_actividad(datos: DatosActividad) -> Indicadores:
    """Indicadores EVM de una actividad."""
    return calcular_indicadores(calcular_montos_actividad(datos))


def calcular_indicadores_proyecto(actividades: list[DatosActividad]) -> Indicadores:
    """Indicadores EVM consolidados: suma los montos y recalcula los índices sobre los totales."""
    montos = [calcular_montos_actividad(actividad) for actividad in actividades]
    return calcular_indicadores(consolidar_montos(montos))
