from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from database import get_db

from werkzeug.utils import secure_filename
import os

publication = Blueprint('publication',__name__)

@publication.route('/publication')
@login_required
def mes_publications():
    db = get_db()
    cursor = db.cursor()

    publications = cursor.execute('''
        SELECT publication.id as pub_id, publication.contenu, publication.image, 
               publication.created_at, user.username, user.id as user_id,
               COUNT(like.user_id) as nb_likes
        FROM publication
        JOIN user ON publication.user_id = user.id
        LEFT JOIN like ON like.publication_id = publication.id
        GROUP BY publication.id
        ORDER BY publication.created_at DESC
    ''').fetchall()

    db.close()
    return render_template('publication.html', publications = publications)

@publication.route('/publication/nouvelle', methods=['GET', 'POST'])
@login_required
def new_publication():
    if request.method == 'POST':    
        contenu = request.form['contenu']
        image = request.files['image']
        nom_fichier = None
        if image.filename != '':
            nom_fichier = secure_filename(image.filename)
            image.save(os.path.join('app/static/uploads', nom_fichier))

        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO publication (contenu, image, user_id)
            VALUES (?, ?, ?)
        ''', (contenu,nom_fichier, current_user.id))
        db.commit()
        db.close()

        return redirect(url_for('publication.mes_publications'))
    
    return render_template('nouvelle_publication.html', publication = publication)

@publication.route('/publication/like/<int:publication_id>', methods=['POST'])
@login_required
def like(publication_id):
    db = get_db()
    cursor = db.cursor()

    deja_like = cursor.execute('''
        SELECT * FROM like WHERE user_id = ? AND publication_id = ?
    ''', (current_user.id, publication_id)).fetchone()

    if deja_like:
        cursor.execute('''
            DELETE FROM like WHERE user_id = ? AND publication_id = ?
        ''', (current_user.id, publication_id))
    else :
        cursor.execute('''
            INSERT INTO like (user_id, publication_id) VALUES (?, ?)
        ''', (current_user.id, publication_id)) 

    db.commit()
    db.close()

    return redirect(url_for('publication.mes_publications'))