from __future__ import annotations

from typing import TYPE_CHECKING, List

from models.magazyn import Magazyn
from models.towar import (
    JednostkaMiary,
    MaterialDluzycowy,
    MaterialPlytowy,
    MaterialSypki,
)
from models.zamowienia import Zamowienie

if TYPE_CHECKING:
    from models.osoby import Osoba
    from models.system import System
    from models.towar import Towar


class DaneStartowe:
    """Tworzy przykładowe dane startowe dla projektu Hurtownia.

    Klasa służy wyłącznie do tworzenia obiektów startowych w kodzie.
    Nie zapisuje danych do plików i nie korzysta z bazy danych.
    """

   

    @staticmethod
    def utworz_towary_startowe() -> List[Towar]:
        """Tworzy przykładowe towary startowe."""
        return [
            MaterialSypki(
                1,
                "Cement",
                "Atlas",
                32.50,
                23.0,
                JednostkaMiary.KILOGRAM,
                1.4,
                True,
            ),
            MaterialPlytowy(
                2,
                "Płyta OSB",
                "Kronospan",
                89.99,
                23.0,
                JednostkaMiary.SZTUKA,
                18.0,
                2500.0,
                1250.0,
            ),
            MaterialDluzycowy(
                3,
                "Profil stalowy",
                "StalBud",
                54.00,
                23.0,
                JednostkaMiary.METR,
                6000.0,
                "40x40",
            ),
            MaterialSypki(
                4,
                "Piasek budowlany",
                "BudMat",
                75.00,
                23.0,
                JednostkaMiary.TONA,
                1.6,
                False,
            ),
            MaterialPlytowy(
                5,
                "Płyta gipsowo-kartonowa",
                "Rigips",
                27.90,
                23.0,
                JednostkaMiary.SZTUKA,
                12.5,
                2600.0,
                1200.0,
            ),
        ]

    @staticmethod
    def utworz_magazyn_startowy() -> Magazyn:
        """Tworzy przykładowy magazyn z pozycjami magazynowymi."""

        magazyn: Magazyn = Magazyn("Magazyn główny", "Kraków")
        towary: List[Towar] = DaneStartowe.utworz_towary_startowe()

        magazyn.dodaj_towar(towary[0], 120.0, 20.0)
        magazyn.dodaj_towar(towary[1], 45.0, 10.0)
        magazyn.dodaj_towar(towary[2], 30.0, 5.0)
        magazyn.dodaj_towar(towary[3], 80.0, 15.0)
        magazyn.dodaj_towar(towary[4], 60.0, 12.0)

        return magazyn

    @staticmethod
    def utworz_zamowienia_startowe() -> List[Zamowienie]:
        """Tworzy przykładowe zamówienia startowe.

        Metoda jest przygotowana dla modułu zamówień, faktur i menu
        terminalowego. Zamówienia są tworzone obiektowo, bez użycia plików
        zewnętrznych ani bazy danych.

        Returns:
            Lista przykładowych zamówień.
        """
        towary: List[Towar] = DaneStartowe.utworz_towary_startowe()

        zamowienie: Zamowienie = Zamowienie(1, 1)
        zamowienie.dodaj_pozycje(towary[0], 10.0)
        zamowienie.dodaj_pozycje(towary[1], 2.0)

        return [zamowienie]

    @staticmethod
    def podlacz_do_systemu(system: System) -> None:
        """Podłącza dane startowe do obiektu systemu."""

        magazyn: Magazyn = DaneStartowe.utworz_magazyn_startowy()

        system.magazyn = magazyn
        system.towary = [pozycja.towar for pozycja in magazyn.pozycje]