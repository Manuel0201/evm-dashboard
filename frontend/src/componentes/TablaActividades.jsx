import { formatearDinero, formatearIndice, formatearPorcentaje } from '../formato'
import Semaforo from './Semaforo'

const COLUMNAS = [
  'Actividad',
  'BAC',
  '% plan.',
  '% real',
  'AC',
  'PV',
  'EV',
  'CV',
  'SV',
  'CPI',
  'SPI',
  'EAC',
  'VAC',
  'Costo',
  'Cronograma',
  'Acciones',
]

function FilaActividad({ actividad, alEditar, alEliminar }) {
  const indicadores = actividad.indicadores
  return (
    <tr>
      <td className="texto">{actividad.nombre}</td>
      <td>{formatearDinero(actividad.presupuesto_total)}</td>
      <td>{formatearPorcentaje(actividad.porcentaje_planificado)}</td>
      <td>{formatearPorcentaje(actividad.porcentaje_real)}</td>
      <td>{formatearDinero(actividad.costo_real)}</td>
      <td>{formatearDinero(indicadores.valor_planificado)}</td>
      <td>{formatearDinero(indicadores.valor_ganado)}</td>
      <td>{formatearDinero(indicadores.variacion_costo)}</td>
      <td>{formatearDinero(indicadores.variacion_cronograma)}</td>
      <td>{formatearIndice(indicadores.cpi)}</td>
      <td>{formatearIndice(indicadores.spi)}</td>
      <td>{formatearDinero(indicadores.eac)}</td>
      <td>{formatearDinero(indicadores.vac)}</td>
      <td className="texto">
        <Semaforo interpretacion={indicadores.interpretacion_costo} />
      </td>
      <td className="texto">
        <Semaforo interpretacion={indicadores.interpretacion_cronograma} />
      </td>
      <td className="texto">
        <button type="button" onClick={() => alEditar(actividad)}>
          Editar
        </button>
        <button type="button" className="peligro" onClick={() => alEliminar(actividad)}>
          Eliminar
        </button>
      </td>
    </tr>
  )
}

export default function TablaActividades({ actividades, alEditar, alEliminar }) {
  if (actividades.length === 0) {
    return <p className="vacio">Este proyecto aún no tiene actividades.</p>
  }
  return (
    <div className="tabla-contenedor">
      <table>
        <thead>
          <tr>
            {COLUMNAS.map((columna) => (
              <th key={columna}>{columna}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {actividades.map((actividad) => (
            <FilaActividad
              key={actividad.id}
              actividad={actividad}
              alEditar={alEditar}
              alEliminar={alEliminar}
            />
          ))}
        </tbody>
      </table>
    </div>
  )
}
