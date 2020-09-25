import click
from futdata.ext.db.commands import create_db, drop_db, populate_db
from futdata.ext.auth.controller import create_user
from flask_login import login_user


def init_app(app):
    
    app.cli.add_command(app.cli.command()(create_db))
    app.cli.add_command(app.cli.command()(create_db))
    app.cli.add_command(app.cli.command()(drop_db))
    app.cli.add_command(app.cli.command()(populate_db))

    @app.cli.command()
    @click.option('--nome', prompt=True, required=True)
    @click.option('--telefone', prompt=True, required=True, hide_input=True, confirmation_prompt=True)
    @click.option('--email', prompt=True, required=True)
    @click.option('--password', prompt=True, required=True)
    @click.option('--proprietario', prompt=True, required=True, default=False)
    def adduser(nome, telefone, email, password, proprietario):
        """Cria um novo usuario"""
        with app.app_context():
            try:
                create_user(nome, telefone, email, password, proprietario)
            except Exception as e:
                click.echo(f'Nao foi possivel criar o usuario {nome}')
                raise
            else:
                click.echo(f"Usuario {nome} criado com sucesso!")

    @app.cli.command()
    def admin_add():
        """Cria um novo usuario"""
        nome = 'admin'
        telefone = '123456'
        email = 'admin@admin.com'
        password = '123'
        proprietario = False
        with app.app_context():
            try:
                create_user(nome, telefone, email, password, proprietario)

            except Exception as e:
                click.echo(f'Nao foi possivel criar o usuario {nome}')
                raise
            else:
                click.echo(f"Usuario {nome} criado com sucesso!")
    
    @app.cli.command()
    def do_something():
        """Simple command that do something"""
        click.echo("Doing something")