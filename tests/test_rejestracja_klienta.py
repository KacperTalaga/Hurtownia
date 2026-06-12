"""Testy jednostkowe rejestracji klientów przez fasadę System."""
from __future__ import annotations
import unittest

from models.system import System
from models.osoby import Klient


class TestRejestracjaKlienta(unittest.TestCase):
    """Sprawdza tworzenie kont klientów oraz walidację loginu."""

    def setUp(self) -> None:
        self.system = System()

    def test_rejestracja_klienta(self) -> None:
        """Poprawna rejestracja tworzy obiekt Klient z podanym adresem."""
        self.assertTrue(self.system.rejestracja_klienta("Anna", "Wojcik", "awojcik", "haslo", "ul. Polna 1"))
        utworzony = next(u for u in self.system.uzytkownicy if u.login == "awojcik")
        self.assertIsInstance(utworzony, Klient)
        self.assertEqual(utworzony.adres, "ul. Polna 1")

    def test_zajety_login_odrzucony(self) -> None:
        """Drugi klient z zajętym loginem nie zostaje zarejestrowany."""
        self.system.rejestracja_klienta("Anna", "Wojcik", "awojcik", "haslo", "ul. Polna 1")
        self.assertFalse(self.system.rejestracja_klienta("Inny", "Klient", "awojcik", "x", "ul. Inna 2"))


if __name__ == "__main__":
    unittest.main()
