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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
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

def getAllMessages():
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return messages

def getMessageText(message_id):
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM messages WHERE id = ?", (message_id,))
    message = cursor.fetchone()
    conn.close()
    return message[0] if message else ""

def addMessage(name, text):
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (name, text) VALUES (?, ?)", (name, text))
    conn.commit()
    conn.close()

def updateMessage(message_id, text):
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE messages SET text = ? WHERE id = ?", (text, message_id))
    conn.commit()
    conn.close()

def deleteMessage(message_id):
    conn = sqlite3.connect('assets/data/app.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()
