import { DECIMALES_DINERO, DECIMALES_INDICE, IDIOMA, TEXTO_NO_DISPONIBLE } from './constantes'

function crearFormateador(decimales) {
  return new Intl.NumberFormat(IDIOMA, {
    minimumFractionDigits: decimales,
    maximumFractionDigits: decimales,
  })
}

const formateadorDinero = crearFormateador(DECIMALES_DINERO)
const formateadorIndice = crearFormateador(DECIMALES_INDICE)

export function formatearDinero(valor) {
  if (valor === null) return TEXTO_NO_DISPONIBLE
  return `$ ${formateadorDinero.format(valor)}`
}

export function formatearIndice(valor) {
  if (valor === null) return TEXTO_NO_DISPONIBLE
  return formateadorIndice.format(valor)
}

export function formatearPorcentaje(valor) {
  return `${valor}%`
}
