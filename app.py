from multiprocessing import connection
import sqlite3
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
from datetime import date, datetime

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("secret_key")

csrf = CSRFProtect(app)


def validate_password(password):

    if len(password) < 8:
        return False

    if not re.search("[A-Z]", password):
        return False

    if not re.search("[a-z]", password):
        return False

    if not re.search("[0-9]", password):
        return False

    return True


def get_db():
    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            due_date DATETIME,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    try:
        cursor.execute("""
            ALTER TABLE tasks
            ADD COLUMN due_date DATETIME
        """)
        print("due_date column added.")
    except sqlite3.OperationalError:
        print("due_date column already exists.")

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        raw_password = request.form["password"]

        if not validate_password(raw_password):
            flash("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")
            return redirect(url_for("register"))

        password = generate_password_hash(raw_password)

        if not username.strip():
            flash("Username is required.")
            return redirect(url_for("register"))

        connection = get_db()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users(username,email,password)
                VALUES(?,?,?)
                """,
                (username, email, password)
            )

            connection.commit()

        except sqlite3.IntegrityError:
            flash("Email already exists. Try another email.")
            return redirect(url_for("register"))
        finally:
            connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        connection = get_db()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email=?
            """,
            (email,)
        )

        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password. Please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db()
    cursor = connection.cursor()

    status = request.args.get("status")

    if status:

        cursor.execute(
            """
            SELECT * FROM tasks
            WHERE user_id = ? AND status = ?
            """,
            (session["user_id"], status)
        )

    else:

        cursor.execute(
            """
            SELECT * FROM tasks
            WHERE user_id = ?
            """,
            (session["user_id"],)
        )

    tasks = [dict(task) for task in cursor.fetchall()]

    for task in tasks:
        if task["due_date"]:
            due_date = datetime.strptime(
                task["due_date"], "%Y-%m-%dT%H:%M"
            )

            if due_date < datetime.now():
                task["is_overdue"] = True
            else:
                task["is_overdue"] = False

    connection.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        tasks=tasks
    )


@app.route("/add_task", methods=["POST"])
def add_task():

    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form["title"].strip()
    description = request.form["description"].strip()
    due_date = request.form.get("due_date")

    if not title:
        flash("Task title is required.")
        return redirect(url_for("dashboard"))

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks(user_id, title, description, due_date, status, created_at)
        VALUES(?,?,?,?,?, CURRENT_TIMESTAMP)
        """,
        (
            session["user_id"],
            title,
            description,
            due_date,
            "Pending"
        )
    )

    connection.commit()
    connection.close()

    return redirect(url_for("dashboard"))


@app.route("/complete/<int:id>")
def complete(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET status='Completed'
        WHERE id=? AND user_id=?
        """,
        (
            id,
            session["user_id"]
        )
    )

    connection.commit()
    connection.close()

    return redirect(url_for("dashboard"))


@app.route("/delete/<int:id>")
def delete(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id=? AND user_id=?
        """,
        (
            id,
            session["user_id"]
        )
    )

    connection.commit()
    connection.close()

    return redirect(url_for("dashboard"))


@app.route("/edit_task/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"].strip()
        description = request.form["description"].strip()

        cursor.execute(
            """
            UPDATE tasks
            SET title=?, description=?
            WHERE id=? AND user_id=?
            """,
            (
                title,
                description,
                id,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        flash("Task updated successfully", "success")

        return redirect(url_for("dashboard"))

    cursor.execute(
        """
        SELECT * FROM tasks
        WHERE id=? AND user_id=?
        """,
        (
            id,
            session["user_id"]
        )
    )

    task = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_task.html",
        task=task
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):

    return render_template("500.html"), 500


create_tables()


if __name__ == "__main__":

    app.run(debug=True)
