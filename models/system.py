from __future__ import annotations
from typing import Dict, List, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from models.osoby import Osoba, Pracownik
    from models.towar import Towar

from models.osoby import Klient, Kierownik, Magazynier, Obsluga
from models.magazyn import Magazyn
from models.repozytorium import Repozytorium
from models.dane_startowe import DaneStartowe

# Typy pracowników, których kierownik może rejestrować (nazwa -> klasa)
TYPY_PRACOWNIKOW: Dict[str, Type[Pracownik]] = {
    "Magazynier": Magazynier,
    "Obsluga": Obsluga,
}
# Dane konta startowego kierownika, zasiewanego przy pierwszym uruchomieniu
LOGIN_KIEROWNIKA: str = "kierownik"
HASLO_KIEROWNIKA: str = "kierownik"


class System:
    """Fasada systemu — zarządza użytkownikami, sesją i referencjami do zasobów."""

    def __init__(self) -> None:
        self.repozytorium: Repozytorium = Repozytorium()
        self.uzytkownicy: List[Osoba] = self.repozytorium.wczytaj_uzytkownikow()
        self.zalogowany_uzytkownik: Optional[Osoba] = None
        self.magazyn: Optional[Magazyn] = DaneStartowe.utworz_magazyn_startowy()
        if self.magazyn is not None:
            self.towary: List[Towar] = [pozycja.towar for pozycja in self.magazyn.pozycje]
        else:
            self.towary = []
        # Konto startowe kierownika — odtwarzane przy starcie, dopóki realny kierownik nie istnieje
        if not any(isinstance(u, Kierownik) for u in self.uzytkownicy):
            self._dodaj_uzytkownika(Kierownik("Anna", "Kowalska", LOGIN_KIEROWNIKA, HASLO_KIEROWNIKA))
        

    def rejestracja_klienta(self, imie: str, nazwisko: str, login: str, haslo: str, adres: str) -> bool:
        """Tworzy i rejestruje nowego klienta.

        Zwraca False jeśli podany login jest już zajęty, True po pomyślnej rejestracji.
        """
        if self.login_istnieje(login):
            return False
        nowy = Klient(imie, nazwisko, login, haslo, adres)
        self._dodaj_uzytkownika(nowy)
        self.repozytorium.zapisz(self)
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
        self.repozytorium.zapisz(self)
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
