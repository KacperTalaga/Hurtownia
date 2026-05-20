from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.towar import Towar


class PozycjaMagazynowa:
    def __init__(self, towar: Towar, ilosc: float, stan_min: float):
        self.towar = towar
        self.ilosc = ilosc
        self.zarezerowane: float = 0.0
        self.stan_min = stan_min

    def dostepna_ilosc(self) -> float:
        pass

    def zarezerwuj(self, ilosc: float) -> bool:
        pass

    def przyjmij(self, ilosc: float) -> None:
        pass

    def wydaj(self, ilosc: float) -> None:
        pass

    def czy_ponizej_min(self) -> bool:
        pass


class Magazyn:
    def __init__(self, nazwa: str, adres: str):
        self.nazwa = nazwa
        self.adres = adres
        self.pozycje: List[PozycjaMagazynowa] = []

    def dodaj_towar(self, towar: Towar, ilosc: float, stan_min: float) -> None:
        pass

    def znajdz_pozycje_towaru(self, id: int) -> PozycjaMagazynowa:
        pass

    def towary_ponizej_minimum(self) -> List[PozycjaMagazynowa]:
        pass
