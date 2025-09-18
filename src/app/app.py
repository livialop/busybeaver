from flask import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = '20r0]5/reyg1@S*v*FZJ58HnH1=oAy{t<6<rx]A(QdPBq(")*Lsd"HbJgPSpVbT'

@login_manager.user_loader
def load_user(user_id):
    '''Retorna o email do usuário, que é definido como chave única'''
    return User.get(user_id)


# start_database('../schema.sql') # Falta implementar isso depois


# Primeira rota. Tentando visualizar o footer e posteriormente a header
@app.route('/')
def index():
    return render_template('index.html')

