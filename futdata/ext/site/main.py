from flask import Blueprint, current_app, render_template, request, redirect, flash, url_for, send_file
from futdata.ext.auth.form import UserForm, UserLogin
# from futdata.ext.db.form import LocalForm
from futdata.ext.auth.controller import create_user, save_user_foto, verify_password, verify_email

from futdata.ext.db.controller import create_reserva, verifica_pagamento
from futdata.ext.db.models import Img, Local, Pessoa, Endereco, Reserva
from futdata.ext.db.form import PagamentoForm
from flask_login import login_user, logout_user, current_user

from futdata.ext.db import db


from datetime import datetime, date, time
import pendulum

import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField

from io import BytesIO
from base64 import b64encode


bp = Blueprint("site", __name__)


@bp.route("/")
def index():

    id_local = []
    nome = []
    telefone = []
    preco = []
    imagem = []

    for loc in Local.query.all():
        id_local.append(int(loc.idlocal))
        nome.append(loc.nome)
        telefone.append(loc.telefone)
        preco.append(float(loc.preco))

        obj = Img.query.filter_by(id=loc.imagem_idimagem).first()
        imagem.append(b64encode(obj.img).decode("utf-8"))

    return render_template(
        "index.html",
        obj=obj,
        id_local=id_local,
        imagem=imagem,
        nome=nome,
        telefone=telefone,
        preco=preco,
        qtd=range(0, len(nome)),
        qtd_row=range(0, int(len(nome)/4))
    )


@bp.route("/local")
def local():
    id_local = []
    nome = []
    telefone = []
    preco = []
    imagem = []

    for loc in Local.query.all():
        id_local.append(int(loc.idlocal))
        nome.append(loc.nome)
        telefone.append(loc.telefone)
        preco.append(float(loc.preco))

        obj = Img.query.filter_by(id=loc.imagem_idimagem).first()
        imagem.append(b64encode(obj.img).decode("utf-8"))

    return render_template(
        "index.html",
        obj=obj,
        id_local=id_local,
        imagem=imagem,
        nome=nome,
        telefone=telefone,
        preco=preco,
        qtd=range(0, len(nome)),
        qtd_row=range(0, int(len(nome)/4))
    )

    return render_template("local.html")


@bp.route("/sobre")
def sobre():
    return render_template("sobre.html")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()

    if form.validate_on_submit():

        if verify_password(email=form.email.data, password=form.password.data):
            user = Pessoa.query.filter_by(email=form.email.data).first()

            login_user(user)
            return redirect('/')
        else:
            flash('Login ou senha errado!')

    return render_template('login.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('site.login'))


@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()

    if form.validate_on_submit():

        if verify_email(form.email.data):
            create_user(
                nome=form.nome.data,
                telefone=form.telefone.data,
                email=form.email.data,
                password=form.password.data
            )

            return redirect('/login')
        else:
            flash('Email já cadastrado!', 'success')

    count_local = len(Local.query.all())
    count_pessoa = len(Pessoa.query.all())
    count_reserva = len(Reserva.query.all())

    return render_template(
                            'cadastro.html',
                             form=form,
                             count_local=count_local,
                             count_pessoa=count_pessoa,
                             count_reserva=count_reserva
                        )


@bp.route('/unique/<int:id>', methods=['GET'])
def unique(id):
    """
        id: Id do local que será alocado 
    """
    class AgendaForm(FlaskForm):

        data = DateField('Data', validators=[wtf.validators.DataRequired()])

        local = Local.query.filter_by(idlocal=id).first()
        horas = []
        contador = 0

        for i in range(local.hora_inicio.hour, local.hora_final.hour + 1):
            if i < 10:
                horas.append((contador, '0' + str(i) + ':00'))
            else:
                horas.append((contador, str(i) + ':00'))

            contador += 1

        hora = wtf.SelectField('Hora', choices=horas)


    form = AgendaForm()
    local = Local.query.filter_by(idlocal=id).first()
    obj = Img.query.filter_by(id=local.imagem_idimagem).first()

    endereco = Endereco.query.filter_by(id=local.endereco_idendereco).first()
    responsavel = Pessoa.query.filter_by(id=local.pessoa_idpessoa).first()

    imagem = b64encode(obj.img).decode("utf-8")

    return render_template(
        'local_unique.html',
        local=local,
        imagem=imagem,
        endereco=endereco,
        responsavel=responsavel,
        form=form,
    )


@bp.route('/agendar/<int:id>', methods=['GET', 'POST'])
def agendar(id):
    
    data = request.form.get('data')
    hora = int(request.form.get('hora'))
    
    if data > date.today().strftime("%Y-%m-%d"):

        local = Local.query.filter_by(idlocal=id).first()

        horas = []
        contador = 0

        for i in range(local.hora_inicio.hour, local.hora_final.hour + 1):
            if i < 10:
                horas.append((contador, '0' + str(i) + ':00'))
            else:
                horas.append((contador, str(i) + ':00'))

            contador += 1


        reserva = Reserva.query.filter_by(local_idlocal=id, data=data ,hora=datetime.strptime(horas[hora][1], '%H:%M').time()).first()

        if reserva:
            flash('Data já ocupada', 'error')
            return redirect(f'/unique/{local.idlocal}')

        else:
            nome = current_user.nome
            email = current_user.email
            telefone = current_user.telefone
            
            form = PagamentoForm()

            obj = Img.query.filter_by(id=local.imagem_idimagem).first()
            endereco = Endereco.query.filter_by(id=local.endereco_idendereco).first()
            responsavel = Pessoa.query.filter_by(id=local.pessoa_idpessoa).first()

            imagem = b64encode(obj.img).decode("utf-8")

            return render_template(
                'reserva.html',
                nome=nome,
                email=email,
                telefone=telefone,

                form=form,
                
                imagem=imagem,

                data= data,
                hora= horas[hora][1],
                
                local=local,
                endereco=endereco,
                responsavel=responsavel
            )

    elif data == date.today().strftime("%Y-%m-%d"):


        local = Local.query.filter_by(idlocal=id).first()

        horas = []
        contador = 0

        for i in range(local.hora_inicio.hour, local.hora_final.hour + 1):
            if i < 10:
                horas.append((contador, '0' + str(i) + ':00'))
            else:
                horas.append((contador, str(i) + ':00'))

            contador += 1
        
        # reserva tem que ser efetuado com uma hora de antecedência
        if int(horas[hora][1].split(':')[0]) > (datetime.now().hour + 1):

            reserva = Reserva.query.filter_by(local_idlocal=id, data=data ,hora=datetime.strptime(horas[hora][1], '%H:%M').time()).first()

            if reserva:
                flash('Data já ocupada', 'error')
                return redirect(f'/unique/{local.idlocal}')

            else:
                nome = current_user.nome
                email = current_user.email
                telefone = current_user.telefone
                
                form = PagamentoForm()

                obj = Img.query.filter_by(id=local.imagem_idimagem).first()
                endereco = Endereco.query.filter_by(id=local.endereco_idendereco).first()
                responsavel = Pessoa.query.filter_by(id=local.pessoa_idpessoa).first()

                imagem = b64encode(obj.img).decode("utf-8")

                return render_template(
                    'reserva.html',
                    nome=nome,
                    email=email,
                    telefone=telefone,

                    form=form,
                    
                    imagem=imagem,

                    data= data,
                    hora= horas[hora][1],
                    
                    local=local,
                    endereco=endereco,
                    responsavel=responsavel
                )
        else:
            flash('A reserva precisa de 1 hora de antecedência', 'error')
            return redirect(f'/unique/{id}')
    
    else:
        flash('Data inferior a atual', 'error')
        return redirect(f'/unique/{id}')


@bp.route('/reservado/<int:id>/<data>/<hora>', methods=['GET', 'POST'])
def reservado(id, data, hora):

        if request.form['cod_pagamento']:
            cod_pagamento = request.form['cod_pagamento']

            local = Local.query.filter_by(idlocal=id).first()
            create_reserva(
                        id_local=local.idlocal,
                        data=data,
                        hora= hora,
                        id_pessoa=current_user.id,
                        cod_pagamento= cod_pagamento
                    )
                    
            return redirect('/')

        else:
            flash('Erro na etapada de reserva!', 'error')

@bp.route('/administrador', methods=['GET', 'POST'])
@bp.route('/administrador/<id_reserva>', methods=['GET', 'POST'])
def administrador(id_reserva=None):

    form = PagamentoForm()

    if request.form:

        if request.form['cod_pagamento']:
            
            verifica = verifica_pagamento(id_reserva, form.cod_pagamento.data)

            if verifica:
                flash('Aprovado com sucesso', 'sucess')
                return redirect('/administrador')

            else:
                flash('Senha errada', 'error')

    locais = Local.query.filter_by(pessoa_idpessoa= current_user.id).all()

    if locais:
        list_reserva = []

        for local in locais:
            reservas = Reserva.query.order_by(Reserva.data.desc(), Reserva.hora.desc() ).filter_by(local_idlocal= local.idlocal).all()
            # reservas = Reserva.query.filter_by(local_idlocal= local.idlocal).all()
            
            for reserva in reservas:
                pessoa = Pessoa.query.filter_by(id= reserva.pessoa_idpessoa).first()
                local_nome = local.nome
                horario = reserva.hora
                data = reserva.data.strftime('%d-%m-%Y')
                nome_pessoa = pessoa.nome
                telefone_pessoa = pessoa.telefone
                id_reserva = reserva.column_not_exist_in_db
                status_pagamento = reserva.pagamento
                list_reserva.append([local_nome, data, horario, nome_pessoa, telefone_pessoa, id_reserva, status_pagamento])

        return render_template(
                'adm.html',
                list_reserva=list_reserva,
                locais= True,
                form=form
            )
    
    flash('Não há local vinculado ao seu usuário', 'error')
    return render_template(
                'adm.html',
                locais=locais,
            )

    
@bp.route('/agendado', methods=['GET', 'POST'])
def agendado():

   
    # * Não ordenado
    # reserva = Reserva.query.filter_by(pessoa_idpessoa= current_user.id).all()

    # * Ordenado ascendente
    # reserva = Reserva.query.order_by(Reserva.data).filter_by(pessoa_idpessoa=current_user.id).all()
    
    # * ordenado descendente
    reserva = Reserva.query.order_by(Reserva.data.desc(), Reserva.hora.desc() ).filter_by(pessoa_idpessoa=current_user.id).all()

    
    reservas = []

    for res in reserva:
        local = Local.query.filter_by(idlocal= res.local_idlocal).first()
        responsavel = Pessoa.query.filter_by(id= local.pessoa_idpessoa).first()
        
        local = local.nome.strip()
        telefone = responsavel.telefone

        responsavel = responsavel.nome


        if res.pagamento:
            pagamento = 'Pago'
        else:
            pagamento = 'Pendente'

        data = res.data.strftime('%d-%m-%Y')
        hora = res.hora

        reservas.append([local, data, hora, responsavel, telefone, pagamento])


    return render_template('agendado.html', reservas=reservas)


@bp.route('/calendar/<int:id>', methods=['GET', 'POST'])
def calendar(id):

    local = Local.query.filter_by(idlocal= id).first()

    if request.form:
        hoje = pendulum.from_format(request.form['data'], 'YYYY-MM-DD').date()
    else:
        hoje =pendulum.now().date()

    futuro = hoje.add(days=6)
    interval_date = pendulum.period(hoje, futuro)

    marcados = []

    for hora in range(local.hora_inicio.hour, local.hora_final.hour + 1):
        aux = []
        aux.append(hora)
        for date in interval_date:
            reservado = Reserva.query.filter_by(local_idlocal=id, data=date ,hora=datetime.strptime(f'{hora}:00', '%H:%M').time()).first()
            if reservado:
                aux.append('Reservado')
            else:
                aux.append('Liberado')
        marcados.append(aux)
        

    return render_template('calendar_2.html', interval_date=interval_date, marcados=marcados)
