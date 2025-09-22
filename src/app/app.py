from flask import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models.model import User, Product, get_session

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = '20r0]5/reyg1@S*v*FZJ58HnH1=oAy{t<6<rx]A(QdPBq(")*Lsd"HbJgPSpVbT'

@login_manager.user_loader
def load_user(user_id):
    '''Carrega usuário baseado no ID'''
    session = get_session()
    return session.get(User, int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        session = get_session()
        user = session.query(User).filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('listar_produtos'))
        else:
            flash('Email ou senha incorretos')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        session = get_session()
        new_user = User(name=name, email=email, password=password)
        
        try:
            session.add(new_user)
            session.commit()
            flash('Cadastro realizado com sucesso! Faça login.')
            return redirect(url_for('login'))
        except:
            flash('Erro ao cadastrar usuário')
    
    return render_template('cadastro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/produtos')
def listar_produtos():
    session = get_session()
    produtos = session.query(Product).all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def criar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        descricao = request.form['descricao']
        
        session = get_session()
        novo_produto = Product(nome=nome, preco=preco, descricao=descricao)
        
        try:
            session.add(novo_produto)
            session.commit()
            flash('Produto criado com sucesso!')
            return redirect(url_for('listar_produtos'))
        except:
            flash('Erro ao criar produto')
    
    return render_template('form_produto.html')

@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    session = get_session()
    produto = session.get(Product, id)
    
    if not produto:
        flash('Produto não encontrado')
        return redirect(url_for('listar_produtos'))
    
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.preco = float(request.form['preco'])
        produto.descricao = request.form['descricao']
        
        try:
            session.commit()
            flash('Produto atualizado com sucesso!')
            return redirect(url_for('listar_produtos'))
        except:
            flash('Erro ao atualizar produto')
    
    return render_template('form_produto.html', produto=produto)

@app.route('/produtos/excluir/<int:id>')
@login_required
def excluir_produto(id):
    session = get_session()
    produto = session.get(Product, id)
    
    if produto:
        try:
            session.delete(produto)
            session.commit()
            flash('Produto excluído com sucesso!')
        except:
            flash('Erro ao excluir produto')
    
    return redirect(url_for('listar_produtos'))

if __name__ == '__main__':
    app.run(debug=True)