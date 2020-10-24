from app import app
from permissions_old.roles import *
from permissions_old.tables import *


app.permission.add(None, visitor)
app.permission.add('banned_user', banned_user)
app.permission.add('inactive_user', inactive_user)
app.permission.add('user', normal_user)
app.permission.add('wiki_editor', wiki_editor)
app.permission.add('superuser', superuser)
app.permission.add('admin', admin)
