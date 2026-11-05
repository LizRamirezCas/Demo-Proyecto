"""Rutas de la API para la racha diaria."""
import re

from flask import Blueprint, jsonify, request

import db
import racha

racha_bp = Blueprint("racha", __name__, url_prefix="/api")

ID_VALIDO = re.compile(r"^[A-Za-z0-9_-]{4,64}$")


def _id_o_error(estudiante_id):
    if not ID_VALIDO.match(estudiante_id):
        return jsonify({"error": "Identificador de estudiante no válido"}), 400
    return None


def _error_db(err):
    print(f"[ERROR BASE DE DATOS] {err}")
    return jsonify({"error": "No se pudo acceder a la base de datos"}), 503


@racha_bp.route("/estudiante/<estudiante_id>/racha", methods=["GET"])
def get_racha(estudiante_id):
    malo = _id_o_error(estudiante_id)
    if malo:
        return malo
    try:
        return jsonify(db.obtener_racha(estudiante_id))
    except Exception as err:
        return _error_db(err)


@racha_bp.route("/estudiante/<estudiante_id>/racha/cuestionario", methods=["POST"])
def post_cuestionario(estudiante_id):
    malo = _id_o_error(estudiante_id)
    if malo:
        return malo
    datos = request.get_json(silent=True) or {}
    try:
        resumen = {
            "total": int(datos["total"]),
            "aciertos": int(datos["aciertos"]),
            "pausas": int(datos["pausas"]),
            "latencia_promedio_s": float(datos["latencia_promedio_s"]),
        }
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Datos del cuestionario incompletos"}), 400
    if not (1 <= resumen["total"] <= 50) or not (0 <= resumen["aciertos"] <= resumen["total"]) \
            or resumen["pausas"] < 0 or resumen["latencia_promedio_s"] < 0:
        return jsonify({"error": "Datos del cuestionario fuera de rango"}), 400
    try:
        return jsonify(db.registrar_cuestionario(estudiante_id, resumen))
    except Exception as err:
        return _error_db(err)


@racha_bp.route("/estudiante/<estudiante_id>/racha/reclamar", methods=["POST"])
def post_reclamar(estudiante_id):
    malo = _id_o_error(estudiante_id)
    if malo:
        return malo
    try:
        return jsonify(db.reclamar_racha(estudiante_id))
    except racha.ReclamoNoDisponible as err:
        return jsonify({"error": str(err)}), 409
    except Exception as err:
        return _error_db(err)
