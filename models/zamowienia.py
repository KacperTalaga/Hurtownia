from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from models.towar import Towar


class StatusZamowienia(Enum):
    """Dostępne statusy zamówienia."""

    NOWE = "NOWE"
    W_REALIZACJI = "W_REALIZACJI"
    SKOMPLETOWANE = "SKOMPLETOWANE"
    ZREALIZOWANE = "ZREALIZOWANE"
    ANULOWANE = "ANULOWANE"


class PozycjaZamowienia:
    """Pojedyncza pozycja zamówienia z migawką ceny jednostkowej."""

    def __init__(self, towar: Towar, ilosc: float, cena_jednostkowa: float, rabat: float) -> None:
        """Tworzy pozycję zamówienia."""

        if ilosc <= 0:
            raise ValueError("Ilość w pozycji zamówienia musi być dodatnia.")
        if cena_jednostkowa < 0:
            raise ValueError("Cena jednostkowa nie może być ujemna.")
        if rabat < 0 or rabat > 100:
            raise ValueError("Rabat musi być z zakresu od 0 do 100.")

        self.towar: Towar = towar
        self.ilosc: float = ilosc
        self.cena_jednostkowa: float = cena_jednostkowa
        self.rabat: float = rabat

    def wartosc_netto(self) -> float:
        """Zwraca wartość netto pozycji bez rabatu."""
        return self.ilosc * self.cena_jednostkowa

    def wartosc_brutto(self) -> float:
        """Zwraca wartość brutto pozycji po rabacie."""
        return self.wartosc() * (1 + self.towar.stawka_vat / 100)

    def wartosc(self) -> float:
        """Zwraca wartość netto pozycji po uwzględnieniu rabatu."""
        return self.wartosc_netto() * (1 - self.rabat / 100)


class Zamowienie:
    """Zamówienie klienta zawierające pozycje i status realizacji."""

    def __init__(self, numer: int, id: int) -> None:
        """Tworzy nowe zamówienie."""

        self.numer: int = numer
        self.id: int = id
        self.data_zlozenia: Optional[datetime] = None
        self.data_realizacji: Optional[datetime] = None
        self.status: StatusZamowienia = StatusZamowienia.NOWE
        self.pozycje: List[PozycjaZamowienia] = []

    def dodaj_pozycje(self, towar: Towar, ilosc: float, rabat: float = 0.0) -> None:
        """Dodaje pozycję do zamówienia z opcjonalnym rabatem (0-100%)."""
        if self.status == StatusZamowienia.ANULOWANE:
            raise ValueError("Nie można dodać pozycji do anulowanego zamówienia.")
        if ilosc <= 0:
            raise ValueError("Ilość w pozycji zamówienia musi być dodatnia.")

        pozycja = PozycjaZamowienia(towar, ilosc, towar.cena_netto, rabat)
        self.pozycje.append(pozycja)

    def usun_pozycje(self, index: int) -> None:
        """Usuwa pozycję zamówienia po indeksie."""
        
        if self.status in (StatusZamowienia.ANULOWANE, StatusZamowienia.ZREALIZOWANE):
            raise ValueError("Nie można usunąć pozycji z zamkniętego zamówienia.")
        if index < 0 or index >= len(self.pozycje):
            raise IndexError("Nie znaleziono pozycji zamówienia o podanym indeksie.")

        del self.pozycje[index]

    def wartosc_netto(self) -> float:
        """Zwraca łączną wartość netto zamówienia bez rabatów."""

        return sum(pozycja.wartosc_netto() for pozycja in self.pozycje)

    def wartosc_brutto(self) -> float:
        """Zwraca łączną wartość brutto zamówienia po rabatach."""

        return sum(pozycja.wartosc_brutto() for pozycja in self.pozycje)

    def liczba_pozycji(self) -> int:
        """Zwraca liczbę pozycji w zamówieniu."""

        return len(self.pozycje)

    def zatwierdz(self) -> None:
        """Zatwierdza zamówienie i przekazuje je do realizacji."""

        if self.status != StatusZamowienia.NOWE:
            raise ValueError("Tylko nowe zamówienie może zostać zatwierdzone.")
        if not self.pozycje:
            raise ValueError("Nie można zatwierdzić zamówienia bez pozycji.")

        self.data_zlozenia = datetime.now()
        self.status = StatusZamowienia.W_REALIZACJI

    def anuluj(self) -> None:
        """Anuluje zamówienie."""

        if self.status == StatusZamowienia.ZREALIZOWANE:
            raise ValueError("Nie można anulować zrealizowanego zamówienia.")

        self.status = StatusZamowienia.ANULOWANE

    def oznacz_skompletowane(self) -> None:
        """Oznacza zamówienie jako skompletowane."""

        if self.status != StatusZamowienia.W_REALIZACJI:
            raise ValueError("Tylko zamówienie w realizacji może zostać skompletowane.")

        self.status = StatusZamowienia.SKOMPLETOWANE

    def oznacz_zrealizowane(self) -> None:
        """Oznacza zamówienie jako zrealizowane."""

        if self.status == StatusZamowienia.ANULOWANE:
            raise ValueError("Nie można zrealizować anulowanego zamówienia.")

        self.data_realizacji = datetime.now()
        self.status = StatusZamowienia.ZREALIZOWANE
