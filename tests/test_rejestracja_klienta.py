"""Testy jednostkowe rejestracji klientów przez fasadę System."""
from __future__ import annotations
import os
import tempfile
import unittest

from models.system import System
from models.osoby import Klient


class TestRejestracjaKlienta(unittest.TestCase):
    """Sprawdza tworzenie kont klientów oraz walidację loginu."""

    def setUp(self) -> None:
        # Izolacja: każdy test działa w pustym katalogu, więc dane.json nie koliduje z repo
        self._katalog = tempfile.TemporaryDirectory()
        self._poprzedni_cwd = os.getcwd()
        os.chdir(self._katalog.name)
        self.system = System()

    def tearDown(self) -> None:
        os.chdir(self._poprzedni_cwd)
        self._katalog.cleanup()

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

    def test_dane_zapisane_i_odtworzone(self) -> None:
        """Zarejestrowany klient jest utrwalony i odczytany przy ponownym starcie."""
        self.system.rejestracja_klienta("Anna", "Wojcik", "awojcik", "haslo", "ul. Polna 1")
        odtworzony = System()  # czyta ten sam dane.json z bieżącego (tymczasowego) katalogu
        self.assertTrue(odtworzony.logowanie("awojcik", "haslo"))
        self.assertIsInstance(odtworzony.zalogowany_uzytkownik, Klient)


if __name__ == "__main__":
    unittest.main()
