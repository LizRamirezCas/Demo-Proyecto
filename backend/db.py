"""Conexión a PostgreSQL y guardado de la racha."""
import os
from contextlib import contextmanager
from datetime import date

import psycopg2
from psycopg2.extras import RealDictCursor

import racha

# Cambia la clave aquí o, mejor, define la variable de entorno DATABASE_URL.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:pamez17102005$@localhost:5432/demo_dqn",
)

RUTA_SCHEMA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")

CAMPOS = ["dias_racha", "dia_actual", "m1", "m2", "m3", "m4", "m5",
          "cuestionarios_hoy", "meta_lograda_el"]


@contextmanager
def conexion():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Crea las tablas si no existen."""
    with open(RUTA_SCHEMA, encoding="utf-8") as f:
        sql = f.read()
    with conexion() as conn, conn.cursor() as cur:
        cur.execute(sql)


def _cargar_bloqueado(cur, estudiante_id, hoy):
    """Crea al estudiante si es nuevo y devuelve su estado, bloqueando la fila
    para que dos peticiones a la vez no se pisen."""
    cur.execute("INSERT INTO estudiantes (id) VALUES (%s) ON CONFLICT DO NOTHING", (estudiante_id,))
    cur.execute(
        "INSERT INTO racha_estado (estudiante_id, dia_actual) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (estudiante_id, hoy),
    )
    cur.execute(
        "SELECT " + ", ".join(CAMPOS) + " FROM racha_estado WHERE estudiante_id = %s FOR UPDATE",
        (estudiante_id,),
    )
    return dict(cur.fetchone())


def _guardar(cur, estudiante_id, estado):
    cur.execute(
        """UPDATE racha_estado
              SET dias_racha = %s, dia_actual = %s,
                  m1 = %s, m2 = %s, m3 = %s, m4 = %s, m5 = %s,
                  cuestionarios_hoy = %s, meta_lograda_el = %s,
                  actualizado_en = now()
            WHERE estudiante_id = %s""",
        [estado[c] for c in CAMPOS] + [estudiante_id],
    )


def _operar(estudiante_id, funcion, hoy=None):
    """Abre una transacción, aplica una regla de racha y guarda el resultado."""
    hoy = hoy or date.today()
    with conexion() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        estado = _cargar_bloqueado(cur, estudiante_id, hoy)
        racha.normalizar_dia(estado, hoy)
        funcion(estado, hoy)
        _guardar(cur, estudiante_id, estado)
        return racha.a_json(estado, hoy)


def obtener_racha(estudiante_id):
    return _operar(estudiante_id, lambda estado, hoy: None)


def registrar_cuestionario(estudiante_id, resumen):
    return _operar(estudiante_id, lambda estado, hoy: racha.evaluar_cuestionario(estado, resumen, hoy))


def reclamar_racha(estudiante_id):
    return _operar(estudiante_id, lambda estado, hoy: racha.reclamar(estado, hoy))
