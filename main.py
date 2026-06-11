from models.system import System
from models.interfejs import InterfejsKonsolowy


def start() -> None:
    """Punkt wejścia aplikacji — montuje fasadę i uruchamia interfejs."""
    InterfejsKonsolowy(System()).uruchom()


if __name__ == "__main__":
    start()
