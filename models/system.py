from models.osoby import Klient, Kierownik

class System:
    def __init__(self):
        self.uzytkownicy = []
        self.zalogowany_uzytkownik = None
    
    def rejerstracja_klienta(self, imie: str, nazwisko: str, login: str, haslo: str, adres: str) -> bool:
        """Każdy może się zarejerstrować jako klient"""
        if self._login_istnieje(login):
            print("Login już zajęty")
            return False
        klient = Klient(imie, nazwisko, login, haslo, adres)
        self.uzytkownicy.append(klient)
        return True
    
    def rejerstracja_pracownika(self, imie: str, nazwisko: str, login: str, haslo: str, rola: str) -> bool:
        """Tylko Kierownik może zarejestrować Pracownika"""
        if not isinstance(self.zalogowany_uzytkownik, Kierownik): # Jeżeli zalogowany użytkownik nie jest typu Kierownik, to False
            print("Tylko kierownik może rejerstrować pracowników")
            return False
        if self._login_istnieje(login):
            print("Login już zajęty")
            return False
        kierownik = Kierownik(imie, nazwisko, login, haslo)
        self.uzytkownicy.append(kierownik)
        return True
    
    def logowanie(self, login: str, haslo: str) -> bool:
        """Każdy może się zalogować"""
        for uzytkownik in self.uzytkownicy:
            if uzytkownik.login == login and uzytkownik.sprawdz_haslo(haslo):
                self.zalogowany_uzytkownik = uzytkownik
                return True
        return False
    
    def wylogowanie(self):
        self.zalogowany_uzytkownik = None

    def _login_istnieje(self, login: str) -> bool:
        return any(u.login == login for u in self.uzytkownicy)