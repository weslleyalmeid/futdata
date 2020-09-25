from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from futdata.ext.db import db

from futdata.ext.db.models import Pessoa, Local, Endereco, Img, Reserva
from futdata.ext.auth.admin import UserAdmin
from futdata.ext.db.admin import ImgAdmin, MyModelView, LocalAdmin


admin = Admin()


def init_app(app):
    admin.name = 'FUTDATA'
    admin.template_mode = 'bootstrap3'
    admin.init_app(app)

    # Local onde adiciona viwes no localhost/admin -> exemplo |Pessoa|Modalidade|
    admin.add_view(UserAdmin(Pessoa, db.session))
    # admin.add_view(MyModelView(Modalidade, db.session))
    admin.add_view(MyModelView(Endereco, db.session))
    admin.add_view(ImgAdmin(Img, db.session))
    admin.add_view(LocalAdmin(Local, db.session))
    admin.add_view(MyModelView(Reserva, db.session))
    # UserAdmin inherits from ModelView
