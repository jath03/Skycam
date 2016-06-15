from me import *
import time
from tkinter import *
from gpiozero import *
import requests
from pprint import pprint
tk = Tk()
canvas = Canvas(tk, width=500, height=500)
canvas.pack()
class Skycam():
	def __init__(self):
		rep = requests.get('http://192.168.1.150:8091/')
		pprint(rep.text)
		

