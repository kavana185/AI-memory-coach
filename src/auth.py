import json, os, hashlib

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        content = f.read().strip()
        return json.loads(content) if content else {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(username, password):
    users = load_users()
    if username in users:
        return {"success": False, "error": "Username already exists"}
    users[username] = hash_password(password)
    save_users(users)
    os.makedirs(f"../data/user", exist_ok=True)
    with open(f"../data/user/{username}.json", "w") as f:
        json.dump({"stats": {}}, f)
    return {"success": True, "message": "User registered successfully"}

def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    if username in users and users[username] == hashed:
        return {"success": True, "message": "Login successful"}
    return {"success": False, "error": "Invalid username or password"}
