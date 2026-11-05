-- Tablas de la demo. Se crean solas al encender el backend (init_db), pero puedes
-- ejecutarlas a mano en pgAdmin si prefieres.

CREATE TABLE IF NOT EXISTS estudiantes (
    id         TEXT PRIMARY KEY,
    creado_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Estado de la racha de cada estudiante (una fila por estudiante)
CREATE TABLE IF NOT EXISTS racha_estado (
    estudiante_id     TEXT PRIMARY KEY REFERENCES estudiantes(id) ON DELETE CASCADE,
    dias_racha        INTEGER NOT NULL DEFAULT 1,
    dia_actual        DATE    NOT NULL,           -- día al que pertenecen las misiones de abajo
    m1                BOOLEAN NOT NULL DEFAULT FALSE,
    m2                BOOLEAN NOT NULL DEFAULT FALSE,
    m3                BOOLEAN NOT NULL DEFAULT FALSE,
    m4                BOOLEAN NOT NULL DEFAULT FALSE,
    m5                BOOLEAN NOT NULL DEFAULT FALSE,
    cuestionarios_hoy INTEGER NOT NULL DEFAULT 0,
    meta_lograda_el   DATE,                       -- día en que completó las 5 misiones (50 %)
    actualizado_en    TIMESTAMPTZ NOT NULL DEFAULT now()
);
