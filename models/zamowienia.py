from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.towar import Towar


class StatusZamowienia(Enum):
    NOWE = "NOWE"
    W_REALIZACJI = "W_REALIZACJI"
    SKOMPLETOWANE = "SKOMPLETOWANE"
    ZREALIZOWANE = "ZREALIZOWANE"
    ANULOWANE = "ANULOWANE"


class PozycjaZamowienia:
    def __init__(self, towar: Towar, ilosc: float, cena_jednostkowa: float, rabat: float):
        self.towar = towar
        self.ilosc = ilosc
        self.cena_jednostkowa = cena_jednostkowa
        self.rabat = rabat

    def wartosc_netto(self) -> float:
        pass

    def wartosc_brutto(self) -> float:
        pass

    def wartosc_z_rabatem(self) -> float:
        pass


class Zamowienie:
    def __init__(self, numer: int, id: int):
        self.numer = numer
        self.id = id
        self.data_zlozenia: datetime = None
        self.data_realizacji: datetime = None
        self.status: StatusZamowienia = StatusZamowienia.NOWE
        self.pozycje: List[PozycjaZamowienia] = []

    def dodaj_pozycje(self, towar: Towar, ilosc: float) -> None:
        pass

    def usun_pozycje(self, index: int) -> None:
        pass

    def wartosc_netto(self) -> float:
        pass

    def wartosc_brutto(self) -> float:
        pass

    def liczba_pozycji(self) -> int:
        pass

    def zatwierdz(self) -> None:
        pass

    def anuluj(self) -> None:
        pass

    def oznacz_zrealizowane(self) -> None:
        pass
