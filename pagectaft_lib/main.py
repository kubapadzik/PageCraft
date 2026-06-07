from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

company: list = []
current_company_idx = None



class Client:
    def __init__(self, imie: str, nazwisko: str):
        self.imie = imie
        self.nazwisko = nazwisko


class Employee:
    def __init__(self, imie: str, nazwisko: str, lokalizacja: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.lokalizacja = lokalizacja
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]


class Bookstore:
    def __init__(self, nazwa: str, lokalizacja: str):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]


class Company:
    def __init__(self, nazwa: str, nip: int, lokalizacja: str):
        self.nazwa = nazwa
        self.nip = nip
        self.lokalizacja = lokalizacja
        self.coordinates = self.get_coordinates()
        self.marker = None

        self.bookstores: list = []
        self.employees: list = []
        self.clients: list = []

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]

def update_map():
    map_widget.delete_all_marker()

    if current_company_idx is None:
        for c in company:
            c.marker = map_widget.set_marker(c.coordinates[0], c.coordinates[1], text=c.nazwa)

    else:
        c = company[current_company_idx]
        c.marker = map_widget.set_marker(c.coordinates[0], c.coordinates[1], text=c.nazwa)
        for b in c.bookstores:
            b.marker = map_widget.set_marker(b.coordinates[0], b.coordinates[1], text=b.nazwa)
        for e in c.employees:
            e.marker = map_widget.set_marker(e.coordinates[0], e.coordinates[1], text=f"{e.imie} {e.nazwisko}")




def refresh_all_lists():
    show_bookstore()
    show_employee()
    show_client()


def show_company() -> None:
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(company):
        listbox_lista_obiektow.insert(idx, user.nazwa)


def show_all_companies():
    global current_company_idx
    current_company_idx = None

    label_firma_szczegoly_obiektu_wartosc.config(text="...")
    label_nip_szczegoly_obiektu_wartosc.config(text="...")
    label_lokalizacja_szczegoly_obiektu_wartosc.config(text="...")

    listbox_ksiegarnie.delete(0, END)
    listbox_pracownicy.delete(0, END)
    listbox_klienci.delete(0, END)

    update_map()
    map_widget.set_position(52.2, 21.0)
    map_widget.set_zoom(6)


def remove_company() -> None:
    global current_company_idx
    if not listbox_lista_obiektow.get(ACTIVE): return
    i = listbox_lista_obiektow.index(ACTIVE)
    company.pop(i)

    if current_company_idx == i:
        show_all_companies()
    else:
        if current_company_idx is not None and current_company_idx > i:
            current_company_idx -= 1
        show_company()
        update_map()


def show_company_details():
    global current_company_idx
    if not listbox_lista_obiektow.get(ACTIVE): return
    i = listbox_lista_obiektow.index(ACTIVE)
    current_company_idx = i

    label_firma_szczegoly_obiektu_wartosc.config(text=company[i].nazwa)
    label_nip_szczegoly_obiektu_wartosc.config(text=company[i].nip)
    label_lokalizacja_szczegoly_obiektu_wartosc.config(text=company[i].lokalizacja)

    update_map()
    map_widget.set_position(company[i].coordinates[0], company[i].coordinates[1])
    map_widget.set_zoom(9)

    refresh_all_lists()


def edit_company():
    if not listbox_lista_obiektow.get(ACTIVE): return
    i = listbox_lista_obiektow.index(ACTIVE)

    entry_nazwa.delete(0, END)
    entry_nip.delete(0, END)
    entry_lokalizacja.delete(0, END)

    entry_nazwa.insert(0, company[i].nazwa)
    entry_nip.insert(0, company[i].nip)
    entry_lokalizacja.insert(0, company[i].lokalizacja)

    button_dodaj_firme.config(text="Zapisz zmiany", command=lambda: update_company(i))


def update_company(i):
    company[i].nazwa = entry_nazwa.get()
    company[i].nip = entry_nip.get()
    company[i].lokalizacja = entry_lokalizacja.get()
    company[i].coordinates = company[i].get_coordinates()

    button_dodaj_firme.config(text="Dodaj firmę", command=add_company)
    entry_nazwa.delete(0, END)
    entry_nip.delete(0, END)
    entry_lokalizacja.delete(0, END)
    show_company()
    update_map()


def add_company():
    nazwa = entry_nazwa.get()
    nip = entry_nip.get()
    lokalizacja = entry_lokalizacja.get()
    new_company = Company(nazwa=nazwa, nip=int(nip), lokalizacja=lokalizacja)
    company.append(new_company)

    entry_nazwa.delete(0, END)
    entry_nip.delete(0, END)
    entry_lokalizacja.delete(0, END)

    show_company()
    update_map()


# FUNKCJE - KSIĘGARNIE

def show_bookstore():
    listbox_ksiegarnie.delete(0, END)
    if listbox_lista_obiektow.get(ACTIVE):
        i_firmy = listbox_lista_obiektow.index(ACTIVE)
        for idx, k in enumerate(company[i_firmy].bookstores):
            listbox_ksiegarnie.insert(idx, k.nazwa)


def add_bookstore():
    if listbox_lista_obiektow.get(ACTIVE):
        i_firmy = listbox_lista_obiektow.index(ACTIVE)
        company[i_firmy].bookstores.append(Bookstore(entry_nazwa_k.get(), entry_lokalizacja_k.get()))
        entry_nazwa_k.delete(0, END)
        entry_lokalizacja_k.delete(0, END)
        show_bookstore()
        update_map()


def remove_bookstore():
    if listbox_lista_obiektow.get(ACTIVE) and listbox_ksiegarnie.get(ACTIVE):
        i_f = listbox_lista_obiektow.index(ACTIVE)
        i_k = listbox_ksiegarnie.index(ACTIVE)
        company[i_f].bookstores.pop(i_k)
        show_bookstore()
        update_map()


def edit_bookstore():
    if listbox_lista_obiektow.get(ACTIVE) and listbox_ksiegarnie.get(ACTIVE):
        i_f = listbox_lista_obiektow.index(ACTIVE)
        i_k = listbox_ksiegarnie.index(ACTIVE)

        entry_nazwa_k.delete(0, END)
        entry_lokalizacja_k.delete(0, END)

        entry_nazwa_k.insert(0, company[i_f].bookstores[i_k].nazwa)
        entry_lokalizacja_k.insert(0, company[i_f].bookstores[i_k].lokalizacja)

        button_dodaj_ksiegarnie.config(text="Zapisz zmiany", command=lambda: update_bookstore(i_f, i_k))


def update_bookstore(i_f, i_k):
    company[i_f].bookstores[i_k].nazwa = entry_nazwa_k.get()
    company[i_f].bookstores[i_k].lokalizacja = entry_lokalizacja_k.get()
    company[i_f].bookstores[i_k].coordinates = company[i_f].bookstores[i_k].get_coordinates()

    button_dodaj_ksiegarnie.config(text="Dodaj", command=add_bookstore)
    entry_nazwa_k.delete(0, END)
    entry_lokalizacja_k.delete(0, END)
    show_bookstore()
    update_map()


def show_bookstore_location():
    if listbox_lista_obiektow.get(ACTIVE) and listbox_ksiegarnie.get(ACTIVE):
        i_f = listbox_lista_obiektow.index(ACTIVE)
        i_k = listbox_ksiegarnie.index(ACTIVE)
        ksiegarnia = company[i_f].bookstores[i_k]

        map_widget.set_position(ksiegarnia.coordinates[0], ksiegarnia.coordinates[1])
        map_widget.set_zoom(12)



# FUNKCJE - PRACOWNICY

def show_employee():
    listbox_pracownicy.delete(0, END)
    if listbox_lista_obiektow.get(ACTIVE):
        i_firmy = listbox_lista_obiektow.index(ACTIVE)
        for idx, p in enumerate(company[i_firmy].employees):
            listbox_pracownicy.insert(idx, f"{p.imie} {p.nazwisko}")


def add_employee():
    if listbox_lista_obiektow.get(ACTIVE):
        i_firmy = listbox_lista_obiektow.index(ACTIVE)
        company[i_firmy].employees.append(
            Employee(entry_imie_p.get(), entry_nazwisko_p.get(), entry_lokalizacja_p.get()))
        entry_imie_p.delete(0, END)
        entry_nazwisko_p.delete(0, END)
        entry_lokalizacja_p.delete(0, END)
        show_employee()
        update_map()


def remove_employee():
    if listbox_lista_obiektow.get(ACTIVE) and listbox_pracownicy.get(ACTIVE):
        i_f = listbox_lista_obiektow.index(ACTIVE)
        i_p = listbox_pracownicy.index(ACTIVE)
        company[i_f].employees.pop(i_p)
        show_employee()
        update_map()


def edit_employee():
    if listbox_lista_obiektow.get(ACTIVE) and listbox_pracownicy.get(ACTIVE):
        i_f = listbox_lista_obiektow.index(ACTIVE)
        i_p = listbox_pracownicy.index(ACTIVE)

        entry_imie_p.delete(0, END)
        entry_nazwisko_p.delete(0, END)
        entry_lokalizacja_p.delete(0, END)

        entry_imie_p.insert(0, company[i_f].employees[i_p].imie)
        entry_nazwisko_p.insert(0, company[i_f].employees[i_p].nazwisko)
        entry_lokalizacja_p.insert(0, company[i_f].employees[i_p].lokalizacja)

        button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: update_employee(i_f, i_p))


def update_employee(i_f, i_p):
    company[i_f].employees[i_p].imie = entry_imie_p.get()
    company[i_f].employees[i_p].nazwisko = entry_nazwisko_p.get()
    company[i_f].employees[i_p].lokalizacja = entry_lokalizacja_p.get()
    company[i_f].employees[i_p].coordinates = company[i_f].employees[i_p].get_coordinates()

    button_dodaj_pracownika.config(text="Dodaj", command=add_employee)
    entry_imie_p.delete(0, END)
    entry_nazwisko_p.delete(0, END)
    entry_lokalizacja_p.delete(0, END)
    show_employee()
    update_map()


def show_employee_location():
    if listbox_lista_obiektow.get(ACTIVE) and listbox_pracownicy.get(ACTIVE):
        i_f = listbox_lista_obiektow.index(ACTIVE)
        i_p = listbox_pracownicy.index(ACTIVE)
        pracownik = company[i_f].employees[i_p]

        map_widget.set_position(pracownik.coordinates[0], pracownik.coordinates[1])
        map_widget.set_zoom(12)



# FUNKCJE - KLIENCI

def show_client():
    listbox_klienci.delete(0, END)
    if listbox_lista_obiektow.get(ACTIVE):
        i_firmy = listbox_lista_obiektow.index(ACTIVE)
        for idx, c in enumerate(company[i_firmy].clients):
            listbox_klienci.insert(idx, f"{c.imie} {c.nazwisko}")


def add_client():
    if listbox_lista_obiektow.get(ACTIVE):
        i_firmy = listbox_lista_obiektow.index(ACTIVE)
        company[i_firmy].clients.append(Client(entry_imie_c.get(), entry_nazwisko_c.get()))
        entry_imie_c.delete(0, END)
        entry_nazwisko_c.delete(0, END)
        show_client()


def remove_client():
    if listbox_lista_obiektow.get(ACTIVE) and listbox_klienci.get(ACTIVE):
        i_f = listbox_lista_obiektow.index(ACTIVE)
        i_c = listbox_klienci.index(ACTIVE)
        company[i_f].clients.pop(i_c)
        show_client()


def edit_client():
    if listbox_lista_obiektow.get(ACTIVE) and listbox_klienci.get(ACTIVE):
        i_f = listbox_lista_obiektow.index(ACTIVE)
        i_c = listbox_klienci.index(ACTIVE)

        entry_imie_c.delete(0, END)
        entry_nazwisko_c.delete(0, END)

        entry_imie_c.insert(0, company[i_f].clients[i_c].imie)
        entry_nazwisko_c.insert(0, company[i_f].clients[i_c].nazwisko)

        button_dodaj_klienta.config(text="Zapisz zmiany", command=lambda: update_client(i_f, i_c))


def update_client(i_f, i_c):
    company[i_f].clients[i_c].imie = entry_imie_c.get()
    company[i_f].clients[i_c].nazwisko = entry_nazwisko_c.get()

    button_dodaj_klienta.config(text="Dodaj", command=add_client)
    entry_imie_c.delete(0, END)
    entry_nazwisko_c.delete(0, END)
    show_client()



# WIDOK (TKINTER)


root = Tk()
root.title("PageCraft - System Zarządzania Księgarniami")
root.geometry("1200x900")

ramka_mapa = Frame(root)
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1150, height=350, corner_radius=4)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)


print("Pobieram współrzędne z Wikipedii... Proszę czekać.")

c1 = Company("Wydawnictwo Alfa", 1111111111, "Warszawa")
c1.bookstores.append(Bookstore("Alfa Centrum", "Siedlce"))
c1.employees.append(Employee("Jan", "Kowalski", "Radom"))
c1.clients.append(Client("Anna", "Nowak"))
company.append(c1)

c2 = Company("Książki Beta", 2222222222, "Radom")
c2.bookstores.append(Bookstore("Beta Rynek", "Siedlce"))
c2.employees.append(Employee("Piotr", "Zieliński", "Warszawa"))
c2.clients.append(Client("Marek", "Kowalczyk"))
company.append(c2)

c3 = Company("Gamma Czyta", 3333333333, "Szczecin")
c3.bookstores.append(Bookstore("Gamma Stare Miasto", "Sopot"))
c3.employees.append(Employee("Zofia", "Wiśniewska", "Bydgoszcz"))
c3.clients.append(Client("Katarzyna", "Lewandowska"))
company.append(c3)

c4 = Company("Delta Books", 4444444444, "Zabrze")
c4.bookstores.append(Bookstore("Delta Morze", "Kalisz"))
c4.employees.append(Employee("Tomasz", "Wójcik", "Opole"))
c4.clients.append(Client("Michał", "Kamiński"))
company.append(c4)

print("Gotowe! Otwieram aplikację.")

# BUDOWA INTERFEJSU

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektu = Frame(root)

ramka_ksiegarnie = Frame(root)
ramka_pracownicy = Frame(root)
ramka_klienci = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, padx=20, pady=10, sticky=N)
ramka_formularz.grid(row=0, column=1, padx=20, pady=10, sticky=N)
ramka_szczegoly_obiektu.grid(row=0, column=2, padx=20, pady=10, sticky=N)

ramka_ksiegarnie.grid(row=1, column=0, padx=20, pady=10, sticky=N)
ramka_pracownicy.grid(row=1, column=1, padx=20, pady=10, sticky=N)
ramka_klienci.grid(row=1, column=2, padx=20, pady=10, sticky=N)

ramka_mapa.grid(row=2, column=0, columnspan=3, pady=20)
map_widget.grid(row=0, column=0)

# --- 1. GŁÓWNA LISTA FIRM ---
Label(ramka_lista_obiektow, text="Lista firm:").grid(row=0, column=0, columnspan=3, sticky=W)
listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=30)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=show_company_details).grid(row=2, column=0, pady=2)
Button(ramka_lista_obiektow, text="Edytuj", command=edit_company).grid(row=2, column=1, pady=2)
Button(ramka_lista_obiektow, text="Usuń", command=remove_company).grid(row=2, column=2, pady=2)
Button(ramka_lista_obiektow, text="Pokaż wszystkie firmy na mapie", command=show_all_companies).grid(row=3, column=0,
                                                                                                     columnspan=3,
                                                                                                     pady=5,
                                                                                                     sticky=W + E)

# --- 2. FORMULARZ FIRMY ---
Label(ramka_formularz, text="Formularz Firmy:").grid(row=0, column=0, columnspan=2)
Label(ramka_formularz, text="Nazwa:").grid(row=1, column=0, sticky=W)
Label(ramka_formularz, text="NIP:").grid(row=2, column=0, sticky=W)
Label(ramka_formularz, text="Lok.:").grid(row=3, column=0, sticky=W)

entry_nazwa = Entry(ramka_formularz)
entry_nip = Entry(ramka_formularz)
entry_lokalizacja = Entry(ramka_formularz)

entry_nazwa.grid(row=1, column=1)
entry_nip.grid(row=2, column=1)
entry_lokalizacja.grid(row=3, column=1)
button_dodaj_firme = Button(ramka_formularz, text="Dodaj firmę", command=add_company)
button_dodaj_firme.grid(row=4, column=0, columnspan=2, pady=5)

# --- 3. SZCZEGÓŁY FIRMY ---
Label(ramka_szczegoly_obiektu, text="Szczegóły firmy").grid(row=0, column=0, columnspan=2, sticky=W)
Label(ramka_szczegoly_obiektu, text="Nazwa:").grid(row=1, column=0, sticky=W)
label_firma_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_firma_szczegoly_obiektu_wartosc.grid(row=1, column=1, sticky=W)

Label(ramka_szczegoly_obiektu, text="NIP:").grid(row=2, column=0, sticky=W)
label_nip_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_nip_szczegoly_obiektu_wartosc.grid(row=2, column=1, sticky=W)

Label(ramka_szczegoly_obiektu, text="Lok.:").grid(row=3, column=0, sticky=W)
label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=3, column=1, sticky=W)

# --- 4. RAMKA KSIĘGARNIE ---
Label(ramka_ksiegarnie, text="Księgarnie: ").grid(row=0, column=0, columnspan=4, sticky=W)
listbox_ksiegarnie = Listbox(ramka_ksiegarnie, width=28, height=4)
listbox_ksiegarnie.grid(row=1, column=0, columnspan=4)

Label(ramka_ksiegarnie, text="Nazwa: ").grid(row=2, column=0, sticky=E)
entry_nazwa_k = Entry(ramka_ksiegarnie, width=15)
entry_nazwa_k.grid(row=2, column=1, columnspan=3, sticky=W)
Label(ramka_ksiegarnie, text="Lokalizacja: ").grid(row=3, column=0, sticky=E)
entry_lokalizacja_k = Entry(ramka_ksiegarnie, width=15)
entry_lokalizacja_k.grid(row=3, column=1, columnspan=3, sticky=W)

Button(ramka_ksiegarnie, text="Pokaż", command=show_bookstore_location).grid(row=4, column=0, pady=5)
button_dodaj_ksiegarnie = Button(ramka_ksiegarnie, text="Dodaj", command=add_bookstore)
button_dodaj_ksiegarnie.grid(row=4, column=1, pady=5)
Button(ramka_ksiegarnie, text="Edytuj", command=edit_bookstore).grid(row=4, column=2, pady=5)
Button(ramka_ksiegarnie, text="Usuń", command=remove_bookstore).grid(row=4, column=3, pady=5)

# --- 5. RAMKA PRACOWNICY ---
Label(ramka_pracownicy, text="Pracownicy: ").grid(row=0, column=0, columnspan=4, sticky=W)
listbox_pracownicy = Listbox(ramka_pracownicy, width=28, height=4)
listbox_pracownicy.grid(row=1, column=0, columnspan=4)

Label(ramka_pracownicy, text="Imię: ").grid(row=2, column=0, sticky=E)
entry_imie_p = Entry(ramka_pracownicy, width=15)
entry_imie_p.grid(row=2, column=1, columnspan=3, sticky=W)
Label(ramka_pracownicy, text="Nazwisko: ").grid(row=3, column=0, sticky=E)
entry_nazwisko_p = Entry(ramka_pracownicy, width=15)
entry_nazwisko_p.grid(row=3, column=1, columnspan=3, sticky=W)
Label(ramka_pracownicy, text="Lokalizacja: ").grid(row=4, column=0, sticky=E)
entry_lokalizacja_p = Entry(ramka_pracownicy, width=15)
entry_lokalizacja_p.grid(row=4, column=1, columnspan=3, sticky=W)

Button(ramka_pracownicy, text="Pokaż", command=show_employee_location).grid(row=5, column=0, pady=5)
button_dodaj_pracownika = Button(ramka_pracownicy, text="Dodaj", command=add_employee)
button_dodaj_pracownika.grid(row=5, column=1, pady=5)
Button(ramka_pracownicy, text="Edytuj", command=edit_employee).grid(row=5, column=2, pady=5)
Button(ramka_pracownicy, text="Usuń", command=remove_employee).grid(row=5, column=3, pady=5)

# --- 6. RAMKA KLIENCI ---
Label(ramka_klienci, text="Klienci: ").grid(row=0, column=0, columnspan=3, sticky=W)
listbox_klienci = Listbox(ramka_klienci, width=25, height=4)
listbox_klienci.grid(row=1, column=0, columnspan=3)

Label(ramka_klienci, text="Imię:").grid(row=2, column=0, sticky=E)
entry_imie_c = Entry(ramka_klienci, width=15)
entry_imie_c.grid(row=2, column=1, columnspan=2, sticky=W)
Label(ramka_klienci, text="Nazwisko:").grid(row=3, column=0, sticky=E)
entry_nazwisko_c = Entry(ramka_klienci, width=15)
entry_nazwisko_c.grid(row=3, column=1, columnspan=2, sticky=W)

button_dodaj_klienta = Button(ramka_klienci, text="Dodaj", command=add_client)
button_dodaj_klienta.grid(row=4, column=0, pady=5)
Button(ramka_klienci, text="Edytuj", command=edit_client).grid(row=4, column=1, pady=5)
Button(ramka_klienci, text="Usuń", command=remove_client).grid(row=4, column=2, pady=5)

show_company()
update_map()
root.mainloop()