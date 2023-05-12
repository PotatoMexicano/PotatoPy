from flask import Blueprint, redirect, url_for, jsonify, request

from potatopy.models import Usuario

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['POST'])
def register():

    login = senha = None

    error = None
    
    if 'login' in request.form:
        login = request.form['login']

    if 'senha' in request.form:
        senha  = request.form['senha']
    
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
