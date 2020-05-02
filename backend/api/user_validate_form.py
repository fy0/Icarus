import re
import config
from model.user import User
from api import ValidateForm
from wtforms import StringField, validators as va, ValidationError


def email_exists_check(form, field):
    email = field.data
    if list(User.select().where(User.email == email)):
        raise ValidationError('此邮箱已注册')
    return True


def nickname_exists_check(form, field):
    name = field.data
    if list(User.select().where(User.nickname == name)):
        raise ValidationError('此昵称已被占用')
    return True


def nickname_check(form, field):
    # 至少两个汉字，或以汉字/英文字符开头至少4个字符
    text = '至少%d个汉字，或以汉字/英文字符开头至少%d个字符' % (config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN)
    name = field.data
    # 检查首字符，检查有无非法字符
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$', name):
        raise ValidationError(text)
    # 若长度大于等于4，直接许可
    if len(name) >= max(config.USER_NICKNAME_FOR_REG_MIN, config.USER_NICKNAME_CN_FOR_REG_MIN):
        return True

    # 当最少汉字要求少于最少英文要求
    if config.USER_NICKNAME_CN_FOR_REG_MIN < config.USER_NICKNAME_FOR_REG_MIN:
        # 长度小于4，检查其中汉字数量
        if not (len(re.findall(r'[\u4e00-\u9fa5]', name)) >= config.USER_NICKNAME_CN_FOR_REG_MIN):
            raise ValidationError(text)
    elif config.USER_NICKNAME_CN_FOR_REG_MIN > config.USER_NICKNAME_FOR_REG_MIN:
        if not (len(re.findall(r'[a-zA-Z0-9]', name)) >= config.USER_NICKNAME_FOR_REG_MIN):
            raise ValidationError(text)

    if config.USER_NICKNAME_CHECK_FUNC and not config.USER_NICKNAME_CHECK_FUNC(name):
        raise ValidationError('昵称被保留')

class PasswordForm(ValidateForm):
    """
    用于重置密码时设置密码
    """
    password = StringField('密码', validators=[
        va.required(),
        # va.Length(config.USER_PASSWORD_MIN, config.USER_PASSWORD_MAX)
    ])


class NicknameForm(ValidateForm):
    """
    用于重置昵称时设置新昵称
    """
    nickname = StringField('昵称', validators=[
        va.required(),
        va.Length(min(config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN), config.USER_NICKNAME_FOR_REG_MAX),
        nickname_check,
        nickname_exists_check
    ])
