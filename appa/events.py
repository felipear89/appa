class Singleton:

    _instance = None

    def __init__(self):
        self.events = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def add_event(key, method):
    Singleton.instance().events[key] = method


def get_action(key):
    return Singleton.instance().events[key]
