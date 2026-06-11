from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.osoby import Osoba
    from models.towar import Towar

from models.osoby import Klient
from models.magazyn import Magazyn
from models.repozytorium import Repozytorium


class System:
    """Fasada systemu — zarządza użytkownikami, sesją i referencjami do zasobów."""

    def __init__(self) -> None:
        self.repozytorium: Repozytorium = Repozytorium()
        self.uzytkownicy: List[Osoba] = self.repozytorium.wczytaj_uzytkownikow()
        self.zalogowany_uzytkownik: Optional[Osoba] = None
        self.towary: List[Towar] = []
        self.magazyn: Optional[Magazyn] = None

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
