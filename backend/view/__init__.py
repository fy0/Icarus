import locale
from slim.base.helper import Route
from wtforms import Form

route = Route()


class ValidateForm(Form):
    class Meta:
        locales = [locale.getdefaultlocale()[0]]
