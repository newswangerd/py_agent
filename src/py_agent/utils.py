class Listener:
    def __init__(self, match, func):
        self.listen_for = match
        self.listener = func
    
    def __call__(self, *args, **kwargs):
        return self.listener(*args, **kwargs)

def listen_for(match):
    def dec(func):
        return Listener(match, func)
    return dec