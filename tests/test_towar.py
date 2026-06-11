"""Testy jednostkowe towarów i materiałów budowlanych."""

from __future__ import annotations

import unittest

from models.towar import (
    JednostkaMiary,
    MaterialDluzycowy,
    MaterialPlytowy,
    MaterialSypki,
)


class TestTowar(unittest.TestCase):
    """Sprawdza obliczanie cen i opisy techniczne towarów."""

    def test_cena_brutto_dla_stawki_vat_23(self) -> None:
        """Cena brutto jest ceną netto powiększoną o VAT."""
        towar = MaterialSypki(
            1,
            "Cement",
            "Atlas",
            100.0,
            23.0,
            JednostkaMiary.KILOGRAM,
            1.4,
            True,
        )

        self.assertEqual(towar.cena_brutto(), 123.0)

    def test_aktualizuj_cene(self) -> None:
        """Aktualizacja ceny zmienia cenę netto towaru."""
        towar = MaterialSypki(
            1,
            "Cement",
            "Atlas",
            100.0,
            23.0,
            JednostkaMiary.KILOGRAM,
            1.4,
            True,
        )

        towar.aktualizuj_cene(150.0)

        self.assertEqual(towar.cena_netto, 150.0)

    def test_aktualizuj_cene_ujemna(self) -> None:
        """Ujemna cena netto zgłasza wyjątek ValueError."""
        towar = MaterialSypki(
            1,
            "Cement",
            "Atlas",
            100.0,
            23.0,
            JednostkaMiary.KILOGRAM,
            1.4,
            True,
        )

        with self.assertRaises(ValueError):
            towar.aktualizuj_cene(-10.0)

    def test_opis_techniczny_materialu_plytowego(self) -> None:
        """Materiał płytowy zwraca opis z wymiarami."""
        towar = MaterialPlytowy(
            2,
            "Płyta OSB",
            "Kronospan",
            50.0,
            23.0,
            JednostkaMiary.SZTUKA,
            18.0,
            2500.0,
            1250.0,
        )

        opis = towar.opis_techniczny()

        self.assertIn("grubość 18.0", opis)
        self.assertIn("długość 2500.0", opis)
        self.assertIn("szerokość 1250.0", opis)

    def test_opis_techniczny_materialu_sypkiego(self) -> None:
        """Materiał sypki zwraca opis z gęstością i pakowaniem."""
        towar = MaterialSypki(
            3,
            "Piasek",
            "BudMat",
            30.0,
            23.0,
            JednostkaMiary.TONA,
            1.6,
            False,
        )

        opis = towar.opis_techniczny()

        self.assertIn("gęstość 1.6", opis)
        self.assertIn("luzem", opis)

    def test_opis_techniczny_materialu_dluzycowego(self) -> None:
        """Materiał dłużycowy zwraca opis z długością i przekrojem."""
        towar = MaterialDluzycowy(
            4,
            "Profil stalowy",
            "StalBud",
            80.0,
            23.0,
            JednostkaMiary.METR,
            6000.0,
            "40x40",
        )

        opis = towar.opis_techniczny()

        self.assertIn("długość 6000.0", opis)
        self.assertIn("przekrój 40x40", opis)


if __name__ == "__main__":
    unittest.main()