from models.zamowienia import Zamowienie

class Osoba:
    def __init__(self, imie: str, nazwisko: str, login: str, haslo:str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.login = login
        self.__haslo = haslo # atrybut prywatny

    def sprawdz_haslo(self, haslo: str) -> bool:
        """Sprawdza hasło (wewnętrznie, bo atrybut prywatny)"""
        return self.__haslo == haslo
        
class Pracownik(Osoba):  # Pracownik dziedziczy po osobie
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str, rola: str):
        super().__init__(imie, nazwisko, login, haslo) # wywoluje konstruktor klasy nadrzednej - atrybuty z klasy nadrzednej(Osoba) zostaną zapisane do tej klasy
        self.rola = rola

    def wprowadz_nowy_towar(self, rola: str) -> bool: # True jak się udało wprowadzić, False jeśli nie - pewnie do zmiany
        if rola == 'Magazynier':
            print("Można wprowadzić")
            return True
        else: 
            print("Metoda dostępna wyłącznie dla magazyniera")
            return False

    def kompletowanie_zamowienia(self, rola: str, zamowienie: Zamowienie) -> bool:
        if rola == 'Obsluga':
            print("Można skompletować")
            return True
        else: 
            print("Metoda dostępna wyłącznie dla obsługi")
            return False
        
class Klient(Osoba):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str, adres: str):
        super().__init__(imie, nazwisko, login, haslo)
        self.adres = adres

class Kierownik(Osoba):
    def __init__(self, imie: str, nazwisko: str, login: str, haslo: str):
        super().__init__(imie, nazwisko, login, haslo)