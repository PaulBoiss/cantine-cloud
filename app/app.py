"""Cantine : l'API de menus qui sert de fil rouge au cours d'architecture cloud.

Volontairement minuscule : ce qui compte dans ce cours, c'est l'architecture
autour d'elle (calcul, réseau, disponibilité, coûts), pas son code.
"""
import os
import socket
import sqlite3

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

VERSION = "1.0"
# Base SQLite locale au conteneur : chaque instance a la sienne, et elle disparaît
# avec le conteneur. C'est un défaut assumé, discuté au bloc 2 (pourquoi une base gérée).
DB = os.environ.get("DB_PATH", "/tmp/cantine.db")
JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi")
MENUS = [
    ("lundi", "Lasagnes", 4.5),
    ("mardi", "Poulet basquaise", 4.8),
    ("mercredi", "Curry de légumes", 4.2),
    ("jeudi", "Hachis parmentier", 4.6),
    ("vendredi", "Poisson pané", 4.4),
]


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS menus (day TEXT, name TEXT, price REAL)")
        if conn.execute("SELECT COUNT(*) FROM menus").fetchone()[0] == 0:
            conn.executemany("INSERT INTO menus VALUES (?, ?, ?)", MENUS)


init_db()


@app.route("/")
def accueil():
    # Le nom d'hôte dit quelle instance ou quelle tâche a répondu (répartition de charge)
    return {"app": "cantine", "version": VERSION, "host": socket.gethostname()}


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/menus")
def menus():
    day = request.args.get("day", "lundi")
    if day not in JOURS:
        abort(400)
    with sqlite3.connect(DB) as conn:
        rows = conn.execute(
            "SELECT name, price FROM menus WHERE day = ?", (day,)
        ).fetchall()
    return jsonify([{"plat": name, "prix": price} for name, price in rows])


if __name__ == "__main__":
    # Lancement local seulement : en conteneur, c'est gunicorn qui sert l'application
    app.run(host="127.0.0.1", port=5000)
