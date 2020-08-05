from time import sleep
from random import randrange
from pynput.keyboard import Key, Controller

keyboard = Controller()

while True:
    keyboard.press(Key.f15)
    keyboard.release(Key.f15)
    sleep(randrange(120))

