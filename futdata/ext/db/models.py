# -*- encoding: utf-8 -*-
from futdata.ext.db import db, login_manager

# parte para Login do User
# from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    """
        Retorna o usuário que está logado. 
    """
    return Pessoa.query.filter_by(id= id).first()

class Endereco(db.Model):
    __tablename__ = "endereco"
    id = db.Column('idEndereco', db.Integer, primary_key=True)
    rua = db.Column('rua', db.Unicode)
    numero = db.Column('numero', db.Integer)
    bairro = db.Column('bairro', db.Unicode)

    def __repr__(self):
        return self.rua

class Pessoa(db.Model):
    __tablename__ = "pessoa"
    
    id = db.Column("id", db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    telefone = db.Column('telefone', db.Unicode)
    email = db.Column("email", db.Unicode, unique=True, nullable=False)
    password = db.Column("password", db.Unicode)
    proprietario = db.Column('proprietario', db.Boolean)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.email
    

# class Modalidade(db.Model):
#     __tablename__ = "modalidade"
#     idmodalidade = db.Column('idModalidade', db.Integer, primary_key=True)
#     nome = db.Column('nome', db.Unicode)

#     def __repr__(self):
#         return self.nome

class Local(db.Model):
    __tablename__ = "local"
    idlocal = db.Column('idLocal', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    telefone = db.Column('telefone', db.Unicode)
    preco = db.Column('preco', db.Numeric(5,2))
    hora_inicio = db.Column('hora_inicial', db.Time())
    hora_final = db.Column('hora_final', db.Time())
    endereco_idendereco = db.Column('Endereco_idEndereco', db.Integer, db.ForeignKey('endereco.idEndereco'))
    pessoa_idpessoa = db.Column('Pessoa_idPessoa', db.Integer, db.ForeignKey('pessoa.id'))
    imagem_idimagem = db.Column('Img_idImg', db.Integer, db.ForeignKey('imagem.id'))

    endereco = db.relationship('Endereco', foreign_keys=endereco_idendereco)
    pessoa = db.relationship('Pessoa', foreign_keys=pessoa_idpessoa)
    imagem = db.relationship('Img', foreign_keys=imagem_idimagem)

    def __repr__(self):
        return self.nome


class Img(db.Model):
    __tablename__ = "imagem"
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)

    def __repr__(self):
        return self.name

class Reserva(db.Model):
    __tablename__ = "reserva"

    # sqlalchemy aprovar a criação
    column_not_exist_in_db = db.Column(db.Integer, primary_key=True)

    # PK composta data, hora e local
    local_idlocal = db.Column('Local_idLocal', db.Integer, db.ForeignKey('local.idLocal'))
    data = db.Column('data', db.Date)
    hora = db.Column('hora', db.Time())
    cod_pagamento = db.Column('cod_pagamento', db.Unicode)

    pagamento = db.Column('pagamento', db.Boolean, default=False)
    pessoa_idpessoa = db.Column('Pessoa_idPessoa', db.Integer, db.ForeignKey('pessoa.id'))
    # modalidade_idmodalidade = db.Column('Modalidade_idModalidade', db.Integer, db.ForeignKey('modalidade.idModalidade'))
    
    pessoa = db.relationship('Pessoa', foreign_keys=pessoa_idpessoa)
    # modalidade = db.relationship('Modalidade', foreign_keys=modalidade_idmodalidade)
    local = db.relationship('Local', foreign_keys=local_idlocal)



