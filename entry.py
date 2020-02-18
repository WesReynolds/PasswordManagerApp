class Entry:
    def __init__(self, account="", login="", password=""):
        self.account = ""
        self.login = ""
        self.password = ""

    def __repr__(self):
        return self.account + ": " + self.login

    def __eq__(self, other):
        if type(other) == type(self):
            return self.account == other.account and self.login == other.login
        return False

    def __lt__(self, other):
        return self.account < other.account

    def __hash__(self):
        return hash((self.account, self.login, self.password))

    def setAccount(self, account):
        self.account = account

    def setLogin(self, login):
        self.login = login

    def setPassword(self, password):
        self.password = password

    def getAccount(self):
        return self.account

    def getLogin(self):
        return self.login

    def getPassword(self):
        return self.password
