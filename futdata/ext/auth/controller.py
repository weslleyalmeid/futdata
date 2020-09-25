from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask import current_app as app

from futdata.ext.db.models import Pessoa
from futdata.ext.db import db
import os.path

# algoritmo de autenticação
ALG = 'pbkdf2:sha256'

# utilizando type anotation
def create_user(nome: str, telefone: str, email: str, password: str, proprietario: bool = False) -> Pessoa:
    """
        nome, telefone, email, password, proprietario 
    """
    # hashing da senha
    password = generate_password_hash(password, ALG)
    user = Pessoa(nome=nome, telefone=telefone, email=email, password=password, proprietario=proprietario)
    db.session.add(user)
    # todo: Tratar exception caso user já exista
    db.session.commit()
    return user


def verify_email(email):
    """
        nome: nome do usuário
    """
    user = Pessoa.query.filter_by(email= email).first()
    if user:
        return False
    return True

def verify_password(email, password):
    """
        email: email do usuário
        password: senha do usuário 
    """
    user = Pessoa.query.filter_by(email= email).first()
    # import ipdb; ipdb.set_trace()
    if user:
        return check_password_hash(user.password, password)
    else:
        return False


def save_user_foto(filename, filestorage):
    """
        Saves user foto in
        ./uploads/foo/ehauehau.ext 
    """
    filename = os.path.join(
        app.config['UPLOAD_FOLDER'],
        secure_filename(filename)
    )
    # todo: verificar se o diretório existe
    # todo: criar o diretório
    filestorage.save(filename)

