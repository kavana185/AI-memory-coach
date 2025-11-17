import json
import os
import random
from datetime import datetime, timedelta

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")


def load_flashcards(domain):
    """Load flashcards from the given domain JSON file."""
    file_path = os.path.join(DATA_FOLDER, f"{domain}.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)


def get_user_file(username):
    """Return the user's progress file path."""
    user_dir = os.path.join(DATA_FOLDER, "user")
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, f"{username}.json")


def load_user_progress(username):
    """Load or initialize user progress."""
    file_path = get_user_file(username)
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    return data


def save_user_progress(username, data):
    """Save user progress."""
    file_path = get_user_file(username)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_next_flashcard(username, domain):
    """Return the next due flashcard for the given user and domain."""
    flashcards = load_flashcards(domain)
    user_data = load_user_progress(username)

    # Track user progress for this domain
    if domain not in user_data:
        user_data[domain] = {"cards": {}, "stats": {"attempted": 0, "correct": 0}}

    cards_progress = user_data[domain]["cards"]

    # Filter due cards (or unattempted)
    due_cards = []
    now = datetime.now()
    for card in flashcards:
        q = card["question"]
        info = cards_progress.get(q, {})
        next_review = info.get("next_review")
        if not next_review or datetime.fromisoformat(next_review) <= now:
            due_cards.append(card)

    # If no due cards, return random for review
    if not due_cards:
        return random.choice(flashcards)

    return random.choice(due_cards)


def update_progress(username, domain, question, correct):
    """Update selective repeat logic and stats after an answer."""
    user_data = load_user_progress(username)

    if domain not in user_data:
        user_data[domain] = {"cards": {}, "stats": {"attempted": 0, "correct": 0}}

    domain_data = user_data[domain]
    domain_data["stats"]["attempted"] += 1
    if correct:
        domain_data["stats"]["correct"] += 1

    card = domain_data["cards"].get(
        question,
        {
            "interval": 1,
            "ef": 2.5,
            "next_review": datetime.now().isoformat()
        }
    )

    if correct:
        card["interval"] *= card["ef"]
        card["ef"] += 0.1
    else:
        card["interval"] = 1
        card["ef"] = max(1.3, card["ef"] - 0.2)

    next_time = datetime.now() + timedelta(days=card["interval"])
    card["next_review"] = next_time.isoformat()
    domain_data["cards"][question] = card

    save_user_progress(username, user_data)


def get_user_stats(username):
    user_dir = f"../data/user/{username}"
    stats_file = os.path.join(user_dir, "stats.json")
    if not os.path.exists(stats_file):
        return {}
    with open(stats_file, "r") as f:
        try:
            return json.load(f)
        except:
            return {}
