"""Testy jednostkowe modulu zamowien."""
from __future__ import annotations
import unittest

from models.towar import JednostkaMiary, MaterialSypki
from models.zamowienia import StatusZamowienia, Zamowienie


class TestZamowienia(unittest.TestCase):
    """Sprawdza pozycje zamowienia, wartosci i zmiane statusow."""

    def setUp(self) -> None:
        self.towar = MaterialSypki(
            1,
            "Cement",
            "Atlas",
            100.0,
            23.0,
            JednostkaMiary.KILOGRAM,
            1.4,
            True,
        )
        self.zamowienie = Zamowienie(1, 1)

    def test_dodanie_pozycji_kopiuje_cene_jako_migawke(self) -> None:
        """Dodanie pozycji zapisuje cene niezaleznie od pozniejszych zmian towaru."""
        self.zamowienie.dodaj_pozycje(self.towar, 2.0)
        self.towar.aktualizuj_cene(200.0)

        self.assertEqual(self.zamowienie.pozycje[0].cena_jednostkowa, 100.0)

    def test_wartosc_netto_pozycji(self) -> None:
        """Wartosc netto pozycji jest iloczynem ilosci i ceny jednostkowej."""
        self.zamowienie.dodaj_pozycje(self.towar, 2.0)

        self.assertEqual(self.zamowienie.pozycje[0].wartosc_netto(), 200.0)

    def test_wartosc_brutto_pozycji(self) -> None:
        """Wartosc brutto pozycji uwzglednia VAT towaru."""
        self.zamowienie.dodaj_pozycje(self.towar, 2.0)

        self.assertEqual(self.zamowienie.pozycje[0].wartosc_brutto(), 246.0)

    def test_liczba_pozycji(self) -> None:
        """Liczba pozycji odpowiada liczbie dodanych towarow."""
        self.zamowienie.dodaj_pozycje(self.towar, 2.0)

        self.assertEqual(self.zamowienie.liczba_pozycji(), 1)

    def test_usuniecie_pozycji(self) -> None:
        """Usuniecie pozycji zmniejsza liczbe pozycji w zamowieniu."""
        self.zamowienie.dodaj_pozycje(self.towar, 2.0)
        self.zamowienie.usun_pozycje(0)

        self.assertEqual(self.zamowienie.liczba_pozycji(), 0)

    def test_zatwierdzenie_zmienia_status_na_w_realizacji(self) -> None:
        """Zatwierdzenie zamowienia ustawia status W_REALIZACJI i date zlozenia."""
        self.zamowienie.dodaj_pozycje(self.towar, 2.0)
        self.zamowienie.zatwierdz()

        self.assertEqual(self.zamowienie.status, StatusZamowienia.W_REALIZACJI)
        self.assertIsNotNone(self.zamowienie.data_zlozenia)

    def test_nie_mozna_zatwierdzic_pustego_zamowienia(self) -> None:
        """Puste zamowienie nie moze zostac zatwierdzone."""
        with self.assertRaises(ValueError):
            self.zamowienie.zatwierdz()

    def test_anulowanie_zmienia_status(self) -> None:
        """Anulowanie zamowienia ustawia status ANULOWANE."""
        self.zamowienie.anuluj()

        self.assertEqual(self.zamowienie.status, StatusZamowienia.ANULOWANE)

    def test_oznaczenie_zrealizowane_ustawia_date_realizacji(self) -> None:
        """Oznaczenie zamowienia jako zrealizowane ustawia status i date realizacji."""
        self.zamowienie.oznacz_zrealizowane()

        self.assertEqual(self.zamowienie.status, StatusZamowienia.ZREALIZOWANE)
        self.assertIsNotNone(self.zamowienie.data_realizacji)


if __name__ == "__main__":
    unittest.main()
