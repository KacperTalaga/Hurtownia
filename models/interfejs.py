from __future__ import annotations
from typing import Callable, Dict, Optional, Tuple, TYPE_CHECKING

from models.osoby import Kierownik, Klient, Magazynier, Obsluga

if TYPE_CHECKING:
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
            uzytkownik = self.system.zalogowany_uzytkownik

            if isinstance(uzytkownik, Kierownik):
                self.menu_kierownika()
            elif isinstance(uzytkownik, Magazynier):
                self.menu_magazyniera()
            elif isinstance(uzytkownik, Obsluga):
                self.menu_obslugi()
            elif isinstance(uzytkownik, Klient):
                self.menu_klienta()
            else:
                self.menu_uzytkownika()

    def menu_klienta(self) -> None:
        """Wyświetla menu dostępne dla klienta."""
        opcje: Opcje = {
            "1": ("Przeglądaj ofertę", self.akcja_przegladanie_oferty),
            "2": ("Pokaż szczegóły towaru", self.akcja_szczegoly_towaru),
            "0": ("Wyloguj się", self.system.wylogowanie),
        }
        self.wyswietl_menu(self._nazwa_zalogowanego(), opcje)
        wybor = self.pobierz_wybor(opcje)
        _, handler = opcje[wybor]
        if handler is not None:
            handler()

    def menu_kierownika(self) -> None:
        """Wyświetla menu dostępne dla kierownika."""
        opcje: Opcje = {
            "1": ("Zarejestruj pracownika", self.akcja_rejestracja_pracownika),
            "2": ("Raport stanu magazynu", self.akcja_raport_stanu_magazynu),
            "3": ("Towary poniżej minimum", self.akcja_towary_ponizej_minimum),
            "4": ("Przeglądaj ofertę", self.akcja_przegladanie_oferty),
            "0": ("Wyloguj się", self.system.wylogowanie),
        }
        self.wyswietl_menu(self._nazwa_zalogowanego(), opcje)
        wybor = self.pobierz_wybor(opcje)
        _, handler = opcje[wybor]
        if handler is not None:
            handler()

    def menu_magazyniera(self) -> None:
        """Wyświetla menu dostępne dla magazyniera."""
        opcje: Opcje = {
            "1": ("Przeglądaj magazyn", self.akcja_przegladanie_magazynu),
            "2": ("Przyjmij dostawę", self.akcja_przyjecie_dostawy),
            "3": ("Przeglądaj ofertę", self.akcja_przegladanie_oferty),
            "0": ("Wyloguj się", self.system.wylogowanie),
        }
        self.wyswietl_menu(self._nazwa_zalogowanego(), opcje)
        wybor = self.pobierz_wybor(opcje)
        _, handler = opcje[wybor]
        if handler is not None:
            handler()

    def menu_obslugi(self) -> None:
        """Wyświetla menu dostępne dla pracownika obsługi."""
        opcje: Opcje = {
            "1": ("Przeglądaj zamówienia", self.akcja_przegladanie_zamowien),
            "2": ("Przeglądaj ofertę", self.akcja_przegladanie_oferty),
            "0": ("Wyloguj się", self.system.wylogowanie),
        }
        self.wyswietl_menu(self._nazwa_zalogowanego(), opcje)
        wybor = self.pobierz_wybor(opcje)
        _, handler = opcje[wybor]
        if handler is not None:
            handler()

    def menu_uzytkownika(self) -> None:
        """Wyświetla awaryjne menu dla nierozpoznanego typu użytkownika."""
        opcje: Opcje = {
            "0": ("Wyloguj się", self.system.wylogowanie),
        }
        self.wyswietl_menu(self._nazwa_zalogowanego(), opcje)
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
            uzytkownik = self.system.zalogowany_uzytkownik
            if uzytkownik is not None:
                print(f"  Witaj, {uzytkownik.imie} {uzytkownik.nazwisko}!")
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

    def akcja_rejestracja_pracownika(self) -> None:
        """Zbiera dane nowego pracownika i deleguje rejestrację do fasady systemu."""
        print("\n  --- Rejestracja pracownika ---")
        typy: Opcje = {
            "1": ("Magazynier", None),
            "2": ("Obsługa", None),
            "0": ("Anuluj", None),
        }
        self.wyswietl_menu("Typ pracownika", typy)
        wybor = self.pobierz_wybor(typy)
        if wybor == "0":
            return

        typ = "Magazynier" if wybor == "1" else "Obsluga"

        imie = input("  Imię: ").strip()
        nazwisko = input("  Nazwisko: ").strip()
        login = input("  Login: ").strip()
        haslo = input("  Hasło: ").strip()

        if self.system.rejestracja_pracownika(typ, imie, nazwisko, login, haslo):
            print(f"  Pracownik ({typ}) zarejestrowany pomyślnie.")
        else:
            print("  Nie udało się — login zajęty lub nieprawidłowy typ.")

    def akcja_przegladanie_oferty(self) -> None:
        """Wyświetla listę towarów dostępnych w ofercie."""
        print("\n  --- Oferta produktów ---")

        if not self.system.towary:
            print("  Brak towarów w ofercie.")
            return

        for towar in self.system.towary:
            print(
                f"  [{towar.id_towaru}] {towar.nazwa} | "
                f"{towar.producent} | "
                f"netto: {towar.cena_netto:.2f} zł | "
                f"brutto: {towar.cena_brutto():.2f} zł | "
                f"{towar.jednostka.value}"
            )

    def akcja_szczegoly_towaru(self) -> None:
        """Wyświetla szczegóły wybranego towaru."""
        print("\n  --- Szczegóły towaru ---")
        id_towaru = self._pobierz_int("  ID towaru: ")

        for towar in self.system.towary:
            if towar.id_towaru == id_towaru:
                print(f"  Nazwa: {towar.nazwa}")
                print(f"  Producent: {towar.producent}")
                print(f"  Cena netto: {towar.cena_netto:.2f} zł")
                print(f"  Cena brutto: {towar.cena_brutto():.2f} zł")
                print(f"  Jednostka: {towar.jednostka.value}")
                print(f"  Opis techniczny: {towar.opis_techniczny()}")
                return

        print("  Nie znaleziono towaru o podanym ID.")

    def akcja_raport_stanu_magazynu(self) -> None:
        """Wyświetla raport stanu magazynu."""
        print("\n  --- Raport stanu magazynu ---")

        if self.system.magazyn is None:
            print("  Brak przypisanego magazynu.")
            return

        print(f"  Magazyn: {self.system.magazyn.nazwa}")
        print(f"  Adres: {self.system.magazyn.adres}")

        if not self.system.magazyn.pozycje:
            print("  Brak pozycji magazynowych.")
            return

        for pozycja in self.system.magazyn.pozycje:
            print(
                f"  [{pozycja.towar.id_towaru}] {pozycja.towar.nazwa} | "
                f"stan: {pozycja.ilosc:.2f} | "
                f"zarezerwowane: {pozycja.zarezerowane:.2f} | "
                f"dostępne: {pozycja.dostepna_ilosc():.2f} | "
                f"minimum: {pozycja.stan_min:.2f}"
            )

    def akcja_towary_ponizej_minimum(self) -> None:
        """Wyświetla towary, których stan jest poniżej minimum."""
        print("\n  --- Towary poniżej minimum ---")

        if self.system.magazyn is None:
            print("  Brak przypisanego magazynu.")
            return

        pozycje = self.system.magazyn.towary_ponizej_minimum()

        if not pozycje:
            print("  Brak towarów poniżej stanu minimalnego.")
            return

        for pozycja in pozycje:
            print(
                f"  [{pozycja.towar.id_towaru}] {pozycja.towar.nazwa} | "
                f"stan: {pozycja.ilosc:.2f} | "
                f"minimum: {pozycja.stan_min:.2f}"
            )

    def akcja_przegladanie_magazynu(self) -> None:
        """Wyświetla aktualny stan magazynu dla magazyniera."""
        self.akcja_raport_stanu_magazynu()

    def akcja_przyjecie_dostawy(self) -> None:
        """Obsługuje przyjęcie dostawy istniejącego towaru do magazynu."""
        print("\n  --- Przyjęcie dostawy ---")

        if self.system.magazyn is None:
            print("  Brak przypisanego magazynu.")
            return

        id_towaru = self._pobierz_int("  ID towaru: ")
        ilosc = self._pobierz_float("  Ilość dostawy: ")

        try:
            pozycja = self.system.magazyn.znajdz_pozycje_towaru(id_towaru)
            pozycja.przyjmij(ilosc)
            print(
                f"  Przyjęto {ilosc:.2f} jednostek towaru "
                f"{pozycja.towar.nazwa}."
            )
        except ValueError as blad:
            print(f"  Błąd: {blad}")

    def akcja_przegladanie_zamowien(self) -> None:
        """Wyświetla listę zamówień dostępnych w systemie."""
        print("\n  --- Zamówienia ---")

        if not self.system.zamowienia:
            print("  Brak zamówień.")
            return

        for zamowienie in self.system.zamowienia:
            print(
                f"  Zamówienie nr {zamowienie.numer} | "
                f"ID: {zamowienie.id} | "
                f"status: {zamowienie.status.value} | "
                f"pozycji: {zamowienie.liczba_pozycji()} | "
                f"brutto: {zamowienie.wartosc_brutto():.2f} zł"
            )

            for indeks, pozycja in enumerate(zamowienie.pozycje, start=1):
                print(
                    f"    {indeks}. {pozycja.towar.nazwa} | "
                    f"ilość: {pozycja.ilosc:.2f} | "
                    f"cena netto: {pozycja.cena_jednostkowa:.2f} zł | "
                    f"wartość brutto: {pozycja.wartosc_brutto():.2f} zł"
                )

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

    def _pobierz_int(self, komunikat: str) -> int:
        """Pobiera liczbę całkowitą z wejścia użytkownika."""
        while True:
            try:
                return int(input(komunikat).strip())
            except ValueError:
                print("  Podaj poprawną liczbę całkowitą.")

    def _pobierz_float(self, komunikat: str) -> float:
        """Pobiera liczbę zmiennoprzecinkową z wejścia użytkownika."""
        while True:
            try:
                return float(input(komunikat).strip().replace(",", "."))
            except ValueError:
                print("  Podaj poprawną liczbę.")

    def _nazwa_zalogowanego(self) -> str:
        """Zwraca imię i nazwisko aktualnie zalogowanego użytkownika."""
        uzytkownik = self.system.zalogowany_uzytkownik
        if uzytkownik is None:
            return "Użytkownik"
        return f"{uzytkownik.imie} {uzytkownik.nazwisko}"

    def _zakoncz(self) -> None:
        """Sygnalizuje pętli głównej zakończenie pracy aplikacji."""
        self.dziala = False