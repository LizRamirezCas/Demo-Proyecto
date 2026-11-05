import math
import random

# Estudiante simulado para entrenar al agente antes de usarlo con alumnos reales.
# El agente NO ve la fatiga ni la estabilidad de memoria (son ocultas);
# solo ve lo que ve la demo: latencia, acierto, repasos y dificultad.

INTERVALOS_DIAS = [2 / 24, 1.0, 3.0]   # acciones 0, 1, 2
ACCION_PAUSA = 3
RECUERDO_OBJETIVO = 0.85               # queremos repasar cuando aún se recuerda ~85 %


class EstudianteSimulado:
    def __init__(self, pasos_por_episodio=25, semilla=None):
        self.rng = random.Random(semilla)
        self.pasos_por_episodio = pasos_por_episodio

    def reset(self):
        self.paso = 0
        self.fatiga = self.rng.uniform(0.0, 0.3)
        self._nuevo_item()
        return self._observar()

    def _nuevo_item(self):
        self.dificultad = self.rng.choice([1, 2, 3])
        self.repasos = self.rng.randint(0, 9)
        # Estabilidad de memoria (en días): sube con los repasos y baja con la dificultad
        base = {1: 3.0, 2: 1.5, 3: 0.8}[self.dificultad]
        self.estabilidad = base * (1.4 ** self.repasos)
        self.dias_desde_ultimo = self.rng.uniform(0.1, 3.0)
        recuerdo = math.exp(-self.dias_desde_ultimo / self.estabilidad)
        p_acierto = min(max(recuerdo * (1 - 0.4 * self.fatiga) + 0.05, 0.0), 1.0)
        self.acierto = 1.0 if self.rng.random() < p_acierto else 0.0
        lat = (0.15 + 0.08 * self.dificultad) * (1 + 1.5 * self.fatiga)
        lat += self.rng.gauss(0, 0.04) + (0.1 if self.acierto == 0 else 0.0)
        self.latencia = min(max(lat, 0.02), 1.0)

    def _observar(self):
        return [self.latencia, self.acierto, self.repasos / 10.0, self.dificultad / 3.0]

    def step(self, accion):
        if accion == ACCION_PAUSA:
            recompensa = 0.6 if self.fatiga > 0.6 else -0.4
            self.fatiga = 0.1
        else:
            s_nueva = self.estabilidad * (1.5 if self.acierto else 0.6)
            recuerdo_proximo = math.exp(-INTERVALOS_DIAS[accion] / s_nueva)
            recompensa = 1.0 - 3.0 * abs(recuerdo_proximo - RECUERDO_OBJETIVO)
            if self.fatiga > 0.8:
                recompensa -= 0.6          # seguir sin descanso estando agotado
        self.fatiga = min(self.fatiga + 0.04 + 0.02 * self.dificultad, 1.0)
        self.paso += 1
        hecho = self.paso >= self.pasos_por_episodio
        self._nuevo_item()
        return self._observar(), recompensa, hecho