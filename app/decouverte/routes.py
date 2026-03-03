from flask import Blueprint, render_template, url_for
from database import get_db

decouverte = Blueprint('decouverte',__name__)

@decouverte.route('/decouverte')
def page_decouverte():
    db = get_db()
    cursor = db.cursor()

    poste = cursor.execute('''
        SELECT user.id, user.username, user.bio, GROUP_CONCAT(passion.icone || ' ' || passion.nom) as passions
        FROM user
        JOIN user_passion ON user.id = user_passion.user_id
        JOIN passion ON passion.id = user_passion.passion_id
        GROUP BY user.id
    ''').fetchall()
    db.close()

    return render_template('decouverte.html', poste=poste)