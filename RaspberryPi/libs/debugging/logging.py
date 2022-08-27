from colorama import init
from termcolor import colored

init()

def piprint(message, *args):
  print(f"{colored('Rasp PI:', 'red', 'on_white')} {message}", *args)

def arduinoprint(message, *args):
  print(f"{colored('Arduino:', 'blue', 'on_white')} {message}", *args)

