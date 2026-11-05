import torch
import torch.nn as nn

# Espacio de Estados S (dim=4): [latencia_normalizada, precision, conteo_repasos, dificultad]
# Espacio de Acciones A (dim=4):
# 0: Repasar en 2 horas (Refuerzo inmediato)
# 1: Repasar en 1 día (Espaciamiento corto)
# 2: Repasar en 3 días (Espaciamiento óptimo)
# 3: Activar Pausa Activa (Mitigación de fatiga atencional)

class DQNNetwork(nn.Module):
    def __init__(self, state_dim=4, action_dim=4):
        super(DQNNetwork, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, action_dim)
        )

    def forward(self, state):
        return self.fc(state)

def get_action_description(action_id):
    descriptions = {
        0: "Programar repaso en 2 horas (Carga cognitiva alta)",
        1: "Programar repaso en 1 día (Espaciamiento corto)",
        2: "Programar repaso en 3 días (Espaciamiento óptimo a largo plazo)",
        3: "Activar Alerta de Pausa Activa (Fatiga atencional detectada)"
    }
    return descriptions.get(action_id, "Acción no definida")