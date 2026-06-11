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
        """Zwraca ilość towaru dostępną do rezerwacji."""
        return self.ilosc - self.zarezerowane

    def zarezerwuj(self, ilosc: float) -> bool:
        """Rezerwuje wskazaną ilość towaru, jeśli jest dostępna."""
        if ilosc <= 0:
            return False

        if ilosc > self.dostepna_ilosc():
            return False

        self.zarezerowane += ilosc
        return True

    def przyjmij(self, ilosc: float) -> None:
        """Zwiększa ilość towaru na stanie magazynowym."""
        if ilosc <= 0:
            raise ValueError("Ilość przyjmowanego towaru musi być dodatnia.")

        self.ilosc += ilosc

    def wydaj(self, ilosc: float) -> None:
        """Wydaje wskazaną ilość towaru z magazynu.

        Wydanie zmniejsza zarówno ilość zarezerwowaną, jak i całkowitą
        ilość towaru na stanie, ponieważ dotyczy wcześniej zarezerwowanego
        towaru."""
        if ilosc <= 0:
            raise ValueError("Ilość wydawanego towaru musi być dodatnia.")

        if ilosc > self.zarezerowane:
            raise ValueError("Nie można wydać więcej towaru niż zarezerwowano.")

        self.zarezerowane -= ilosc
        self.ilosc -= ilosc

    def czy_ponizej_min(self) -> bool:
        """Sprawdza, czy stan towaru jest poniżej minimum."""
        return self.ilosc < self.stan_min


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
