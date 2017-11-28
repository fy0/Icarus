import locale
from slim.base.route import Route
from wtforms import Form

route = Route()


class ValidateForm(Form):
    class Meta:
        locales = [locale.getdefaultlocale()[0]]
