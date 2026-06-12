from __future__ import annotations
from typing import Callable, Dict, List, Optional, Tuple, TYPE_CHECKING

from models.osoby import Kierownik, Klient, Magazynier, Obsluga
from models.zamowienia import Zamowienie

if TYPE_CHECKING:
    from models.system import System
    from models.towar import Towar
    from models.faktury import Faktura

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
            "2": ("Szczegóły towaru", self.akcja_szczegoly_towaru),
            "3": ("Złóż zamówienie", self.akcja_zlozenie_zamowienia),
            "4": ("Moje zamówienia", self.akcja_moje_zamowienia),
            "5": ("Sprawdź status zamówienia", self.akcja_status_zamowienia),
            "6": ("Moje faktury", self.akcja_moje_faktury),
            "7": ("Opłać fakturę", self.akcja_oplacenie_faktury),
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
            "2": ("Kompletuj zamówienie", self.akcja_kompletowanie_zamowienia),
            "3": ("Wystaw fakturę", self.akcja_wystawienie_faktury),
            "4": ("Przeglądaj faktury", self.akcja_przegladanie_faktur),
            "5": ("Przeglądaj ofertę", self.akcja_przegladanie_oferty),
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

        
    def akcja_zlozenie_zamowienia(self) -> None:
        """Obsługuje złożenie zamówienia przez zalogowanego klienta."""
        klient = self._pobierz_zalogowanego_klienta()
        if klient is None:
            print("  Tylko klient może złożyć zamówienie.")
            return

        if not self.system.towary:
            print("  Brak towarów w ofercie.")
            return

        zamowienie = Zamowienie(
            self._nastepny_numer_zamowienia(),
            self._nastepne_id_zamowienia(),
        )

        print("\n  --- Nowe zamówienie ---")

        while True:
            self.akcja_przegladanie_oferty()
            id_towaru = self._pobierz_int("  ID towaru (0 - zakończ dodawanie): ")

            if id_towaru == 0:
                break

            towar = self._znajdz_towar(id_towaru)
            if towar is None:
                print("  Nie znaleziono towaru o podanym ID.")
                continue

            ilosc = self._pobierz_float("  Ilość: ")

            try:
                zamowienie.dodaj_pozycje(towar, ilosc)
                print(f"  Dodano pozycję: {towar.nazwa}, ilość: {ilosc:.2f}.")
            except ValueError as blad:
                print(f"  Błąd: {blad}")
                continue

            opcje: Opcje = {
                "1": ("Dodaj kolejny towar", None),
                "2": ("Zatwierdź zamówienie", None),
                "0": ("Anuluj zamówienie", None),
            }
            self.wyswietl_menu("Co dalej?", opcje)
            wybor = self.pobierz_wybor(opcje)

            if wybor == "1":
                continue
            if wybor == "2":
                break
            if wybor == "0":
                print("  Zamówienie anulowane.")
                return

        if not zamowienie.pozycje:
            print("  Nie dodano żadnych pozycji — zamówienie nie zostało utworzone.")
            return

        self._wyswietl_zamowienie(zamowienie)

        opcje_potwierdzenia: Opcje = {
            "1": ("Potwierdź zamówienie", None),
            "0": ("Anuluj zamówienie", None),
        }
        self.wyswietl_menu("Potwierdzenie", opcje_potwierdzenia)
        wybor = self.pobierz_wybor(opcje_potwierdzenia)

        if wybor == "0":
            print("  Zamówienie anulowane.")
            return

        try:
            zamowienie = klient.zloz_zamowienie(zamowienie)
        except ValueError as blad:
            print(f"  Błąd: {blad}")
            return

        self.system.zamowienia.append(zamowienie)

        print(
            f"  Zamówienie nr {zamowienie.numer} zostało złożone. "
            f"Status: {zamowienie.status.value}."
        )


    def akcja_moje_zamowienia(self) -> None:
        """Wyświetla zamówienia zalogowanego klienta."""
        klient = self._pobierz_zalogowanego_klienta()
        if klient is None:
            print("  Tylko klient może przeglądać swoje zamówienia.")
            return

        print("\n  --- Moje zamówienia ---")

        zamowienia = klient.historia_zamowien()
        if not zamowienia:
            print("  Brak zamówień.")
            return

        for zamowienie in zamowienia:
            self._wyswietl_zamowienie(zamowienie)

    def akcja_oplacenie_faktury(self) -> None:
        """Obsługuje opłacenie faktury przez zalogowanego klienta."""
        klient = self._pobierz_zalogowanego_klienta()
        if klient is None:
            print("  Tylko klient może opłacać swoje faktury.")
            return

        faktury = self._faktury_klienta(klient)
        if not faktury:
            print("  Brak faktur do opłacenia.")
            return

        print("\n  --- Moje faktury ---")
        for faktura in faktury:
            self._wyswietl_fakture(faktura)

        numer_zamowienia = self._pobierz_int(
            "  Podaj numer zamówienia z faktury do opłacenia: "
        )

        faktura = self._znajdz_fakture_klienta_po_numerze_zamowienia(
            klient, numer_zamowienia
        )
        if faktura is None:
            print("  Nie znaleziono faktury dla podanego zamówienia.")
            return

        kwota = self._pobierz_float("  Kwota płatności: ")
        if kwota <= 0:
            print("  Kwota płatności musi być większa od zera.")
            return

        try:
            faktura.zaplac(kwota)
        except ValueError as blad:
            print(f"  Nie udało się opłacić faktury: {blad}")
            return

        print("  Płatność została zarejestrowana.")
        self._wyswietl_fakture(faktura)


    def akcja_moje_faktury(self) -> None:
        """Wyświetla faktury wystawione dla zamówień zalogowanego klienta."""
        klient = self._pobierz_zalogowanego_klienta()
        if klient is None:
            print("  Tylko klient może przeglądać swoje faktury.")
            return

        print("\n  --- Moje faktury ---")

        faktury = self._faktury_klienta(klient)
        if not faktury:
            print("  Brak wystawionych faktur.")
            return

        for faktura in faktury:
            self._wyswietl_fakture(faktura)

    def akcja_status_zamowienia(self) -> None:
        """Wyświetla status zamówienia zalogowanego klienta."""
        klient = self._pobierz_zalogowanego_klienta()
        if klient is None:
            print("  Tylko klient może sprawdzić status swojego zamówienia.")
            return

        if not klient.zamowienia:
            print("  Nie masz jeszcze żadnych zamówień.")
            return

        numer = self._pobierz_int("  Numer zamówienia: ")
        zamowienie = self._znajdz_zamowienie_klienta(klient, numer)

        if zamowienie is None:
            print("  Nie znaleziono zamówienia o podanym numerze.")
            return

        print(f"  Zamówienie nr {zamowienie.numer}: {zamowienie.status.value}")


    def akcja_kompletowanie_zamowienia(self) -> None:
        """Obsługuje kompletowanie zamówienia przez pracownika obsługi."""
        obsluga = self._pobierz_zalogowana_obsluge()
        if obsluga is None:
            print("  Tylko pracownik obsługi może kompletować zamówienia.")
            return

        if self.system.magazyn is None:
            print("  Brak przypisanego magazynu.")
            return

        if not self.system.zamowienia:
            print("  Brak zamówień do kompletowania.")
            return

        self.akcja_przegladanie_zamowien()
        numer = self._pobierz_int("  Numer zamówienia do skompletowania: ")

        zamowienie = self._znajdz_zamowienie(numer)
        if zamowienie is None:
            print("  Nie znaleziono zamówienia o podanym numerze.")
            return

        if obsluga.kompletuj_zamowienie(zamowienie, self.system.magazyn):
            print(
                f"  Zamówienie nr {zamowienie.numer} zostało skompletowane. "
                f"Status: {zamowienie.status.value}."
            )
        else:
            print(
                "  Nie udało się skompletować zamówienia. "
                "Sprawdź status zamówienia lub dostępność towarów."
            )    

    def akcja_wystawienie_faktury(self) -> None:
        """Obsługuje wystawienie faktury przez pracownika obsługi."""
        obsluga = self._pobierz_zalogowana_obsluge()
        if obsluga is None:
            print("  Tylko pracownik obsługi może wystawiać faktury.")
            return

        if self.system.magazyn is None:
            print("  Brak przypisanego magazynu.")
            return

        if not self.system.zamowienia:
            print("  Brak zamówień.")
            return

        self.akcja_przegladanie_zamowien()
        numer = self._pobierz_int("  Numer zamówienia do wystawienia faktury: ")

        zamowienie = self._znajdz_zamowienie(numer)
        if zamowienie is None:
            print("  Nie znaleziono zamówienia o podanym numerze.")
            return

        if self._znajdz_fakture_dla_zamowienia(numer) is not None:
            print("  Faktura dla tego zamówienia została już wystawiona.")
            return

        try:
            faktura = obsluga.wystaw_fakture(zamowienie, self.system.magazyn)
        except ValueError as blad:
            print(f"  Nie udało się wystawić faktury: {blad}")
            return

        self.system.faktury.append(faktura)

        print("  Faktura została wystawiona.")
        self._wyswietl_fakture(faktura)

    def akcja_przegladanie_faktur(self) -> None:
        """Wyświetla listę wystawionych faktur."""
        print("\n  --- Faktury ---")

        if not self.system.faktury:
            print("  Brak wystawionych faktur.")
            return

        for faktura in self.system.faktury:
            self._wyswietl_fakture(faktura)


    def akcja_raport_stanu_magazynu(self) -> None:
        """Wyświetla raport stanu magazynu dla kierownika."""
        print("\n  --- Raport stanu magazynu ---")

        if self.system.magazyn is None:
            print("  Brak przypisanego magazynu.")
            return

        kierownik = self.system.zalogowany_uzytkownik
        if not isinstance(kierownik, Kierownik):
            print("  Tylko kierownik może wyświetlić raport stanu magazynu.")
            return

        pozycje = kierownik.raport_stanu_magazynu(self.system.magazyn)

        print(f"  Magazyn: {self.system.magazyn.nazwa}")
        print(f"  Adres: {self.system.magazyn.adres}")

        if not pozycje:
            print("  Brak pozycji magazynowych.")
            return

        for pozycja in pozycje:
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
        print("\n  --- Przegląd magazynu ---")

        if self.system.magazyn is None:
            print("  Brak przypisanego magazynu.")
            return

        magazynier = self.system.zalogowany_uzytkownik
        if not isinstance(magazynier, Magazynier):
            print("  Tylko magazynier może przeglądać magazyn.")
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

    def akcja_przyjecie_dostawy(self) -> None:
        """Obsługuje przyjęcie dostawy istniejącego towaru do magazynu."""
        print("\n  --- Przyjęcie dostawy ---")

        if self.system.magazyn is None:
            print("  Brak przypisanego magazynu.")
            return

        magazynier = self.system.zalogowany_uzytkownik
        if not isinstance(magazynier, Magazynier):
            print("  Tylko magazynier może przyjmować dostawy.")
            return

        id_towaru = self._pobierz_int("  ID towaru: ")
        ilosc = self._pobierz_float("  Ilość dostawy: ")

        try:
            pozycja = self.system.magazyn.znajdz_pozycje_towaru(id_towaru)
            magazynier.przyjmij_dostawe(self.system.magazyn, pozycja.towar, ilosc)
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
    
    def _pobierz_zalogowanego_klienta(self) -> Optional[Klient]:
        """Zwraca zalogowanego klienta albo None, jeśli zalogowany użytkownik nie jest klientem."""
        uzytkownik = self.system.zalogowany_uzytkownik
        if isinstance(uzytkownik, Klient):
            return uzytkownik
        return None
    
    def _znajdz_towar(self, id_towaru: int) -> Optional[Towar]:
        """Wyszukuje towar po identyfikatorze."""
        for towar in self.system.towary:
            if towar.id_towaru == id_towaru:
                return towar
        return None
    
    def _nastepny_numer_zamowienia(self) -> int:
        """Wyznacza kolejny numer zamówienia na podstawie listy zamówień systemu."""
        if not self.system.zamowienia:
            return 1
        return max(zamowienie.numer for zamowienie in self.system.zamowienia) + 1

    def _nastepne_id_zamowienia(self) -> int:
        """Wyznacza kolejne ID zamówienia na podstawie listy zamówień systemu."""
        if not self.system.zamowienia:
            return 1
        return max(zamowienie.id for zamowienie in self.system.zamowienia) + 1
    
    def _znajdz_zamowienie_klienta(self, klient: Klient, numer: int) -> Optional[Zamowienie]:
        """Wyszukuje zamówienie klienta po numerze."""
        for zamowienie in klient.zamowienia:
            if zamowienie.numer == numer:
                return zamowienie
        return None

    def _wyswietl_zamowienie(self, zamowienie: Zamowienie) -> None:
        """Wyświetla szczegóły zamówienia wraz z pozycjami."""
        print(
            f"\n  Zamówienie nr {zamowienie.numer} | "
            f"ID: {zamowienie.id} | "
            f"status: {zamowienie.status.value} | "
            f"pozycji: {zamowienie.liczba_pozycji()} | "
            f"netto: {zamowienie.wartosc_netto():.2f} zł | "
            f"brutto: {zamowienie.wartosc_brutto():.2f} zł"
        )

        for indeks, pozycja in enumerate(zamowienie.pozycje, start=1):
            print(
                f"    {indeks}. {pozycja.towar.nazwa} | "
                f"ilość: {pozycja.ilosc:.2f} | "
                f"cena netto: {pozycja.cena_jednostkowa:.2f} zł | "
                f"wartość brutto: {pozycja.wartosc_brutto():.2f} zł"
            )

    def _pobierz_zalogowana_obsluge(self) -> Optional[Obsluga]:
        """Zwraca zalogowanego pracownika obsługi albo None."""
        uzytkownik = self.system.zalogowany_uzytkownik
        if isinstance(uzytkownik, Obsluga):
            return uzytkownik
        return None

    def _znajdz_zamowienie(self, numer: int) -> Optional[Zamowienie]:
        """Wyszukuje zamówienie po numerze na liście zamówień systemu."""
        for zamowienie in self.system.zamowienia:
            if zamowienie.numer == numer:
                return zamowienie
        return None
    
    def _znajdz_fakture_dla_zamowienia(self, numer_zamowienia: int) -> Optional[Faktura]:
        """Wyszukuje fakturę wystawioną dla zamówienia o podanym numerze."""
        for faktura in self.system.faktury:
            if faktura.zamowienie.numer == numer_zamowienia:
                return faktura
        return None
    
    def _faktury_klienta(self, klient: Klient) -> List[Faktura]:
        """Zwraca faktury wystawione dla zamówień wskazanego klienta."""
        faktury: List[Faktura] = []

        for faktura in self.system.faktury:
            if faktura.zamowienie in klient.zamowienia:
                faktury.append(faktura)

        return faktury

    def _wyswietl_fakture(self, faktura: Faktura) -> None:
        """Wyświetla podstawowe dane faktury."""
        print(
            f"\n  Faktura {faktura.numer} | "
            f"ID: {faktura.id} | "
            f"zamówienie nr: {faktura.zamowienie.numer}"
        )
        print(f"  Data wystawienia: {faktura.data_wystawienia.strftime('%Y-%m-%d')}")
        print(f"  Termin płatności: {faktura.termin_platnosci.strftime('%Y-%m-%d')}")
        print(f"  Kwota brutto: {faktura.zamowienie.wartosc_brutto():.2f} zł")
        print(f"  Kwota zapłacona: {faktura.kwota_zaplacona:.2f} zł")
        print(f"  Do zapłaty: {faktura.kwota_do_zaplaty():.2f} zł")
        print(f"  Status płatności: {faktura.status.value}")

    def _znajdz_fakture_klienta_po_numerze_zamowienia(
        self, klient: Klient, numer_zamowienia: int
    ) -> Optional[Faktura]:
        """Wyszukuje fakturę klienta po numerze powiązanego zamówienia."""
        for faktura in self._faktury_klienta(klient):
            if faktura.zamowienie.numer == numer_zamowienia:
                return faktura
        return None

        


    def _zakoncz(self) -> None:
        """Sygnalizuje pętli głównej zakończenie pracy aplikacji."""
        self.dziala = False