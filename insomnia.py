import sys
from threading import Thread, Event
from datetime import datetime
from random import randrange
from time import sleep
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget
from pynput.keyboard import Key, Controller


def log(msg):
    print(f'{datetime.now()}: {msg}')


class StoppableThread(Thread):

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Insomnia:

    def __init__(self):
        self.running = False
        self.print_caffeine()
        self.keyboard = Controller()

    def start(self):
        if self.running:
            log('Already working!')
            return
        self.running = True
        log('Starting...')
        t1 = StoppableThread(target=self.__do_work)
        t1.start()

    def __do_work(self):
        log('Doing some hard work...')
        while self.running:
            self.keyboard.press(Key.f15)
            self.keyboard.release(Key.f15)
            sleep_time = randrange(60, 180)
            sleep(sleep_time)

    def stop(self):
        self.running = False
        log('Finishing work ...Stopped')

    @staticmethod
    def print_caffeine():
        with open('res/insomnia.txt', 'r') as f:
            print(f.read())


# noinspection PyUnresolvedReferences
class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon: QIcon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('Insomnia')
        self.worker = Insomnia()
        menu = QMenu(parent)
        start_action = menu.addAction('Start')
        start_action.triggered.connect(self.worker.start)
        start_action.setIcon(icon)
        stop_action = menu.addAction('Stop')
        stop_action.triggered.connect(self.worker.stop)
        exit_ = menu.addAction('Exit')
        exit_.triggered.connect(self.__exit_process)
        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.__tray_icon_activated)

    def __tray_icon_activated(self, reason):
        if reason == self.DoubleClick:
            log('double click detected..')
            self.worker.start()

    def __exit_process(self):
        # TODO: Handle exit
        self.worker.stop()
        log('... Process Finished')
        sys.exit()


def main():
    app = QApplication(sys.argv)
    icon = QIcon('res\\insomnia-96.png')
    w = QWidget()
    tray_icon = SystemTrayIcon(icon, w)
    tray_icon.show()
    tray_icon.showMessage('Ready To Work', 'Insomnia')
    sys.exit(app.exec_())


# Program driver
if __name__ == '__main__':
    # sys.stdout = open('res\\log.txt', 'w')
    main()
