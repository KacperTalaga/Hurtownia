from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod


class JednostkaMiary(Enum):
    SZTUKA = "SZTUKA"
    METR = "METR"
    METR_KW = "METR_KW"
    METR_SZ = "METR_SZ"
    KILOGRAM = "KILOGRAM"
    TONA = "TONA"
    PALETA = "PALETA"


class Towar(ABC):
    def __init__(self, id_towaru: int, nazwa: str, producent: str, cena_netto: float, stawka_vat: float, jednostka: JednostkaMiary):
        self.id_towaru = id_towaru
        self.nazwa = nazwa
        self.producent = producent
        self.cena_netto = cena_netto
        self.stawka_vat = stawka_vat
        self.jednostka = jednostka

    def cena_brutto(self) -> float:
        """Oblicza cenę brutto towaru."""
        return self.cena_netto * (1 + self.stawka_vat / 100)

    @abstractmethod
    def opis_techniczny(self) -> str:
        pass

    def aktualizuj_cene(self, nowa_cena: float) -> None:
        """Aktualizuje cenę netto towaru."""
        if nowa_cena < 0:
            raise ValueError("Cena netto nie może być ujemna.")

        self.cena_netto = nowa_cena
        


class MaterialPlytowy(Towar):
    def __init__(self, id_towaru: int, nazwa: str, producent: str, cena_netto: float, stawka_vat: float, jednostka: JednostkaMiary, grubosc: float, dlugosc: float, szerokosc: float):
        super().__init__(id_towaru, nazwa, producent, cena_netto, stawka_vat, jednostka)
        self.grubosc = grubosc
        self.dlugosc = dlugosc
        self.szerokosc = szerokosc

    def opis_techniczny(self) -> str:
        """Zwraca opis techniczny materiału płytowego."""
        return (
            f"Materiał płytowy: grubość {self.grubosc}, "
            f"długość {self.dlugosc}, szerokość {self.szerokosc}."
        )
        


class MaterialSypki(Towar):
    def __init__(self, id_towaru: int, nazwa: str, producent: str, cena_netto: float, stawka_vat: float, jednostka: JednostkaMiary, gestosc: float, workowany: bool):
        super().__init__(id_towaru, nazwa, producent, cena_netto, stawka_vat, jednostka)
        self.gestosc = gestosc
        self.workowany = workowany

    def opis_techniczny(self) -> str:
        """Zwraca opis techniczny materiału sypkiego."""
        if self.workowany:
            sposob_pakowania: str = "workowany"
        else:
            sposob_pakowania = "luzem"

        return (
            f"Materiał sypki: gęstość {self.gestosc}, "
            f"sposób pakowania: {sposob_pakowania}."
        )


class MaterialDluzycowy(Towar):
    def __init__(self, id_towaru: int, nazwa: str, producent: str, cena_netto: float, stawka_vat: float, jednostka: JednostkaMiary, dlugosc: float, przekroj: str):
        super().__init__(id_towaru, nazwa, producent, cena_netto, stawka_vat, jednostka)
        self.dlugosc = dlugosc
        self.przekroj = przekroj

    def opis_techniczny(self) -> str:
        """Zwraca opis techniczny materiału dłużycowego."""
        return (
            f"Materiał dłużycowy: długość {self.dlugosc}, "
            f"przekrój {self.przekroj}."
        )
