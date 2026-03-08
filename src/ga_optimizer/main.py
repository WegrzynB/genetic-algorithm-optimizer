# główny punkt wejścia aplikacji

import traceback

from ga_optimizer.gui.app import run_app


def main() -> int:
    try:
        run_app()
        return 0
    except KeyboardInterrupt:
        print("\nZamknięto aplikację przez użytkownika.")
        return 130
    except Exception as exc:
        print("Wystąpił błąd krytyczny podczas uruchamiania aplikacji GUI.")
        print(f"Typ błędu: {type(exc).__name__}")
        print(f"Szczegóły: {exc}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())