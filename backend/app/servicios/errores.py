"""Errores de negocio que los routers traducen a respuestas HTTP."""


class RecursoNoEncontradoError(Exception):
    """Se pidió un proyecto o una actividad que no existe."""

    def __init__(self, nombre_recurso: str, identificador: int) -> None:
        super().__init__(f"{nombre_recurso} {identificador} no existe")
