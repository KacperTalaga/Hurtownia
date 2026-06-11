# Hurtownia

Projekt zaliczeniowy przedstawiający system zarządzania hurtownią materiałów budowlanych. Aplikacja została napisana w języku Python i opiera się na klasach domenowych reprezentujących użytkowników, towary, magazyn, zamówienia oraz faktury.

## Zakres projektu

System umożliwia obsługę podstawowych procesów występujących w hurtowni, takich jak:

* zarządzanie użytkownikami i rolami,
* logowanie oraz wylogowanie użytkownika,
* przechowywanie informacji o towarach budowlanych,
* zarządzanie stanem magazynowym,
* tworzenie zamówień,
* obsługa faktur,
* testowanie wybranych elementów systemu.


## Moduły

### Towary i magazyn

Moduł odpowiada za reprezentację towarów budowlanych oraz zarządzanie stanem magazynowym. W projekcie występują towary bazowe oraz ich specjalizacje: materiały sypkie, płytowe i dłużycowe. Magazyn przechowuje pozycje magazynowe, umożliwia rezerwację, przyjmowanie, wydawanie towaru oraz sprawdzanie stanów minimalnych.

### Użytkownicy i role

Moduł obejmuje hierarchię osób w systemie. Wyróżniono klientów oraz pracowników, w tym magazyniera, obsługę i kierownika. Role określają zakres działań dostępnych dla danego użytkownika.

### Zamówienia i faktury

Moduł odpowiada za tworzenie zamówień, pozycje zamówienia oraz faktury. Cena w pozycji zamówienia jest zapisywana jako migawka ceny z momentu złożenia zamówienia.


## Technologie

* Python
* unittest
* Visual Paradigm
* Git i GitHub

## Autorzy
Kinga Szeliga
Michał Szarek
Kacper Talaga
Projekt został przygotowany zespołowo w ramach zajęć z podziałem na role.
