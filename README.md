README — Sistema de Controle de Vendas (Flask)
Descrição do projeto

Este é um sistema web de controle de vendas, desenvolvido com Python (Flask) e SQLite, como parte do meu portfólio.
O objetivo é demonstrar habilidades em desenvolvimento backend, CRUD, autenticação de usuários e deploy na nuvem.

O sistema permite:

Cadastrar, editar e excluir clientes;
Cadastrar e gerenciar produtos;
Criar e listar pedidos;
Fazer login e logout com controle de acesso;
Exclusão automática em cascata (clientes e seus pedidos);

Tecnologias utilizadas:

Python 3
Flask
SQLite
Flask-Login
HTML / CSS / Jinja
Render (Deploy)
Acesso de demonstração

Para testar o sistema online, acesse:
[https://controle-de-vendas-flask.onrender.com]

Use as credenciais públicas:
Usuário: demo
Senha: demo123

Como rodar localmente:

# Clone o repositório
git clone https://github.com/seuusuario/controle_vendas.git

# Entre na pasta
cd controle_vendas

# Crie e ative o ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Rode o servidor
python app.py

Depois, acesse no navegador:

http://127.0.0.1:5000

Funcionalidades principais:

-Login e autenticação com Flask-Login
-CRUD completo de clientes e produtos
-Registro e visualização de pedidos
-Exclusão em cascata (ao apagar cliente, os pedidos são removidos)
-Interface simples e intuitiva
-Banco de dados criado automaticamente ao iniciar o app

Objetivo:

Este projeto faz parte do meu portfólio e demonstra:

Lógica e estruturação de aplicações Flask
Manipulação de banco de dados relacional
Criação de rotas seguras com autenticação
Deploy completo de app Python em ambiente de produção
--------------------------------------------------------------------------
