import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch

from dqn_model import DQNNetwork, get_action_description
from preguntas import QUESTIONS, TEMAS_DATA

app = Flask(__name__)
CORS(app)  # Permite que el frontend se comunique con el backend

import db
from rutas_racha import racha_bp
app.register_blueprint(racha_bp)

# --- Configuración -----------------------------------------------------------
PESOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dqn_weights.pth")
USAR_REGLA_FATIGA = True
UMBRAL_FATIGA = 0.8   # 0.8 * 10 s = 8 s

# --- Red neuronal en modo inferencia ----------------------------------------
policy_net = DQNNetwork(state_dim=4, action_dim=4)
if os.path.exists(PESOS):
    policy_net.load_state_dict(torch.load(PESOS, map_location="cpu"))
    print(f"Pesos entrenados cargados desde {PESOS}")
else:
    print("AVISO: no se encontró dqn_weights.pth. La red usa pesos aleatorios. Ejecuta train_dqn.py.")
policy_net.eval()

# --- Base de datos PostgreSQL (racha) ----------------------------------------
try:
    db.init_db()
    print("PostgreSQL conectado: tablas listas.")
except Exception as err:
    print(f"AVISO: no se pudo conectar a PostgreSQL ({err}). La racha no se guardará.")

# Cuántas veces se ha respondido cada reactivo en la sesión actual
review_counts = {}


def buscar_pregunta_por_id(q_id):
    """Busca una pregunta por ID en QUESTIONS y dentro de todos los cuestionarios de TEMAS_DATA."""
    # 1. Buscar en la lista general inicial
    for q in QUESTIONS:
        if q["id"] == q_id:
            return q
            
    # 2. Si no está en QUESTIONS, buscar dentro de TEMAS_DATA (cuestionarios temáticos)
    for tema_info in TEMAS_DATA.values():
        for cuestionario in tema_info["cuestionarios"]:
            for q in cuestionario:
                if q["id"] == q_id:
                    return q
    return None


@app.route('/api/questions', methods=['GET'])
def get_questions():
    review_counts.clear()
    safe_questions = [
        {
            "id": q["id"],
            "tema": q["tema"],
            "enunciado": q["enunciado"],
            "opciones": q["opciones"],
            "dificultad": q["dificultad"]
        }
        for q in QUESTIONS
    ]
    return jsonify(safe_questions)


@app.route('/api/tema/<tema_nombre>/cuestionario/<int:cuestionario_num>', methods=['GET'])
def get_tema_cuestionario(tema_nombre, cuestionario_num):
    if tema_nombre not in TEMAS_DATA:
        return jsonify({"error": "Tema no encontrado"}), 404
    
    cuestionarios = TEMAS_DATA[tema_nombre]["cuestionarios"]
    if cuestionario_num < 1 or cuestionario_num > len(cuestionarios):
        return jsonify({"error": "Cuestionario fuera de rango"}), 404

    raw_list = cuestionarios[cuestionario_num - 1]
    safe_list = [
        {
            "id": q["id"],
            "tema": tema_nombre,
            "enunciado": q["enunciado"],
            "opciones": q["opciones"],
            "dificultad": q["dificultad"]
        }
        for q in raw_list
    ]
    return jsonify(safe_list)


@app.route('/api/infer', methods=['POST'])
def infer():
    data = request.get_json(silent=True) or {}
    q_id = data.get("question_id")
    selected_option = data.get("selected_option")
    latency_ms = data.get("latency_ms", 1000)

    # Búsqueda global del reactivo (soporta IDs de evaluación general e IDs > 100 de cuestionarios temáticos)
    question = buscar_pregunta_por_id(q_id)
    if question is None:
        return jsonify({"error": "Reactivo no encontrado"}), 404

    is_correct = 1.0 if selected_option == question["correcta"] else 0.0

    # 1. Normalización de latencia (escalada a 10 segundos máx.)
    norm_latency = min(max(latency_ms, 0) / 10000.0, 1.0)

    # 2. Conteo real de repasos de este reactivo
    repasos_previos = review_counts.get(q_id, 0)
    review_counts[q_id] = repasos_previos + 1
    review_norm = min(repasos_previos, 10) / 10.0

    difficulty = question.get("dificultad", 2.0)

    # 3. Vector de estado continuo S
    state_tensor = torch.tensor(
        [norm_latency, is_correct, review_norm, difficulty / 3.0], dtype=torch.float32
    )

    # 4. Inferencia mediante red DQN en PyTorch
    with torch.no_grad():
        q_values = policy_net(state_tensor.unsqueeze(0))
        if USAR_REGLA_FATIGA and norm_latency > UMBRAL_FATIGA:
            action_id = 3
        else:
            action_id = int(torch.argmax(q_values).item())

    action_desc = get_action_description(action_id)

    # Logging telemétrico de consola
    print(f"[LOG TELEMETRÍA] Q_ID: {q_id} | Latencia: {latency_ms} ms | Acierto: {is_correct} "
          f"| Repasos previos: {repasos_previos} | Acción DQN: {action_id} ({action_desc})")

    return jsonify({
        "is_correct": bool(is_correct),
        "latency_ms": latency_ms,
        "state_vector": [round(x.item(), 3) for x in state_tensor],
        "q_values": [round(v.item(), 3) for v in q_values[0]],
        "action_id": action_id,
        "action_desc": action_desc
    })


if __name__ == '__main__':
    print("Servidor backend corriendo en http://127.0.0.1:5000")
    app.run(port=5000, debug=True)