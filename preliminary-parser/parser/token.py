class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position
        self.length = len(value)
