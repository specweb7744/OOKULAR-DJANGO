# Blok 1A — rejestracja i logowanie OOKULAR

Ten dokument opisuje podblok kont pracownika i pracodawcy. Kolejny wykonany krok
opisuje [prywatny szkic profilu](08-profil-pracownika.md). Firmy, oferty i dopasowanie
pozostają kolejnymi etapami.

## Co działa

| Funkcja | Przeglądarka | API dla aplikacji natywnej |
|---|---|---|
| Rejestracja pracownika lub pracodawcy | Formularz z wyborem roli | JSON z `role: employee` albo `employer` |
| Potwierdzenie adresu | Link ważny 24 h, potwierdzenie przyciskiem POST | Klucz z tego samego linku |
| Ponowna wysyłka | Formularz e-mail, wspólny komunikat | Ogólna odpowiedź 200 |
| Logowanie | E-mail, hasło, opcja zapamiętania | E-mail, hasło, `X-Session-Token` |
| Wylogowanie | Formularz POST | DELETE sesji |
| Odzyskanie hasła | Jednorazowy link ważny godzinę | Żądanie i wykonanie resetu przez API |
| Zmiana hasła | Obecne hasło i dwukrotne nowe | Obecne i nowe hasło |
| Własne konto | Własny adres, rola i stan weryfikacji | `/api/v1/me/` |
| Zmiana adresu | Nowy adres wymaga potwierdzenia | Mechanizm allauth; opis głównego podbloku dotyczy rejestracji i logowania |

Ekrany webowe są responsywne i działają bez JavaScript. JavaScript służy wyłącznie
do pokazania hasła i ustawienia fokusu na błędnym polu. Natywne ekrany React Native
oraz paczki APK/IPA nie należą do tej zmiany. Klient TypeScript rzeczywiście
łączy się z API; nie jest makietą uwierzytelnienia.

[Podgląd kont i test poczty](07-podglad-i-poczta.md) opisuje poprawki czytelności,
ograniczenia podglądu oraz kolejny krok dla istniejącego hostingu w home.pl.

## Uruchomienie i ręczne przejście

Po standardowym uruchomieniu z głównego README otwórz:

| Adres lokalny | Ekran |
|---|---|
| `http://127.0.0.1:8000/konta/login/` | Wspólne logowanie |
| `http://127.0.0.1:8000/konta/signup/` | Rejestracja, domyślnie pracownik |
| `http://127.0.0.1:8000/konta/signup/?role=employer` | Rejestracja, wybrany pracodawca |
| `http://127.0.0.1:8000/konta/potwierdz-ponownie/` | Ponowna wysyłka potwierdzenia |
| `http://127.0.0.1:8000/konta/password/reset/` | Odzyskiwanie hasła |
| `http://127.0.0.1:8000/konto/` | Własne konto po logowaniu |

1. Wybierz rolę, podaj adres i hasło o długości co najmniej 12 znaków.
2. Odczytaj link z konsoli `runserver`; lokalny backend poczty niczego nie wysyła.
3. Otwórz link i naciśnij „Potwierdzam adres e-mail”. Sam GET nie aktywuje adresu.
4. Zaloguj się. Strona konta pokaże wyłącznie własny adres i rolę.
5. Wyloguj się, a następnie sprawdź odzyskiwanie hasła analogicznie linkiem z konsoli.

Istniejące środowisko należy zaktualizować przez `pip install -r requirements.txt`
i `python manage.py migrate`. Migracje dodają tabele allauth i współdzielony cache.
Nie tworzymy przykładowych kont ani wspólnego hasła. Administracja także korzysta
z formularza OOKULAR; nowe konto `createsuperuser` potwierdza adres przy pierwszym logowaniu.

## Rola i uprawnienia

Rejestracja tworzy konto, wybraną rolę i adres e-mail w jednej transakcji.
Nie tworzy profilu firmy ani profilu zawodowego. Rola pracodawcy nie daje dostępu
administracyjnego ani uprawnień do cudzej firmy. E-mail jest normalizowany do małych
liter; unikalność wymusza również baza danych.

Powtórna rejestracja istniejącego adresu daje ogólny ekran weryfikacji i nie zmienia
jego hasła ani ról. Ta sama obsługa dotyczy konfliktu dwóch równoczesnych zapisów.
Model dopuszcza dwie role w przyszłości, ale samodzielne dodawanie drugiej roli
nie zostało włączone. Dane konta nie przyjmują parametrów `is_staff`/`is_superuser`.

API wymaga aktywnego konta i potwierdzenia bieżącego adresu e-mail. Ma też osobną
kontrolę uprawnień administracyjnych. Nadpisując domyślne permissions w nowym module,
trzeba zachować `HasVerifiedAccount` dla prywatnych funkcji.

## Sesje mobilne

Prefiks: `/api/auth/app/v1/`; nazwy endpointów nie mają końcowego ukośnika.
Kontrakt: [OpenAPI](../contracts/openapi.json).

| Metoda | Ścieżka po prefiksie | Pola JSON |
|---|---|---|
| POST | `auth/signup` | `email`, `password`, `role` |
| POST | `auth/login` | `email`, `password` |
| GET / DELETE | `auth/session` | brak |
| POST | `auth/email/verify` | `key` |
| POST | `auth/email/verify/resend` | `email` |
| POST | `auth/password/request` | `email` |
| POST | `auth/password/reset` | `key`, `password` |
| POST | `account/password/change` | `current_password`, `new_password` |

JSON ma `status`, opcjonalne `data`, `meta` i `errors`. HTTP 401 po rejestracji
z `verify_email` w `data.flows` oznacza oczekiwanie na potwierdzenie, a nie błąd
utworzenia konta. Zapamiętaj `meta.session_token`, również dla sesji oczekującej,
i przekazuj w `X-Session-Token`. Sesja oczekująca nie daje dostępu do `/api/v1/me/`.
Po potwierdzeniu zaloguj się; token zostanie obrócony i zastąpi poprzedni.

HTTP 401 po DELETE oznacza poprawne wylogowanie. HTTP 410 oznacza usuniętą sesję.
HTTP 400 to błędy pól, 409 — niepasujący etap, 429 — limit prób. Klient obsługuje
te stany i serializuje operacje, aby zapis tokenu nie ścigał się z wylogowaniem.

`createMobileAuthClient(origin, store)` otrzymuje magazyn z asynchronicznymi metodami
`get()` i `set(token | null)`. W aplikacji podłącz Keychain/Keystore. Nie używaj
localStorage ani zwykłego pliku. Aplikacja otrzymuje tylko token własnej sesji;
sekrety Django i SMTP pozostają na serwerze.

API natywne ignoruje cookies przeglądarki i przyjmuje JSON. Web korzysta z formularzy
Django i CSRF. Nie otwieramy CORS dla dowolnych domen. Odnośniki e-mail otwierają
Django również na telefonie; deep linki będą dodane z natywnymi ekranami.

## Zabezpieczenia uwierzytelnienia

- Hasła są hashowane przez Django. Minimum 12 znaków, walidacja popularnych,
  całkowicie numerycznych i zbyt podobnych do adresu haseł.
- Potwierdzenie e-mail wymaga POST. Reset jest jednorazowy. Linki używają
  `OOKULAR_PUBLIC_ORIGIN`, nie dowolnego nagłówka Host.
- Zmiana/reset hasła unieważnia dostęp starych sesji przy następnym żądaniu,
  zarówno cookies, jak i tokenów API. Logowanie obraca identyfikator sesji.
- Opcja „zapamiętaj” utrzymuje sesję do 14 dni; bez niej cookie jest sesyjne.
  Natywne sesje mają limit 14 dni. Wylogowanie kończy sesję danego urządzenia.
- Prywatne odpowiedzi mają `Cache-Control: no-store` i `Referrer-Policy: no-referrer`.
  Formularze wymagają CSRF; przekierowania poza dozwolony serwis są odrzucane.
- Ograniczenia obejmują IP, adres oraz nieudane logowania. Cache jest w bazie,
  wspólny dla procesów, tworzony migracją. Limity allauth są przybliżone przy
  równoległych żądaniach; nie są twardym limitem połączeń na brzegu sieci.
- `X-Forwarded-For` domyślnie nie jest zaufany. `ALLAUTH_TRUSTED_PROXY_COUNT`
  konfiguruj dopiero po sprawdzeniu rzeczywistego łańcucha proxy.

## Poczta i produkcja

Lokalnie: console. Testy: locmem. W produkcji wymagamy SMTP i ustawień:
`EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`, `EMAIL_HOST`, `EMAIL_PORT`,
`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, właściwego `DEFAULT_FROM_EMAIL` oraz jednej
opcji `EMAIL_USE_TLS` albo `EMAIL_USE_SSL`. Wzór znajduje się w `.env.example`.
Sekrety wpisuj tylko do środowiska serwera; nie do kodu ani aplikacji mobilnej.

`OOKULAR_PUBLIC_ORIGIN` ustaw na docelowy adres HTTPS portalu, bez ścieżki.
Ustawienia produkcyjne wymagają PostgreSQL, listy hostów, mocnego sekretu i konfiguracji
poczty. Statyczne pliki po `collectstatic` musi obsłużyć serwer wdrożenia. Ustalona
konfiguracja proxy musi także prawidłowo przekazywać informację o HTTPS.

Dostarczanie poczty i prawidłowe dane SMTP nie były sprawdzane na prawdziwej domenie.
Wysyłka jest synchroniczna: błąd dostawcy nie oznacza cofnięcia utworzonego konta;
po przywróceniu SMTP można ponownie wysłać link. Kolejka z ponawianiem dostaw
jest częścią przyszłego wdrożenia, nie tego podbloku. Brak publicznego wdrożenia
ani migracji rzeczywistych danych w tej zmianie.

Przed otwarciem produkcyjnej rejestracji pozostaje ustalenie preferowanej reguły
numeracji kont. Techniczne ID nadal jest BigAutoField; na ekranie konta go nie pokazujemy.

## Weryfikacja i źródła

Zestaw `manage.py test backend --settings=config.settings.test` obejmuje oba typy
rejestracji, kompletne przepływy web i API, ponowną rejestrację, błędy walidacji,
CSRF, tokeny, role, linki, ograniczenia prób i utratę dostępu po zmianie hasła.
`test_client.py` uruchamia klienta TypeScript przeciw prawdziwemu serwerowi HTTP;
CI ma Node 24 i powtarza zestaw również na PostgreSQL.

Wykorzystujemy mechanizmy aktualnego django-allauth, zamiast kodu logowania ze starego
wydania RailsSpace: [konfiguracja kont](https://docs.allauth.org/en/latest/account/configuration.html),
[instalacja API](https://docs.allauth.org/en/latest/headless/installation.html),
[sesje mobilne](https://docs.allauth.org/en/latest/headless/tokens.html),
[cache Django](https://docs.djangoproject.com/en/5.2/topics/cache/#database-caching).
