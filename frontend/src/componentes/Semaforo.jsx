import { ESTADO_SEMAFORO } from '../constantes'

export default function Semaforo({ interpretacion }) {
  const color = ESTADO_SEMAFORO[interpretacion]
  return (
    <span className={`semaforo semaforo-${color}`}>
      <span className="semaforo-punto" aria-hidden="true" />
      {interpretacion}
    </span>
  )
}
