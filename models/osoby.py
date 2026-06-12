from __future__ import annotations
from typing import TYPE_CHECKING, List

from models.faktury import Faktura
from models.zamowienia import StatusZamowienia

if TYPE_CHECKING:
    from models.magazyn import Magazyn
    from models.towar import Towar
    from models.zamowienia import Zamowienie
    


class Osoba:
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.login = login
        self.__haslo = haslo

    def sprawdz_haslo(self, haslo: str) -> bool:
        return self.__haslo == haslo


class Pracownik(Osoba):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str):
        super().__init__(imie, nazwisko, login, haslo)


class Klient(Osoba):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str, adres: str, saldo: float = 0.0):
        super().__init__(imie, nazwisko, login, haslo)
        self.adres = adres
        self.saldo = saldo
        self.zamowienia: List[Zamowienie] = []

    def zloz_zamowienie(self) -> Zamowienie:
        pass

    def historia_zamowien(self) -> List[Zamowienie]:
        """Zwraca listę zamówień złożonych przez klienta."""
        return self.zamowienia

    def aktualizuj_saldo(self, kwota: float) -> None:
        pass


class Kierownik(Pracownik):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str):
        super().__init__(imie, nazwisko, login, haslo)

    def inwentaryzacja(self, magazyn: Magazyn) -> None:
        pass

    def raport_stanu_magazynu(self, magazyn: Magazyn) -> None:
        pass


class Magazynier(Pracownik):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str):
        super().__init__(imie, nazwisko, login, haslo)

    def przyjmij_dostawe(self, magazyn: Magazyn, towar: Towar, ilosc: float) -> None:
        """Przyjmuje dostawę towaru, zwiększając jego stan w magazynie.

        ValueError: Gdy towar nie ma pozycji w magazynie albo ilość jest niedodatnia.
        """
        pozycja = magazyn.znajdz_pozycje_towaru(towar.id_towaru)
        pozycja.przyjmij(ilosc)

    def wprowadz_nowy_towar(self, magazyn: Magazyn, towar: Towar) -> None:
        pass


class Obsluga(Pracownik):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str):
        super().__init__(imie, nazwisko, login, haslo)

    def kompletuj_zamowienie(self, zamowienie: Zamowienie, magazyn: Magazyn) -> bool:
           """Kompletuje zamówienie przez rezerwację wymaganych towarów w magazynie."""
           if zamowienie.status != StatusZamowienia.W_REALIZACJI:
            return False

           if not zamowienie.pozycje:
            return False

           for pozycja_zamowienia in zamowienie.pozycje:
            try:
                pozycja_magazynowa = magazyn.znajdz_pozycje_towaru(
                    pozycja_zamowienia.towar.id_towaru
                )
            except ValueError:
                return False

            if pozycja_zamowienia.ilosc > pozycja_magazynowa.dostepna_ilosc():
                return False

           for pozycja_zamowienia in zamowienie.pozycje:
            pozycja_magazynowa = magazyn.znajdz_pozycje_towaru(
                pozycja_zamowienia.towar.id_towaru
            )
            pozycja_magazynowa.zarezerwuj(pozycja_zamowienia.ilosc)

           zamowienie.oznacz_skompletowane()
           return True

    def wystaw_fakture(self, zamowienie: Zamowienie) -> Faktura:
        """Wystawia fakturę dla skompletowanego zamówienia."""

        if zamowienie.status != StatusZamowienia.SKOMPLETOWANE:
            raise ValueError("Fakturę można wystawić tylko dla skompletowanego zamówienia.")

        numer_faktury = f"FV/{zamowienie.numer}"
        faktura = Faktura(numer_faktury, zamowienie.id, zamowienie)

        zamowienie.oznacz_zrealizowane()

        return faktura
