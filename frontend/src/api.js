import { CODIGO_DATOS_INVALIDOS, CODIGO_SIN_CONTENIDO, PREFIJO_API } from './constantes'

async function extraerMensajeDeError(respuesta) {
  const cuerpo = await respuesta.json().catch(() => null)
  if (respuesta.status === CODIGO_DATOS_INVALIDOS && Array.isArray(cuerpo?.detail)) {
    const campos = cuerpo.detail.map((error) => error.loc[error.loc.length - 1])
    return `Datos inválidos. Revise: ${campos.join(', ')}`
  }
  return cuerpo?.detail ?? `Error ${respuesta.status} al comunicarse con el servidor`
}

async function solicitar(ruta, metodo = 'GET', cuerpo = undefined) {
  const respuesta = await fetch(`${PREFIJO_API}${ruta}`, {
    method: metodo,
    headers: { 'Content-Type': 'application/json' },
    body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
  })
  if (!respuesta.ok) throw new Error(await extraerMensajeDeError(respuesta))
  if (respuesta.status === CODIGO_SIN_CONTENIDO) return null
  return respuesta.json()
}

export const listarProyectos = () => solicitar('/proyectos')
export const crearProyecto = (nombre) => solicitar('/proyectos', 'POST', { nombre })
export const renombrarProyecto = (id, nombre) => solicitar(`/proyectos/${id}`, 'PUT', { nombre })
export const eliminarProyecto = (id) => solicitar(`/proyectos/${id}`, 'DELETE')

export const listarActividades = (proyectoId) => solicitar(`/proyectos/${proyectoId}/actividades`)
export const consultarIndicadores = (proyectoId) =>
  solicitar(`/proyectos/${proyectoId}/indicadores`)
export const crearActividad = (proyectoId, datos) =>
  solicitar(`/proyectos/${proyectoId}/actividades`, 'POST', datos)
export const editarActividad = (id, datos) => solicitar(`/actividades/${id}`, 'PUT', datos)
export const eliminarActividad = (id) => solicitar(`/actividades/${id}`, 'DELETE')
