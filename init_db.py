import sqlite3

DB_PATH = "users.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0
);
""")

# Create questions table with 'answered' field
cur.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    question TEXT NOT NULL,
    recipient TEXT NOT NULL,
    answered INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# Seed data
cur.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            ("testuser", "1234", 1))
cur.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            ("alice", "1234", 0))

conn.commit()
conn.close()

print("Database initialized.")
print("Admin user: testuser / 1234")
print("Regular user: alice / 1234")
