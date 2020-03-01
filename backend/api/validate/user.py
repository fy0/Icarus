from schematics import Model
from schematics.types import StringType, EmailType

import config
from slim.base.types.doc import ValidatorDoc
from slim.utils.schematics_ext import BlobType


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


class SignupDataModel(Model):
    email = EmailType(min_length=3, max_length=30, required=True, metadata=ValidatorDoc('Email'))
    username = StringType(min_length=2, max_length=30, metadata=ValidatorDoc('Username'))
    password = StringType(required=True, min_length=6, max_length=64, metadata=ValidatorDoc('Password'))
    nickname = StringType(min_length=2, max_length=10, metadata=ValidatorDoc('Nickname'))
