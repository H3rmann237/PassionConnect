from flask_login import UserMixin
from database import get_db

class User(UserMixin):
    def __init__(self, id, username, email, bio):
        self.id = id
        self.username = username
        self.email = email
        self.bio = bio

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        cursor = db.cursor()
        user = cursor.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        db.close()
        if user:
            return User(user['id'], user['username'], user['email'], user['bio'])
        return None
    
    @staticmethod
    def get_by_email(email):
        db = get_db()
        cursor = db.cursor()
        user = cursor.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()
        db.close()
        return user