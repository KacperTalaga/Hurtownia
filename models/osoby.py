from __future__ import annotations
from typing import TYPE_CHECKING, List

from models.faktury import Faktura
from models.zamowienia import StatusZamowienia

if TYPE_CHECKING:
    from models.magazyn import Magazyn, PozycjaMagazynowa
    from models.towar import Towar
    from models.zamowienia import Zamowienie
    


class Osoba:
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str) -> None:
        self.imie: str = imie
        self.nazwisko: str = nazwisko
        self.login: str = login
        self.__haslo: str = haslo

    def sprawdz_haslo(self, haslo: str) -> bool:
        return self.__haslo == haslo


class Pracownik(Osoba):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str) -> None:
        super().__init__(imie, nazwisko, login, haslo)


class Klient(Osoba):
    """Klient hurtowni, który może składać zamówienia i przeglądać ich historię."""

    def __init__(self, imie: str, nazwisko: str, login: str,haslo: str,adres: str,saldo: float = 0.0,) -> None:
        """Tworzy klienta hurtowni. """

        super().__init__(imie, nazwisko, login, haslo)
        self.adres: str = adres
        self.saldo: float = saldo
        self.zamowienia: List[Zamowienie] = []

    def zloz_zamowienie(self, zamowienie: Zamowienie) -> Zamowienie:
        """Zatwierdza zamówienie i dodaje je do historii klienta."""

        if zamowienie in self.zamowienia:
            raise ValueError("Zamówienie znajduje się już w historii klienta.")

        zamowienie.zatwierdz()
        self.zamowienia.append(zamowienie)

        return zamowienie

    def historia_zamowien(self) -> List[Zamowienie]:
        """Zwraca listę zamówień złożonych przez klienta."""

        return self.zamowienia

    def aktualizuj_saldo(self, kwota: float) -> None:
        """Aktualizuje saldo klienta o wskazaną kwotę. """

        self.saldo = round(self.saldo + kwota, 2)



class Kierownik(Pracownik):
    """Pracownik zarządzający raportami magazynowymi."""

    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str) -> None:
        """Tworzy kierownika."""

        super().__init__(imie, nazwisko, login, haslo)

    def raport_stanu_magazynu(self, magazyn: Magazyn) -> List[PozycjaMagazynowa]:
        """Zwraca pozycje magazynowe do raportu stanu magazynu."""

        return list(magazyn.pozycje)


class Magazynier(Pracownik):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str) -> None:
        super().__init__(imie, nazwisko, login, haslo)

    def przyjmij_dostawe(self, magazyn: Magazyn, towar: Towar, ilosc: float) -> None:
        """Przyjmuje dostawę towaru, zwiększając jego stan w magazynie.

        ValueError: Gdy towar nie ma pozycji w magazynie albo ilość jest niedodatnia.
        """
        pozycja = magazyn.znajdz_pozycje_towaru(towar.id_towaru)
        pozycja.przyjmij(ilosc)

    def wprowadz_nowy_towar(self, magazyn: Magazyn, towar: Towar, ilosc: float, stan_min: float) -> None:
        """Wprowadza nowy towar do magazynu, tworząc dla niego pozycję magazynową.

        ValueError: Gdy towar o tym samym identyfikatorze już istnieje
            albo gdy ilość lub stan minimalny są niepoprawne.
        """
        magazyn.dodaj_towar(towar, ilosc, stan_min)


class Obsluga(Pracownik):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str) -> None:
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

    def wystaw_fakture(self, zamowienie: Zamowienie, magazyn: Magazyn) -> Faktura:
        """Wystawia fakturę dla skompletowanego zamówienia i wydaje towar z magazynu."""
        
        if zamowienie.status != StatusZamowienia.SKOMPLETOWANE:
            raise ValueError("Fakturę można wystawić tylko dla skompletowanego zamówienia.")

        for pozycja_zamowienia in zamowienie.pozycje:
            pozycja_magazynowa = magazyn.znajdz_pozycje_towaru(
                pozycja_zamowienia.towar.id_towaru
            )
            pozycja_magazynowa.wydaj(pozycja_zamowienia.ilosc)

        numer_faktury = f"FV/{zamowienie.numer}"
        faktura = Faktura(numer_faktury, zamowienie.id, zamowienie)

        zamowienie.oznacz_zrealizowane()

        return faktura
