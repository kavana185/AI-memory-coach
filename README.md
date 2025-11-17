# 🧠 AI Memory Coach (Fullstack Web App)

A complete **Full‑Stack Spaced Repetition Learning Platform** built
using:

-   **Flask (Python)** for backend\
-   **HTML + CSS + JS** for frontend\
-   **JSON** for data storage\
-   **Flashcards + Quiz + Stats Tracking**

------------------------------------------------------------------------

## 🚀 Features

### 🔹 Intelligent Flashcards (Mastery‑Based Scheduling)

Each flashcard automatically adjusts difficulty using:

    mastery_score = correct_count - wrong_count

Meaning:

-   ❗ **Negative score** → Very weak → Shown first\
-   ⚠️ **Low score** → Shown frequently\
-   ✔ **High score** → Shown rarely\
-   ⭐ **Very high** → Nearly mastered

Both **Flashcard mode** and **Quiz mode** update mastery score in real
time.

------------------------------------------------------------------------

## 📚 Supported Domains

-   📝 **C++**
-   🌐 **Computer Networks**
-   🗄️ **DBMS**
-   📖 **English Vocabulary**

Each domain has its own JSON under `/data/`.

------------------------------------------------------------------------

## 🧩 Fullstack Architecture

    /AI-memory-coach
    │
    ├── /src                 
    │     ├── flashcards.json
    │     ├── users.json
    │     ├── auth.py
    │     ├── server.py
    │     └── flashcards.py
    ├── /static               # Frontend JS/CSS
    │     ├── script.js
    │     └── style.css
    │
    ├── /templates
    │     └── index.html      # Main UI
    │
    ├── /data                 # Flashcard data
    │     ├── users/user1/stats.json #stats of every user saved her
    │     ├── cpp.json
    │     ├── english.json
    │     ├── dbms.json
    │     └── cn.json
    │
    |── .gitignore
    └── README.md

------------------------------------------------------------------------

# 🔧 Setup & Installation

## 1️⃣ Clone the repository

``` bash
git clone https://github.com/<your-username>/AI-memory-coach.git
cd AI-memory-coach
```

------------------------------------------------------------------------

## 2️⃣ Create a virtual environment

``` bash
python -m venv venv
```

------------------------------------------------------------------------

## 3️⃣ Activate it

### Windows:

``` bash
venv\Scripts\activate
```

### Mac/Linux:

``` bash
source venv/bin/activate
```

------------------------------------------------------------------------

## 4️⃣ Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# ▶️ Running the Web App

Start the Flask server:

``` bash
python src/server.py
```

Then open:

    http://localhost:5000

🎉 You now have the full web app running locally!

------------------------------------------------------------------------

# 🖥️ Frontend UI Overview

### Layout

-   **Left side:** Flashcards + Quiz\
-   **Right side:** Live stats panel\
-   Stats refresh automatically


------------------------------------------------------------------------

# 🔥 Flashcards & Mastery Algorithm

Each card contains:

    id
    question
    options[]
    answer_index
    correct_count
    wrong_count

Whenever a user answers:

### ✔ Correct:

    correct_count++

### ❌ Wrong:

    wrong_count++

### Mastery score decides priority:

    lower score → shown first

The backend sorts by mastery when sending flashcards.

------------------------------------------------------------------------

# 🧠 Quiz System

-   Random order\
-   Shows feedback\
-   Updates stats after each question\
-   Final score displayed\
-   Stats saved to `/user/{user}/stats.json`

------------------------------------------------------------------------

# ✨ Adding New Flashcards

Open any file in `/data/`, example `dbms.json`:

``` json
{
  "id": "20",
  "question": "What does a primary key ensure?",
  "options": ["Uniqueness", "Speed", "Indexing", "Duplicate rows allowed"],
  "answer_index": 0
}
```

Just add new objects --- the system picks them up automatically.

------------------------------------------------------------------------

# 🛠 Technologies Used

### **Frontend**

-   HTML\
-   CSS (custom responsive layout)\
-   JavaScript

### **Backend**

-   Python\
-   Flask\
-   JSON storage

------------------------------------------------------------------------

# 🤝 Contribute

Pull requests are welcome!\
You can contribute:

-   New flashcard sets\
-   Better UI\
-   Leaderboard system\
-   Account system upgrade

------------------------------------------------------------------------

# ⭐ Show Your Support

If you like the project, star ⭐ the GitHub repo!\
Feel free to share suggestions

------------------------------------------------------------------------
