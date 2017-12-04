import locale
import app
from slim.base.route import Route
from wtforms import Form

route = app.app.route


class ValidateForm(Form):
    class Meta:
        locales = [locale.getdefaultlocale()[0]]
