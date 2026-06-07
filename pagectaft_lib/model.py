import requests
from bs4 import BeautifulSoup

# Globalna lista przechowująca zarejestrowane firmy
company_list: list = []
current_company_idx = None  # Indeks wybranej firmy (None = widok ogólny)

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
        # Zmienione na bezpieczniejszy indeks [0]
        latitude = float(response_html.select(".latitude")[0].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[0].text.replace(",", "."))
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
        # Zmienione na bezpieczniejszy indeks [0]
        latitude = float(response_html.select(".latitude")[0].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[0].text.replace(",", "."))
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
        # Zmienione na bezpieczniejszy indeks [0]
        latitude = float(response_html.select(".latitude")[0].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[0].text.replace(",", "."))
        return [latitude, longitude]