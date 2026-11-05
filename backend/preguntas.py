# Banco de reactivos estructurado por temas y cuestionarios
# Cada tema tiene:
# - evaluacion_general: 4 reactivos (los evaluados al inicio)
# - cuestionarios: 3 cuestionarios de 5 reactivos c/u (el Cuestionario 1 reutiliza los 4 iniciales + 1 extra)

TEMAS_DATA = {
    "Sucesiones y Series Lógicas": {
        "id_tema": "sucesiones",
        "cuestionarios": [
            # Cuestionario 1 (4 de la eval. general + 1 nueva)
            [
                {"id": 1, "dificultad": 1.0, "enunciado": "¿Qué número continúa en la serie: 5, 10, 15, 20, ...?", "opciones": ["22", "30", "25", "35"], "correcta": 2},
                {"id": 2, "dificultad": 2.0, "enunciado": "¿Qué número continúa en la serie lógica: 2, 6, 12, 20, 30, ...?", "opciones": ["40", "42", "44", "36"], "correcta": 1},
                {"id": 3, "dificultad": 2.0, "enunciado": "¿Qué número continúa en la serie: 1, 1, 2, 3, 5, 8, ...?", "opciones": ["11", "13", "12", "15"], "correcta": 1},
                {"id": 4, "dificultad": 3.0, "enunciado": "¿Qué término continúa: 3, 4, 7, 11, 18, 29, ...?", "opciones": ["45", "47", "51", "38"], "correcta": 1},
                {"id": 101, "dificultad": 2.0, "enunciado": "¿Qué número sigue en: 2, 3, 5, 7, 11, ...?", "opciones": ["12", "13", "15", "17"], "correcta": 1}
            ],
            # Cuestionario 2 (5 de refuerzo)
            [
                {"id": 102, "dificultad": 1.0, "enunciado": "¿Qué número sigue en: 100, 90, 80, 70, ...?", "opciones": ["50", "60", "65", "55"], "correcta": 1},
                {"id": 103, "dificultad": 2.0, "enunciado": "¿Qué número sigue en: 1, 4, 9, 16, 25, ...?", "opciones": ["30", "36", "49", "32"], "correcta": 1},
                {"id": 104, "dificultad": 2.0, "enunciado": "¿Qué letra sigue en la serie: A, C, E, G, ...?", "opciones": ["H", "I", "J", "K"], "correcta": 1},
                {"id": 105, "dificultad": 3.0, "enunciado": "¿Qué número sigue en: 2, 4, 8, 16, ...?", "opciones": ["24", "30", "32", "64"], "correcta": 2},
                {"id": 106, "dificultad": 3.0, "enunciado": "¿Qué número sigue en: 1, 2, 6, 24, ...?", "opciones": ["96", "120", "100", "144"], "correcta": 1}
            ],
            # Cuestionario 3 (5 de consolidación)
            [
                {"id": 107, "dificultad": 1.0, "enunciado": "¿Qué número sigue en: 4, 8, 12, 16, ...?", "opciones": ["18", "20", "22", "24"], "correcta": 1},
                {"id": 108, "dificultad": 2.0, "enunciado": "¿Qué número sigue en: 1, 8, 27, 64, ...?", "opciones": ["100", "125", "128", "81"], "correcta": 1},
                {"id": 109, "dificultad": 2.0, "enunciado": "¿Qué letra sigue: B, D, F, H, ...?", "opciones": ["I", "J", "K", "L"], "correcta": 1},
                {"id": 110, "dificultad": 3.0, "enunciado": "¿Qué número sigue: 3, 6, 11, 18, 27, ...?", "opciones": ["36", "38", "35", "40"], "correcta": 1},
                {"id": 111, "dificultad": 3.0, "enunciado": "¿Qué número sigue: 5, 6, 8, 11, 15, ...?", "opciones": ["19", "20", "21", "22"], "correcta": 1}
            ]
        ]
    },
    "Planteo de Ecuaciones y Proporciones": {
        "id_tema": "ecuaciones",
        "cuestionarios": [
            # Cuestionario 1 (4 eval. general + 1 nueva)
            [
                {"id": 5, "dificultad": 1.0, "enunciado": "Ana tiene el doble de lápices que Beto. Si entre los dos suman 18, ¿cuántos lápices tiene Ana?", "opciones": ["12", "6", "9", "14"], "correcta": 0},
                {"id": 6, "dificultad": 2.0, "enunciado": "Si 3 gatos cazan 3 ratones en 3 minutos, ¿cuántos minutos tardarán 10 gatos en cazar 10 ratones?", "opciones": ["3 minutos", "10 minutos", "30 minutos", "1 minuto"], "correcta": 0},
                {"id": 7, "dificultad": 2.0, "enunciado": "Un grifo llena un depósito en 6 h y otro en 3 h. Abiertos juntos, ¿en cuántas horas lo llenan?", "opciones": ["2 horas", "3 horas", "4.5 horas", "1.5 horas"], "correcta": 0},
                {"id": 8, "dificultad": 3.0, "enunciado": "Si x + 1/x = 3, ¿cuál es el valor numérico de x² + 1/x²?", "opciones": ["7", "5", "9", "11"], "correcta": 0},
                {"id": 201, "dificultad": 2.0, "enunciado": "La suma de tres números consecutivos es 33. ¿Cuál es el mayor?", "opciones": ["10", "11", "12", "13"], "correcta": 2}
            ],
            # Cuestionario 2
            [
                {"id": 202, "dificultad": 1.0, "enunciado": "El triple de un número aumentado en 5 es 20. ¿Cuál es el número?", "opciones": ["4", "5", "6", "3"], "correcta": 1},
                {"id": 203, "dificultad": 2.0, "enunciado": "Dos números están en relación 3 a 5 y suman 40. ¿Cuál es el menor?", "opciones": ["15", "25", "12", "18"], "correcta": 0},
                {"id": 204, "dificultad": 2.0, "enunciado": "Si a 20 le restas el doble de un número obtienes 6. ¿Cuál es el número?", "opciones": ["6", "7", "8", "9"], "correcta": 1},
                {"id": 205, "dificultad": 3.0, "enunciado": "Un padre tiene 40 años y su hijo 10. ¿Dentro de cuántos años el padre tendrá el triple de la edad del hijo?", "opciones": ["5 años", "10 años", "15 años", "8 años"], "correcta": 0},
                {"id": 206, "dificultad": 3.0, "enunciado": "En una granja hay 20 cabezas y 56 patas entre gallinas y conejos. ¿Cuántos conejos hay?", "opciones": ["8", "12", "10", "14"], "correcta": 0}
            ],
            # Cuestionario 3
            [
                {"id": 207, "dificultad": 1.0, "enunciado": "La mitad de un número es 14. ¿Cuál es su doble?", "opciones": ["28", "56", "42", "70"], "correcta": 1},
                {"id": 208, "dificultad": 2.0, "enunciado": "Si 4 cuadernos cuestan S/ 20, ¿cuánto costarán 7 cuadernos?", "opciones": ["S/ 35", "S/ 30", "S/ 28", "S/ 40"], "correcta": 0},
                {"id": 209, "dificultad": 2.0, "enunciado": "Un número sumado con su consecutivo da 45. ¿Cuál es el menor?", "opciones": ["21", "22", "23", "20"], "correcta": 1},
                {"id": 210, "dificultad": 3.0, "enunciado": "Si 5 obreros hacen una obra en 12 días, ¿cuántos obreros harán la misma obra en 6 días?", "opciones": ["8", "10", "12", "15"], "correcta": 1},
                {"id": 211, "dificultad": 3.0, "enunciado": "Un número excede a 15 tanto como 35 excede a dicho número. ¿Cuál es?", "opciones": ["20", "25", "30", "24"], "correcta": 1}
            ]
        ]
    },
    "Problemas de Móviles y Cronometría": {
        "id_tema": "moviles",
        "cuestionarios": [
            # Cuestionario 1 (4 eval. general + 1 nueva)
            [
                {"id": 9, "dificultad": 1.0, "enunciado": "Si el día de hoy es martes, ¿qué día de la semana será dentro de exactamente 10 días?", "opciones": ["Jueves", "Sábado", "Viernes", "Domingo"], "correcta": 2},
                {"id": 10, "dificultad": 2.0, "enunciado": "Dos autos distan 300 km y van al encuentro con 60 km/h y 40 km/h. ¿En cuántas horas se cruzan?", "opciones": ["2 h", "3 h", "4 h", "5 h"], "correcta": 1},
                {"id": 11, "dificultad": 3.0, "enunciado": "Un tren de 200 m viaja a 72 km/h. ¿Cuánto tarda en cruzar por completo un túnel de 400 m?", "opciones": ["20 s", "30 s", "45 s", "60 s"], "correcta": 1},
                {"id": 12, "dificultad": 3.0, "enunciado": "Una moto recorre 120 km a 60 km/h y regresa a 40 km/h. ¿Cuál es su velocidad media?", "opciones": ["50 km/h", "52 km/h", "48 km/h", "45 km/h"], "correcta": 2},
                {"id": 301, "dificultad": 2.0, "enunciado": "Un auto recorre 180 km en 3 horas a rapidez constante. ¿Cuál es su velocidad?", "opciones": ["50 km/h", "60 km/h", "70 km/h", "80 km/h"], "correcta": 1}
            ],
            # Cuestionario 2
            [
                {"id": 302, "dificultad": 1.0, "enunciado": "¿Cuántos minutos hay en 3 horas y media?", "opciones": ["180 min", "200 min", "210 min", "220 min"], "correcta": 2},
                {"id": 303, "dificultad": 2.0, "enunciado": "Dos móviles distan 200 m y van en el mismo sentido con 25 m/s y 15 m/s. ¿En qué tiempo se alcanza?", "opciones": ["10 s", "15 s", "20 s", "25 s"], "correcta": 2},
                {"id": 304, "dificultad": 2.0, "enunciado": "Si un reloj da 3 campanadas en 2 segundos, ¿cuánto tarda en dar 6 campanadas?", "opciones": ["4 s", "5 s", "6 s", "7 s"], "correcta": 1},
                {"id": 305, "dificultad": 3.0, "enunciado": "Un ciclista viaja a 36 km/h. Expresado en metros por segundo es:", "opciones": ["10 m/s", "12 m/s", "15 m/s", "8 m/s"], "correcta": 0},
                {"id": 306, "dificultad": 3.0, "enunciado": "¿Qué hora marca el reloj si el tiempo transcurrido del día es el triple de lo que falta transcurrir?", "opciones": ["16:00", "18:00", "20:00", "21:00"], "correcta": 1}
            ],
            # Cuestionario 3
            [
                {"id": 307, "dificultad": 1.0, "enunciado": "Si hoy es domingo, ¿qué día fue hace 8 días?", "opciones": ["Viernes", "Sábado", "Domingo", "Lunes"], "correcta": 1},
                {"id": 308, "dificultad": 2.0, "enunciado": "Un atleta recorre 400 m a 8 m/s. ¿Cuánto tarda?", "opciones": ["40 s", "50 s", "60 s", "45 s"], "correcta": 1},
                {"id": 309, "dificultad": 2.0, "enunciado": "Dos autos parten en sentidos opuestos a 50 km/h y 70 km/h. ¿A qué distancia están tras 2 horas?", "opciones": ["200 km", "220 km", "240 km", "260 km"], "correcta": 2},
                {"id": 310, "dificultad": 3.0, "enunciado": "Un tren cruza un poste en 8 s y viaja a 20 m/s. ¿Cuál es la longitud del tren?", "opciones": ["120 m", "140 m", "160 m", "180 m"], "correcta": 2},
                {"id": 311, "dificultad": 3.0, "enunciado": "Si faltan para las 12 del mediodía la mitad de horas que han pasado, ¿qué hora es?", "opciones": ["06:00", "07:00", "08:00", "09:00"], "correcta": 2}
            ]
        ]
    },
    "Porcentajes y Probabilidades": {
        "id_tema": "porcentajes",
        "cuestionarios": [
            # Cuestionario 1 (4 eval. general + 1 nueva)
            [
                {"id": 13, "dificultad": 1.0, "enunciado": "¿A cuánto equivale el 25 % del 40 % de 200?", "opciones": ["15", "20", "25", "30"], "correcta": 1},
                {"id": 14, "dificultad": 2.0, "enunciado": "Un producto sube 20 % y ahora cuesta S/ 60. ¿Cuánto costaba antes del incremento?", "opciones": ["S/ 48", "S/ 52", "S/ 40", "S/ 50"], "correcta": 3},
                {"id": 15, "dificultad": 2.0, "enunciado": "Al lanzar dos dados legales, ¿cuál es la probabilidad de que la suma sea 7?", "opciones": ["1/12", "1/9", "7/36", "1/6"], "correcta": 3},
                {"id": 16, "dificultad": 3.0, "enunciado": "En una urna hay 4 bolas rojas y 6 negras. Si se extraen 2 sin reposición, ¿probabilidad de 2 rojas?", "opciones": ["2/15", "4/25", "1/5", "3/10"], "correcta": 0},
                {"id": 401, "dificultad": 2.0, "enunciado": "¿Cuál es el 15 % de 180?", "opciones": ["25", "27", "28", "26"], "correcta": 1}
            ],
            # Cuestionario 2
            [
                {"id": 402, "dificultad": 1.0, "enunciado": "¿Qué porcentaje representa 15 de 60?", "opciones": ["20 %", "25 %", "30 %", "15 %"], "correcta": 1},
                {"id": 403, "dificultad": 2.0, "enunciado": "Si se lanza una moneda dos veces, ¿probabilidad de obtener dos caras?", "opciones": ["1/2", "1/3", "1/4", "1/6"], "correcta": 2},
                {"id": 404, "dificultad": 2.0, "enunciado": "Un artículo de S/ 100 tiene dos descuentos sucesivos del 10 % y 10 %. ¿Precio final?", "opciones": ["S/ 80", "S/ 81", "S/ 85", "S/ 90"], "correcta": 1},
                {"id": 405, "dificultad": 3.0, "enunciado": "En una bolsa hay 5 bolas azules y 3 amarillas. ¿Probabilidad de sacar una azul?", "opciones": ["3/8", "5/8", "1/2", "5/3"], "correcta": 1},
                {"id": 406, "dificultad": 3.0, "enunciado": "Si el lado de un cuadrado aumenta en 20 %, ¿en qué porcentaje aumenta su área?", "opciones": ["40 %", "44 %", "20 %", "24 %"], "correcta": 1}
            ],
            # Cuestionario 3
            [
                {"id": 407, "dificultad": 1.0, "enunciado": "¿Cuánto es el 50 % del 50 % de 400?", "opciones": ["100", "150", "200", "50"], "correcta": 0},
                {"id": 408, "dificultad": 2.0, "enunciado": "Al lanzar un dado, ¿cuál es la probabilidad de sacar un número primo?", "opciones": ["1/3", "1/2", "2/3", "1/6"], "correcta": 1},
                {"id": 409, "dificultad": 2.0, "enunciado": "Un televisor de S/ 800 tiene un descuento del 25 %. ¿Cuánto se paga?", "opciones": ["S/ 500", "S/ 600", "S/ 650", "S/ 550"], "correcta": 1},
                {"id": 410, "dificultad": 3.0, "enunciado": "De una baraja de 52 cartas, ¿probabilidad de extraer un as?", "opciones": ["1/13", "1/26", "1/52", "4/13"], "correcta": 0},
                {"id": 411, "dificultad": 3.0, "enunciado": "Dos aumentos sucesivos del 20 % y 25 % equivalen a un aumento único de:", "opciones": ["45 %", "50 %", "55 %", "48 %"], "correcta": 1}
            ]
        ]
    }
}

# Lista plana de las 16 preguntas para la Evaluación General inicial (primeras 4 de cada tema)
QUESTIONS = []
for tema_nombre, data in TEMAS_DATA.items():
    # Primeras 4 del cuestionario 1 de cada tema
    for q in data["cuestionarios"][0][:4]:
        q_copy = dict(q)
        q_copy["tema"] = tema_nombre
        QUESTIONS.append(q_copy)