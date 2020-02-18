from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition

import time

screenManager = ScreenManager(transition=NoTransition())


class SwitchingScreen(Screen):

    @staticmethod
    def getScreenManager():
        return screenManager

    @staticmethod
    def switchScreen(screen):
        startTime = time.clock()
        while time.clock() - startTime < 0.1:
            pass
        screenManager.current = screen
