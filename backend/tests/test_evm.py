"""Pruebas unitarias de los cálculos EVM, con valores calculados a mano."""

from decimal import Decimal

from app.calculos.evm import (
    calcular_cpi,
    calcular_eac,
    calcular_indicadores,
    calcular_indicadores_actividad,
    calcular_indicadores_proyecto,
    calcular_montos_actividad,
    calcular_spi,
    calcular_vac,
    calcular_valor_ganado,
    calcular_valor_planificado,
    calcular_variacion_costo,
    calcular_variacion_cronograma,
    consolidar_montos,
    dividir_o_nulo,
    interpretar_costo,
    interpretar_cronograma,
    redondear,
)
from app.calculos.tipos import (
    DatosActividad,
    InterpretacionCosto,
    InterpretacionCronograma,
    Montos,
)


def crear_actividad(presupuesto, planificado, real, costo_real) -> DatosActividad:
    return DatosActividad(
        presupuesto_total=Decimal(presupuesto),
        porcentaje_planificado=Decimal(planificado),
        porcentaje_real=Decimal(real),
        costo_real=Decimal(costo_real),
    )


ACTIVIDAD_SOBRE_PRESUPUESTO_Y_ATRASADA = crear_actividad("1000", "50", "40", "600")
ACTIVIDAD_BAJO_PRESUPUESTO_Y_ADELANTADA = crear_actividad("2000", "30", "45", "800")
ACTIVIDAD_GRANDE_EFICIENTE = crear_actividad("3000", "50", "60", "1500")


# --- Fórmulas individuales ---


def test_valor_planificado_es_porcentaje_planificado_por_presupuesto():
    assert calcular_valor_planificado(Decimal("50"), Decimal("1000")) == Decimal("500")


def test_valor_planificado_con_porcentaje_decimal_es_exacto():
    assert calcular_valor_planificado(Decimal("33.33"), Decimal("1000")) == Decimal("333.30")


def test_valor_ganado_es_porcentaje_real_por_presupuesto():
    assert calcular_valor_ganado(Decimal("40"), Decimal("1000")) == Decimal("400")


def test_variacion_costo_es_valor_ganado_menos_costo_real():
    assert calcular_variacion_costo(Decimal("400"), Decimal("600")) == Decimal("-200")


def test_variacion_cronograma_es_valor_ganado_menos_valor_planificado():
    assert calcular_variacion_cronograma(Decimal("400"), Decimal("500")) == Decimal("-100")


def test_cpi_es_valor_ganado_dividido_costo_real():
    assert calcular_cpi(Decimal("900"), Decimal("800")) == Decimal("1.125")


def test_spi_es_valor_ganado_dividido_valor_planificado():
    assert calcular_spi(Decimal("900"), Decimal("600")) == Decimal("1.5")


def test_eac_es_presupuesto_dividido_cpi():
    assert calcular_eac(Decimal("1000"), Decimal("0.5")) == Decimal("2000")


def test_vac_es_presupuesto_menos_eac():
    assert calcular_vac(Decimal("1000"), Decimal("1500")) == Decimal("-500")


# --- Casos borde: divisiones por cero ---


def test_dividir_por_cero_devuelve_none():
    assert dividir_o_nulo(Decimal("10"), Decimal("0")) is None


def test_cpi_es_none_cuando_costo_real_es_cero():
    assert calcular_cpi(Decimal("400"), Decimal("0")) is None


def test_spi_es_none_cuando_valor_planificado_es_cero():
    assert calcular_spi(Decimal("400"), Decimal("0")) is None


def test_eac_es_none_cuando_cpi_es_none():
    assert calcular_eac(Decimal("1000"), None) is None


def test_eac_es_none_cuando_cpi_es_cero():
    assert calcular_eac(Decimal("1000"), Decimal("0")) is None


def test_vac_es_none_cuando_eac_es_none():
    assert calcular_vac(Decimal("1000"), None) is None


def test_redondear_conserva_none():
    assert redondear(None, Decimal("0.01")) is None


def test_redondear_sube_la_mitad():
    assert redondear(Decimal("0.66665"), Decimal("0.0001")) == Decimal("0.6667")


# --- Interpretaciones ---


def test_cpi_mayor_a_uno_es_bajo_presupuesto():
    assert interpretar_costo(Decimal("1.125")) == InterpretacionCosto.BAJO_PRESUPUESTO


def test_cpi_menor_a_uno_es_sobre_presupuesto():
    assert interpretar_costo(Decimal("0.6667")) == InterpretacionCosto.SOBRE_PRESUPUESTO


def test_cpi_igual_a_uno_es_en_presupuesto():
    assert interpretar_costo(Decimal("1")) == InterpretacionCosto.EN_PRESUPUESTO


def test_cpi_none_no_es_calculable():
    assert interpretar_costo(None) == InterpretacionCosto.NO_CALCULABLE


def test_spi_mayor_a_uno_es_adelantado():
    assert interpretar_cronograma(Decimal("1.5")) == InterpretacionCronograma.ADELANTADO


def test_spi_menor_a_uno_es_atrasado():
    assert interpretar_cronograma(Decimal("0.8")) == InterpretacionCronograma.ATRASADO


def test_spi_igual_a_uno_es_en_tiempo():
    assert interpretar_cronograma(Decimal("1")) == InterpretacionCronograma.EN_TIEMPO


def test_spi_none_no_es_calculable():
    assert interpretar_cronograma(None) == InterpretacionCronograma.NO_CALCULABLE


# --- Actividad completa (ejemplos calculados a mano) ---


def test_actividad_sobre_presupuesto_y_atrasada():
    indicadores = calcular_indicadores_actividad(ACTIVIDAD_SOBRE_PRESUPUESTO_Y_ATRASADA)

    assert indicadores.valor_planificado == Decimal("500.00")
    assert indicadores.valor_ganado == Decimal("400.00")
    assert indicadores.variacion_costo == Decimal("-200.00")
    assert indicadores.variacion_cronograma == Decimal("-100.00")
    assert indicadores.cpi == Decimal("0.6667")
    assert indicadores.spi == Decimal("0.8000")
    assert indicadores.eac == Decimal("1500.00")
    assert indicadores.vac == Decimal("-500.00")
    assert indicadores.interpretacion_costo == InterpretacionCosto.SOBRE_PRESUPUESTO
    assert indicadores.interpretacion_cronograma == InterpretacionCronograma.ATRASADO


def test_actividad_bajo_presupuesto_y_adelantada():
    indicadores = calcular_indicadores_actividad(ACTIVIDAD_BAJO_PRESUPUESTO_Y_ADELANTADA)

    assert indicadores.valor_planificado == Decimal("600.00")
    assert indicadores.valor_ganado == Decimal("900.00")
    assert indicadores.variacion_costo == Decimal("100.00")
    assert indicadores.variacion_cronograma == Decimal("300.00")
    assert indicadores.cpi == Decimal("1.1250")
    assert indicadores.spi == Decimal("1.5000")
    assert indicadores.eac == Decimal("1777.78")
    assert indicadores.vac == Decimal("222.22")
    assert indicadores.interpretacion_costo == InterpretacionCosto.BAJO_PRESUPUESTO
    assert indicadores.interpretacion_cronograma == InterpretacionCronograma.ADELANTADO


def test_actividad_en_el_plan_exacto():
    indicadores = calcular_indicadores_actividad(crear_actividad("1000", "50", "50", "500"))

    assert indicadores.cpi == Decimal("1.0000")
    assert indicadores.spi == Decimal("1.0000")
    assert indicadores.eac == Decimal("1000.00")
    assert indicadores.vac == Decimal("0.00")
    assert indicadores.interpretacion_costo == InterpretacionCosto.EN_PRESUPUESTO
    assert indicadores.interpretacion_cronograma == InterpretacionCronograma.EN_TIEMPO


# --- Casos borde de una actividad ---


def test_actividad_con_costo_real_cero_no_calcula_cpi_eac_ni_vac():
    indicadores = calcular_indicadores_actividad(crear_actividad("1000", "50", "40", "0"))

    assert indicadores.valor_ganado == Decimal("400.00")
    assert indicadores.variacion_costo == Decimal("400.00")
    assert indicadores.cpi is None
    assert indicadores.eac is None
    assert indicadores.vac is None
    assert indicadores.spi == Decimal("0.8000")
    assert indicadores.interpretacion_costo == InterpretacionCosto.NO_CALCULABLE


def test_actividad_con_avance_real_cero_tiene_cpi_cero_y_no_calcula_eac():
    indicadores = calcular_indicadores_actividad(crear_actividad("1000", "50", "0", "300"))

    assert indicadores.valor_ganado == Decimal("0.00")
    assert indicadores.variacion_costo == Decimal("-300.00")
    assert indicadores.cpi == Decimal("0.0000")
    assert indicadores.spi == Decimal("0.0000")
    assert indicadores.eac is None
    assert indicadores.vac is None
    assert indicadores.interpretacion_costo == InterpretacionCosto.SOBRE_PRESUPUESTO
    assert indicadores.interpretacion_cronograma == InterpretacionCronograma.ATRASADO


def test_actividad_con_avance_planificado_cero_no_calcula_spi():
    indicadores = calcular_indicadores_actividad(crear_actividad("1000", "0", "10", "100"))

    assert indicadores.valor_planificado == Decimal("0.00")
    assert indicadores.spi is None
    assert indicadores.interpretacion_cronograma == InterpretacionCronograma.NO_CALCULABLE
    assert indicadores.cpi == Decimal("1.0000")


def test_actividad_sin_nada_ejecutado_ni_gastado():
    indicadores = calcular_indicadores_actividad(crear_actividad("1000", "0", "0", "0"))

    assert indicadores.valor_planificado == Decimal("0.00")
    assert indicadores.valor_ganado == Decimal("0.00")
    assert indicadores.cpi is None
    assert indicadores.spi is None
    assert indicadores.eac is None
    assert indicadores.vac is None


# --- Montos y consolidado del proyecto ---


def test_montos_de_una_actividad():
    montos = calcular_montos_actividad(ACTIVIDAD_SOBRE_PRESUPUESTO_Y_ATRASADA)

    assert montos == Montos(
        presupuesto_total=Decimal("1000"),
        valor_planificado=Decimal("500"),
        valor_ganado=Decimal("400"),
        costo_real=Decimal("600"),
    )


def test_consolidar_montos_suma_cada_monto():
    montos = consolidar_montos(
        [
            calcular_montos_actividad(ACTIVIDAD_SOBRE_PRESUPUESTO_Y_ATRASADA),
            calcular_montos_actividad(ACTIVIDAD_GRANDE_EFICIENTE),
        ]
    )

    assert montos == Montos(
        presupuesto_total=Decimal("4000"),
        valor_planificado=Decimal("2000"),
        valor_ganado=Decimal("2200"),
        costo_real=Decimal("2100"),
    )


def test_proyecto_consolida_sumando_y_recalculando_indices():
    indicadores = calcular_indicadores_proyecto(
        [ACTIVIDAD_SOBRE_PRESUPUESTO_Y_ATRASADA, ACTIVIDAD_GRANDE_EFICIENTE]
    )

    assert indicadores.valor_planificado == Decimal("2000.00")
    assert indicadores.valor_ganado == Decimal("2200.00")
    assert indicadores.variacion_costo == Decimal("100.00")
    assert indicadores.variacion_cronograma == Decimal("200.00")
    assert indicadores.cpi == Decimal("1.0476")
    assert indicadores.spi == Decimal("1.1000")
    assert indicadores.eac == Decimal("3818.18")
    assert indicadores.vac == Decimal("181.82")
    assert indicadores.interpretacion_costo == InterpretacionCosto.BAJO_PRESUPUESTO
    assert indicadores.interpretacion_cronograma == InterpretacionCronograma.ADELANTADO


def test_proyecto_no_promedia_los_indices_de_las_actividades():
    promedio_de_cpi = Decimal("0.9333")

    indicadores = calcular_indicadores_proyecto(
        [ACTIVIDAD_SOBRE_PRESUPUESTO_Y_ATRASADA, ACTIVIDAD_GRANDE_EFICIENTE]
    )

    assert indicadores.cpi != promedio_de_cpi


def test_proyecto_sin_actividades_tiene_montos_en_cero_e_indices_no_calculables():
    indicadores = calcular_indicadores_proyecto([])

    assert indicadores.valor_planificado == Decimal("0.00")
    assert indicadores.valor_ganado == Decimal("0.00")
    assert indicadores.variacion_costo == Decimal("0.00")
    assert indicadores.variacion_cronograma == Decimal("0.00")
    assert indicadores.cpi is None
    assert indicadores.spi is None
    assert indicadores.eac is None
    assert indicadores.vac is None
    assert indicadores.interpretacion_costo == InterpretacionCosto.NO_CALCULABLE
    assert indicadores.interpretacion_cronograma == InterpretacionCronograma.NO_CALCULABLE


def test_proyecto_con_una_actividad_es_igual_a_esa_actividad():
    solo_la_actividad = calcular_indicadores_actividad(ACTIVIDAD_BAJO_PRESUPUESTO_Y_ADELANTADA)

    como_proyecto = calcular_indicadores_proyecto([ACTIVIDAD_BAJO_PRESUPUESTO_Y_ADELANTADA])

    assert como_proyecto == solo_la_actividad


def test_calcular_indicadores_desde_montos_directos():
    montos = Montos(
        presupuesto_total=Decimal("1000"),
        valor_planificado=Decimal("500"),
        valor_ganado=Decimal("400"),
        costo_real=Decimal("600"),
    )

    assert calcular_indicadores(montos).cpi == Decimal("0.6667")
