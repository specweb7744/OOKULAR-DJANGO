# OOKULAR — konta pracownika i pracodawcy v0.2

Pierwszy fundament portalu społecznościowo-zawodowego OOKULAR.
Jeden backend Django i wspólne API dla strony oraz przyszłej aplikacji mobilnej.

**Zacznij od [mapy bloków](docs/01-bloki.md)** i [przełożenia książki RailsSpace na OOKULAR](docs/00-ksiazka.md).

## Co jest wykonane

- Konfiguracja Django 5.2 LTS dla developmentu, testów i przyszłej produkcji.
- Własny model użytkownika od pierwszej migracji: e-mail, hashowane hasło, role pracownik/pracodawca.
- Rejestracja pracownika/pracodawcy, potwierdzanie i zmiana e-maila, logowanie, wylogowanie, reset i zmiana hasła.
- Polskie formularze dopasowane do komputera i telefonu, bez konieczności JavaScript.
- Sesje mobilne, limity prób i unieważnianie starych sesji po zmianie hasła.
- Administracja korzysta ze wspólnego logowania; role biznesowe nie nadają uprawnień administratora.
- Diagnostyka procesu i bazy; API własnego konta oraz katalog modułów dla administratora.
- 18 katalogów domen z opisanymi odpowiedzialnościami, zależnościami i stanem realizacji.
- Kontrakt OpenAPI oraz niewielki klient TypeScript wspólny dla web/mobile.
- Testy granic dostępu, walidacji i migracji; konfiguracja kontroli GitHub Actions dla SQLite i PostgreSQL.

**To fundament, nie gotowy portal ani APK.** Moduły profilu, wyszukiwania, Matchera,
treści, wiadomości, edukacji i płatności mają przygotowane miejsca i dokumentację;
ich funkcje nie są jeszcze wdrożone. Interfejs kont działa w przeglądarce, również mobilnej. Natywny klient ma obsługiwane
API i klienta TypeScript; ekrany React Native oraz APK/IPA są późniejszym zadaniem.
[Instrukcja bloku kont](docs/06-konta.md) opisuje bieżący zakres i testy.

## Uruchomienie na Windows — PowerShell

Wymagany Python 3.12. Otwórz PowerShell w pobranym katalogu OOKULAR-DJANGO:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/init_local.py
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Otwórz [logowanie OOKULAR](http://127.0.0.1:8000/konta/login/).
Wybierz rejestrację pracownika albo mniejsze wejście pracodawcy.
W trybie lokalnym link potwierdzający pojawi się w konsoli serwera. Otwórz go
w przeglądarce, potwierdź adres i zaloguj się. Wiadomości nie są wysyłane do Internetu.
Ten adres działa dopiero po uruchomieniu serwera na własnym komputerze.

Aby używać administracji, w drugim oknie PowerShell uruchom:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Otwórz [lokalną administrację](http://127.0.0.1:8000/admin/).
Logowanie przechodzi przez formularz OOKULAR; przy pierwszej próbie potwierdź e-mail
administratora linkiem z konsoli, a następnie ponownie otwórz `/admin/`.
Hasło podajesz interaktywnie. Paczka nie zawiera gotowego konta ani wspólnego hasła.

Na Linux/macOS: `python3.12 -m venv .venv`, a następnie te same polecenia,
używając `.venv/bin/python` zamiast `.\.venv\Scripts\python.exe`.

## Dane i środowiska

Lokalny start korzysta z SQLite. PostgreSQL jest bazą docelową.
Opcjonalny `compose.yaml` uruchamia lokalny PostgreSQL z obrazem zawierającym pgvector:
po utworzeniu `.env` wykonaj `docker compose up -d db`, następnie ustaw w `.env`
`DATABASE_URL=postgres://ookular:TWOJE_POSTGRES_PASSWORD@127.0.0.1:5432/ookular`
i uruchom migracje. Użyj losowego hasła z własnego `.env`, bez umieszczania go w kodzie.

Rozszerzenie i indeksy wektorowe będą dodane w etapie wyszukiwania semantycznego;
obecny szkielet ich nie wykorzystuje.

`scripts/init_local.py` generuje unikalne sekrety i zachowuje istniejący `.env`.
Pliki `.env`, lokalna baza, media i środowisko Pythona są wyłączone z repozytorium.

## Kontrola projektu

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe manage.py check --settings=config.settings.test
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run --settings=config.settings.test
.\.venv\Scripts\python.exe manage.py test backend --settings=config.settings.test
```

Testy przechodzą przez rejestrację obu ról, e-mail, logowanie, reset hasła, wygasanie
linków i sesji, CSRF oraz limity prób. Klient TypeScript jest sprawdzany przez HTTP
z rzeczywistym serwerem Django (wymaga Node 24; bez Node ten jeden test jest pomijany).
CI instaluje Node i uruchamia pełny zestaw również z PostgreSQL.

## Mapa plików

| Katalog | Zawartość |
|---|---|
| `backend/config` | Ustawienia, routing, ASGI i WSGI. |
| `backend/apps` | Domeny OOKULAR; stan każdej opisany w jej README. |
| `backend/api` | Wspólne API `/api/v1/`. |
| `backend/templates`, `backend/static` | Działający interfejs kont. |
| `clients/web`, `clients/mobile` | Opisy klientów i dalsze kroki. |
| `packages/api-client` | Wspólny klient TypeScript dla aktywnych endpointów. |
| `contracts` | Opis OpenAPI rzeczywiście dostępnych endpointów. |
| `docs` | Książka, bloki, silnik, interfejs, etapy i źródła. |

## Dalsza praca

Bieżący blok kończy się na kontach. Kolejny blok funkcjonalny to słowniki i kreator
profilu; nie został uruchomiony w tej zmianie. Preferowana numeracja publicznych kont
wymaga jeszcze ustalonej reguły. Nie wykonano wdrożenia pod domeną produkcyjną.
Kryteria ukończenia zawiera [plan etapów](docs/04-etapy.md).

[API i silnik](docs/02-api-i-silnik.md) · [Interfejs](docs/03-interfejs.md) ·
[Źródła i dobór narzędzi](docs/05-zrodla-i-narzedzia.md).
