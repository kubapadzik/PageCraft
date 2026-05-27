from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

users:list=[]

class User:
    def __init__(self, imie: str, nazwisko: str, posty: int, lokalizacja: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.posty = posty
        self.lokalizacja = lokalizacja
        self.coordinates = User.get_coordinates(self)

        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie)

root = Tk()

root.title("PageCraft")
root.geometry("1024x760")



root.mainloop()