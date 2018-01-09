import app
import locale
from wtforms import Form

route = app.app.route


class ValidateForm(Form):
    class Meta:
        locales = [locale.getdefaultlocale()[0]]
