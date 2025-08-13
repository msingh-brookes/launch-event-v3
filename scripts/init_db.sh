#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/init_db.sh [db_path]
# Default DB path is users.db in the project root.
DB_PATH="${1:-users.db}"

# Ensure sqlite3 is available
if ! command -v sqlite3 >/dev/null 2>&1; then
  echo "Error: sqlite3 CLI not found. Install it and retry."
  echo " - macOS: brew install sqlite"
  echo " - Ubuntu/Debian: sudo apt-get install sqlite3"
  echo " - Windows: install sqlite3.exe and run via Git Bash/WSL, or run a Python init instead."
  exit 1
fi

echo "Initializing database at: $DB_PATH"

# If you want a completely fresh DB each run, uncomment the next line:
# rm -f "$DB_PATH"

sqlite3 "$DB_PATH" <<'SQL'
PRAGMA foreign_keys = ON;
BEGIN;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  username  TEXT NOT NULL UNIQUE,
  password  TEXT NOT NULL,
  is_admin  INTEGER NOT NULL DEFAULT 0
);

-- QUESTIONS TABLE
CREATE TABLE IF NOT EXISTS questions (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  asker     TEXT NOT NULL,
  question  TEXT NOT NULL,
  target    TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_questions_timestamp ON questions (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_questions_target ON questions (target);

-- Seed users (idempotent)
INSERT OR IGNORE INTO users (username, password, is_admin)
VALUES ('testuser', '1234', 1);   -- Admin

INSERT OR IGNORE INTO users (username, password, is_admin)
VALUES ('alice', '1234', 0);      -- Regular attendee

COMMIT;
SQL

echo "-----------------------------------------"
echo "DB initialized."
echo " Users:"
sqlite3 "$DB_PATH" "SELECT id, username, is_admin FROM users;"

echo
echo "Tip: Admin user is 'testuser' with password '1234'."
echo "     Regular user is 'alice' with password '1234'."
echo "     Change these later in the DB if you like."
echo "-----------------------------------------"
