import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from futdata.ext.db import db
# from futdata.ext.db.models import Local


class AgendaForm(FlaskForm):

    def form_reserva(self, id_local, Local):
        data = DateField('Data', validators=[wtf.validators.DataRequired()])
        
        local = Local.query.filter_by(idlocal=id_local).first()

        horas = []
        contador = 0
        for i in range(local.hora_inicio.hour, local.hora_final.hour + 1):
            horas.append((contador, str(i)))
            contador += 1

        hora = wtf.SelectField('Hora', default=(0, "6"), choices=horas)

        # hora = wtf.SelectField('Hora', default=(0, "6"), choices=[(
        #     0, "18:00"), (1, "19:00"), (2, "20:00"), (3, "21:00"), (4, "22:00"), (5, "23:00")])


class PagamentoForm(FlaskForm):
    cod_pagamento = wtf.StringField('Código de Pagamento', [wtf.validators.DataRequired()])