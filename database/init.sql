-- Script de inicialización de la base de datos del EVM Dashboard.
-- Uso: psql -U postgres -d evm_db -f database/init.sql
-- Es seguro ejecutarlo más de una vez: solo crea lo que no existe.

CREATE TABLE IF NOT EXISTS proyectos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS actividades (
    id SERIAL PRIMARY KEY,
    proyecto_id INTEGER NOT NULL REFERENCES proyectos (id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    presupuesto_total NUMERIC(14, 2) NOT NULL CHECK (presupuesto_total >= 0),
    porcentaje_planificado NUMERIC(5, 2) NOT NULL
        CHECK (porcentaje_planificado BETWEEN 0 AND 100),
    porcentaje_real NUMERIC(5, 2) NOT NULL
        CHECK (porcentaje_real BETWEEN 0 AND 100),
    costo_real NUMERIC(14, 2) NOT NULL CHECK (costo_real >= 0)
);

CREATE INDEX IF NOT EXISTS ix_actividades_proyecto_id ON actividades (proyecto_id);
