from futdata.ext.db.models import Pessoa
from futdata.ext.db import db


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with sample data"""
    data = [
        Pessoa(),
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return Pessoa.query.all()