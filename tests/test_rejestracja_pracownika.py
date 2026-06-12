"""Testy jednostkowe rejestracji pracowników przez fasadę System."""
from __future__ import annotations
import unittest

from models.system import System
from models.osoby import Magazynier, Obsluga, Osoba


class TestRejestracjaPracownika(unittest.TestCase):
    """Sprawdza tworzenie kont pracowników oraz walidację typu i loginu."""

    def setUp(self) -> None:
        self.system = System()

    def _znajdz(self, login: str) -> Osoba:
        """Zwraca użytkownika o danym loginie z listy systemu."""
        return next(u for u in self.system.uzytkownicy if u.login == login)

    def test_rejestracja_magazyniera(self) -> None:
        """Poprawna rejestracja tworzy obiekt Magazynier."""
        self.assertTrue(self.system.rejestracja_pracownika("Magazynier", "Jan", "Nowak", "jnowak", "tajne"))
        self.assertIsInstance(self._znajdz("jnowak"), Magazynier)

    def test_rejestracja_obslugi(self) -> None:
        """Poprawna rejestracja tworzy obiekt Obsluga."""
        self.assertTrue(self.system.rejestracja_pracownika("Obsluga", "Ewa", "Lis", "elis", "tajne"))
        self.assertIsInstance(self._znajdz("elis"), Obsluga)

    def test_nieobslugiwany_typ_odrzucony(self) -> None:
        """Kierownika ani nieznanego typu nie wolno utworzyć przez rejestrację pracownika."""
        self.assertFalse(self.system.rejestracja_pracownika("Kierownik", "X", "Y", "xy", "t"))
        self.assertFalse(self.system.rejestracja_pracownika("Ktokolwiek", "X", "Y", "xy2", "t"))

    def test_zajety_login_odrzucony(self) -> None:
        """Drugi pracownik z zajętym loginem nie zostaje zarejestrowany."""
        self.system.rejestracja_pracownika("Magazynier", "Jan", "Nowak", "jnowak", "t")
        self.assertFalse(self.system.rejestracja_pracownika("Obsluga", "Inny", "Ktos", "jnowak", "t"))


if __name__ == "__main__":
    unittest.main()
