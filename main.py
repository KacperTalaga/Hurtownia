from models.system import System

def start():
    system = System()
    
    while True:
        print("Witaj w hurtowni Małpka")
        print("1. Zaloguj się")
        print("2. Zarejestruj się (klient)")
        choice = input()
        
        if choice == "1":
            login = input("Login: ")
            haslo = input("Hasło: ")
            if system.logowanie(login, haslo):
                print("Zalogowano")
        
        elif choice == "2":
            imie = input("Imię: ")
            nazwisko = input("Nazwisko: ")
            login = input("Login: ")
            haslo = input("Hasło: ")
            adres = input("Adres: ")
            system.rejerstracja_klienta(imie, nazwisko, login, haslo, adres)

if __name__ == "__main__":
    start()