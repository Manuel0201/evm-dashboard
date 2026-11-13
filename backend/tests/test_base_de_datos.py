"""Pruebas de los modelos y del script de inicialización contra PostgreSQL de pruebas."""

from decimal import Decimal

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modelos import Actividad, Proyecto
from tests.conftest import SCRIPT_INICIALIZACION


def crear_actividad(**cambios) -> Actividad:
    datos = {
        "nombre": "Desarrollar el bot",
        "presupuesto_total": Decimal("1000.50"),
        "porcentaje_planificado": Decimal("33.33"),
        "porcentaje_real": Decimal("40"),
        "costo_real": Decimal("600"),
    }
    datos.update(cambios)
    return Actividad(**datos)


def guardar_proyecto_con(sesion: Session, *actividades: Actividad) -> Proyecto:
    proyecto = Proyecto(nombre="Proyecto de prueba", actividades=list(actividades))
    sesion.add(proyecto)
    sesion.commit()
    return proyecto


def test_guarda_y_lee_valores_decimales_exactos(sesion: Session):
    guardar_proyecto_con(sesion, crear_actividad())
    sesion.expire_all()

    actividad = sesion.scalars(select(Actividad)).one()

    assert actividad.presupuesto_total == Decimal("1000.50")
    assert actividad.porcentaje_planificado == Decimal("33.33")
    assert actividad.porcentaje_real == Decimal("40.00")
    assert actividad.costo_real == Decimal("600.00")


def test_una_actividad_queda_asociada_a_su_proyecto(sesion: Session):
    proyecto = guardar_proyecto_con(
        sesion, crear_actividad(nombre="A"), crear_actividad(nombre="B")
    )
    sesion.expire_all()

    proyecto_leido = sesion.get(Proyecto, proyecto.id)

    assert sorted(a.nombre for a in proyecto_leido.actividades) == ["A", "B"]


def test_borrar_un_proyecto_borra_sus_actividades(sesion: Session):
    proyecto = guardar_proyecto_con(sesion, crear_actividad(), crear_actividad())

    sesion.delete(proyecto)
    sesion.commit()

    assert sesion.scalars(select(Actividad)).all() == []


def test_rechaza_porcentaje_real_mayor_a_cien(sesion: Session):
    with pytest.raises(IntegrityError):
        guardar_proyecto_con(sesion, crear_actividad(porcentaje_real=Decimal("100.01")))


def test_rechaza_porcentaje_planificado_negativo(sesion: Session):
    with pytest.raises(IntegrityError):
        guardar_proyecto_con(sesion, crear_actividad(porcentaje_planificado=Decimal("-1")))


def test_acepta_porcentajes_en_los_limites_cero_y_cien(sesion: Session):
    guardar_proyecto_con(
        sesion,
        crear_actividad(porcentaje_planificado=Decimal("0"), porcentaje_real=Decimal("100")),
    )

    assert sesion.scalars(select(Actividad)).one().porcentaje_real == Decimal("100.00")


def test_rechaza_costo_real_negativo(sesion: Session):
    with pytest.raises(IntegrityError):
        guardar_proyecto_con(sesion, crear_actividad(costo_real=Decimal("-5")))


def test_rechaza_presupuesto_negativo(sesion: Session):
    with pytest.raises(IntegrityError):
        guardar_proyecto_con(sesion, crear_actividad(presupuesto_total=Decimal("-1")))


def test_rechaza_actividad_sin_proyecto_existente(sesion: Session):
    sesion.add(crear_actividad(proyecto_id=999999))

    with pytest.raises(IntegrityError):
        sesion.commit()


def test_el_script_de_inicializacion_se_puede_ejecutar_dos_veces(sesion: Session):
    guardar_proyecto_con(sesion, crear_actividad())

    sesion.execute(text(SCRIPT_INICIALIZACION.read_text(encoding="utf-8")))
    sesion.commit()

    assert len(sesion.scalars(select(Actividad)).all()) == 1
