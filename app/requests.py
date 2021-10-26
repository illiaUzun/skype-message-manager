from skpy import Skype

skype = Skype("Sabansky5000@gmail.com", "Iluhakorol99")


class Contact(object):

    def __init__(self, id, name, location, birthday):
        self.id = id
        self.name = name
        self.location = location
        self.birthday = birthday


class Chat(object):

    def __init__(self, id, topic):
        self.id = id
        self.topic = topic
