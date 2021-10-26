from mongoengine import *

class UserMapping(Document):
    name = StringField()
    external_id = StringField()
