from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'users.db'

# Database helper
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def load_logged_in_user():
    username = session.get('username')
    if username:
        db = get_db()
        g.user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    else:
        g.user = None

# Initialize DB
def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            is_admin INTEGER DEFAULT 0
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            question TEXT,
            recipient TEXT,
            answered INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add admin test user if not exists
    user = db.execute("SELECT * FROM users WHERE username=?", ("testuser",)).fetchone()
    if not user:
        db.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                   ("testuser", "1234", 1))
    db.commit()

@app.route('/')
def home():
    return render_template('home.html', username=g.user['username'] if g.user else None, is_admin=g.user['is_admin'] if g.user else 0)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username=? AND password=?',
                          (username, password)).fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error="Invalid login")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/agenda')
def agenda():
    return render_template('agenda.html', username=g.user['username'] if g.user else None)

@app.route('/about')
def about():
    return render_template('about.html', username=g.user['username'] if g.user else None)

@app.route('/scan')
def scan():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('scan.html', username=g.user['username'])

@app.route('/submit_question', methods=['GET', 'POST'])
def submit_question():
    if not g.user:
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        question = request.form['question']
        recipient = request.form['recipient']
        db.execute("INSERT INTO questions (username, question, recipient) VALUES (?, ?, ?)",
                   (g.user['username'], question, recipient))
        db.commit()
        return redirect(url_for('submit_question'))
    my_questions = db.execute("SELECT * FROM questions WHERE username=? ORDER BY created_at DESC",
                               (g.user['username'],)).fetchall()
    return render_template('submit_question.html', username=g.user['username'], my_questions=my_questions)

@app.route('/admin_questions', methods=['GET', 'POST'])
def admin_questions():
    if not g.user or g.user['is_admin'] == 0:
        return redirect(url_for('home'))
    db = get_db()
    if request.method == 'POST':
        q_id = request.form.get('question_id')
        db.execute("UPDATE questions SET answered=1 WHERE id=?", (q_id,))
        db.commit()
        return redirect(url_for('admin_questions'))
    questions = db.execute("SELECT * FROM questions ORDER BY created_at DESC").fetchall()
    return render_template('admin_questions.html', questions=questions, username=g.user['username'])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
