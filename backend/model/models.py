from model import db
from model.test import Test

db.connect()
db.create_tables([Test], safe=True)
