import { useState } from 'react'
import { ACTIVIDAD_VACIA, PASO_DECIMAL, PORCENTAJE_MAXIMO } from '../constantes'

function aTexto(actividad) {
  return {
    nombre: actividad.nombre,
    presupuesto_total: String(actividad.presupuesto_total),
    porcentaje_planificado: String(actividad.porcentaje_planificado),
    porcentaje_real: String(actividad.porcentaje_real),
    costo_real: String(actividad.costo_real),
  }
}

function aDatosDelApi(campos) {
  return {
    nombre: campos.nombre,
    presupuesto_total: Number(campos.presupuesto_total),
    porcentaje_planificado: Number(campos.porcentaje_planificado),
    porcentaje_real: Number(campos.porcentaje_real),
    costo_real: Number(campos.costo_real),
  }
}

function Campo({ etiqueta, nombre, valor, alCambiar, ...atributos }) {
  return (
    <label className="campo">
      <span>{etiqueta}</span>
      <input name={nombre} value={valor} onChange={alCambiar} required {...atributos} />
    </label>
  )
}

export default function FormularioActividad({ actividadEnEdicion, alGuardar, alCancelar }) {
  const [campos, setCampos] = useState(
    actividadEnEdicion ? aTexto(actividadEnEdicion) : ACTIVIDAD_VACIA,
  )
  const editando = actividadEnEdicion !== null

  function cambiarCampo(evento) {
    setCampos({ ...campos, [evento.target.name]: evento.target.value })
  }

  function enviar(evento) {
    evento.preventDefault()
    alGuardar(aDatosDelApi(campos))
  }

  return (
    <form className="formulario" onSubmit={enviar}>
      <h3>{editando ? 'Editar actividad' : 'Nueva actividad'}</h3>
      <div className="campos">
        <Campo etiqueta="Nombre" nombre="nombre" valor={campos.nombre} alCambiar={cambiarCampo} />
        <Campo
          etiqueta="Presupuesto total (BAC)"
          nombre="presupuesto_total"
          valor={campos.presupuesto_total}
          alCambiar={cambiarCampo}
          type="number"
          min="0"
          step={PASO_DECIMAL}
        />
        <Campo
          etiqueta="% planificado"
          nombre="porcentaje_planificado"
          valor={campos.porcentaje_planificado}
          alCambiar={cambiarCampo}
          type="number"
          min="0"
          max={PORCENTAJE_MAXIMO}
          step={PASO_DECIMAL}
        />
        <Campo
          etiqueta="% real"
          nombre="porcentaje_real"
          valor={campos.porcentaje_real}
          alCambiar={cambiarCampo}
          type="number"
          min="0"
          max={PORCENTAJE_MAXIMO}
          step={PASO_DECIMAL}
        />
        <Campo
          etiqueta="Costo real (AC)"
          nombre="costo_real"
          valor={campos.costo_real}
          alCambiar={cambiarCampo}
          type="number"
          min="0"
          step={PASO_DECIMAL}
        />
      </div>
      <div className="acciones-formulario">
        <button type="submit" className="primario">
          {editando ? 'Guardar cambios' : 'Agregar actividad'}
        </button>
        {editando && (
          <button type="button" onClick={alCancelar}>
            Cancelar
          </button>
        )}
      </div>
    </form>
  )
}
