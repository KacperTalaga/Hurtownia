"""Testy jednostkowe logowania i wylogowania w fasadzie System."""
from __future__ import annotations
import os
import tempfile
import unittest

from models.system import System, LOGIN_KIEROWNIKA, HASLO_KIEROWNIKA


class TestLogowanie(unittest.TestCase):
    """Sprawdza uwierzytelnianie użytkownika i zarządzanie sesją."""

    def setUp(self) -> None:
        # Izolacja: każdy test działa w pustym katalogu, więc dane.json nie koliduje z repo
        self._katalog = tempfile.TemporaryDirectory()
        self._poprzedni_cwd = os.getcwd()
        os.chdir(self._katalog.name)
        self.system = System()

    def tearDown(self) -> None:
        os.chdir(self._poprzedni_cwd)
        self._katalog.cleanup()

    def test_logowanie_domyslnego_kierownika(self) -> None:
        """Konto startowe kierownika pozwala zalogować się tuż po starcie."""
        self.assertTrue(self.system.logowanie(LOGIN_KIEROWNIKA, HASLO_KIEROWNIKA))
        self.assertIsNotNone(self.system.zalogowany_uzytkownik)

    def test_logowanie_bledne_haslo(self) -> None:
        """Złe hasło nie loguje i nie ustawia sesji."""
        self.assertFalse(self.system.logowanie(LOGIN_KIEROWNIKA, "zle_haslo"))
        self.assertIsNone(self.system.zalogowany_uzytkownik)

    def test_logowanie_nieistniejacy_login(self) -> None:
        """Nieznany login nie loguje i nie ustawia sesji."""
        self.assertFalse(self.system.logowanie("nikt", "cokolwiek"))
        self.assertIsNone(self.system.zalogowany_uzytkownik)

    def test_wylogowanie_czysci_sesje(self) -> None:
        """Wylogowanie kończy aktywną sesję użytkownika."""
        self.system.logowanie(LOGIN_KIEROWNIKA, HASLO_KIEROWNIKA)
        self.system.wylogowanie()
        self.assertIsNone(self.system.zalogowany_uzytkownik)


if __name__ == "__main__":
    unittest.main()
