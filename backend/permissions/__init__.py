from app import app
from permissions.roles import *
from permissions.tables import *


app.permission.add(visitor)
app.permission.add(banned_user)
app.permission.add(inactive_user)
app.permission.add(normal_user)
app.permission.add(wiki_editor)
app.permission.add(superuser)
app.permission.add(admin)
