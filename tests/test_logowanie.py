"""Testy jednostkowe logowania i wylogowania w fasadzie System."""
from __future__ import annotations
import unittest

from models.system import System, LOGIN_KIEROWNIKA, HASLO_KIEROWNIKA


class TestLogowanie(unittest.TestCase):
    """Sprawdza uwierzytelnianie użytkownika i zarządzanie sesją."""

    def setUp(self) -> None:
        self.system = System()

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
