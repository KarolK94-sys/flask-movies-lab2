
from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "movies.db"

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def ensure_table_and_seed_if_empty():
    """Tworzy tabelę 'movies' i zapełnia 3 rekordami, jeśli pusta."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            actors TEXT
        );
    """)
    cur.execute("SELECT COUNT(*) FROM movies")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
            [
                ("The Matrix", 1999, "Keanu Reeves, Laurence Fishburne"),
                ("Indiana Jones", 1989, "Harrison Ford, Sean Connery"),
                ("Casino Royal", 2006, "Daniel Craig, Eva Green"),
            ],
        )
        conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ids_to_remove = request.form.getlist("movieToRemove")
        if ids_to_remove:
            conn = get_db()
            cur = conn.cursor()
            for mid in ids_to_remove:
                cur.execute("DELETE FROM movies WHERE id = ?", (mid,))
            conn.commit()
            conn.close()
        return redirect(url_for("home"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, year, actors FROM movies ORDER BY id ASC")
    movies = cur.fetchall()
    conn.close()
    return render_template("home.html", movies=movies)

@app.route("/addMovie", methods=["GET", "POST"])
def addMovie():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        year = (request.form.get("year") or "").strip()
        actors = (request.form.get("actors") or "").strip()

        # Walidacja: Title wymagany
        if not title:
            return render_template("add.html", error="Title is required.")

        # Walidacja: Year = 4 cyfry + zakres
        year_val = None
        if year:
            if not year.isdigit() or len(year) != 4:
                return render_template("add.html", error="Year must be 4 digits (e.g. 1999).")
            y = int(year)
            if y < 1888 or y > 2100:
                return render_template("add.html", error="Year must be between 1888 and 2100.")
            year_val = y

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
            (title, year_val, actors)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    return render_template("add.html")

if __name__ == "__main__":
    ensure_table_and_seed_if_empty()
    app.run(debug=True)
