from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from database import get_db

decouverte = Blueprint('decouverte',__name__)

@decouverte.route('/decouverte')
@login_required
def page_decouverte():
    db = get_db()
    cursor = db.cursor()

    toutes_passions = cursor.execute(
        'SELECT * FROM passion'
    ).fetchall()

    poste = cursor.execute('''
        SELECT user.id, user.username, user.bio, 
            GROUP_CONCAT(passion.icone || ' ' || passion.nom) as passions
        FROM user
        LEFT JOIN user_passion ON user.id = user_passion.user_id
        LEFT JOIN passion ON passion.id = user_passion.passion_id
        GROUP BY user.id
    ''').fetchall()

    passion_choisie = request.args.get('passion')

    if passion_choisie:
        poste = cursor.execute('''
            SELECT user.id, user.username, user.bio, 
                GROUP_CONCAT(passion.icone || ' ' || passion.nom) as passions
            FROM user
            LEFT JOIN user_passion ON user.id = user_passion.user_id
            LEFT JOIN passion ON passion.id = user_passion.passion_id
            WHERE passion.nom = ?
            GROUP BY user.id
        ''', (passion_choisie,)).fetchall()
    db.close()
    return render_template('decouverte.html', poste=poste, toutes_passions=toutes_passions)