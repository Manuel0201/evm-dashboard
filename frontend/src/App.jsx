import { useEffect, useState } from 'react'
import * as api from './api'
import FormularioActividad from './componentes/FormularioActividad'
import GraficaActividades from './componentes/GraficaActividades'
import SelectorProyecto from './componentes/SelectorProyecto'
import TablaActividades from './componentes/TablaActividades'
import TarjetasIndicadores from './componentes/TarjetasIndicadores'
import './App.css'

export default function App() {
  const [proyectos, setProyectos] = useState([])
  const [proyectoId, setProyectoId] = useState(null)
  const [datos, setDatos] = useState(null)
  const [actividadEnEdicion, setActividadEnEdicion] = useState(null)
  const [error, setError] = useState(null)
  const [versionProyectos, setVersionProyectos] = useState(0)
  const [versionDatos, setVersionDatos] = useState(0)

  useEffect(() => {
    let cancelado = false
    api
      .listarProyectos()
      .then((lista) => {
        if (cancelado) return
        setProyectos(lista)
        setProyectoId((actual) =>
          lista.some((proyecto) => proyecto.id === actual) ? actual : (lista[0]?.id ?? null),
        )
      })
      .catch((falla) => !cancelado && setError(falla.message))
    return () => {
      cancelado = true
    }
  }, [versionProyectos])

  useEffect(() => {
    if (proyectoId === null) return undefined
    let cancelado = false
    Promise.all([api.listarActividades(proyectoId), api.consultarIndicadores(proyectoId)])
      .then(([actividades, indicadores]) => {
        if (!cancelado) setDatos({ proyectoId, actividades, indicadores })
      })
      .catch((falla) => !cancelado && setError(falla.message))
    return () => {
      cancelado = true
    }
  }, [proyectoId, versionDatos])

  const recargarProyectos = () => setVersionProyectos((version) => version + 1)
  const recargarDatos = () => setVersionDatos((version) => version + 1)
  const datosDelProyecto = datos?.proyectoId === proyectoId ? datos : null
  const proyectoActual = proyectos.find((proyecto) => proyecto.id === proyectoId)

  async function ejecutar(accion) {
    try {
      await accion()
      setError(null)
    } catch (falla) {
      setError(falla.message)
    }
  }

  function seleccionarProyecto(id) {
    setActividadEnEdicion(null)
    setProyectoId(id)
  }

  function crearProyecto() {
    const nombre = window.prompt('Nombre del nuevo proyecto')
    if (!nombre) return
    ejecutar(async () => {
      const nuevo = await api.crearProyecto(nombre)
      seleccionarProyecto(nuevo.id)
      recargarProyectos()
    })
  }

  function renombrarProyecto() {
    const nombre = window.prompt('Nuevo nombre del proyecto', proyectoActual.nombre)
    if (!nombre) return
    ejecutar(async () => {
      await api.renombrarProyecto(proyectoId, nombre)
      recargarProyectos()
    })
  }

  function eliminarProyecto() {
    if (!window.confirm(`¿Eliminar "${proyectoActual.nombre}" y todas sus actividades?`)) return
    ejecutar(async () => {
      await api.eliminarProyecto(proyectoId)
      seleccionarProyecto(null)
      recargarProyectos()
    })
  }

  function guardarActividad(datosActividad) {
    ejecutar(async () => {
      if (actividadEnEdicion) {
        await api.editarActividad(actividadEnEdicion.id, datosActividad)
      } else {
        await api.crearActividad(proyectoId, datosActividad)
      }
      setActividadEnEdicion(null)
      recargarDatos()
    })
  }

  function eliminarActividad(actividad) {
    if (!window.confirm(`¿Eliminar la actividad "${actividad.nombre}"?`)) return
    ejecutar(async () => {
      await api.eliminarActividad(actividad.id)
      if (actividadEnEdicion?.id === actividad.id) setActividadEnEdicion(null)
      recargarDatos()
    })
  }

  return (
    <main className="aplicacion">
      <header>
        <h1>EVM Dashboard</h1>
        <p>Seguimiento de proyectos con Valor Ganado</p>
      </header>

      {error && (
        <div className="error" role="alert">
          <span>{error}</span>
          <button type="button" onClick={() => setError(null)}>
            Cerrar
          </button>
        </div>
      )}

      <SelectorProyecto
        proyectos={proyectos}
        proyectoId={proyectoId}
        alSeleccionar={seleccionarProyecto}
        alCrear={crearProyecto}
        alRenombrar={renombrarProyecto}
        alEliminar={eliminarProyecto}
      />

      {proyectoId === null && <p className="vacio">Cree un proyecto para comenzar.</p>}

      {datosDelProyecto && (
        <>
          <TarjetasIndicadores indicadores={datosDelProyecto.indicadores} />
          <section>
            <h2>Actividades</h2>
            <TablaActividades
              actividades={datosDelProyecto.actividades}
              alEditar={setActividadEnEdicion}
              alEliminar={eliminarActividad}
            />
            <FormularioActividad
              key={`${actividadEnEdicion?.id ?? 'nueva'}-${versionDatos}`}
              actividadEnEdicion={actividadEnEdicion}
              alGuardar={guardarActividad}
              alCancelar={() => setActividadEnEdicion(null)}
            />
          </section>
          <GraficaActividades actividades={datosDelProyecto.actividades} />
        </>
      )}
    </main>
  )
}
