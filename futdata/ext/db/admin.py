# from flask import current_app as app
from flask import request
from flask import current_app as app
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField, FileUploadField

from futdata.ext.db.models import Img, Pessoa, Local
from futdata.ext.db import db
from flask_login import current_user
from werkzeug.utils import secure_filename
import os.path
# from werkzeug.utils import secure_filename
import imghdr

from wtforms.fields import TextField

class MyModelView(ModelView):

    def is_accessible(self):
        try:
            return current_user.email == 'admin@admin.com'
            # return current_user.is_authenticated
        except:
            return False

class ImgAdmin(MyModelView):
    '''Interface admin de Img'''

    column_list = ['name']
    form_columns = ['img']

    def on_model_change(self, form, model, is_created):

        pic = request.files['img']
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        if not filename or not mimetype:
            return 'Bad upload!', 400

        model.img = form.img.data
        model.name = filename
        model.mimetype = mimetype



    def picture_validation(form, field):
        if field.data:
            filename = field.data.filename
            if filename[-4:] != '.jpg':
                raise ValidationError('file must be .jpg')
            if imghdr.what(field.data) != 'jpeg':
                raise ValidationError('file must be a valid jpeg image.')
        field.data = field.data.stream.read()
        return True

    def pic_formatter(view, context, model, name):
        return 'NULL' if len(getattr(model, name)) == 0 else 'a picture'


    DIR_NAME = os.path.abspath('.')
    DIR_IMAGE = os.path.join(DIR_NAME, 'img')
    column_formatters = dict(pic=pic_formatter)
    form_overrides = dict(img=FileUploadField)
    form_args = {
                    'img': {'validators':[picture_validation]},
                    'path':{
                                'label': 'File',
                                # 'base_path':   current_app.config['UPLOAD_FOLDER'],
                                'base_path': DIR_IMAGE,
                                'allow_overwrite': True
                            }
                }           

    # See other customizations at:
    # https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-built-in-views

class LocalAdmin(MyModelView):

    column_searchable_list = ['nome']
