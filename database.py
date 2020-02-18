class Database:
    def __init__(self):
        self.database = []

    def __repr__(self):
        return self.database.__repr__()

    def addEntry(self, entry):
        if entry not in self.database:
            self.database.append(entry)
            self.database.sort()

    def removeEntry(self, entry):
        self.database.remove(entry)

    def getEntry(self, index):
        if index < self.getSize():
            return self.database[index]

    def findEntryIndex(self, account, login, password):
        for index in range(self.getSize()):
            if self.database[index].getAccount() == account and self.database[index].getLogin() == login and self.database[index].getPassword() == password:
                return index

    def getSize(self):
        return len(self.database)

    def getButtonText(self, index):
        if index < self.getSize():
            entry = self.getEntry(index)
            return entry.getAccount() + " (" + entry.getLogin() + ")"
        else:
            return ""
