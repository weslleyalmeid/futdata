from werkzeug.utils import secure_filename
from futdata.ext.db.models import Local, Reserva
from flask import current_app as app
from futdata.ext.db import db
import os.path
from datetime import datetime


def save_user_foto(filename, filestorage):
    """
        Saves user foto in
        ./uploads/foo/ehauehau.ext 
    """
    filename = os.path.join(
        app.config['UPLOAD_FOLDER'],
        secure_filename(filename)
    )

    filestorage.save(filename)

def create_reserva(id_local, data, hora, id_pessoa, cod_pagamento):

    reserva = Reserva(
                           local_idlocal=id_local,
                            # data=data,
                            data=datetime.strptime(data, '%Y-%m-%d').date(),
                            # hora=hora,
                            hora=datetime.strptime(hora, '%H:%M').time(),
                            pagamento=0,
                            pessoa_idpessoa=id_pessoa,
                            cod_pagamento=cod_pagamento
                            # modalidade_idmodalidade=1,
                )

    db.session.add(reserva)
    db.session.commit()

def verifica_pagamento(id_reserva, cod_pagamento):

    reserva = Reserva.query.filter_by(column_not_exist_in_db=id_reserva).first()

    if reserva.cod_pagamento == cod_pagamento:

        reserva.pagamento = True
        db.session.commit()
        return True

    return False


