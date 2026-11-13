import { formatearDinero, formatearIndice } from '../formato'
import Semaforo from './Semaforo'

function TarjetaIndice({ titulo, valor, interpretacion }) {
  return (
    <div className="tarjeta tarjeta-indice">
      <span className="tarjeta-titulo">{titulo}</span>
      <span className="tarjeta-valor">{formatearIndice(valor)}</span>
      <Semaforo interpretacion={interpretacion} />
    </div>
  )
}

function TarjetaMonto({ titulo, valor }) {
  return (
    <div className="tarjeta">
      <span className="tarjeta-titulo">{titulo}</span>
      <span className="tarjeta-valor">{formatearDinero(valor)}</span>
    </div>
  )
}

export default function TarjetasIndicadores({ indicadores }) {
  return (
    <section>
      <h2>Indicadores del proyecto</h2>
      <div className="tarjetas tarjetas-indices">
        <TarjetaIndice
          titulo="CPI · Desempeño de costo"
          valor={indicadores.cpi}
          interpretacion={indicadores.interpretacion_costo}
        />
        <TarjetaIndice
          titulo="SPI · Desempeño de cronograma"
          valor={indicadores.spi}
          interpretacion={indicadores.interpretacion_cronograma}
        />
      </div>
      <div className="tarjetas">
        <TarjetaMonto titulo="PV · Valor planificado" valor={indicadores.valor_planificado} />
        <TarjetaMonto titulo="EV · Valor ganado" valor={indicadores.valor_ganado} />
        <TarjetaMonto titulo="CV · Variación de costo" valor={indicadores.variacion_costo} />
        <TarjetaMonto
          titulo="SV · Variación de cronograma"
          valor={indicadores.variacion_cronograma}
        />
        <TarjetaMonto titulo="EAC · Costo estimado final" valor={indicadores.eac} />
        <TarjetaMonto titulo="VAC · Variación al final" valor={indicadores.vac} />
      </div>
    </section>
  )
}
