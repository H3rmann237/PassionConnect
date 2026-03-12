from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from database import get_db

profil = Blueprint('profil', __name__)

@profil.route('/profil')
@login_required
def mon_profil():
    db = get_db()
    cursor = db.cursor()

    passion = cursor.execute('''
        SELECT passion.nom, passion.icone FROM passion
        JOIN user_passion ON passion.id = user_passion.passion_id
        WHERE user_passion.user_id = ?
    ''',(current_user.id,)).fetchall()

    db.close()
    return render_template('profil.html', passion = passion)

@profil.route('/profil/modifier', methods=['GET','POST'])
@login_required
def modifier_profil():
    db = get_db()
    cursor =db.cursor()

    toutes_passions = cursor.execute('SELECT * FROM passion').fetchall()
    print("Passions trouvées :", len(toutes_passions))

    if request.method == 'POST':
        bio = request.form['bio']
        passions_choisies = request.form.getlist('passions')

        cursor.execute(
            'UPDATE user SET bio = ? WHERE id = ?',
            (bio, current_user.id,)
        )
        
        cursor.execute(
            'DELETE FROM user_passion WHERE user_id = ?',
            (current_user.id,)
        )

        for passion_id in passions_choisies:
            cursor.execute(
                'INSERT INTO user_passion (user_id, passion_id) VALUES (?, ?)',
                (current_user.id, passion_id,)
            )

        db.commit()
        db.close()
        return redirect(url_for('profil.mon_profil'))
    db.close()
    return render_template('modifier_profil.html', toutes_passions = toutes_passions)

@profil.route('/profil/<int:user_id>')
def profil_public(user_id):
    db = get_db()
    cursor = db.cursor()
    
    user = cursor.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    passions = cursor.execute('''
        SELECT passion.nom, passion.icone FROM passion
        JOIN user_passion ON passion.id = user_passion.passion_id
        WHERE user_passion.user_id = ?
    ''', (user_id,)).fetchall()

    publications = cursor.execute('''
        SELECT * FROM publication
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,)).fetchall()

    db.close()
    return render_template('profil_public.html', user=user, passions=passions, publications=publications)