from __future__ import annotations
from enum import Enum
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.zamowienia import Zamowienie


class StatusPlatnosci(Enum):
    """Dostępne statusy płatności faktury."""

    NIEZAPLACONA = "NIEZAPLACONA"
    CZESCIOWO = "CZESCIOWO"
    ZAPLACONA = "ZAPLACONA"


class Faktura:
    """Faktura wystawiana na podstawie zamówienia."""

    def __init__(self, numer: str, id: int, zamowienie: Zamowienie) -> None:
        """Tworzy fakturę dla wskazanego zamówienia."""
        self.numer: str = numer
        self.id: int = id
        self.zamowienie: Zamowienie = zamowienie
        self.data_wystawienia: datetime = datetime.now()
        self.termin_platnosci: datetime = self.data_wystawienia + timedelta(days=14)
        self.kwota_zaplacona: float = 0.0
        self.status: StatusPlatnosci = StatusPlatnosci.NIEZAPLACONA

    def kwota_do_zaplaty(self) -> float:
        """Zwraca pozostałą kwotę brutto do zapłaty."""
        return self.zamowienie.wartosc_brutto() - self.kwota_zaplacona

    def zaplac(self, kwota: float) -> None:
        """Rejestruje wpłatę dla faktury i aktualizuje status płatności."""

        if kwota <= 0:
            raise ValueError("Kwota wpłaty musi być dodatnia.")

        if kwota > self.kwota_do_zaplaty():
            raise ValueError("Kwota wpłaty nie może przekraczać kwoty do zapłaty.")

        self.kwota_zaplacona += kwota
        self._aktualizuj_status()

    def _aktualizuj_status(self) -> None:
        """Aktualizuje status płatności na podstawie wpłaconej kwoty."""
        wartosc_faktury = self.zamowienie.wartosc_brutto()

        if self.kwota_zaplacona == 0:
            self.status = StatusPlatnosci.NIEZAPLACONA
        elif self.kwota_zaplacona < wartosc_faktury:
            self.status = StatusPlatnosci.CZESCIOWO
        else:
            self.status = StatusPlatnosci.ZAPLACONA
