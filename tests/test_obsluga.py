"""Testy jednostkowe operacji obsługi: kompletowanie i wystawianie faktury."""
from __future__ import annotations
import unittest

from models.magazyn import Magazyn
from models.osoby import Obsluga
from models.towar import JednostkaMiary, MaterialSypki
from models.zamowienia import StatusZamowienia, Zamowienie


class TestObslugaRealizacja(unittest.TestCase):
    """Sprawdza rezerwację przy kompletowaniu i wydanie przy realizacji."""

    def setUp(self) -> None:
        self.obsluga = Obsluga("Maria", "Nowak", "mnowak", "tajne")
        self.towar = MaterialSypki(1, "Cement", "Atlas", 100.0, 23.0, JednostkaMiary.KILOGRAM, 1.4, True)
        self.magazyn = Magazyn("Magazyn", "ul. Składowa 1")
        self.magazyn.dodaj_towar(self.towar, 100.0, 10.0)

        self.zamowienie = Zamowienie(1, 1)
        self.zamowienie.dodaj_pozycje(self.towar, 30.0)
        self.zamowienie.zatwierdz()

    def test_kompletowanie_rezerwuje_bez_zdejmowania_stanu(self) -> None:
        """Kompletowanie rezerwuje towar, ale nie zmniejsza jeszcze ilości na stanie."""
        self.assertTrue(self.obsluga.kompletuj_zamowienie(self.zamowienie, self.magazyn))

        pozycja = self.magazyn.znajdz_pozycje_towaru(1)
        self.assertEqual(pozycja.zarezerowane, 30.0)
        self.assertEqual(pozycja.ilosc, 100.0)
        self.assertEqual(self.zamowienie.status, StatusZamowienia.SKOMPLETOWANE)

    def test_wystawienie_faktury_wydaje_towar_ze_stanu(self) -> None:
        """Wystawienie faktury wydaje zarezerwowany towar i realizuje zamówienie."""
        self.obsluga.kompletuj_zamowienie(self.zamowienie, self.magazyn)
        faktura = self.obsluga.wystaw_fakture(self.zamowienie, self.magazyn)

        pozycja = self.magazyn.znajdz_pozycje_towaru(1)
        self.assertEqual(pozycja.ilosc, 70.0)
        self.assertEqual(pozycja.zarezerowane, 0.0)
        self.assertEqual(self.zamowienie.status, StatusZamowienia.ZREALIZOWANE)
        self.assertEqual(faktura.numer, "FV/1")


if __name__ == "__main__":
    unittest.main()
