"""Reglas de la racha diaria. No toca la base de datos: recibe y devuelve diccionarios,
así se pueden probar sin PostgreSQL."""

MISIONES = ["m1", "m2", "m3", "m4", "m5"]
PORCENTAJE_POR_MISION = 20          # 5 misiones x 20 % = 100 % (tope diario)


class ReclamoNoDisponible(Exception):
    pass


def estado_nuevo(hoy):
    estado = {"dias_racha": 1, "dia_actual": hoy, "cuestionarios_hoy": 0, "meta_lograda_el": None}
    estado.update({m: False for m in MISIONES})
    return estado


def _reiniciar_misiones(estado, hoy):
    for m in MISIONES:
        estado[m] = False
    estado["cuestionarios_hoy"] = 0
    estado["meta_lograda_el"] = None
    estado["dia_actual"] = hoy


def normalizar_dia(estado, hoy):
    """Si cambió el día y la meta anterior NO se había logrado, las misiones empiezan de cero.
    Si la meta sí se logró y aún no se reclamó, se conserva hasta que la reclame."""
    if estado["dia_actual"] != hoy and estado["meta_lograda_el"] is None:
        _reiniciar_misiones(estado, hoy)
    return estado


def progreso(estado):
    return sum(1 for m in MISIONES if estado[m]) * PORCENTAJE_POR_MISION


def evaluar_cuestionario(estado, resumen, hoy):
    """resumen: total, aciertos, pausas, latencia_promedio_s de un cuestionario por tema."""
    normalizar_dia(estado, hoy)
    if estado["meta_lograda_el"] is not None:
        return estado                      # ya completó todo; falta reclamar

    estado["cuestionarios_hoy"] += 1
    total = resumen["total"]
    if total >= 5:
        estado["m1"] = True
    if resumen["pausas"] == 0:
        estado["m2"] = True
    if total > 0 and resumen["aciertos"] / total >= 0.6:
        estado["m3"] = True
    if resumen["latencia_promedio_s"] < 6.0:
        estado["m4"] = True
    if estado["cuestionarios_hoy"] >= 2:
        estado["m5"] = True

    if all(estado[m] for m in MISIONES):
        estado["meta_lograda_el"] = hoy
    return estado


def puede_reclamar(estado, hoy):
    meta = estado["meta_lograda_el"]
    return meta is not None and meta < hoy


def reclamar(estado, hoy):
    if not puede_reclamar(estado, hoy):
        raise ReclamoNoDisponible("Aún no se puede reclamar la racha.")
    estado["dias_racha"] += 1
    _reiniciar_misiones(estado, hoy)
    return estado


def a_json(estado, hoy):
    return {
        "streakDays": estado["dias_racha"],
        "dailyProgressPercent": progreso(estado),
        "missions": {m: bool(estado[m]) for m in MISIONES},
        "goalReached": estado["meta_lograda_el"] is not None,
        "canClaim": puede_reclamar(estado, hoy),
    }
