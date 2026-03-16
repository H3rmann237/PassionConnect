import sqlite3
import os

def get_db():
    db = sqlite3.connect('passionconnect.db') #retoune des dictionnaires au lieu des tuples
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            bio TEXT,
            photo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP           
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE,
            icone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_passion (
            user_id INTEGER,
            passion_id INTEGER,
            PRIMARY KEY (user_id, passion_id),
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (passion_id) REFERENCES passion(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publication (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenu TEXT NOT NULL,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS like (
            user_id INTEGER NOT NULL,
            publication_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, publication_id),
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (publication_id) REFERENCES publication(id)?
        )
    ''')

    passions = [
        ('3D', '🗿'),
        ('Jeux Vidéo', '🎮'),
        ('Animation', '🎬'),
        ('Illustration', '🎨'),
        ('Développement Jeux', '💻'),
        ('Musique', '🎵'),
        ('Montage Vidéo', '📽️'),
        ('Design Graphique', '🖥️')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO passion (nom,icone) VALUES(?,?)
    ''', passions)

    db.commit()
    db.close()
    print('Base de données initialisée !')

if __name__ == '__main__':
    init_db()