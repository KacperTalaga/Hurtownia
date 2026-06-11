from __future__ import annotations
from typing import Callable, Dict, Optional, Tuple

from models.system import System

Opcje = Dict[str, Tuple[str, Optional[Callable[[], None]]]]


class InterfejsKonsolowy:
    """Warstwa prezentacji — konsolowy interfejs użytkownika dla systemu hurtowni."""

    SZEROKOSC: int = 44

    def __init__(self, system: System) -> None:
        self.system = system
        self.dziala: bool = True

    def uruchom(self) -> None:
        """Uruchamia główną pętlę aplikacji."""
        while self.dziala:
            self.menu_glowne()
        print("\n  Do widzenia!\n")

    def menu_glowne(self) -> None:
        """Wyświetla menu główne dla niezalogowanego użytkownika."""
        opcje: Opcje = {
            "1": ("Zaloguj się", self.akcja_logowanie),
            "2": ("Zarejestruj się", self.akcja_rejestracja),
            "0": ("Wyjdź", self._zakoncz),
        }
        self.wyswietl_menu("Hurtownia Małpka", opcje)
        wybor = self.pobierz_wybor(opcje)
        _, handler = opcje[wybor]
        if handler is not None:
            handler()

    def sesja(self) -> None:
        """Pętla menu dla zalogowanego użytkownika."""
        while self.system.zalogowany_uzytkownik is not None:
            u = self.system.zalogowany_uzytkownik
            opcje: Opcje = {
                "0": ("Wyloguj się", self.system.wylogowanie),
            }
            self.wyswietl_menu(f"{u.imie} {u.nazwisko}", opcje)
            wybor = self.pobierz_wybor(opcje)
            _, handler = opcje[wybor]
            if handler is not None:
                handler()

    def akcja_logowanie(self) -> None:
        """Obsługuje formularz logowania i przejście do sesji."""
        print("\n  --- Logowanie ---")
        login = input("  Login: ").strip()
        haslo = input("  Hasło: ").strip()
        if self.system.logowanie(login, haslo):
            u = self.system.zalogowany_uzytkownik
            print(f"  Witaj, {u.imie} {u.nazwisko}!")
            self.sesja()
        else:
            print("  Błędny login lub hasło.")

    def akcja_rejestracja(self) -> None:
        """Zbiera dane klienta i deleguje rejestrację do fasady systemu."""
        print("\n  --- Rejestracja klienta ---")
        imie = input("  Imię: ").strip()
        nazwisko = input("  Nazwisko: ").strip()
        login = input("  Login: ").strip()
        haslo = input("  Hasło: ").strip()
        adres = input("  Adres: ").strip()
        if self.system.rejestracja_klienta(imie, nazwisko, login, haslo, adres):
            print("  Rejestracja zakończona pomyślnie — możesz się zalogować.")
        else:
            print("  Login jest już zajęty — wybierz inny.")

    def wyswietl_menu(self, tytul: str, opcje: Opcje) -> None:
        """Wyświetla nagłówek menu i ponumerowane opcje."""
        szer = self.SZEROKOSC
        print(f"\n╔{'═' * szer}╗")
        print(f"║  {tytul:<{szer - 2}}║")
        print(f"╠{'═' * szer}╣")
        for klucz, (etykieta, _) in opcje.items():
            print(f"║  {klucz}. {etykieta:<{szer - 5}}║")
        print(f"╚{'═' * szer}╝")

    def pobierz_wybor(self, opcje: Opcje) -> str:
        """Pobiera wybór użytkownika i waliduje go względem dostępnych opcji."""
        while True:
            wybor = input("  Wybór: ").strip()
            if wybor in opcje:
                return wybor
            print("  Nieprawidłowy wybór — spróbuj ponownie.")

    def _zakoncz(self) -> None:
        """Sygnalizuje pętli głównej zakończenie pracy aplikacji."""
        self.dziala = False
