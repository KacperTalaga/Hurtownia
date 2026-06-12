"""Testy jednostkowe magazynu i pozycji magazynowych."""

from __future__ import annotations

import unittest

from models.magazyn import Magazyn, PozycjaMagazynowa
from models.towar import JednostkaMiary, MaterialSypki


class TestMagazyn(unittest.TestCase):
    """Sprawdza podstawowe operacje magazynu."""

    def utworz_towar(self, id_towaru: int) -> MaterialSypki:
        """Tworzy przykładowy towar do testów.

        Args:
            id_towaru: Identyfikator tworzonego towaru.

        Returns:
            Przykładowy materiał sypki.
        """
        return MaterialSypki(
            id_towaru,
            "Cement",
            "Atlas",
            100.0,
            23.0,
            JednostkaMiary.KILOGRAM,
            1.4,
            True,
        )

    def test_rezerwacja_i_wydanie_towaru(self) -> None:
        """Rezerwacja zwiększa zarezerowane, a wydanie zmniejsza stan."""
        pozycja = PozycjaMagazynowa(self.utworz_towar(1), 10.0, 2.0)

        wynik = pozycja.zarezerwuj(4.0)
        pozycja.wydaj(3.0)

        self.assertTrue(wynik)
        self.assertEqual(pozycja.zarezerowane, 1.0)
        self.assertEqual(pozycja.ilosc, 7.0)
        self.assertEqual(pozycja.dostepna_ilosc(), 6.0)

    def test_nie_mozna_wydac_wiecej_niz_zarezerwowano(self) -> None:
        """Wydanie większej ilości niż zarezerwowana zgłasza ValueError."""
        pozycja = PozycjaMagazynowa(self.utworz_towar(1), 10.0, 2.0)
        pozycja.zarezerwuj(2.0)

        with self.assertRaises(ValueError):
            pozycja.wydaj(3.0)

    def test_dodaj_i_znajdz_towar_w_magazynie(self) -> None:
        """Dodanie towaru pozwala później znaleźć jego pozycję."""
        magazyn = Magazyn("Magazyn główny", "Kraków")
        towar = self.utworz_towar(1)

        magazyn.dodaj_towar(towar, 10.0, 2.0)
        pozycja = magazyn.znajdz_pozycje_towaru(1)

        self.assertEqual(len(magazyn.pozycje), 1)
        self.assertEqual(pozycja.towar.id_towaru, 1)

    def test_nie_mozna_dodac_duplikatu_towaru(self) -> None:
        """Dodanie towaru o tym samym identyfikatorze zgłasza ValueError."""
        magazyn = Magazyn("Magazyn główny", "Kraków")
        towar = self.utworz_towar(1)

        magazyn.dodaj_towar(towar, 10.0, 2.0)

        with self.assertRaises(ValueError):
            magazyn.dodaj_towar(towar, 5.0, 1.0)

    def test_wartosc_zapasow_sumuje_wartosc_brutto(self) -> None:
        """Wartość zapasów to suma wartości brutto wszystkich pozycji na stanie."""
        magazyn = Magazyn("Magazyn główny", "Kraków")
        magazyn.dodaj_towar(self.utworz_towar(1), 10.0, 2.0)
        magazyn.dodaj_towar(self.utworz_towar(2), 5.0, 2.0)

        # cena_brutto = 100 * 1.23 = 123; 123*10 + 123*5 = 1845
        self.assertEqual(magazyn.wartosc_zapasow(), 1845.0)

    def test_wartosc_zapasow_pustego_magazynu(self) -> None:
        """Pusty magazyn ma zerową wartość zapasów."""
        magazyn = Magazyn("Magazyn główny", "Kraków")

        self.assertEqual(magazyn.wartosc_zapasow(), 0.0)

    def test_towary_ponizej_minimum(self) -> None:
        """Magazyn zwraca tylko pozycje poniżej stanu minimalnego."""
        magazyn = Magazyn("Magazyn główny", "Kraków")

        magazyn.dodaj_towar(self.utworz_towar(1), 1.0, 2.0)
        magazyn.dodaj_towar(self.utworz_towar(2), 10.0, 2.0)

        pozycje = magazyn.towary_ponizej_minimum()

        self.assertEqual(len(pozycje), 1)
        self.assertEqual(pozycje[0].towar.id_towaru, 1)


if __name__ == "__main__":
    unittest.main()