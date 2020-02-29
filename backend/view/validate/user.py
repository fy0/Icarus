from schematics import Model
from schematics.types import StringType

from slim.base.types.doc import ValidatorDoc
from slim.utils.schematics_ext import BlobType


class ValidatePasswordResetPost(Model):
    password = StringType(required=True, metadata=ValidatorDoc('新密码'))
    uid = BlobType(required=True)
    code = BlobType(required=True)
