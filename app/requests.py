from skpy import Skype

skype = Skype("stels.1334@gmail.com", "CE06Sgr94ukuO8lw")


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
