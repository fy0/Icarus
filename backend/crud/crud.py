from crud.roles.vistor import visitor
from crud.user import User
from model import db
from model.user_model import UserModel
from pycurd.crud.ext.peewee_crud import PeeweeCrud

c = PeeweeCrud({
    None: visitor
}, {
    User: UserModel,
}, db)
