from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
import sqlite3

app = Flask(__name__)
app.secret_key = 'key_sessione_user' #chiave per la sessione user
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#inizializza db e flask-login
db.init_app(app)
login_manager = LoginManager() #inizializza flask-login
login_manager.init_app(app) #collega flask-login e flask
login_manager.login_view = 'login'

with app.app_context(): 
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'] #prende dati dalle form
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Questo username è già in uso.")
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', error=None)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] #prende dati dalle form
        password = request.form['password']
    #cerca user db
        user = User.query.filter_by(username=username, password=password).first()
        if user: #se user esiste
            login_user(user)
            session['user_id'] = user.id
            return redirect(url_for('home'))
        return render_template('login.html', error="Credenziali non valide.") #errore se credenziali errate
    return render_template('login.html', error=None)

def authenticate_user(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return {'id': user.id, 'username': user.username}
    return None
    pass

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/home')
def home(): 
    user_id = session.get('user_id')

    if __name__ == '__main__': #debug
        app.run(debug=True)