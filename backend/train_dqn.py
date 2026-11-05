import random
from collections import deque

import torch
import torch.nn as nn

from dqn_model import DQNNetwork
from simulador import EstudianteSimulado

EPISODIOS = 2000
GAMMA = 0.9
LR = 1e-3
BATCH = 64
CAPACIDAD_MEMORIA = 20000
ACTUALIZAR_TARGET_CADA = 200      # pasos
EPS_INICIO, EPS_FIN = 1.0, 0.05
SALIDA = "dqn_weights.pth"

torch.manual_seed(0)
random.seed(0)

env = EstudianteSimulado(semilla=0)
policy_net = DQNNetwork(4, 4)
target_net = DQNNetwork(4, 4)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizador = torch.optim.Adam(policy_net.parameters(), lr=LR)
memoria = deque(maxlen=CAPACIDAD_MEMORIA)
pasos_totales = 0


def elegir_accion(estado, epsilon):
    if random.random() < epsilon:
        return random.randrange(4)
    with torch.no_grad():
        return int(policy_net(torch.tensor(estado).unsqueeze(0)).argmax().item())


def entrenar_un_lote():
    if len(memoria) < BATCH:
        return
    lote = random.sample(memoria, BATCH)
    s, a, r, s2, d = zip(*lote)
    s = torch.tensor(s, dtype=torch.float32)
    a = torch.tensor(a).unsqueeze(1)
    r = torch.tensor(r, dtype=torch.float32)
    s2 = torch.tensor(s2, dtype=torch.float32)
    d = torch.tensor(d, dtype=torch.float32)

    q_actual = policy_net(s).gather(1, a).squeeze(1)
    with torch.no_grad():
        q_siguiente = target_net(s2).max(1).values
        objetivo = r + GAMMA * q_siguiente * (1 - d)
    perdida = nn.functional.smooth_l1_loss(q_actual, objetivo)

    optimizador.zero_grad()
    perdida.backward()
    nn.utils.clip_grad_norm_(policy_net.parameters(), 5.0)
    optimizador.step()


def evaluar(politica, episodios=200):
    prueba = EstudianteSimulado(semilla=123)
    total = 0.0
    for _ in range(episodios):
        s, hecho = prueba.reset(), False
        while not hecho:
            s, r, hecho = prueba.step(politica(s))
            total += r
    return total / episodios


for ep in range(EPISODIOS):
    epsilon = max(EPS_FIN, EPS_INICIO - ep / (EPISODIOS * 0.6) * (EPS_INICIO - EPS_FIN))
    estado, hecho = env.reset(), False
    while not hecho:
        accion = elegir_accion(estado, epsilon)
        estado2, recompensa, hecho = env.step(accion)
        memoria.append((estado, accion, recompensa, estado2, float(hecho)))
        estado = estado2
        entrenar_un_lote()
        pasos_totales += 1
        if pasos_totales % ACTUALIZAR_TARGET_CADA == 0:
            target_net.load_state_dict(policy_net.state_dict())

    if (ep + 1) % 250 == 0:
        voraz = lambda s: elegir_accion(s, 0.0)
        print(f"Episodio {ep + 1}/{EPISODIOS} | recompensa media (política aprendida): {evaluar(voraz):.2f}")

aleatoria = evaluar(lambda s: random.randrange(4))
aprendida = evaluar(lambda s: elegir_accion(s, 0.0))
print(f"\nPolítica aleatoria: {aleatoria:.2f}")
print(f"Política DQN entrenada: {aprendida:.2f}")

torch.save(policy_net.state_dict(), SALIDA)
print(f"Pesos guardados en {SALIDA}")