import sqlite3

def create_db():
    conn = sqlite3.connect('jarvis.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (query TEXT PRIMARY KEY, response TEXT, keywords TEXT)''')
    conn.commit()
    conn.close()

def insert_response(query, response, keywords):
    conn = sqlite3.connect('jarvis.db')
    c = conn.cursor()
    c.execute('INSERT INTO responses (query, response, keywords) VALUES (?, ?, ?)', (query, response, keywords))
    conn.commit()
    conn.close()

def get_response(query):
    conn = sqlite3.connect('jarvis.db')
    c = conn.cursor()
    c.execute('SELECT response FROM responses WHERE query=?', (query,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
