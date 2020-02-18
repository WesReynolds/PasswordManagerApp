from kivy.app import App
import pickle
import time
import pyperclip
import ctypes

from switchingScreen import SwitchingScreen
from appManager import AppManager
from entry import Entry
from passwordGenerator import PasswordGenerator

screenManager = SwitchingScreen.getScreenManager()
appManager = AppManager()


class HomeScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
        self.entry = Entry()

    def createEntry(self):
        newEntry = Entry()
        self.entry = newEntry
        appManager.getApp().getNewAccountScreen().updateEntry(newEntry)
        appManager.getApp().getGeneratePasswordScreen().updateEntry(newEntry)

    def getEntry(self):
        return self.entry

    def resetNewAccountScreen(self):
        newAccountScreen = appManager.getApp().getNewAccountScreen()
        specificationsScreen = appManager.getApp().getSpecificationsScreen()

        newAccountScreen.ids.accountEntry.text = self.entry.getAccount()
        newAccountScreen.ids.loginEntry.text = self.entry.getLogin()

        specificationsScreen.ids.lengthEntry.text = ""
        specificationsScreen.ids.specialsEntry.text = ""
        specificationsScreen.ids.numbersEntry.text = ""
        specificationsScreen.ids.capitalsEntry.text = ""

    def resetGeneratePasswordScreen(self):
        generatePasswordScreen = appManager.getApp().getGeneratePasswordScreen()

        generatePasswordScreen.ids.accountLabel.text = self.entry.getAccount()
        generatePasswordScreen.ids.loginLabel.text = self.entry.getLogin()
        generatePasswordScreen.ids.passwordLabel.text = self.entry.getPassword()

    @staticmethod
    def setExistingAccountScreen():
        existingAccountScreen = appManager.getApp().getExistingAccountScreen()
        existingAccountScreen.showAllButtonText()

    @staticmethod
    def killApp():
        startTime = time.clock()
        while time.clock()-startTime < 0.25:
            pass
        exit()

    @staticmethod
    def saveData():
        with open("databaseFile", "wb") as databaseFile:
            pickle.dump(appManager.getApp().getDatabase(), databaseFile)


class NewAccountScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(NewAccountScreen, self).__init__(**kw)
        self.entry = appManager.getApp().getHomeScreen().getEntry()
        self.generatePasswordScreen = appManager.getApp().getGeneratePasswordScreen()
        self.passwordGenerator = appManager.getApp().getSpecificationsScreen().getPasswordGenerator()

    def setAccount(self, account):
        self.entry.setAccount(account)

    def setLogin(self, login):
        self.entry.setLogin(login)

    def setPassword(self):
        self.entry.setPassword(self.passwordGenerator.generatePassword())

    def updateEntry(self, entry):
        self.entry = entry

    def setGeneratePasswordScreen(self):
        self.generatePasswordScreen.ids.accountLabel.text = self.entry.getAccount()
        self.generatePasswordScreen.ids.loginLabel.text = self.entry.getLogin()
        self.generatePasswordScreen.ids.passwordLabel.text = self.entry.getPassword()

    @staticmethod
    def setPreviousScreen():
        specsScreen = appManager.getApp().getSpecificationsScreen()
        specsScreen.setPreviousScreen("newAccount")

    def attemptSwitchScreen(self, screen):
        if len(self.ids.accountEntry.text) < 1 or len(self.ids.loginEntry.text) < 1:
            return
        else:
            self.switchScreen(screen)


class ExistingAccountScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(ExistingAccountScreen, self).__init__(**kw)
        self.startingIndex = 0
        self.database = appManager.getApp().getDatabase()
        self.entryDetailsScreen = appManager.getApp().getEntryDetailsScreen()
        self.currentIndex = 0

    def getCurrentIndex(self):
        return self.currentIndex

    def getStartingIndex(self):
        return self.startingIndex

    def getDatabase(self):
        return self.database

    @staticmethod
    def getButtonText(index):
        database = appManager.getApp().getDatabase()
        if database.getSize() > index:
            return database.getButtonText(index)
        else:
            return ""

    def upButton(self):
        if self.startingIndex - 5 >= 0:
            self.startingIndex -= 5
            self.showAllButtonText()
        else:
            self.startingIndex = 0

    def downButton(self):
        database = appManager.getApp().getDatabase()
        if self.startingIndex + 5 < database.getSize():
            self.startingIndex += 5
        else:
            pass

    def showAllButtonText(self):
        self.ids.entry0.text = self.getButtonText(0 + self.startingIndex)
        self.ids.entry1.text = self.getButtonText(1 + self.startingIndex)
        self.ids.entry2.text = self.getButtonText(2 + self.startingIndex)
        self.ids.entry3.text = self.getButtonText(3 + self.startingIndex)
        self.ids.entry4.text = self.getButtonText(4 + self.startingIndex)

    def showEntryDetails(self, index):
        if self.database.getSize() > index + self.startingIndex:
            self.entryDetailsScreen.ids.account.text = self.database.getEntry(index + self.startingIndex).getAccount()
            self.entryDetailsScreen.ids.login.text = self.database.getEntry(index + self.startingIndex).getLogin()
            self.entryDetailsScreen.ids.password.text = self.database.getEntry(index + self.startingIndex).getPassword()
            self.currentIndex = index + self.startingIndex
        else:
            self.entryDetailsScreen.ids.account.text = "Empty"
            self.entryDetailsScreen.ids.login.text = "Empty"
            self.entryDetailsScreen.ids.password.text = "Empty"

    def attemptSwitchScreen(self, screen, index):
        database = appManager.getApp().getDatabase()
        if screen == "entryDetails":
            if database.getSize() <= index + self.startingIndex:
                pass
            else:
                self.switchScreen(screen)
        else:
            self.switchScreen(screen)


class EntryDetailsScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(EntryDetailsScreen, self).__init__(**kw)

    def getEntry(self):
        database = appManager.getApp().getExistingAccountScreen().getDatabase()

        account = self.ids.account.text
        login = self.ids.login.text
        password = self.ids.password.text

        return database.getEntry(database.findEntryIndex(account, login, password))

    def deleteEntry(self):
        database = appManager.getApp().getExistingAccountScreen().getDatabase()

        account = self.ids.account.text
        login = self.ids.login.text
        password = self.ids.password.text

        try:
            database.removeEntry(database.getEntry(database.findEntryIndex(account, login, password)))
        except ValueError:
            pass

    def setEditEntryScreen(self):
        editEntryScreen = appManager.getApp().getEditEntryScreen()

        entry = self.getEntry()

        editEntryScreen.ids.accountEntry.text = entry.getAccount()
        editEntryScreen.ids.loginEntry.text = entry.getLogin()
        editEntryScreen.ids.passwordEntry.text = entry.getPassword()

    @staticmethod
    def setExistingAccountScreen():
        existingAccountScreen = appManager.getApp().getExistingAccountScreen()
        existingAccountScreen.showAllButtonText()

    @staticmethod
    def copyLogin(login):
        pyperclip.copy(login)

    @staticmethod
    def copyPassword(password):
        pyperclip.copy(password)


class SpecificationsScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(SpecificationsScreen, self).__init__(**kw)
        self.passwordGenerator = PasswordGenerator()
        self.previous = "newAccountScreen"

    def setLength(self, length):
        self.passwordGenerator.setLength(length)

    def setCapitals(self, capitals):
        self.passwordGenerator.setCapitals(capitals)

    def setSpecials(self, specials):
        self.passwordGenerator.setSpecials(specials)

    def setNumbers(self, numbers):
        self.passwordGenerator.setNumbers(numbers)

    def getPasswordGenerator(self):
        return self.passwordGenerator

    def setPreviousScreen(self, previous):
        self.previous = previous

    def switchScreenPrevious(self):
        screenManager.current = self.previous


class EditEntryScreen(SwitchingScreen):
    @staticmethod
    def generatePassword():
        passwordGenerator = appManager.getApp().getSpecificationsScreen().getPasswordGenerator()
        return passwordGenerator.generatePassword()

    def updateEntry(self, newAccount, newLogin, newPassword):
        existingAccountScreen = appManager.getApp().getExistingAccountScreen()
        database = appManager.getApp().getExistingAccountScreen().getDatabase()

        account = self.ids.accountEntry.text
        login = self.ids.loginEntry.text
        password = self.ids.passwordEntry.text

        try:
            entry = database.getEntry(existingAccountScreen.getCurrentIndex())
            entry.setAccount(newAccount)
            entry.setLogin(newLogin)
            entry.setPassword(newPassword)
            existingAccountScreen.showEntryDetails(existingAccountScreen.getCurrentIndex() - existingAccountScreen.getStartingIndex())
        except ValueError:
            pass

    def updateEntryDetailsScreen(self):
        database = appManager.getApp().getExistingAccountScreen().getDatabase()

        account = self.ids.accountEntry.text
        login = self.ids.loginEntry.text
        password = self.ids.passwordEntry.text

        existingAccountScreen = appManager.getApp().getExistingAccountScreen()
        existingAccountScreen.showEntryDetails(database.getEntry(database.findEntryIndex(account, login, password) - existingAccountScreen.getStartingIndex()))

    @staticmethod
    def setPreviousScreen():
        specsScreen = appManager.getApp().getSpecificationsScreen()
        specsScreen.setPreviousScreen("editEntry")


class GeneratePasswordScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(GeneratePasswordScreen, self).__init__(**kw)
        self.entry = appManager.getApp().getHomeScreen().getEntry()
        self.database = appManager.getApp().getDatabase()

    def getAccount(self):
        return self.entry.getAccount()

    def getLogin(self):
        return self.entry.getLogin()

    def getPassword(self):
        return self.entry.getPassword()

    def showInfo(self):
        self.ids.accountLabel.text = self.getAccount()
        self.ids.loginLabel.text = self.getLogin()
        self.ids.passwordLabel.text = self.getPassword()

    def resetPage(self):
        self.ids.accountLabel.text = "Account"
        self.ids.loginLabel.text = "Login"
        self.ids.passwordLabel.text = "Password"

    def storeEntry(self):
        self.database.addEntry(self.entry)

    def updateEntry(self, entry):
        self.entry = entry

    @staticmethod
    def copyLogin(login):
        pyperclip.copy(login)

    @staticmethod
    def copyPassword(password):
        pyperclip.copy(password)


class PWManagerApp(App):
    def __init__(self):
        super(PWManagerApp, self).__init__()
        self.existingAccountScreen = None
        self.homeScreen = None
        self.newAccountScreen = None
        self.specificationsScreen = None
        self.generatePasswordScreen = None
        self.entryDetailsScreen = None
        self.editEntryScreen = None
        with open("databaseFile", "rb") as databaseFile:
            self.database = pickle.load(databaseFile)

    def getHomeScreen(self):
        return self.homeScreen

    def getNewAccountScreen(self):
        return self.newAccountScreen

    def getExistingAccountScreen(self):
        return self.existingAccountScreen

    def getSpecificationsScreen(self):
        return self.specificationsScreen

    def getGeneratePasswordScreen(self):
        return self.generatePasswordScreen

    def getEntryDetailsScreen(self):
        return self.entryDetailsScreen

    def getEditEntryScreen(self):
        return self.editEntryScreen

    def getDatabase(self):
        return self.database

    def build(self):
        self.homeScreen = HomeScreen(name="home")
        self.specificationsScreen = SpecificationsScreen(name="specifications")
        self.generatePasswordScreen = GeneratePasswordScreen(name="generatePassword")
        self.newAccountScreen = NewAccountScreen(name="newAccount")
        self.entryDetailsScreen = EntryDetailsScreen(name="entryDetails")
        self.existingAccountScreen = ExistingAccountScreen(name="existingAccount")
        self.editEntryScreen = EditEntryScreen(name="editEntry")

        screenManager.add_widget(self.homeScreen)
        screenManager.add_widget(self.newAccountScreen)
        screenManager.add_widget(self.existingAccountScreen)
        screenManager.add_widget(self.specificationsScreen)
        screenManager.add_widget(self.generatePasswordScreen)
        screenManager.add_widget(self.entryDetailsScreen)
        screenManager.add_widget(self.editEntryScreen)
        return screenManager


def main():
    pwManagerApp = PWManagerApp()
    appManager.setApp(pwManagerApp)
    pwManagerApp.run()

    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


if __name__ == "__main__":
    main()
