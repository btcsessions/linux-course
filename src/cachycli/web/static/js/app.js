/* ============================================================
   CachyCLI — Frontend Application
   ============================================================ */

const WEEK_NAMES = [
    "Terminal & Navigation",
    "File Operations",
    "Viewing & Editing",
    "Permissions & Users",
    "Text Processing",
    "Pipes & Redirection",
    "System Admin (CachyOS)",
];

let allLessons = [];
let currentView = "dashboard";
let currentLessonId = null;
let terminalHistory = [];
let sandboxActive = false;

/* ── Init ───────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", async () => {
    allLessons = await api("/api/lessons");
    renderSidebar();
    showProgress();
});

/* ── API helper ─────────────────────────────────────────────── */

async function api(url, opts) {
    const res = await fetch(url, opts);
    return res.json();
}

async function post(url, body) {
    return api(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
}

/* ── Sidebar ────────────────────────────────────────────────── */

function renderSidebar() {
    const el = document.getElementById("sidebar-list");
    let html = "";
    for (let w = 1; w <= 7; w++) {
        const weekLessons = allLessons.filter((l) => l.week === w);
        html += `<div class="week-group">`;
        html += `<div class="week-header">Week ${w} — ${WEEK_NAMES[w - 1]}</div>`;
        for (const l of weekLessons) {
            const active = l.id === currentLessonId ? " active" : "";
            const done = l.completed ? " done" : "";
            const check = l.completed ? "✓" : "";
            html += `<div class="lesson-item${active}" onclick="openLesson(${l.id})">
                <div class="check${done}">${check}</div>
                <div class="title">${l.title}</div>
                <div class="num">${l.id}</div>
            </div>`;
        }
        html += `<div class="quiz-item" onclick="openWeeklyQuiz(${w})">
            ✦ Week ${w} Quiz
        </div>`;
        html += `</div>`;
    }
    el.innerHTML = html;
}

function setNavActive(tab) {
    document.getElementById("nav-lessons").classList.toggle("active", tab === "lessons");
    document.getElementById("nav-progress").classList.toggle("active", tab === "progress");
}

/* ── Sidebar nav handlers ───────────────────────────────────── */

function showLessons() {
    setNavActive("lessons");
    if (currentLessonId) {
        openLesson(currentLessonId);
    } else {
        // Open the next lesson or lesson 1
        const next = allLessons.find((l) => !l.completed);
        openLesson(next ? next.id : 1);
    }
}

async function showProgress() {
    setNavActive("progress");
    currentView = "dashboard";
    const data = await api("/api/progress");
    const main = document.getElementById("main-content");

    let weeksHtml = "";
    for (const w of data.weeks) {
        const pct = w.total ? (w.done / w.total) * 100 : 0;
        const fillClass = pct === 100 ? " complete" : "";
        let badge = "";
        if (w.quiz_passed) {
            badge = `<span class="badge pass">${w.quiz_score.toFixed(0)}% ✓</span>`;
        } else if (pct === 100) {
            badge = `<span class="badge ready">Quiz Ready</span>`;
        }
        weeksHtml += `
        <div class="week-card">
            <div class="week-num">${w.week}</div>
            <div class="week-info">
                <div class="week-name">${w.name}</div>
                <div class="week-detail">${w.done}/${w.total} lessons complete</div>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill${fillClass}" style="width:${pct}%"></div>
            </div>
            ${badge}
        </div>`;
    }

    main.innerHTML = `
    <div class="dashboard fade-in">
        <h2>Your Progress</h2>
        <div class="stats-grid">
            <div class="stat-card streak">
                <div class="value">${data.current_streak}</div>
                <div class="label">Day Streak</div>
            </div>
            <div class="stat-card">
                <div class="value">${data.completed}/${data.total_lessons}</div>
                <div class="label">Lessons Done</div>
            </div>
            <div class="stat-card score">
                <div class="value">${data.avg_score > 0 ? data.avg_score.toFixed(0) + "%" : "—"}</div>
                <div class="label">Avg Score</div>
            </div>
            <div class="stat-card streak">
                <div class="value">${data.longest_streak}</div>
                <div class="label">Best Streak</div>
            </div>
        </div>
        <div class="week-cards">${weeksHtml}</div>
    </div>`;
}

/* ── Lesson View ────────────────────────────────────────────── */

async function openLesson(id) {
    setNavActive("lessons");
    currentLessonId = id;
    currentView = "lesson";
    renderSidebar();

    const les = await api("/api/lesson/" + id);
    const main = document.getElementById("main-content");

    const objHtml = les.objectives.map(function(o) { return "<li>" + o + "</li>"; }).join("");
    const cmdsHtml = les.commands.map(function(c) { return '<span class="command-tag">' + c + "</span>"; }).join("");

    const hasSandbox = les.sandbox_commands && les.sandbox_commands.length > 0;

    // Build shell without markdown body to avoid backtick/template-literal breakage.
    var shell = '<div class="lesson-view fade-in">' +
        '<div class="lesson-header">' +
            '<div class="lesson-breadcrumb">Week ' + les.week + ' &middot; Lesson ' + les.id + '</div>' +
            '<h2>' + escapeHtml(les.title) + '</h2>' +
            '<div class="lesson-meta">' +
                '<span>&#9201; ' + les.duration + ' min</span>' +
                '<span>' + (les.completed ? "&#10003; Completed" : "&#9675; Not started") + '</span>' +
            '</div>' +
        '</div>' +
        '<div class="objectives">' +
            '<h3>Learning Objectives</h3>' +
            '<ul>' + objHtml + '</ul>' +
        '</div>' +
        '<div class="commands-bar">' + cmdsHtml + '</div>' +
        '<div class="lesson-body" id="lesson-body"></div>';

    if (hasSandbox) {
        shell += '<div class="terminal-section">' +
            '<h3>Practice Terminal</h3>' +
            '<div class="terminal">' +
                '<div class="terminal-titlebar">' +
                    '<div class="terminal-dot red"></div>' +
                    '<div class="terminal-dot yellow"></div>' +
                    '<div class="terminal-dot green"></div>' +
                    '<span>sandbox &mdash; CachyCLI</span>' +
                '</div>' +
                '<div class="terminal-body" id="terminal-body">' +
                    '<div class="terminal-output" id="terminal-output"></div>' +
                    '<div class="terminal-input-line">' +
                        '<span class="terminal-prompt">$</span>' +
                        '<input class="terminal-input" id="terminal-input" ' +
                               'placeholder="Type a command..." ' +
                               'autocomplete="off" spellcheck="false">' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>';
    }

    shell += '<div class="lesson-actions">';
    if (!les.completed) {
        shell += '<button class="btn btn-success" onclick="completeLesson(' + les.id + ')">&#10003; Mark Complete</button>';
    }
    shell += '<button class="btn btn-primary" onclick="openLessonQuiz(' + les.id + ')">Take Quiz &rarr;</button>';
    if (les.id < 35) {
        shell += '<button class="btn btn-secondary" onclick="openLesson(' + (les.id + 1) + ')">Next Lesson &rarr;</button>';
    }
    shell += '</div></div>';

    main.innerHTML = shell;

    // Now inject the markdown body separately — safe from template literal issues.
    document.getElementById("lesson-body").innerHTML = marked.parse(les.body || "");

    // Scroll to top
    main.scrollTop = 0;

    // Init sandbox if available
    if (hasSandbox) {
        try {
            await initSandbox(les.sandbox_commands, les.sandbox_setup || "");
            var input = document.getElementById("terminal-input");
            if (input) {
                input.addEventListener("keydown", handleTerminalKey);
                input.focus();
            }
        } catch (err) {
            console.error("Sandbox init failed:", err);
            var output = document.getElementById("terminal-output");
            if (output) {
                output.innerHTML = '<span class="stderr">Sandbox failed to start: ' + escapeHtml(String(err)) + '</span>\n';
            }
        }
    }
}

async function completeLesson(id) {
    await post(`/api/lesson/${id}/complete`);
    allLessons = await api("/api/lessons");
    renderSidebar();
    openLesson(id);
}

/* ── Terminal / Sandbox ─────────────────────────────────────── */

async function initSandbox(allowedCommands, setupScript) {
    if (sandboxActive) {
        await post("/api/sandbox/stop");
    }
    var res = await post("/api/sandbox/start", {
        allowed_commands: allowedCommands,
        setup_script: setupScript,
    });
    sandboxActive = true;
    terminalHistory = [];
    var output = document.getElementById("terminal-output");
    if (output) {
        output.innerHTML = '<span class="stdout" style="color:#86868b">Sandbox started. Allowed: ' +
            escapeHtml(allowedCommands.join(", ")) + '\nType commands to practice.\n\n</span>';
    }
}

async function handleTerminalKey(e) {
    if (e.key !== "Enter") return;
    var input = document.getElementById("terminal-input");
    var cmd = input.value.trim();
    if (!cmd) return;

    input.value = "";
    terminalHistory.push(cmd);

    var output = document.getElementById("terminal-output");
    output.innerHTML += '<span class="cmd">$ ' + escapeHtml(cmd) + '</span>\n';

    if (cmd === "clear") {
        output.innerHTML = "";
        return;
    }

    try {
        var res = await post("/api/sandbox/run", { command: cmd });
        if (res.error) {
            output.innerHTML += '<span class="stderr">' + escapeHtml(res.error) + '</span>\n';
        } else {
            if (res.stdout) output.innerHTML += '<span class="stdout">' + escapeHtml(res.stdout) + '</span>';
            if (res.stderr) output.innerHTML += '<span class="stderr">' + escapeHtml(res.stderr) + '</span>\n';
            if (!res.stdout && !res.stderr) output.innerHTML += "\n";
        }
    } catch (err) {
        output.innerHTML += '<span class="stderr">Error: ' + escapeHtml(String(err)) + '</span>\n';
    }

    // Scroll terminal to bottom
    var body = document.getElementById("terminal-body");
    body.scrollTop = body.scrollHeight;
}

function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
}

/* ── Quiz View ──────────────────────────────────────────────── */

let quizData = null;
let quizAnswers = [];
let quizCurrentQ = 0;
let quizSubmitted = false;

async function openLessonQuiz(lessonId) {
    currentView = "quiz";
    const data = await api(`/api/quiz/lesson/${lessonId}`);
    startQuiz(data);
}

async function openWeeklyQuiz(week) {
    currentView = "quiz";
    const data = await api(`/api/quiz/weekly/${week}`);
    startQuiz(data);
}

function startQuiz(data) {
    quizData = data;
    quizAnswers = new Array(data.questions.length).fill(null);
    quizCurrentQ = 0;
    quizSubmitted = false;
    renderQuestion();
}

function renderQuestion() {
    const main = document.getElementById("main-content");
    const q = quizData.questions[quizCurrentQ];
    const total = quizData.questions.length;
    const pct = ((quizCurrentQ) / total) * 100;

    const title = quizData.quiz_type === "weekly"
        ? `Week ${quizData.quiz_id.split("_")[1]} Quiz`
        : `Lesson ${quizData.quiz_id.split("_")[1]} Quiz`;

    let choicesHtml = "";
    if (q.type === "multiple_choice") {
        const letters = ["A", "B", "C", "D", "E", "F"];
        choicesHtml = `<div class="choice-list">`;
        q.choices.forEach((c, idx) => {
            const sel = quizAnswers[quizCurrentQ] === String(idx) ? " selected" : "";
            choicesHtml += `
            <button class="choice-btn${sel}" onclick="selectAnswer('${idx}')">
                <div class="choice-letter">${letters[idx]}</div>
                <div>${c}</div>
            </button>`;
        });
        choicesHtml += `</div>`;
    } else if (q.type === "true_false") {
        const selT = quizAnswers[quizCurrentQ] === "true" ? " selected" : "";
        const selF = quizAnswers[quizCurrentQ] === "false" ? " selected" : "";
        choicesHtml = `
        <div class="tf-buttons">
            <button class="choice-btn${selT}" onclick="selectAnswer('true')">True</button>
            <button class="choice-btn${selF}" onclick="selectAnswer('false')">False</button>
        </div>`;
    } else if (q.type === "fill_in_blank") {
        const val = quizAnswers[quizCurrentQ] || "";
        choicesHtml = `
        <input class="fill-input" id="fill-input" placeholder="Type your answer..."
               value="${escapeHtml(val)}"
               onkeydown="if(event.key==='Enter')submitFill()"
               oninput="quizAnswers[quizCurrentQ]=this.value">`;
    }

    main.innerHTML = `
    <div class="quiz-view fade-in">
        <h2>${title}</h2>
        <div class="quiz-progress-text">Question ${quizCurrentQ + 1} of ${total}</div>
        <div class="quiz-progress-bar">
            <div class="quiz-progress-fill" style="width:${pct}%"></div>
        </div>
        <div class="question-card">
            <div class="q-number">Question ${quizCurrentQ + 1}</div>
            <div class="q-text">${q.question}</div>
            ${choicesHtml}
            <div id="quiz-feedback"></div>
        </div>
        <div class="lesson-actions">
            ${quizCurrentQ > 0 ? `<button class="btn btn-secondary" onclick="prevQuestion()">← Back</button>` : ""}
            <button class="btn btn-primary" id="next-btn" onclick="nextQuestion()" style="margin-left:auto">
                ${quizCurrentQ < total - 1 ? "Next →" : "Submit Quiz"}
            </button>
        </div>
    </div>`;

    main.scrollTop = 0;
    if (q.type === "fill_in_blank") {
        document.getElementById("fill-input").focus();
    }
}

function selectAnswer(val) {
    quizAnswers[quizCurrentQ] = val;
    renderQuestion();
}

function submitFill() {
    nextQuestion();
}

function prevQuestion() {
    if (quizCurrentQ > 0) {
        quizCurrentQ--;
        renderQuestion();
    }
}

function nextQuestion() {
    // Save fill-in answer if needed
    const fillInput = document.getElementById("fill-input");
    if (fillInput) {
        quizAnswers[quizCurrentQ] = fillInput.value;
    }

    if (quizAnswers[quizCurrentQ] === null || quizAnswers[quizCurrentQ] === "") {
        const fb = document.getElementById("quiz-feedback");
        fb.innerHTML = `<div class="feedback wrong">Please select or type an answer.</div>`;
        return;
    }

    if (quizCurrentQ < quizData.questions.length - 1) {
        quizCurrentQ++;
        renderQuestion();
    } else {
        submitQuiz();
    }
}

async function submitQuiz() {
    const result = await post("/api/quiz/submit", {
        quiz_type: quizData.quiz_type,
        quiz_id: quizData.quiz_id,
        answers: quizAnswers,
    });

    allLessons = await api("/api/lessons");
    renderSidebar();

    const main = document.getElementById("main-content");
    const passClass = result.passed ? "pass" : "fail";
    const statusText = result.passed ? "Passed!" : "Keep Practicing";

    let detailHtml = "";
    quizData.questions.forEach((q, i) => {
        const r = result.results[i];
        const icon = r.correct ? "✓" : "✗";
        const cls = r.correct ? "correct" : "wrong";
        detailHtml += `
        <div class="question-card" style="padding:16px 20px; margin-bottom:12px;">
            <div style="display:flex;gap:10px;align-items:start;">
                <span style="font-size:18px;color:${r.correct ? 'var(--green)' : 'var(--red)'}">${icon}</span>
                <div>
                    <div style="font-weight:600;margin-bottom:4px;">${q.question}</div>
                    ${!r.correct ? `<div style="font-size:13px;color:var(--red)">Your answer: ${quizAnswers[i]}</div>` : ""}
                    <div style="font-size:13px;color:var(--green)">Correct: ${r.correct_answer}</div>
                    ${r.explanation ? `<div style="font-size:12px;color:var(--text-muted);margin-top:4px">${r.explanation}</div>` : ""}
                </div>
            </div>
        </div>`;
    });

    main.innerHTML = `
    <div class="quiz-view fade-in">
        <div class="quiz-results">
            <div class="score-circle ${passClass}">
                ${result.percentage.toFixed(0)}%
                <span class="score-label">${result.score}/${result.total}</span>
            </div>
            <h3>${statusText}</h3>
            <p class="result-detail">You answered ${result.score} out of ${result.total} questions correctly.</p>
            <div class="lesson-actions" style="justify-content:center">
                <button class="btn btn-secondary" onclick="showProgress()">← Progress</button>
                ${currentLessonId ? `<button class="btn btn-primary" onclick="openLesson(${currentLessonId})">Back to Lesson</button>` : ""}
            </div>
        </div>
        <div style="margin-top:32px;">${detailHtml}</div>
    </div>`;

    main.scrollTop = 0;
}
