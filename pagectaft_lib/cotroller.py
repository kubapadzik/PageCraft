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

    def add_user():
        name = entry_imie.get()
        surname = entry_nazwisko.get()
        posts = entry_liczba_postow.get()
        lokalizacja = entry_lokalizacja.get()

    def show_users() -> None:
        listbox_lista_obiektow.delete(0, END)  # czyszczenie
        for idx, user in enumerate(users):
            listbox_lista_obiektow.insert(idx, user.imie)

    def remove_user() -> None:
        i = listbox_lista_obiektow.index(ACTIVE)
        users[i].marker.delete()
        users.pop(i)
        show_users()

    def show_user_details():
        i = listbox_lista_obiektow.index(ACTIVE)  # edycja kliknietego uzytkownika
        imie = users[i].imie
        nazwisko = users[i].nazwisko
        posty = users[i].posty
        lokalizacja = users[i].lokalizacja

        label_imie_szczegoly_obiektu_wartosc.configure(text=imie)
        label_nazwisko_szczegoly_obiektu_wartosc.configure(text=nazwisko)
        label_liczba_postow_szczegly_obiektu_wartosc.configure(text=posty)
        label_lokalizacja_szczegoly_obiektu_wartosc.configure(text=lokalizacja)
        map_widget.set_position(users[i].coordinates[0], users[i].coordinates[1])
        map_widget.set_zoom(12)

    def edit_user():
        i = listbox_lista_obiektow.index(ACTIVE)
        imie = users[i].imie
        nazwisko = users[i].nazwisko
        posty = users[i].posty
        lokalizacja = users[i].lokalizacja

        entry_imie.insert(0, imie)
        entry_nazwisko.insert(0, nazwisko)
        entry_liczba_postow.insert(0, posty)
        entry_lokalizacja.insert(0, lokalizacja)

        button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=lambda: update_user(i))

    def update_user(i):
        users[i].imie = entry_imie.get()  # get to wyciaganie info
        users[i].nazwisko = entry_nazwisko.get()
        users[i].posty = entry_liczba_postow.get()
        users[i].lokalizacja = entry_lokalizacja.get()
        users[i].coordinates = User.get_coordinates(users[i])
        users[i].marker.delete(0, END)
        users[i].marker = map_widget.set_marker(users[i].coordinates[0], users[i].coordinates[1], text=users[i].imie)

        button_dodaj_uzytkownika.config(text="Dodaj użytkownika", command=add_user)
        show_users()
        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_liczba_postow.delete(0, END)
        entry_lokalizacja.delete(0, END)

    def add_user():
        name = entry_imie.get()
        surname = entry_nazwisko.get()
        posts = entry_liczba_postow.get()
        lokalizacja = entry_lokalizacja.get()

        # print(name, surname, posts, lokalizacja)
        new_user = User(imie=name, nazwisko=surname, posty=int(posts), lokalizacja=lokalizacja)
        users.append(new_user)
        # print(users)
        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_liczba_postow.delete(0, END)
        entry_lokalizacja.delete(0, END)

root = Tk()

root.title("PageCraft")
root.geometry("1024x760")



root.mainloop()