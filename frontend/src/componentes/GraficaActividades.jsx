import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { ALTO_GRAFICA, COLORES_GRAFICA } from '../constantes'
import { formatearDinero } from '../formato'

export default function GraficaActividades({ actividades }) {
  if (actividades.length === 0) return null

  const datos = actividades.map((actividad) => ({
    nombre: actividad.nombre,
    PV: actividad.indicadores.valor_planificado,
    EV: actividad.indicadores.valor_ganado,
    AC: actividad.costo_real,
  }))

  return (
    <section>
      <h2>PV vs EV vs AC por actividad</h2>
      <ResponsiveContainer width="100%" height={ALTO_GRAFICA}>
        <BarChart data={datos}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="nombre" />
          <YAxis tickFormatter={formatearDinero} width={110} />
          <Tooltip formatter={formatearDinero} />
          <Legend />
          <Bar dataKey="PV" name="PV (planificado)" fill={COLORES_GRAFICA.valorPlanificado} />
          <Bar dataKey="EV" name="EV (ganado)" fill={COLORES_GRAFICA.valorGanado} />
          <Bar dataKey="AC" name="AC (costo real)" fill={COLORES_GRAFICA.costoReal} />
        </BarChart>
      </ResponsiveContainer>
    </section>
  )
}
