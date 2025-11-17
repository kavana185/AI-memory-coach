from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import json
from auth import register_user, login_user
from flashcards import load_flashcards

from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data/user")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app)
app.secret_key = "supersecretkey"

os.makedirs(DATA_DIR, exist_ok=True)


@app.route("/")
def home():
    if "username" in session:
        return render_template("index.html", logged_in=True)
    return render_template("index.html", logged_in=False)


# ========== AUTH ROUTES ==========
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    result = register_user(data["username"], data["password"])
    return jsonify(result)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    result = login_user(data["username"], data["password"])
    if result["success"]:
        session["username"] = data["username"]
    return jsonify(result)


@app.route("/api/logout")
def logout():
    session.pop("username", None)
    return jsonify({"success": True})


# ========== FLASHCARD ROUTES ==========
@app.route("/api/get_flashcards", methods=["POST"])
def get_flashcards():
    data = request.get_json()
    domain = data.get("domain")
    username = session.get("username")

    if not username:
        return jsonify({"success": False, "error": "Not logged in"})
    if not domain:
        return jsonify({"success": False, "error": "No domain selected"})

    # Load all flashcards
    cards = load_flashcards(domain)
    if not cards:
        return jsonify({"success": False, "error": "No flashcards found"})

    # Load user stats
    stats, _ = load_stats(username)
    suggested_ids = stats.get(domain, {}).get("suggested_cards", [])

    # Map cards with ids (for suggested filtering)
    cards_with_id = [{**c, "id": idx} for idx, c in enumerate(cards)]

    # Prioritize suggested cards first
    suggested_cards = [c for c in cards_with_id if c["id"] in suggested_ids]
    mastered_cards = [c for c in cards_with_id if c["id"] not in suggested_ids]

    # Combine: suggested first, then the rest
    ordered_cards = suggested_cards + mastered_cards

    return jsonify({"success": True, "cards": ordered_cards})


@app.route("/api/update_progress", methods=["POST"])
def update_card():
    if "username" not in session:
        return jsonify({"success": False, "error": "Not logged in"})

    data = request.json
    username = session["username"]
    # Keep your update_progress logic from flashcards module
    return jsonify({"success": True})


# ======= STATS =======
def load_stats(username):
    user_dir = os.path.join(DATA_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    stats_file = os.path.join(user_dir, "stats.json")

    if os.path.exists(stats_file) and os.path.getsize(stats_file) > 0:
        with open(stats_file, "r") as f:
            stats = json.load(f)
    else:
        stats = {}

    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)

    return stats, stats_file


@app.route("/api/stats", methods=["GET"])
def stats():
    username = session.get("username")
    if not username:
        return jsonify({"success": False, "error": "Not logged in"})

    stats, _ = load_stats(username)

    ui_stats = {}
    for d, info in stats.items():
        total_attempted = sum(c["attempted"] for c in info["cards"].values())
        total_correct = sum(c["correct"] for c in info["cards"].values())
        ui_stats[d] = {"attempted": total_attempted, "correct": total_correct}

    return jsonify({"success": True, "stats": ui_stats})


@app.route("/api/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    domain = data.get("domain")
    card_id = str(data.get("card_id"))
    correct = data.get("correct")
    username = session.get("username")

    if not username:
        return jsonify({"success": False, "error": "Not logged in"})

    stats, stats_file = load_stats(username)

    # Initialize domain if new
    if domain not in stats:
        stats[domain] = {
            "attempts": 0,
            "last_quiz": None,
            "progress": 0,
            "next_quiz": None,
            "cards": {},
            "suggested_cards": []
        }

    domain_data = stats[domain]

    # Update card stats
    if card_id not in domain_data["cards"]:
        domain_data["cards"][card_id] = {"attempted": 0, "correct": 0}

    domain_data["cards"][card_id]["attempted"] += 1
    if correct:
        domain_data["cards"][card_id]["correct"] += 1

    # Update progress & suggested cards
    total_cards = len(domain_data["cards"])
    mastered = sum(1 for c in domain_data["cards"].values() if c["correct"] >= 3)
    domain_data["progress"] = round((mastered / total_cards) * 100) if total_cards else 0
    domain_data["suggested_cards"] = [cid for cid, c in domain_data["cards"].items() if c["correct"] < 3]

    # Update attempts and timestamps
    domain_data["attempts"] += 1
    domain_data["last_quiz"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    domain_data["next_quiz"] = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")

    # Save to stats.json
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)

    # Prepare stats for UI
    ui_stats = {}
    for d, info in stats.items():
        total_attempted = sum(c["attempted"] for c in info["cards"].values())
        total_correct = sum(c["correct"] for c in info["cards"].values())
        ui_stats[d] = {"attempted": total_attempted, "correct": total_correct}

    return jsonify({"success": True, "stats": ui_stats})


if __name__ == "__main__":
    app.run(debug=True)
