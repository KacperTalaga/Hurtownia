from __future__ import annotations
from typing import Dict, List, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from models.osoby import Osoba, Pracownik
    from models.towar import Towar
    from models.zamowienia import Zamowienie
    from models.faktury import Faktura

from models.osoby import Klient, Kierownik, Magazynier, Obsluga
from models.magazyn import Magazyn
from models.dane_startowe import DaneStartowe

# Typy pracowników, których kierownik może rejestrować (nazwa -> klasa)
TYPY_PRACOWNIKOW: Dict[str, Type[Pracownik]] = {
    "Magazynier": Magazynier,
    "Obsluga": Obsluga,
}
# Dane kont startowych, zasiewanych przy każdym uruchomieniu (brak persystencji)
LOGIN_KIEROWNIKA: str = "kierownik"
HASLO_KIEROWNIKA: str = "kierownik"
LOGIN_KLIENTA: str = "klient"
HASLO_KLIENTA: str = "klient"
LOGIN_OBSLUGI: str = "obsluga"
HASLO_OBSLUGI: str = "obsluga"
LOGIN_MAGAZYNIERA: str = "magazynier"
HASLO_MAGAZYNIERA: str = "magazynier"


class System:
    """Fasada systemu — zarządza użytkownikami, sesją i referencjami do zasobów."""

    def __init__(self) -> None:
        self.uzytkownicy: List[Osoba] = []
        self.zalogowany_uzytkownik: Optional[Osoba] = None

        self.magazyn: Optional[Magazyn] = DaneStartowe.utworz_magazyn_startowy()

        if self.magazyn is not None:
            self.towary: List[Towar] = [pozycja.towar for pozycja in self.magazyn.pozycje]
        else:
            self.towary = []

        self.zamowienia: List[Zamowienie] = DaneStartowe.utworz_zamowienia_startowe()
        self.faktury: List[Faktura] = []

        # Konta startowe — zasiewane przy każdym uruchomieniu (brak persystencji)
        self._dodaj_uzytkownika(Kierownik("Anna", "Kowalska", LOGIN_KIEROWNIKA, HASLO_KIEROWNIKA))
        self._dodaj_uzytkownika(Klient("Jan", "Nowak", LOGIN_KLIENTA, HASLO_KLIENTA, "ul. Budowlana 1, Kraków"))
        self._dodaj_uzytkownika(Obsluga("Piotr", "Wiśniewski", LOGIN_OBSLUGI, HASLO_OBSLUGI))
        self._dodaj_uzytkownika(Magazynier("Tomasz", "Lewandowski", LOGIN_MAGAZYNIERA, HASLO_MAGAZYNIERA))

    def rejestracja_klienta(self, imie: str, nazwisko: str, login: str, haslo: str, adres: str) -> bool:
        """Tworzy i rejestruje nowego klienta.

        Zwraca False jeśli podany login jest już zajęty, True po pomyślnej rejestracji.
        """
        if self.login_istnieje(login):
            return False
        nowy = Klient(imie, nazwisko, login, haslo, adres)
        self._dodaj_uzytkownika(nowy)
        return True

    def rejestracja_pracownika(self, typ: str, imie: str, nazwisko: str, login: str, haslo: str) -> bool:
        """Tworzy i rejestruje nowego pracownika wskazanego typu.

        Obsługiwane typy: 'Magazynier', 'Obsluga'. Zwraca False, gdy typ jest
        nieobsługiwany lub login jest już zajęty; True po pomyślnej rejestracji.
        """
        klasa = TYPY_PRACOWNIKOW.get(typ)
        if klasa is None:
            return False
        if self.login_istnieje(login):
            return False
        nowy = klasa(imie, nazwisko, login, haslo)
        self._dodaj_uzytkownika(nowy)
        return True

    def _dodaj_uzytkownika(self, osoba: Osoba) -> None:
        """Dodaje osobę do listy użytkowników systemu."""
        self.uzytkownicy.append(osoba)

    def logowanie(self, login: str, haslo: str) -> bool:
        """Uwierzytelnia użytkownika i ustawia aktywną sesję.

        Zwraca True po pomyślnym zalogowaniu, False przy błędnych danych.
        """
        for uzytkownik in self.uzytkownicy:
            if uzytkownik.login == login and uzytkownik.sprawdz_haslo(haslo):
                self.zalogowany_uzytkownik = uzytkownik
                return True
        return False

    def wylogowanie(self) -> None:
        """Kończy bieżącą sesję użytkownika."""
        self.zalogowany_uzytkownik = None

    def login_istnieje(self, login: str) -> bool:
        """Sprawdza, czy login jest już zajęty przez innego użytkownika."""
        return any(u.login == login for u in self.uzytkownicy)
