export default function SelectorProyecto({
  proyectos,
  proyectoId,
  alSeleccionar,
  alCrear,
  alRenombrar,
  alEliminar,
}) {
  const hayProyecto = proyectoId !== null
  return (
    <div className="selector-proyecto">
      <label htmlFor="selector-proyecto">Proyecto</label>
      <select
        id="selector-proyecto"
        value={proyectoId ?? ''}
        onChange={(evento) => alSeleccionar(Number(evento.target.value))}
        disabled={!hayProyecto}
      >
        {proyectos.map((proyecto) => (
          <option key={proyecto.id} value={proyecto.id}>
            {proyecto.nombre}
          </option>
        ))}
      </select>
      <button type="button" onClick={alCrear}>
        Nuevo
      </button>
      <button type="button" onClick={alRenombrar} disabled={!hayProyecto}>
        Renombrar
      </button>
      <button type="button" className="peligro" onClick={alEliminar} disabled={!hayProyecto}>
        Eliminar
      </button>
    </div>
  )
}
