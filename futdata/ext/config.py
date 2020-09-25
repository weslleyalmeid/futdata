from dynaconf import FlaskDynaconf

import jinja2


def init_app(app):
    FlaskDynaconf(app)
    app.config.load_extensions("EXTENSIONS")
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')