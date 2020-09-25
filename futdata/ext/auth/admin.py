from flask import Markup, flash
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView, filters

from futdata.ext.db.models import Pessoa
from futdata.ext.db import db

from wtforms.fields import TextField
from futdata.ext.db.admin import MyModelView

class UserAdmin(MyModelView):
    '''Interface admin de user'''

    def format_user(self, request, user, *args):
        return user.email.split('@')[0]

    # column_formatters = {'email': format_user}
    column_list = ['nome', 'proprietario', 'email']
    
    # Labels apresentadas na tela
    column_labels = {'email': 'email_login'}
    
    column_searchable_list = ['email']
    column_filters = [
        'email',
        'proprietario',
        filters.FilterLike(
            Pessoa.email, 'dominio', options=(
                ('gmail', 'Gmail'), ('uol', 'Uol')
            )
        ),
    ]
    can_edit = False
    can_create = True
    can_delete = True
    
    # exemple of flask action
    @action('toggle_admin', 'mudar_admin_status', 'Tem certeza?')
    def mudar_admin_status(self, ids):
        users = Pessoa.query.filter(Pessoa.id.in_(ids))
        for user in users.all():
            user.proprietario = not user.proprietario
        db.session.commit()
        flash('Success!', 'success')

    # See other customizations at:
    # https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-built-in-views