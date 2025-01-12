import os
import sqlite3


class UserDatabase:
    def __init__(self, databaseDir: str):
        self.conn = sqlite3.connect(os.path.join(databaseDir, "database.db"))
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    email TEXT
                )"""
        )
        self.conn.commit()

        self.conn.commit()

    def insert(self, username, password, email):
        self.cursor.execute(
            """INSERT INTO users (username, password, email) VALUES (?, ?, ?)""",
            (username, password, email),
        )
        self.conn.commit()

    def get(self, username):
        self.cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
        return self.cursor.fetchone()

    def get_all(self):
        self.cursor.execute("""SELECT * FROM users""")
        return self.cursor.fetchall()

    def update(self, username, password, email):
        self.cursor.execute(
            """UPDATE users SET password = ?, email = ? WHERE username = ?""",
            (password, email, username),
        )
        self.conn.commit()

    def delete(self, username):
        self.cursor.execute("""DELETE FROM users WHERE username = ?""", (username,))
        self.conn.commit()

    def close(self):
        self.conn.close()


class JobDatabase:
    def __init__(self, databaseDir: str):
        self.conn = sqlite3.connect(os.path.join(databaseDir, "database.db"))
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS jobs(
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    path TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    responsible_for TEXT
                )"""
        )
        self.conn.commit()

    def insert(self, title, description, path, created_time, updated_time, user):
        self.cursor.execute(
            """INSERT INTO jobs (title, description, path, created_at, updated_at, responsible_for) VALUES (?, ?, ?, ?, ?, ?)""",
            (title, description, path, created_time, updated_time, user),
        )
        self.conn.commit()

    def get(self, title):
        self.cursor.execute("""SELECT * FROM jobs WHERE title = ?""", (title,))
        return self.cursor.fetchone()

    def get_all(self):
        self.cursor.execute("""SELECT * FROM jobs""")
        return self.cursor.fetchall()

    def update(self, title, update_time):
        self.cursor.execute(
            """UPDATE jobs SET updated_at = ? WHERE title = ?""",
            (update_time, title),
        )
        self.conn.commit()

    def delete(self, title):
        self.cursor.execute("""DELETE FROM jobs WHERE title = ?""", (title,))
        self.conn.commit()

    def close(self):
        self.conn.close()
