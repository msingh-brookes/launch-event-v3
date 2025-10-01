import sqlite3

DB_PATH = "users.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Drop old tables to reset schema (only run this in dev!)
#cur.execute("DROP TABLE IF EXISTS users;")
#cur.execute("DROP TABLE IF EXISTS questions;")
#cur.execute("DROP TABLE IF EXISTS votes;")

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    organisation TEXT NOT NULL,
    password TEXT,         -- still kept for admins
    is_admin INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# Create questions table with 'answered' field
cur.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    user_id INTEGER,
    question TEXT NOT NULL,
    recipient TEXT NOT NULL,
    answered INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

# Create a table for storing poll answers
cur.execute("""
CREATE TABLE IF NOT EXISTS poll_votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    option TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

# Create interests table
cur.execute("""
CREATE TABLE IF NOT EXISTS interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    phrase TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")



# Seed data
cur.execute("INSERT OR IGNORE INTO users (first_name, last_name, organisation, password, is_admin) VALUES (?, ?, ?, ?, ?)",
            ("admin","","", "1234", 1))
#cur.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)", ("alice", "1234", 0))
#cur.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)",("bob", "1234", 0))

conn.commit()
conn.close()

print("Database initialized.")
print("Admin user: admin / 1234")
#print("Regular user: alice / 1234")
#print("Regular user: bob / 1234")


