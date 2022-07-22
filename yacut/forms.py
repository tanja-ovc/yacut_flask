from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .models import URL_map


class LinkCreationForm(FlaskForm):
    original_link = StringField(
        label='Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        # в продолжение этого текста в шаблоне будет указан URL хоста сервиса
        label='Создайте короткий вариант ссылки: впишите продолжение адреса, '
              'которое вы хотели бы увидеть после ',
        description='Вы можете не вводить ничего в это поле, а просто '
                    'нажать "Создать". Тогда короткая ссылка сгенерируется '
                    'автоматически.',
        validators=[
            Length(1, 16, 'Максимальная длина ввода здесь - 16 символов.'),
            Regexp(regex=r'^[A-Za-z0-9]+$',
                   message='Допустимые символы для ссылки: a-z, A-Z, 0-9.'),
            Optional()
        ]
    )
    submit = SubmitField('Создать короткую ссылку')

    def validate_custom_id(form, field):
        custom_id = field.data
        if URL_map.query.filter_by(short=custom_id).first() is not None:
            flash(f'Имя {custom_id} уже занято!')
            raise ValidationError(
                'Такая ссылка уже создавалась, введите другой вариант.'
            )
