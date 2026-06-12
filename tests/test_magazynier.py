"""Testy jednostkowe operacji magazyniera na magazynie."""
from __future__ import annotations
import unittest

from models.magazyn import Magazyn
from models.osoby import Magazynier
from models.towar import JednostkaMiary, MaterialSypki


class TestMagazynierPrzyjmijDostawe(unittest.TestCase):
    """Sprawdza przyjmowanie dostawy towaru przez magazyniera."""

    def setUp(self) -> None:
        self.magazynier = Magazynier("Jan", "Nowak", "jnowak", "tajne")
        self.towar = MaterialSypki(1, "Cement", "Atlas", 100.0, 23.0, JednostkaMiary.KILOGRAM, 1.4, True)
        self.magazyn = Magazyn("Magazyn", "ul. Składowa 1")
        self.magazyn.dodaj_towar(self.towar, 100.0, 20.0)

    def test_przyjmij_dostawe_zwieksza_stan(self) -> None:
        """Przyjęcie dostawy zwiększa ilość towaru na pozycji magazynowej."""
        self.magazynier.przyjmij_dostawe(self.magazyn, self.towar, 50.0)

        pozycja = self.magazyn.znajdz_pozycje_towaru(self.towar.id_towaru)
        self.assertEqual(pozycja.ilosc, 150.0)

    def test_przyjmij_dostawe_nieznany_towar(self) -> None:
        """Przyjęcie dostawy towaru spoza magazynu zgłasza ValueError."""
        obcy = MaterialSypki(99, "Wapno", "Atlas", 50.0, 23.0, JednostkaMiary.KILOGRAM, 1.1, False)
        with self.assertRaises(ValueError):
            self.magazynier.przyjmij_dostawe(self.magazyn, obcy, 10.0)

    def test_przyjmij_dostawe_niepoprawna_ilosc(self) -> None:
        """Przyjęcie niedodatniej ilości zgłasza ValueError i nie zmienia stanu."""
        with self.assertRaises(ValueError):
            self.magazynier.przyjmij_dostawe(self.magazyn, self.towar, 0.0)

        pozycja = self.magazyn.znajdz_pozycje_towaru(self.towar.id_towaru)
        self.assertEqual(pozycja.ilosc, 100.0)


if __name__ == "__main__":
    unittest.main()
