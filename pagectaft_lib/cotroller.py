from tkinter import END, ACTIVE
import model

# Referencja do widoku głównego (zostanie ustawiona przez main.py)
view = None

def init_controller(main_view):
    global view
    view = main_view

def update_map():
    """Dynamicznie odświeża markery na mapie w zależności od stanu aplikacji."""
    view.map_widget.delete_all_marker()

    if model.current_company_idx is None:
        for c in model.company_list:
            c.marker = view.map_widget.set_marker(c.coordinates[0], c.coordinates[1], text=c.nazwa)
    else:
        c = model.company_list[model.current_company_idx]
        c.marker = view.map_widget.set_marker(c.coordinates[0], c.coordinates[1], text=c.nazwa)
        for b in c.bookstores:
            b.marker = view.map_widget.set_marker(b.coordinates[0], b.coordinates[1], text=b.nazwa)
        for e in c.employees:
            e.marker = view.map_widget.set_marker(e.coordinates[0], e.coordinates[1], text=f"{e.imie} {e.nazwisko}")


def refresh_all_lists():
    show_bookstore()
    show_employee()
    show_client()


def show_company() -> None:
    view.listbox_lista_obiektow.delete(0, END)
    for idx, comp in enumerate(model.company_list):
        view.listbox_lista_obiektow.insert(idx, comp.nazwa)


def show_all_companies():
    model.current_company_idx = None

    view.label_firma_szczegoly_obiektu_wartosc.config(text="...")
    view.label_nip_szczegoly_obiektu_wartosc.config(text="...")
    view.label_lokalizacja_szczegoly_obiektu_wartosc.config(text="...")

    view.listbox_ksiegarnie.delete(0, END)
    view.listbox_pracownicy.delete(0, END)
    view.listbox_klienci.delete(0, END)

    update_map()
    view.map_widget.set_position(52.2, 21.0)
    view.map_widget.set_zoom(6)


def remove_company() -> None:
    if not view.listbox_lista_obiektow.get(ACTIVE): return
    i = view.listbox_lista_obiektow.index(ACTIVE)

    model.company_list.pop(i)

    if model.current_company_idx == i:
        show_all_companies()
    else:
        if model.current_company_idx is not None and model.current_company_idx > i:
            model.current_company_idx -= 1
        show_company()
        update_map()


def show_company_details():
    if not view.listbox_lista_obiektow.get(ACTIVE): return
    i = view.listbox_lista_obiektow.index(ACTIVE)
    model.current_company_idx = i

    view.label_firma_szczegoly_obiektu_wartosc.config(text=model.company_list[i].nazwa)
    view.label_nip_szczegoly_obiektu_wartosc.config(text=model.company_list[i].nip)
    view.label_lokalizacja_szczegoly_obiektu_wartosc.config(text=model.company_list[i].lokalizacja)

    update_map()
    view.map_widget.set_position(model.company_list[i].coordinates[0], model.company_list[i].coordinates[1])
    view.map_widget.set_zoom(9)

    refresh_all_lists()


def edit_company():
    if not view.listbox_lista_obiektow.get(ACTIVE): return
    i = view.listbox_lista_obiektow.index(ACTIVE)

    view.entry_nazwa.delete(0, END)
    view.entry_nip.delete(0, END)
    view.entry_lokalizacja.delete(0, END)

    view.entry_nazwa.insert(0, model.company_list[i].nazwa)
    view.entry_nip.insert(0, str(model.company_list[i].nip))
    view.entry_lokalizacja.insert(0, model.company_list[i].lokalizacja)

    view.button_dodaj_firme.config(text="Zapisz zmiany", command=lambda: update_company(i))


def update_company(i):
    model.company_list[i].nazwa = view.entry_nazwa.get()
    model.company_list[i].nip = int(view.entry_nip.get())
    model.company_list[i].lokalizacja = view.entry_lokalizacja.get()
    model.company_list[i].coordinates = model.company_list[i].get_coordinates()

    view.button_dodaj_firme.config(text="Dodaj firmę", command=add_company)
    view.entry_nazwa.delete(0, END)
    view.entry_nip.delete(0, END)
    view.entry_lokalizacja.delete(0, END)

    show_company()
    update_map()


def add_company():
    nazwa = view.entry_nazwa.get()
    nip = view.entry_nip.get()
    lokalizacja = view.entry_lokalizacja.get()
    new_company = model.Company(nazwa=nazwa, nip=int(nip), lokalizacja=lokalizacja)
    model.company_list.append(new_company)

    view.entry_nazwa.delete(0, END)
    view.entry_nip.delete(0, END)
    view.entry_lokalizacja.delete(0, END)

    show_company()
    update_map()


# --- KSIĘGARNIE ---
def show_bookstore():
    view.listbox_ksiegarnie.delete(0, END)
    if view.listbox_lista_obiektow.get(ACTIVE):
        i_firmy = view.listbox_lista_obiektow.index(ACTIVE)
        for idx, k in enumerate(model.company_list[i_firmy].bookstores):
            view.listbox_ksiegarnie.insert(idx, k.nazwa)


def add_bookstore():
    if view.listbox_lista_obiektow.get(ACTIVE):
        i_firmy = view.listbox_lista_obiektow.index(ACTIVE)
        model.company_list[i_firmy].bookstores.append(model.Bookstore(view.entry_nazwa_k.get(), view.entry_lokalizacja_k.get()))
        view.entry_nazwa_k.delete(0, END)
        view.entry_lokalizacja_k.delete(0, END)
        show_bookstore()
        update_map()


def remove_bookstore():
    if view.listbox_lista_obiektow.get(ACTIVE) and view.listbox_ksiegarnie.get(ACTIVE):
        i_f = view.listbox_lista_obiektow.index(ACTIVE)
        i_k = view.listbox_ksiegarnie.index(ACTIVE)
        model.company_list[i_f].bookstores.pop(i_k)
        show_bookstore()
        update_map()


def edit_bookstore():
    if view.listbox_lista_obiektow.get(ACTIVE) and view.listbox_ksiegarnie.get(ACTIVE):
        i_f = view.listbox_lista_obiektow.index(ACTIVE)
        i_k = view.listbox_ksiegarnie.index(ACTIVE)

        view.entry_nazwa_k.delete(0, END)
        view.entry_lokalizacja_k.delete(0, END)

        view.entry_nazwa_k.insert(0, model.company_list[i_f].bookstores[i_k].nazwa)
        view.entry_lokalizacja_k.insert(0, model.company_list[i_f].bookstores[i_k].lokalizacja)

        view.button_dodaj_ksiegarnie.config(text="Zapisz zmiany", command=lambda: update_bookstore(i_f, i_k))


def update_bookstore(i_f, i_k):
    model.company_list[i_f].bookstores[i_k].nazwa = view.entry_nazwa_k.get()
    model.company_list[i_f].bookstores[i_k].lokalizacja = view.entry_lokalizacja_k.get()
    model.company_list[i_f].bookstores[i_k].coordinates = model.company_list[i_f].bookstores[i_k].get_coordinates()

    view.button_dodaj_ksiegarnie.config(text="Dodaj", command=add_bookstore)
    view.entry_nazwa_k.delete(0, END)
    view.entry_lokalizacja_k.delete(0, END)
    show_bookstore()
    update_map()


def show_bookstore_location():
    if view.listbox_lista_obiektow.get(ACTIVE) and view.listbox_ksiegarnie.get(ACTIVE):
        i_f = view.listbox_lista_obiektow.index(ACTIVE)
        i_k = view.listbox_ksiegarnie.index(ACTIVE)
        ksiegarnia = model.company_list[i_f].bookstores[i_k]

        view.map_widget.set_position(ksiegarnia.coordinates[0], ksiegarnia.coordinates[1])
        view.map_widget.set_zoom(12)


# --- PRACOWNICY ---
def show_employee():
    view.listbox_pracownicy.delete(0, END)
    if view.listbox_lista_obiektow.get(ACTIVE):
        i_firmy = view.listbox_lista_obiektow.index(ACTIVE)
        for idx, p in enumerate(model.company_list[i_firmy].employees):
            view.listbox_pracownicy.insert(idx, f"{p.imie} {p.nazwisko}")


def add_employee():
    if view.listbox_lista_obiektow.get(ACTIVE):
        i_firmy = view.listbox_lista_obiektow.index(ACTIVE)
        model.company_list[i_firmy].employees.append(
            model.Employee(view.entry_imie_p.get(), view.entry_nazwisko_p.get(), view.entry_lokalizacja_p.get()))
        view.entry_imie_p.delete(0, END)
        view.entry_nazwisko_p.delete(0, END)
        view.entry_lokalizacja_p.delete(0, END)
        show_employee()
        update_map()


def remove_employee():
    if view.listbox_lista_obiektow.get(ACTIVE) and view.listbox_pracownicy.get(ACTIVE):
        i_f = view.listbox_lista_obiektow.index(ACTIVE)
        i_p = view.listbox_pracownicy.index(ACTIVE)
        model.company_list[i_f].employees.pop(i_p)
        show_employee()
        update_map()


def edit_employee():
    if view.listbox_lista_obiektow.get(ACTIVE) and view.listbox_pracownicy.get(ACTIVE):
        i_f = view.listbox_lista_obiektow.index(ACTIVE)
        i_p = view.listbox_pracownicy.index(ACTIVE)

        view.entry_imie_p.delete(0, END)
        view.entry_nazwisko_p.delete(0, END)
        view.entry_lokalizacja_p.delete(0, END)

        view.entry_imie_p.insert(0, model.company_list[i_f].employees[i_p].imie)
        view.entry_nazwisko_p.insert(0, model.company_list[i_f].employees[i_p].nazwisko)
        view.entry_lokalizacja_p.insert(0, model.company_list[i_f].employees[i_p].lokalizacja)

        view.button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: update_employee(i_f, i_p))


def update_employee(i_f, i_p):
    model.company_list[i_f].employees[i_p].imie = view.entry_imie_p.get()
    model.company_list[i_f].employees[i_p].nazwisko = view.entry_nazwisko_p.get()
    model.company_list[i_f].employees[i_p].lokalizacja = view.entry_lokalizacja_p.get()
    model.company_list[i_f].employees[i_p].coordinates = model.company_list[i_f].employees[i_p].get_coordinates()

    view.button_dodaj_pracownika.config(text="Dodaj", command=add_employee)
    view.entry_imie_p.delete(0, END)
    view.entry_nazwisko_p.delete(0, END)
    view.entry_lokalizacja_p.delete(0, END)
    show_employee()
    update_map()


def show_employee_location():
    if view.listbox_lista_obiektow.get(ACTIVE) and view.listbox_pracownicy.get(ACTIVE):
        i_f = view.listbox_lista_obiektow.index(ACTIVE)
        i_p = view.listbox_pracownicy.index(ACTIVE)
        pracownik = model.company_list[i_f].employees[i_p]

        view.map_widget.set_position(pracownik.coordinates[0], pracownik.coordinates[1])
        view.map_widget.set_zoom(12)


# --- KLIENCI ---
def show_client():
    view.listbox_klienci.delete(0, END)
    if view.listbox_lista_obiektow.get(ACTIVE):
        i_firmy = view.listbox_lista_obiektow.index(ACTIVE)
        for idx, c in enumerate(model.company_list[i_firmy].clients):
            view.listbox_klienci.insert(idx, f"{c.imie} {c.nazwisko}")


def add_client():
    if view.listbox_lista_obiektow.get(ACTIVE):
        i_firmy = view.listbox_lista_obiektow.index(ACTIVE)
        model.company_list[i_firmy].clients.append(model.Client(view.entry_imie_c.get(), view.entry_nazwisko_c.get()))
        view.entry_imie_c.delete(0, END)
        view.entry_nazwisko_c.delete(0, END)
        show_client()


def remove_client():
    if view.listbox_lista_obiektow.get(ACTIVE) and view.listbox_klienci.get(ACTIVE):
        i_f = view.listbox_lista_obiektow.index(ACTIVE)
        i_c = view.listbox_klienci.index(ACTIVE)
        model.company_list[i_f].clients.pop(i_c)
        show_client()


def edit_client():
    if view.listbox_lista_obiektow.get(ACTIVE) and view.listbox_klienci.get(ACTIVE):
        i_f = view.listbox_lista_obiektow.index(ACTIVE)
        i_c = view.listbox_klienci.index(ACTIVE)

        view.entry_imie_c.delete(0, END)
        view.entry_nazwisko_c.delete(0, END)

        view.entry_imie_c.insert(0, model.company_list[i_f].clients[i_c].imie)
        view.entry_nazwisko_c.insert(0, model.company_list[i_f].clients[i_c].nazwisko)

        view.button_dodaj_klienta.config(text="Zapisz zmiany", command=lambda: update_client(i_f, i_c))


def update_client(i_f, i_c):
    model.company_list[i_f].clients[i_c].imie = view.entry_imie_c.get()
    model.company_list[i_f].clients[i_c].nazwisko = view.entry_nazwisko_c.get()

    view.button_dodaj_klienta.config(text="Dodaj", command=add_client)
    view.entry_imie_c.delete(0, END)
    view.entry_nazwisko_c.delete(0, END)
    show_client()