const API_URL = "http://127.0.0.1:5000/api";

const $ = (id) => document.getElementById(id);

// Código del estudiante
function getStudentId() {
    return localStorage.getItem('demo_student_id') || 'EST-80818-01';
}

function setStudentId(code) {
    const cleanCode = (code || 'EST-80818-01').trim().toUpperCase();
    localStorage.setItem('demo_student_id', cleanCode);
    return cleanCode;
}

const ACTIONS = ["Repasar en 2 horas", "Repasar en 1 día", "Repasar en 3 días", "Pausa activa"];
const WHEN_STUDENT = [
    "Te lo mostraremos de nuevo en 2 horas.",
    "Te lo mostraremos de nuevo en 1 día.",
    "Te lo mostraremos de nuevo en 3 días."
];
const STATE_NAMES = ["Latencia (normalizada)", "Acierto", "Repasos (÷10)", "Dificultad (÷3)"];

let themeRepasos = {
    "Sucesiones y Series Lógicas": "Pendiente",
    "Planteo de Ecuaciones y Proporciones": "Pendiente",
    "Problemas de Móviles y Cronometría": "Pendiente",
    "Porcentajes y Probabilidades": "Pendiente"
};

let streakData = {
    streakDays: 1,
    dailyProgressPercent: 0,
    missions: { m1: false, m2: false, m3: false, m4: false, m5: false },
    goalReached: false,
    canClaim: false
};
let streakError = false;

// ==============================================================
// GESTIÓN DE LA MASCOTA VIRTUAL
// ==============================================================
let mascotAccessories = { head: '🎓', body: '👔' };

const PHRASES_CORRECT = [
    "¡Brillante razonamiento! Deducción impecable. 👏",
    "¡Exacto! El patrón lógico estaba ahí. ⭐",
    "¡Muy bien resuelto! Agilidad mental en aumento. 🚀",
    "¡Excelente! Ritmo óptimo para afianzar el tema. 🎯",
    "¡Correcto! Fortaleciendo tu retención matemática. 🧠"
];

const PHRASES_WRONG = [
    "¡No te desanimes! De los errores surge el razonamiento. 💪",
    "Estuviste cerca. Fíjate en los detalles intermedios. 🧐",
    "¡Buen intento! El algoritmo adaptará este reactivo. 🔄",
    "¡Ánimo! Respira hondo y analiza la siguiente. 🦉",
    "Errar es parte del aprendizaje adaptativo. ¡Tú puedes! ✨"
];

function getRandomPhrase(isCorrect) {
    const list = isCorrect ? PHRASES_CORRECT : PHRASES_WRONG;
    return list[Math.floor(Math.random() * list.length)];
}

function updateMascotVisuals() {
    const qHead = $('quiz-acc-head');
    const qBody = $('quiz-acc-body');
    if (qHead) qHead.textContent = mascotAccessories.head;
    if (qBody) qBody.textContent = mascotAccessories.body;

    const dHead = $('dash-acc-head');
    const dBody = $('dash-acc-body');
    if (dHead) dHead.textContent = mascotAccessories.head;
    if (dBody) dBody.textContent = mascotAccessories.body;
}

function setAccessory(slot, icon) {
    if (streakData.dailyProgressPercent < 50 && !streakData.goalReached) {
        alert("¡Debes completar el 50% de las misiones diarias para equipar este accesorio!");
        return;
    }
    mascotAccessories[slot] = icon;
    localStorage.setItem("dqn_mascot_acc", JSON.stringify(mascotAccessories));
    updateMascotVisuals();
}

function loadMascotAccessories() {
    const saved = localStorage.getItem("dqn_mascot_acc");
    if (saved) {
        try { mascotAccessories = JSON.parse(saved); } catch (e) {}
    }
    updateMascotVisuals();
}

// ==============================================================
// API POSTGRESQL / RACHA
// ==============================================================
async function apiRacha(ruta = '', metodo = 'GET', cuerpo = null) {
    const res = await fetch(`${API_URL}/estudiante/${encodeURIComponent(getStudentId())}/racha${ruta}`, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: cuerpo ? JSON.stringify(cuerpo) : undefined
    });
    if (!res.ok) throw new Error(`Error ${res.status}`);
    return res.json();
}

async function loadStreak() {
    try {
        streakData = await apiRacha();
        streakError = false;
    } catch (err) {
        console.error(err);
        streakError = true;
    }
    renderStreakUI();
}

// ==============================================================
// PANTALLA INICIAL DE ACCESO
// ==============================================================
function showLoginView() {
    $('main-layout').className = 'layout login-mode';
    if ($('main-top-header')) $('main-top-header').hidden = true; // <-- Oculta el encabezado en el ingreso
    $('view-login').hidden = false;
    $('view-quiz').hidden = true;
    $('view-dashboard').hidden = true;
    $('lab-panel').hidden = true;
    $('btn-volver-dashboard').hidden = true;
}

function handleLogin(event) {
    if (event) event.preventDefault();
    const val = $('input-student-code').value;
    setStudentId(val);
    startGeneralQuiz();
}

let isGeneralQuiz = true;
let questions = [];
let currentIndex = 0;
let renderTime = 0;
let pauseTimer = null;
let results = [];
let selectedTemaForQuiz = null;

function shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

// ==============================================================
// FASE 1: EVALUACIÓN GENERAL (16 PREGUNTAS DIAGNÓSTICAS)
// ==============================================================
async function startGeneralQuiz() {
    isGeneralQuiz = true;
    loadMascotAccessories();
    loadStreak();

    $('main-layout').className = 'layout';
    if ($('main-top-header')) $('main-top-header').hidden = false; // <-- Se muestra en el cuestionario
    $('view-login').hidden = true;
    $('view-dashboard').hidden = true;
    $('view-quiz').hidden = false;
    $('lab-panel').hidden = false;

    $('btn-volver-dashboard').hidden = true;
    $('summary-tema').hidden = true;
    $('quiz-body').hidden = false;
    $('modal-final').hidden = true;
    $('modal-cuestionarios').hidden = true;

    if ($('mascot-quiz-bar')) $('mascot-quiz-bar').hidden = true;
    $('main-heading').textContent = "Evaluación General: Razonamiento Lógico-Matemático";

    try {
        const res = await fetch(`${API_URL}/questions`);
        if (!res.ok) throw new Error("Error al obtener banco general");
        const rawQuestions = await res.json();
        
        questions = shuffleArray(rawQuestions);
        currentIndex = 0;
        results = [];
        renderCurrentQuestion();
    } catch (err) {
        $('counter').innerText = "Sin conexión";
        $('question-title').innerText = "No se pudo conectar con el backend Flask. Ejecuta 'python backend/app.py' y recarga la página.";
        console.error(err);
    }
}

function renderProgress() {
    $('progress').innerHTML = questions.map((_, i) => {
        const cls = i < currentIndex ? 'done' : (i === currentIndex ? 'now' : '');
        return `<span class="${cls}"></span>`;
    }).join('');
}

function renderCurrentQuestion() {
    const q = questions[currentIndex];
    clearInterval(pauseTimer);
    $('pause-alert').hidden = true;
    $('next-btn').hidden = true;
    $('next-btn').textContent = currentIndex === questions.length - 1 ? 'Finalizar evaluación' : 'Siguiente reactivo';
    $('feedback').textContent = '';
    $('feedback').className = 'feedback';

    $('counter').innerHTML = `<b>Reactivo ${currentIndex + 1} de ${questions.length}</b> &nbsp;|&nbsp; <span class="theme-tag">${q.tema}</span>`;
    $('question-title').textContent = q.enunciado;
    renderProgress();

    const container = $('options-container');
    container.innerHTML = '';
    q.opciones.forEach((opt, index) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'opt-btn';
        btn.innerHTML = `<span class="letter">${String.fromCharCode(65 + index)}</span><span></span>`;
        btn.lastChild.textContent = opt;
        btn.onclick = () => handleAnswer(index, btn);
        container.appendChild(btn);
    });

    $('question-title').focus({ preventScroll: true });
    renderTime = performance.now();
}

async function handleAnswer(selectedIndex, clickedBtn) {
    const latencyMs = Math.round(performance.now() - renderTime);
    const q = questions[currentIndex];

    document.querySelectorAll('.opt-btn').forEach(b => { b.disabled = true; });
    $('telemetry-output').textContent = `Latencia: ${latencyMs} ms. Transmitiendo vector al algoritmo DQN…`;

    try {
        const res = await fetch(`${API_URL}/infer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: q.id, selected_option: selectedIndex, latency_ms: latencyMs })
        });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const result = await res.json();

        results.push({
            id: q.id,
            tema: q.tema,
            enunciado: q.enunciado,
            correct: result.is_correct,
            latency: latencyMs,
            action: result.action_id,
            action_desc: result.action_desc
        });

        // La mascota lanza frases solo si está visible (cuestionarios temáticos)
        if ($('mascot-quiz-bar') && !$('mascot-quiz-bar').hidden) {
            $('mascot-speech').textContent = getRandomPhrase(result.is_correct);
        }

        if (result.action_id === 0) themeRepasos[q.tema] = "Repasar en 2 horas";
        else if (result.action_id === 1) themeRepasos[q.tema] = "Repasar en 1 día";
        else if (result.action_id === 2) themeRepasos[q.tema] = "Repasar en 3 días";

        document.querySelectorAll('.opt-btn').forEach(b => { if (b !== clickedBtn) b.classList.add('dim'); });
        clickedBtn.classList.add(result.is_correct ? 'right' : 'wrong');

        const fb = $('feedback');
        fb.classList.add(result.is_correct ? 'ok' : 'bad');
        const verdict = document.createElement('span');
        verdict.className = 'verdict';
        verdict.textContent = result.is_correct ? 'Respuesta correcta.' : 'Respuesta incorrecta.';
        fb.appendChild(verdict);

        if (result.action_id !== 3) {
            const when = document.createElement('span');
            when.className = 'when';
            when.textContent = WHEN_STUDENT[result.action_id];
            fb.appendChild(when);
        }

        renderLab(result);

        if (result.action_id === 3) {
            if ($('mascot-quiz-bar') && !$('mascot-quiz-bar').hidden) {
                $('mascot-speech').textContent = "¡Tiempo elevado! Te recomiendo descansar 2 minutos.";
            }
            startPause();
        } else {
            $('next-btn').hidden = false;
            $('next-btn').focus();
        }
    } catch (err) {
        console.error(err);
        $('feedback').textContent = 'Error de comunicación con el backend.';
        $('feedback').classList.add('bad');
    }
}

function renderLab(r) {
    const argmax = r.q_values.indexOf(Math.max(...r.q_values));
    const byRule = r.action_id !== argmax;
    const maxAbs = Math.max(...r.q_values.map(Math.abs), 0.001);

    const bars = r.q_values.map((v, i) => {
        const w = Math.max(4, Math.round(Math.abs(v) / maxAbs * 100));
        return `<div class="qrow ${i === r.action_id ? 'chosen' : ''}">
            <div class="qlabel"><span>${ACTIONS[i]}</span><span>${v}</span></div>
            <div class="qtrack"><div class="qfill" style="width:${w}%"></div></div>
        </div>`;
    }).join('');

    const state = r.state_vector.map((v, i) => `<dt>${STATE_NAMES[i]}</dt><dd>${v}</dd>`).join('');

    $('telemetry-output').innerHTML = `
        <dl>
            <dt>Latencia</dt><dd>${r.latency_ms} ms</dd>
            <dt>Evaluación</dt><dd>${r.is_correct ? 'Correcto' : 'Incorrecto'}</dd>
        </dl>
        <h4>Vector de estado</h4>
        <dl>${state}</dl>
        <h4>Valores Q por acción</h4>
        <div class="qbars">${bars}</div>
        <div class="decision ${byRule ? 'rule' : ''}">
            <b>Decisión del algoritmo DQN: ${r.action_desc}</b>
            ${byRule ? '<br><small>Activado por regla de fatiga (latencia > 8 s).</small>' : ''}
        </div>`;
}

function startPause() {
    let remaining = 120;
    const show = () => {
        const m = Math.floor(remaining / 60);
        const s = String(remaining % 60).padStart(2, '0');
        $('pause-time').textContent = `${m}:${s}`;
    };
    $('pause-alert').hidden = false;
    show();
    pauseTimer = setInterval(() => {
        remaining--;
        show();
        if (remaining <= 0) endPause();
    }, 1000);
}

function endPause() {
    clearInterval(pauseTimer);
    $('pause-alert').hidden = true;
    $('next-btn').hidden = false;
    $('next-btn').focus();
}

function nextQuestion() {
    if (currentIndex === questions.length - 1) {
        if (isGeneralQuiz) {
            $('modal-final').hidden = false;
        } else {
            showTemaSummary();
        }
        return;
    }
    currentIndex++;
    renderCurrentQuestion();
}

// ==============================================================
// FASE 2: DASHBOARD (PÁGINA PRINCIPAL)
// ==============================================================
function goToDashboard() {
    $('modal-final').hidden = true;

    $('main-layout').className = 'layout dashboard-mode';
    if ($('main-top-header')) $('main-top-header').hidden = false; // <-- Visible en el dashboard
    $('view-login').hidden = true;
    $('view-quiz').hidden = true;
    $('lab-panel').hidden = true;
    $('view-dashboard').hidden = false;
    $('btn-volver-dashboard').hidden = true;
    $('main-heading').textContent = "Página Principal: Seguimiento y Repaso Adaptativo";

    loadStreak();
    renderDashboardThemes();
}

async function evaluateMissionsOnThemeQuiz(sessionResults) {
    if (isGeneralQuiz) return;
    const total = sessionResults.length;
    if (total === 0) return;

    const aciertos = sessionResults.filter(r => r.correct).length;
    const pausas = sessionResults.filter(r => r.action === 3).length;
    const latenciaPromedio = sessionResults.reduce((acc, r) => acc + r.latency, 0) / total / 1000;

    try {
        streakData = await apiRacha('/cuestionario', 'POST', {
            total, aciertos, pausas, latencia_promedio_s: latenciaPromedio
        });
        streakError = false;
    } catch (err) {
        console.error(err);
        streakError = true;
    }
    renderStreakUI();
}

function renderStreakUI() {
    $('streak-count-text').textContent = `Racha: ${streakData.streakDays} ${streakData.streakDays === 1 ? 'día' : 'días'}`;
    $('daily-progress-percent').textContent = `${streakData.dailyProgressPercent}% / 50%`;
    $('daily-progress-bar').style.width = `${(streakData.dailyProgressPercent / 50) * 100}%`;

    ['m1', 'm2', 'm3', 'm4', 'm5'].forEach((key, idx) => {
        const el = $(`m-${idx + 1}`);
        if (!el) return;
        if (streakData.missions[key]) {
            el.classList.add('done');
            el.querySelector('b').textContent = '✓ Listo (+10%)';
        } else {
            el.classList.remove('done');
            el.querySelector('b').textContent = '+10%';
        }
    });

    const btnClaim = $('btn-claim-streak');
    const hint = $('streak-status-hint');

    // Desbloqueo de la mascota al alcanzar el 50%
    const accControls = $('acc-controls');
    const badge = $('mascot-badge');
    const unlockMsg = $('mascot-unlock-msg');

    if (streakData.dailyProgressPercent >= 50 || streakData.goalReached) {
        if (accControls) {
            accControls.style.opacity = '1';
            accControls.style.pointerEvents = 'auto';
        }
        if (badge) {
            badge.textContent = '⭐ Desbloqueado';
            badge.classList.add('unlocked');
        }
        if (unlockMsg) {
            unlockMsg.textContent = '¡Felicidades! Has ganado la personalización de tu Mini Profesor.';
            unlockMsg.style.color = '#15803d';
            unlockMsg.style.fontWeight = 'bold';
        }
    }

    if (streakError) {
        btnClaim.hidden = true;
        hint.textContent = "No se pudo conectar con la base de datos. La racha no se está guardando.";
    } else if (streakData.canClaim) {
        btnClaim.hidden = false;
        hint.textContent = "¡Volviste al día siguiente! Reclama tu nuevo día de racha.";
    } else if (streakData.goalReached || streakData.dailyProgressPercent >= 50) {
        btnClaim.hidden = true;
        hint.textContent = "Meta diaria alcanzada (50%). Vuelve mañana para reclamar tu siguiente día de racha (+1 🔥).";
    } else {
        btnClaim.hidden = true;
        hint.textContent = "Resuelve los cuestionarios temáticos para completar las misiones de hoy.";
    }
}

async function claimNextStreak() {
    try {
        streakData = await apiRacha('/reclamar', 'POST');
        streakError = false;
        renderStreakUI();
        alert(`🎉 ¡Felicidades! Racha reclamada. Ahora tienes ${streakData.streakDays} días consecutivos.`);
    } catch (err) {
        console.error(err);
        alert("No se pudo reclamar la racha en este momento.");
        loadStreak();
    }
}

function renderDashboardThemes() {
    const container = $('themes-list-container');
    container.innerHTML = '';

    const badgeCls = (text) => {
        if (text.includes("2 horas")) return "repaso-2h";
        if (text.includes("1 día")) return "repaso-1d";
        if (text.includes("3 días")) return "repaso-3d";
        return "repaso-pending";
    };

    const listaTemas = [
        "Sucesiones y Series Lógicas",
        "Planteo de Ecuaciones y Proporciones",
        "Problemas de Móviles y Cronometría",
        "Porcentajes y Probabilidades"
    ];

    listaTemas.forEach(tema => {
        const val = themeRepasos[tema] && themeRepasos[tema] !== "Pendiente" 
            ? themeRepasos[tema] 
            : "Repasar en 1 día";

        const card = document.createElement('div');
        card.className = 'theme-item-card';
        card.onclick = () => openThemeModal(tema);
        card.innerHTML = `
            <div>
                <div class="theme-item-title">📘 ${tema}</div>
                <div class="theme-item-sub">3 cuestionarios disponibles (5 preguntas c/u)</div>
            </div>
            <span class="repaso-badge ${badgeCls(val)}">⏱️ ${val}</span>
        `;
        container.appendChild(card);
    });
}

function openThemeModal(tema) {
    selectedTemaForQuiz = tema;
    $('modal-tema-title').innerText = tema;
    $('modal-cuestionarios').hidden = false;
}

// ==============================================================
// FASE 3: CUESTIONARIOS TEMÁTICOS (MASCOTA ACTIVA)
// ==============================================================
async function startThemeQuiz(cuestionarioNum) {
    $('modal-cuestionarios').hidden = true;
    isGeneralQuiz = false;

    try {
        const res = await fetch(`${API_URL}/tema/${encodeURIComponent(selectedTemaForQuiz)}/cuestionario/${cuestionarioNum}`);
        if (!res.ok) throw new Error("Error al obtener cuestionario del tema");
        questions = await res.json();

        $('main-layout').className = 'layout';
        if ($('main-top-header')) $('main-top-header').hidden = false; // <-- Visible en el cuestionario temático
        $('view-dashboard').hidden = true;
        $('view-quiz').hidden = false;
        $('lab-panel').hidden = false;

        if ($('mascot-quiz-bar')) {
            $('mascot-quiz-bar').hidden = false;
            $('mascot-speech').textContent = "¡Cuestionario temático! Analiza con calma para desbloquear accesorios.";
        }

        $('btn-volver-dashboard').hidden = false;
        $('summary-tema').hidden = true;
        $('quiz-body').hidden = false;
        $('main-heading').textContent = `${selectedTemaForQuiz} - Cuestionario ${cuestionarioNum}`;

        currentIndex = 0;
        results = [];
        renderCurrentQuestion();
    } catch (err) {
        alert("Error al cargar el cuestionario. Verifica que el backend esté activo.");
        console.error(err);
    }
}

async function showTemaSummary() {
    clearInterval(pauseTimer);
    $('quiz-body').hidden = true;
    $('summary-tema').hidden = false;

    await evaluateMissionsOnThemeQuiz(results);

    const total = results.length;
    const aciertos = results.filter(r => r.correct).length;
    const promedio = total ? (results.reduce((a, r) => a + r.latency, 0) / total / 1000).toFixed(1) : '0.0';

    $('tema-stats').innerHTML = `
        <div><dt>Aciertos en este tema</dt><dd>${aciertos} de ${total}</dd></div>
        <div><dt>Tiempo Promedio</dt><dd>${promedio} s</dd></div>
        <div><dt>Progreso de Racha</dt><dd style="color:#c2410c;">${streakData.dailyProgressPercent}% / 50%</dd></div>
    `;
}

$('next-btn').addEventListener('click', nextQuestion);
$('skip-pause').addEventListener('click', endPause);

const btnClaim = $('btn-claim-streak');
if (btnClaim) btnClaim.addEventListener('click', claimNextStreak);

// Al cargar: solo muestra la tarjeta de acceso
window.onload = () => {
    $('input-student-code').value = getStudentId();
    showLoginView();
};