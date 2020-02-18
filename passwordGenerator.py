import random


class PasswordGenerator:
    def __init__(self):
        self.length = 12
        self.capitals = 0
        self.specials = 0
        self.numbers = 0

    def setLength(self, length):
        try:
            self.length = int(length)
        except ValueError:
            self.length = 12

    def setCapitals(self, capitals):
        try:
            self.capitals = int(capitals)
        except ValueError:
            self.capitals = 0

    def setSpecials(self, specials):
        try:
            self.specials = int(specials)
        except ValueError:
            self.specials = 0

    def setNumbers(self, numbers):
        try:
            self.numbers = int(numbers)
        except ValueError:
            self.numbers = 0

    # User enters the number of characters they desire their password to be
    def generatePassword(self):
        password = ""
        s = 0
        n = 0
        c = 0
        for i in range(self.length):
            char = chr(random.randint(32, 126))
            if 97 <= ord(char) <= 122:
                pass
            elif 48 <= ord(char) <= 57:
                n += 1
            elif 65 <= ord(char) <= 90:
                c += 1
            else:
                s += 1
            password += char
        if s < self.specials or n < self.numbers or c < self.capitals:
            try:
                return self.generatePassword()
            except RecursionError as e:
                return "Try again please"
        return password
