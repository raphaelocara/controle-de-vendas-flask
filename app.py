from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Cliente, Produto, Pedido, ItemPedido, Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Troque para uma chave secreta segura
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Trata o usuário demo (id = 0)
    if user_id == "0":
        from flask_login import UserMixin
        class DemoUser(UserMixin):
            id = 0
            username = "demo"
        return DemoUser()
    # Para os outros usuários normais do banco
    return Usuario.query.get(int(user_id))

@app.before_request
def criar_tabelas():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        app.db_initialized = True

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        # --- Login público para demonstração ---
        if username == "demo" and senha == "demo123":
            from flask_login import UserMixin
            class DemoUser(UserMixin):
                id = 0
                username = "demo"
            user = DemoUser()
            login_user(user)
            flash('Login de demonstração realizado com sucesso!')
            return redirect(url_for('index'))

        # --- Login normal via banco ---
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.')

    return render_template('login.html', current_year=datetime.now().year)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Proteja as rotas com @login_required
@app.route('/')
@login_required
def index():
    return render_template('index.html', current_year=datetime.now().year)

# Outras rotas também podem ser protegidas, por exemplo:
@app.route('/clientes')
@login_required
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes, current_year=datetime.now().year)

# Cria o banco de dados e as tabelas ao iniciar a aplicação
with app.app_context():
    db.create_all()

@app.route('/clientes/novo', methods=['POST'])
def adicionar_cliente():
    nome = request.form['nome']
    email = request.form['email']
    novo_cliente = Cliente(nome=nome, email=email)
    db.session.add(novo_cliente)
    db.session.commit()
    return redirect(url_for('listar_clientes'))

@app.route('/clientes/excluir/<int:cliente_id>', methods=['POST'])
def excluir_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('listar_clientes'))

@app.route('/clientes/editar/<int:cliente_id>')
def form_editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return render_template('editar_cliente.html', cliente=cliente, current_year=datetime.now().year)

@app.route('/clientes/editar/<int:cliente_id>', methods=['POST'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    cliente.nome = request.form['nome']
    cliente.email = request.form['email']
    db.session.commit()
    return redirect(url_for('listar_clientes'))

# ... seu código atual ...

@app.route('/produtos')
@login_required
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos, current_year=datetime.now().year)

@app.route('/produtos/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        estoque = int(request.form['estoque'])
        produto = Produto(nome=nome, preco=preco, estoque=estoque)
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('listar_produtos'))
    return render_template('novo_produto.html', current_year=datetime.now().year)

@app.route('/produtos/editar/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.preco = float(request.form['preco'])
        produto.estoque = int(request.form['estoque'])
        db.session.commit()
        return redirect(url_for('listar_produtos'))
    return render_template('editar_produto.html', produto=produto, current_year=datetime.now().year)

@app.route('/produtos/excluir/<int:produto_id>', methods=['POST'])
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('listar_produtos'))

@app.route('/pedidos')
def listar_pedidos():
    pedidos = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos, current_year=datetime.now().year)

@app.route('/pedidos/novo', methods=['GET', 'POST'])
def novo_pedido():
    if request.method == 'POST':
        cliente_id = request.form['cliente']
        produtos_ids = request.form.getlist('produtos')
        quantidades = request.form.getlist('quantidades')

        pedido = Pedido(cliente_id=cliente_id)
        db.session.add(pedido)
        db.session.commit()

        for produto_id, quantidade in zip(produtos_ids, quantidades):
            if int(quantidade) > 0:
                item = ItemPedido(pedido_id=pedido.id, produto_id=produto_id, quantidade=quantidade)
                db.session.add(item)

        db.session.commit()
        return redirect(url_for('listar_pedidos'))

    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template('novo_pedido.html', clientes=clientes, produtos=produtos, current_year=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True)

