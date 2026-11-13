export const PREFIJO_API = '/api'
export const CODIGO_SIN_CONTENIDO = 204
export const CODIGO_DATOS_INVALIDOS = 422

export const TEXTO_NO_DISPONIBLE = 'N/D'
export const DECIMALES_DINERO = 2
export const DECIMALES_INDICE = 2
export const PORCENTAJE_MAXIMO = 100
export const PASO_DECIMAL = '0.01'
export const IDIOMA = 'es-CO'

export const ALTO_GRAFICA = 340

export const COLORES_GRAFICA = {
  valorPlanificado: '#4f7cff',
  valorGanado: '#2e9e5b',
  costoReal: '#e0702b',
}

export const ESTADO_SEMAFORO = {
  'Bajo presupuesto': 'verde',
  Adelantado: 'verde',
  'En presupuesto': 'amarillo',
  'En tiempo': 'amarillo',
  'Sobre presupuesto': 'rojo',
  Atrasado: 'rojo',
  'No calculable': 'gris',
}

export const ACTIVIDAD_VACIA = {
  nombre: '',
  presupuesto_total: '',
  porcentaje_planificado: '',
  porcentaje_real: '',
  costo_real: '',
}
