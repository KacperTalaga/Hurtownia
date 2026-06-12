"""Testy jednostkowe operacji klienta."""
from __future__ import annotations
import unittest

from models.osoby import Klient
from models.zamowienia import Zamowienie


class TestKlientHistoriaZamowien(unittest.TestCase):
    """Sprawdza dostęp do historii zamówień klienta."""

    def setUp(self) -> None:
        self.klient = Klient("Anna", "Wojcik", "awojcik", "tajne", "ul. Polna 1")

    def test_historia_zwraca_zamowienia_klienta(self) -> None:
        """Historia zwraca zamówienia złożone przez klienta w kolejności dodania."""
        pierwsze = Zamowienie(1, 1)
        drugie = Zamowienie(2, 2)
        self.klient.zamowienia.append(pierwsze)
        self.klient.zamowienia.append(drugie)

        self.assertEqual(self.klient.historia_zamowien(), [pierwsze, drugie])

    def test_historia_pusta_dla_nowego_klienta(self) -> None:
        """Nowy klient ma pustą historię zamówień."""
        self.assertEqual(self.klient.historia_zamowien(), [])


if __name__ == "__main__":
    unittest.main()
