let cards = [];
let current = 0;
let currentDomain = "";
let currentUser = null;
const quizNextBtn = document.getElementById("quiz-next-btn");


// Register new user
function register() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  fetch("/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      const msg = document.getElementById("auth-message");
      if (data.success) {
        msg.textContent = "✅ Registered successfully! Please log in.";
        msg.style.color = "limegreen";
      } else {
        msg.textContent = "⚠️ " + data.error;
        msg.style.color = "red";
      }
    });
}

// Login user
function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      const msg = document.getElementById("auth-message");
      if (data.success) {
        currentUser = username;
        localStorage.setItem("user", username);

        document.getElementById("auth-section").classList.add("hidden");
        document.getElementById("dashboard").classList.remove("hidden");

        loadFlashcards(); // load default domain
      } else {
        msg.textContent = "⚠️ " + data.error;
        msg.style.color = "red";
      }
    });
}

// Logout
function logout() {
  localStorage.removeItem("user");
  currentUser = null;
  fetch("/api/logout").finally(() => location.reload());
}

// Load flashcards for chosen domain
function loadFlashcards() {
  const domain = document.getElementById("domain-select").value;
  currentDomain = domain;

  fetch("/api/get_flashcards", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ domain }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success && data.cards.length > 0) {
        cards = data.cards;
        current = 0;
        showCard();
      } else {
        document.getElementById("flashcard").classList.add("hidden");
        document.getElementById("flashcard-message").textContent =
          "⚠️ No flashcards available for this domain yet.";
      }
    });
}

// Show current flashcard
function showCard() {
  if (cards.length === 0) return;

  const card = cards[current];
  const flashcard = document.getElementById("flashcard");

  flashcard.classList.remove("hidden");
  document.getElementById("flashcard-message").textContent = "";

  document.getElementById("question").textContent = card.question;
  document.getElementById("answer").textContent =
    "💡 Answer: " + card.options[card.answer_index];
}

// Next card
function nextCard() {
  if (cards.length === 0) return;
  current = (current + 1) % cards.length;
  showCard();
}

// Show stats modal
function showStats() {
  fetch("/api/stats")
    .then(res => res.json())
    .then(data => {
      const statsList = document.getElementById("stats-list");
      statsList.innerHTML = "";

      if (data.success && Object.keys(data.stats).length > 0) {
        for (const [domain, s] of Object.entries(data.stats)) {
          const acc = s.attempted > 0 ? ((s.correct / s.attempted) * 100).toFixed(1) : "0.0";
          const li = document.createElement("li");
          li.textContent = `${domain.toUpperCase()} → ${acc}% (${s.correct}/${s.attempted})`;
          statsList.appendChild(li);
        }
      } else {
        const li = document.createElement("li");
        li.textContent = "No stats yet — start your revision!";
        statsList.appendChild(li);
      }
    });
}
// Close stats modal
function closeStats() {
  document.getElementById("stats-modal").classList.add("hidden");
}

// Close modal on outside click
window.addEventListener("click", (event) => {
  const modal = document.getElementById("stats-modal");
  if (event.target === modal) {
    modal.classList.add("hidden");
  }
});

// Auto-login if user is saved in localStorage
document.addEventListener("DOMContentLoaded", () => {
  const savedUser = localStorage.getItem("user");
  if (savedUser) {
    currentUser = savedUser;
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("dashboard").classList.remove("hidden");
    loadFlashcards();
  }
});


let quizCards = [];
let quizIndex = 0;

// Start Quiz
// Start Quiz
function startQuiz() {
  const domain = document.getElementById("domain-select").value;
  currentDomain = domain;

  fetch("/api/get_flashcards", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ domain }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success && data.cards.length > 0) {
        // Add unique IDs to cards
        quizCards = data.cards.map((c, idx) => ({ ...c, id: idx }));
        quizIndex = 0;
        document.getElementById("quiz-section").classList.remove("hidden");
        showQuizQuestion();
      } else {
        alert("⚠️ No flashcards found for this domain.");
      }
    });
}

function updateStatsUI(stats) {
  const statsList = document.getElementById("stats-list");
  statsList.innerHTML = "";

  for (const [domain, s] of Object.entries(stats)) {
    const acc = s.attempted > 0 ? ((s.correct / s.attempted) * 100).toFixed(1) : "0.0";
    const li = document.createElement("li");
    li.textContent = `${domain.toUpperCase()} → ${acc}% (${s.correct}/${s.attempted})`;
    statsList.appendChild(li);
  }
}


// Next Question
function nextQuiz() {
  quizIndex++;
  if (quizIndex >= quizCards.length) {
    document.getElementById("quiz-section").innerHTML =
      `<h3>🎉 Quiz Completed!</h3>
       <p>You answered all ${quizCards.length} questions in ${currentDomain.toUpperCase()}.</p>`;
    showStats(); // refresh sidebar stats
    return;
  }
  showQuizQuestion();
}

let quizScore = 0; // track correct answers in this quiz

let quizAnswered = false; // track if current question is answered

function showQuizQuestion() {
  const card = quizCards[quizIndex];
  const questionEl = document.getElementById("quiz-question");
  const optionsEl = document.getElementById("quiz-options");
  const feedbackEl = document.getElementById("quiz-feedback");
  const nextBtn = document.getElementById("quiz-next-btn");

  questionEl.textContent = card.question;
  optionsEl.innerHTML = "";
  feedbackEl.textContent = "";
  quizAnswered = false;

  nextBtn.textContent = (quizIndex === quizCards.length - 1) ? "Submit Quiz" : "Next Question";

  nextBtn.onclick = () => {
    if (!quizAnswered) {
      alert("⚠️ Please select an option first!");
      return;
    }
    if (quizIndex < quizCards.length - 1) {
      quizIndex++;
      showQuizQuestion();
    } else {
      submitQuiz();
    }
  };

  card.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.textContent = opt;
    btn.className = "option-btn";
    btn.onclick = () => submitAnswer(i === card.answer_index, card.id);
    optionsEl.appendChild(btn);
  });
}

function submitAnswer(isCorrect, card_id) {
  if (!card_id && card_id !== 0) {
    console.error("Card ID missing!");
    return;
  }

  const feedbackEl = document.getElementById("quiz-feedback");
  feedbackEl.textContent = isCorrect ? "✅ Correct!" : "❌ Wrong!";
  feedbackEl.style.color = isCorrect ? "green" : "red";

  document.querySelectorAll(".option-btn").forEach((btn) => btn.disabled = true);

  quizAnswered = true;
  if (isCorrect) quizScore++;

  fetch("/api/submit_answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      domain: currentDomain,
      card_id: card_id,
      correct: isCorrect
    }),
  })
  .then(res => res.json())
  .then(data => {
    console.log("Updated stats:", data.stats);
    updateStatsUI(data.stats);
  });
}

function submitQuiz() {
  alert(`🎉 Quiz Completed!\nYou scored ${quizScore} / ${quizCards.length} in ${currentDomain.toUpperCase()}.`);

  document.getElementById("quiz-section").innerHTML =
    `<h3>🎉 Quiz Completed!</h3>
     <p>You answered all ${quizCards.length} questions in ${currentDomain.toUpperCase()}.</p>`;

  showStats();
  quizScore = 0;
}

