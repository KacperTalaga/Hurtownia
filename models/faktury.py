from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.zamowienia import Zamowienie


class StatusPlatnosci(Enum):
    NIEZAPLACONA = "NIEZAPLACONA"
    CZESCIOWO = "CZESCIOWO"
    ZAPLACONA = "ZAPLACONA"


class Faktura:
    def __init__(self, numer: str, id: int):
        self.numer = numer
        self.id = id
        self.data_wystawienia: datetime = None
        self.termin_platnosci: datetime = None
        self.kwota_zaplacona: float = 0.0
        self.status: StatusPlatnosci = StatusPlatnosci.NIEZAPLACONA

    def kwota_do_zaplaty(self) -> float:
        pass

    def zaplac(self, kwota: float) -> None:
        pass
