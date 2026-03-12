from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

from app.models import User
from database import get_db

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

@auth.route('/')
def accueil():
    if current_user.is_authenticated:
        return redirect(url_for('publication.mes_publications'))
    return render_template('accueil.html')

@auth.route('/inscription', methods=['GET','POST'])
def inscription():
    if request.method == 'POST':
        Username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        #print(Username,email,password)

        password_chiffre = bcrypt.generate_password_hash(password).decode('utf-8')

        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO user (username, email, password)
            VALUES (?, ?, ?)
        ''', (Username,email,password_chiffre))
        db.commit()
        db.close()

        return redirect(url_for('auth.connexion'))
    
    return render_template('inscription.html')

@auth.route('/connexion', methods=['GET','POST'])
def connexion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        utilisateur = User.get_by_email(email)

        #db = get_db()
        #cursor = db.cursor()
        #utilisateur =cursor.execute(
        #    'SELECT * FROM user WHERE email = ?', (email,)
        #).fetchone()
        #db.close()

        if utilisateur and bcrypt.check_password_hash(utilisateur['password'], password):
            user_obj = User(utilisateur['id'], utilisateur['username'], utilisateur['email'], utilisateur['bio'])
            login_user(user_obj)
            return redirect(url_for('auth.accueil'))
        else:
            erreur = 'Email ou mot de passe incorrect'
            return render_template('connexion.html', erreur=erreur)
    return render_template('connexion.html')

@auth.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('auth.accueil'))