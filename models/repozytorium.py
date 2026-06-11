from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from models.osoby import Kierownik, Klient, Magazynier, Obsluga, Osoba, Pracownik

# Mapowanie nazwa typu -> klasa pracownika przy odtwarzaniu z pliku
TYPY_PRACOWNIKOW = {
    "Magazynier": Magazynier,
    "Obsluga": Obsluga,
    "Kierownik": Kierownik,
}


class Repozytorium:
    """Repozytorium danych systemu — serializuje stan do pliku JSON i odtwarza go przy starcie."""

    def __init__(self, sciezka: str = "dane.json") -> None:
        self.sciezka: Path = Path(sciezka)

    def wczytaj_uzytkownikow(self) -> List[Osoba]:
        """Wczytuje listę użytkowników z pliku JSON.

        Zwraca pustą listę, gdy plik nie istnieje (pierwsze uruchomienie).
        """
        if not self.sciezka.exists():
            return []
        with self.sciezka.open("r", encoding="utf-8") as plik:
            dane: Dict[str, Any] = json.load(plik)
        return [self._osoba_z_dict(rekord) for rekord in dane.get("uzytkownicy", [])]

    def zapisz(self, system: System) -> None:
        """Zapisuje aktualny stan systemu do pliku JSON."""
        dane: Dict[str, Any] = {
            "uzytkownicy": [self._osoba_do_dict(u) for u in system.uzytkownicy],
        }
        with self.sciezka.open("w", encoding="utf-8") as plik:
            json.dump(dane, plik, ensure_ascii=False, indent=2)

    def _osoba_do_dict(self, osoba: Osoba) -> Dict[str, Any]:
        """Konwertuje obiekt Osoby na słownik z dyskryminatorem typu."""
        # name-mangling: Osoba.__haslo jest dostępne jako _Osoba__haslo
        haslo = osoba._Osoba__haslo  # type: ignore[attr-defined]
        if isinstance(osoba, Klient):
            return {
                "typ": "Klient",
                "imie": osoba.imie,
                "nazwisko": osoba.nazwisko,
                "login": osoba.login,
                "haslo": haslo,
                "adres": osoba.adres,
                "saldo": osoba.saldo,
            }
        if isinstance(osoba, Pracownik):
            return {
                "typ": type(osoba).__name__,
                "imie": osoba.imie,
                "nazwisko": osoba.nazwisko,
                "login": osoba.login,
                "haslo": haslo,
            }
        raise ValueError(f"Nieobsługiwany typ użytkownika: {type(osoba).__name__}")

    def _osoba_z_dict(self, rekord: Dict[str, Any]) -> Osoba:
        """Rekonstruuje obiekt Osoby na podstawie słownika z dyskryminatorem typu."""
        typ = rekord["typ"]
        if typ == "Klient":
            return Klient(
                rekord["imie"],
                rekord["nazwisko"],
                rekord["login"],
                rekord["haslo"],
                rekord["adres"],
                rekord.get("saldo", 0.0),
            )
        klasa = TYPY_PRACOWNIKOW.get(typ)
        if klasa is not None:
            return klasa(
                rekord["imie"],
                rekord["nazwisko"],
                rekord["login"],
                rekord["haslo"],
            )
        raise ValueError(f"Nieznany typ użytkownika w pliku danych: {typ}")
