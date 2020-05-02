import re

from schematics import Model
from schematics.exceptions import ValidationError
from schematics.types import StringType, EmailType

import config
from model.user import User
from slim.base.types.doc import ValidatorDoc
from slim.utils.schematics_ext import BlobType


def email_exists_check(email):
    if list(User.select().where(User.email == email)):
        raise ValidationError('此邮箱已注册')
    return True


def nickname_exists_check(name):
    if list(User.select().where(User.nickname == name)):
        raise ValidationError('此昵称已被占用')
    return True


def nickname_check(name):
    # 至少两个汉字，或以汉字/英文字符开头至少4个字符
    text = '至少%d个汉字，或以汉字/英文字符开头至少%d个字符' % (config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN)
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


nickname_type = StringType(
    min_length=min(config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN),
    max_length=config.USER_NICKNAME_FOR_REG_MAX,
    validators=[nickname_check, nickname_exists_check],
    metadata=ValidatorDoc('昵称')
)


class ValidatePasswordResetPost(Model):
    password = StringType(required=True, metadata=ValidatorDoc('新密码'))
    uid = BlobType(required=True)
    code = BlobType(required=True)


class ChangePasswordDataModel(Model):
    old_password = StringType(required=True, metadata=ValidatorDoc('旧密码'))  # va.Length(config.USER_PASSWORD_MIN, config.USER_PASSWORD_MAX)
    password = StringType(required=True, metadata=ValidatorDoc('新密码'))


class SigninDataModel(Model):
    """
    email和nickname是二选一，但是model中没法体现，要代码检测
    """
    email = EmailType(min_length=3, max_length=config.USER_EMAIL_MAX, metadata=ValidatorDoc('邮箱'))
    nickname = StringType(metadata=ValidatorDoc('昵称'))
    password = StringType(required=True, metadata=ValidatorDoc('密码'))


class SignupConfirmByEmailDataModel(Model):
    email = EmailType(min_length=3, max_length=config.USER_EMAIL_MAX, required=True, metadata=ValidatorDoc('邮箱'))
    code = BlobType(required=True, metadata=ValidatorDoc('验证码'))


class SignupDirectDataModel(Model):
    email = EmailType(min_length=3, max_length=config.USER_EMAIL_MAX, required=True, metadata=ValidatorDoc('邮箱'))
    password = StringType(required=True, min_length=6, max_length=64, metadata=ValidatorDoc('密码'))
    nickname = nickname_type


class SignupRequestByEmailDataModel(Model):
    """
    申请进行邮箱注册
    """
    email = EmailType(min_length=3, max_length=config.USER_EMAIL_MAX, required=True, validators=[email_exists_check], metadata=ValidatorDoc('邮箱'))
    password = StringType(required=True, min_length=6, max_length=64, metadata=ValidatorDoc('密码'))
    nickname = StringType(min_length=2, max_length=10, metadata=ValidatorDoc('昵称'))


class ChangeNicknameDataModel(Model):
    nickname = nickname_type
