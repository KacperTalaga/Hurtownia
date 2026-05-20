from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.osoby import Osoba
    from models.towar import Towar

from models.osoby import Klient, Pracownik
from models.magazyn import Magazyn


class System:
    def __init__(self):
        self.uzytkownicy: List[Osoba] = []
        self.zalogowany_uzytkownik: Osoba = None
        self.towary: List[Towar] = []
        self.magazyn: Magazyn = None

    def rejestracja_klienta(self, imie: str, nazwisko: str, login: str, haslo: str, adres: str) -> bool:
        pass

    def logowanie(self, login: str, haslo: str) -> bool:
        pass

    def wylogowanie(self) -> None:
        pass

    def login_istnieje(self, login: str) -> bool:
        pass
