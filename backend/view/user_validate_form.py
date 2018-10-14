import config
from model.user import User
from view import ValidateForm
from wtforms import StringField, validators as va, ValidationError

# 注册


def email_exists_check(form, field):
    email = field.data
    if list(User.select().where(User.email == email)):
        raise ValidationError('此邮箱已注册')
    return True


class RequestSignupByEmailForm(ValidateForm):
    email = StringField('邮箱', validators=[
        va.required(),
        va.Length(3, config.USER_EMAIL_MAX),
        va.Email(),
        email_exists_check
    ])

    password = StringField('密码', validators=[
        va.required(),
        # va.Length(config.USER_PASSWORD_MIN, config.USER_PASSWORD_MAX)
    ])

    password2 = StringField('重复密码', validators=[
        va.required(),
        va.EqualTo('password')
    ])
