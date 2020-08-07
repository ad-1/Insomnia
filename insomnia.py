from random import randrange
from sys import exit, argv
from time import sleep
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from pynput.keyboard import Key, Controller
from datetime import date
import threading


def print_caffeine():
    with open('res/insomnia.txt', 'r') as f:
        print(f.read())


def insomnia():
    print('running insomnia on background thread...')
    print('Creating keyboard controller...\n')
    keyboard = Controller()

    while True:
        print(f"{date.today()}: doing some hard work...")
        keyboard.press(Key.f15)
        keyboard.release(Key.f15)
        sleep(randrange(120))


def main():
    print_caffeine()
    print('Starting app main method...')
    app = QApplication(argv)

    print('Setting up system tray icon...')
    icon = QIcon('res/insomnia-96.png')
    tray_icon = QSystemTrayIcon(icon, parent=app)
    tray_icon.setToolTip('Insomnia')
    tray_icon.show()

    print('Adding menu option to exit...')
    menu = QMenu()

    exit_act = QAction(QIcon('exit.png'), '&Exit', None)
    # noinspection PyUnresolvedReferences
    exit_act.triggered.connect()
    # exit_act.setShortcut('Ctrl+Q')

    menu.addAction(exit_act)
    tray_icon.setContextMenu(menu)

    t1 = threading.Thread(target=insomnia)
    t1.start()

    exit(app.exec_())


def close_app(app, t1):
    app.quit()


# Program driver
if __name__ == '__main__':
    main()
