from flask import Blueprint, jsonify, request, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from potatopy.models import Usuario
from potatopy import role_required

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():

    login = senha = None

    error = None

    if 'login' in request.form:
        login = request.form['login']

    if 'senha' in request.form:
        senha = request.form['senha']

    if login is None:
        error = 'field Login is required.'
        return jsonify({'message': str(error)}), 400

    if senha is None:
        error = 'field Senha is required.'
        return jsonify({'message': str(error)}), 400

    usuario = Usuario.get_by_login(login=login)

    if usuario is not None:

        if check_password_hash(usuario.senha, senha):

            session.clear()
            login_user(usuario)

            return jsonify({'message': f'Bem vindo {usuario.login}', 'usuario':str(current_user)})

        return jsonify({'message':'Senha inválida'}), 403

    return jsonify({'message':'usuário não encontrado.'}), 400

@auth.route('/logout', methods=['POST'])
def logout():
    session.clear()
    logout_user()

    return jsonify({'message':'Usuário saiu do sistema.', 'usuario':str(current_user)})

@auth.route('/register', methods=['POST'])
def register():

    login = senha = None

    error = None

    if 'login' in request.form:
        login = request.form['login']

    if 'senha' in request.form:
        senha = request.form['senha']

    if login is None:
        error = "field Login is required."
        return jsonify({'message': str(error)}), 400

    if senha is None:
        error = "field Senha is required."
        return jsonify({'message': str(error)}), 400

    novo_usuario = Usuario(login, senha).register()

    if novo_usuario is None:
        error = "fail to add new user."
        return jsonify({'message': str(error)}), 400

    return jsonify({'message': str(f'Usuário adicionado com sucesso. {repr(novo_usuario)}')}), 200

@auth.route('/update/<int:id_usuario>', methods=['PATCH','PUT','POST'])
def update(id_usuario: int):

    usuario = Usuario.get_by_id(pk=id_usuario)

    values = request.form.to_dict()

    if usuario is None:
        return jsonify({'message': 'Usuário não encontrado'})

    if g.user.role != 'admin':

        if 'senha' in values:
            values.pop('senha')

        if 'role' in values:
            values.pop('role')

    if g.user.role == 'admin':

        if 'senha' in values:
            values['senha'] = generate_password_hash(values['senha'])

    if g.user.id == id_usuario:

        if 'role' in values:
            values.pop('role')

    usuario.update(values=values)

    return jsonify({'message': f'Usuário {usuario} atualizado.'})


@auth.route('/user', methods=['GET'])
@login_required
def user():
    return jsonify({'message':'Página de usuário', 'usuario': current_user.to_dict()})

@auth.route('/admin', methods=['GET'])
@role_required('admin')
@login_required
def admin():
    return jsonify({'message':'Página de admin', 'usuario': current_user.to_dict()})
