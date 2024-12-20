import sqlite3
import bcrypt

def initializeDatabase():
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.execute("INSERT OR IGNORE INTO users (user, password) VALUES (?, ?)", ('a', hashPassword('a')))
    conn.commit()
    conn.close()

def hashPassword(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def checkUserCredentials(username, password):
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE user = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    return False

def addUser(username, password):
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user FROM users WHERE user = ?", (username,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("Username already exists")
    hashed_password = hashPassword(password)
    cursor.execute("INSERT INTO users (user, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def changePassword(username, newPassword):
    hashed_password = hashPassword(newPassword)
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE user = ?", (hashed_password, username))
    conn.commit()
    conn.close()

def deleteUser(username):
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user = ?", (username,))
    conn.commit()
    conn.close()

def getAllUsers():
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users
