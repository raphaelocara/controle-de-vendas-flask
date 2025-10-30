# criar_usuario.py

from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

def criar_usuario(username, senha):
    with app.app_context():
        # Checa se o usu�rio j� existe
        if Usuario.query.filter_by(username=username).first():
            print(f"Usu�rio '{username}' j� existe!")
            return
        # Cria usu�rio
        senha_criptografada = generate_password_hash(senha)
        novo_usuario = Usuario(username=username, senha=senha_criptografada)
        db.session.add(novo_usuario)
        db.session.commit()
        print(f"Usu�rio '{username}' criado com sucesso!")

# Exemplo de uso
if __name__ == "__main__":
    criar_usuario("demo", "demo123")
