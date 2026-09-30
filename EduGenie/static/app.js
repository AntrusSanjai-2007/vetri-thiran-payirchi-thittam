const state = { task: "qa" };

const labels = {
    qa: {
        label: "Ask a question",
        placeholder: "Example: Which is the largest ocean?",
        button: "Ask EduGenie",
        title: "Answer"
    },
    explain: {
        label: "Topic or concept",
        placeholder: "Example: Explain photosynthesis in simple words.",
        button: "Explain",
        title: "Explanation"
    },
    quiz: {
        label: "Topic or educational passage",
        placeholder: "Paste a passage or enter a topic. EduGenie will create 3 MCQs.",
        button: "Generate Quiz",
        title: "Practice Quiz"
    },
    summarize: {
        label: "Educational passage",
        placeholder: "Paste the paragraph or notes you want to summarize.",
        button: "Summarize",
        title: "Summary"
    },
    learn: {
        label: "Learning topic",
        placeholder: "Example: SQL",
        button: "Build Learning Path",
        title: "Learning Path"
    }
};

const taskButtons = document.querySelectorAll(".task-btn");
const input = document.getElementById("user-input");
const label = document.getElementById("input-label");
const submitText = document.getElementById("submit-text");
const form = document.getElementById("task-form");
const resultCard = document.getElementById("result-card");
const result = document.getElementById("result");
const resultTitle = document.getElementById("result-title");
const spinner = document.getElementById("spinner");
const extraOptions = document.getElementById("extra-options");
const level = document.getElementById("level");

function setTask(task) {
    state.task = task;
    taskButtons.forEach(btn => btn.classList.toggle("active", btn.dataset.task === task));

    const config = labels[task];
    label.textContent = config.label;
    input.placeholder = config.placeholder;
    submitText.textContent = config.button;
    extraOptions.classList.toggle("hidden", task !== "learn");
    input.focus();
}

taskButtons.forEach(btn => btn.addEventListener("click", () => setTask(btn.dataset.task)));

document.getElementById("clear-btn").addEventListener("click", () => {
    input.value = "";
    result.innerHTML = "";
    resultCard.classList.add("hidden");
});

document.getElementById("copy-btn").addEventListener("click", async () => {
    const text = result.innerText.trim();
    if (!text) return;
    try {
        await navigator.clipboard.writeText(text);
        document.getElementById("copy-btn").textContent = "Copied";
        setTimeout(() => document.getElementById("copy-btn").textContent = "Copy", 1200);
    } catch {
        alert("Copy is not available in this browser.");
    }
});

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderText(text) {
    const safe = escapeHtml(text);
    return safe
        .split(/\n{2,}/)
        .map(block => `<p>${block.replaceAll("\n", "<br>")}</p>`)
        .join("");
}

function renderQuiz(quiz) {
    return quiz.map((item, index) => {
        const options = item.options.map(option =>
            `<button class="option" data-question="${index}" data-answer="${escapeHtml(option)}">${escapeHtml(option)}</button>`
        ).join("");

        return `
            <div class="quiz-question">
                <h3>${index + 1}. ${escapeHtml(item.question)}</h3>
                <div>${options}</div>
                <div class="quiz-explanation hidden">
                    <strong>Explanation:</strong> ${escapeHtml(item.explanation || "")}
                </div>
            </div>
        `;
    }).join("");
}

function attachQuizHandlers(quiz) {
    result.querySelectorAll(".quiz-question").forEach((box, index) => {
        const question = quiz[index];
        const explanation = box.querySelector(".quiz-explanation");

        box.querySelectorAll(".option").forEach(button => {
            button.addEventListener("click", () => {
                box.querySelectorAll(".option").forEach(btn => {
                    btn.disabled = true;
                    if (btn.dataset.answer === question.correct_answer) {
                        btn.classList.add("correct");
                    }
                });

                if (button.dataset.answer !== question.correct_answer) {
                    button.classList.add("wrong");
                }
                explanation.classList.remove("hidden");
            });
        });
    });
}

async function postJson(url, payload) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.detail || `Request failed with HTTP ${response.status}`);
    }

    return data;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = input.value.trim();
    if (!text) {
        input.focus();
        return;
    }

    spinner.classList.remove("hidden");
    submitText.textContent = "Working...";
    resultCard.classList.remove("hidden");
    resultTitle.textContent = labels[state.task].title;
    result.innerHTML = "<p>EduGenie is generating your result...</p>";

    try {
        let data;

        if (state.task === "qa") {
            data = await postJson("/qa", { question: text });
            result.innerHTML = renderText(data.answer);
        } else if (state.task === "explain") {
            data = await postJson("/explain", { text });
            result.innerHTML = renderText(data.explanation);
        } else if (state.task === "summarize") {
            data = await postJson("/summarize", { text });
            result.innerHTML = renderText(data.summary);
        } else if (state.task === "quiz") {
            data = await postJson("/quiz", { text, count: 3 });
            result.innerHTML = renderQuiz(data.quiz);
            attachQuizHandlers(data.quiz);
        } else if (state.task === "learn") {
            data = await postJson("/learn/recommendations", {
                topic: text,
                level: level.value
            });
            result.innerHTML = renderText(data.recommendations);
        }
    } catch (error) {
        result.innerHTML = `<div class="error"><strong>Error:</strong> ${escapeHtml(error.message)}</div>`;
    } finally {
        spinner.classList.add("hidden");
        submitText.textContent = labels[state.task].button;
    }
});

setTask("qa");
