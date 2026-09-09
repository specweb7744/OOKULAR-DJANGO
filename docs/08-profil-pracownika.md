# Blok 2A — prywatny szkic podstawowego profilu

Pracownik po zalogowaniu może rozpocząć profil, zapisać część odpowiedzi i wrócić
do nich w innej sesji lub z klienta mobilnego. To pierwszy krok kreatora. Nie ma
jeszcze publikacji, tagów, suwaków, doświadczenia, umiejętności ani dopasowania.

## Pola i zachowanie

| Pole | Znaczenie | Limit |
|---|---|---|
| `display_name` | Imię lub pseudonim do zwracania się do użytkownika | 80 znaków |
| `location` | Miejscowość, bez dokładnego adresu | 120 znaków |
| `desired_role` | Szukane stanowisko lub obszar pracy | 120 znaków |
| `career_goal` | Opis celu zawodowego | 1000 znaków |

Wszystkie cztery pola są opcjonalne. Można zapisać pusty szkic, później uzupełnić
lub wyczyścić pola. Tekst jest pozbawiany otaczających spacji. Formularz nie zapisuje
podczas pisania: użytkownik wybiera „Zapisz szkic”. Niezapisane zmiany nie przetrwają
zamknięcia strony. Dane zapisane w bazie pojawiają się przy kolejnym wejściu.

Szkic należy do jednego konta i zawsze jest prywatny. Nie ma listy profili ani
endpointu wybierającego cudze ID. Odczyt i zapis wymagają aktywnego konta,
potwierdzonego bieżącego e-maila i roli pracownika. Pracodawca ani flaga `is_staff`
nie omijają tej kontroli. Konto z obiema rolami może zarządzać własnym szkicem.
Model nie jest udostępniony w panelu administracyjnym; operator bazy nadal ma
techniczny dostęp do przechowywanych danych.

## Formularz web

Po zastosowaniu migracji otwórz `/konto/` i wybierz „Rozpocznij profil”.
Bezpośredni adres: `/konto/profil/`. Formularz używa sesji Django i tokenu CSRF.
Poprawny zapis przekierowuje do formularza i pokazuje potwierdzenie. Błędy walidacji
zwracają 400, zachowując wpisane wartości; konflikt zapisu zwraca 409.

W konflikcie formularz zachowuje wpisane odpowiedzi i prosi o skopiowanie zmian
przed wczytaniem aktualnego szkicu. Nie odświeża automatycznie rewizji ani nie
nadpisuje danych zapisanych w międzyczasie. Wyświetlany czas dotyczy ostatniego zapisu.

## API web/mobile

GET oraz PATCH `/api/v1/me/employee-profile/`. GET (także HEAD) nie tworzy rekordu.
Bez szkicu odpowiedź ma puste teksty, `revision: 0` oraz `updated_at: null`.

Pierwszy zapis, na przykład:

```json
{
  "revision": 0,
  "display_name": "Ala",
  "location": "Gdańsk",
  "career_goal": "Chcę zmienić branżę."
}
```

Odpowiedź 200 zawiera wszystkie pola oraz `revision`, `updated_at`, `status: "draft"`,
`visibility: "private"` i `schema_version: 1`. Te trzy ostatnie pola opisują obecny
stały zakres funkcji. Klient nie może ich zmienić ani podać właściciela rekordu.
Nieobsługiwane pola, wartości niebędące tekstem i przekroczenie limitów zwracają 400.

Każdy PATCH wymaga rewizji z ostatniego GET lub udanego PATCH. Ominięte pola
zachowują poprzednie wartości; pusty tekst czyści wskazane pole. Sprawdzenie rewizji
i aktualizacja odbywają się w pojedynczym warunkowym UPDATE bazy. Pierwszy zapis
chroni unikalna relacja do konta. Dwa urządzenia nie mogą zapisać tej samej rewizji:
starsze żądanie dostaje 409 z `code: "draft_conflict"` i `current_revision`.
Numer rewizji nie jest historią wersji ani kopią do przywrócenia.

Przeglądarka przekazuje cookie sesji i `X-CSRFToken`. Aplikacja natywna przekazuje
`X-Session-Token`; endpoint przyjmuje JSON. Wygaśnięcie sesji, zmiana hasła,
dezaktywacja lub utrata roli odbierają dostęp. Odpowiedzi mają `no-store`
i `Referrer-Policy: no-referrer`, również w przypadku odmowy dostępu.

Klient TypeScript:

```ts
const draft = await mobile.employeeProfile();
const saved = await mobile.saveEmployeeProfile({
  revision: draft.revision,
  desired_role: "Operator produkcji",
});
```

`createOokularClient` ma te same metody; zapis web otrzymuje token CSRF jako drugi
argument. `ApiError.status` zwraca kod HTTP, a `ApiError.details` treść błędu zapisu.
Po 409 należy pobrać aktualne dane i uzgodnić zmiany, bez automatycznego ponawiania.
Pełny kontrakt: [OpenAPI](../contracts/openapi.json).

## Uruchomienie i weryfikacja

Zainstalowane zależności pozostają bez zmian. Uruchom migracje nowej tabeli:

```sh
python manage.py migrate
python manage.py test backend --settings=config.settings.test
```

Testy obejmują zapis i wznowienie, częściowe aktualizacje i czyszczenie pól,
granice uprawnień, brak wyboru cudzych danych, walidację, CSRF, bezpieczne wyświetlanie
tekstu oraz unieważnienie dostępu. Rzeczywisty klient TypeScript wykonuje żądania
HTTP dla sesji natywnej i cookie z CSRF. PostgreSQL w CI sprawdza dodatkowo dwa
równoległe pierwsze zapisy i dwie równoległe aktualizacje tej samej rewizji.
Test równoległości jest pomijany na lokalnym SQLite.

Nie wykonano wdrożenia na VPS, testu fizycznego telefonu ani wysyłki prawdziwych
e-maili. Dostępne środowisko podglądu nie obsługuje Django, więc nie deklarujemy
ukończonego przeglądu wizualnego. Natywne ekrany i APK/IPA pozostają osobnym etapem.

Źródła implementacji: [warunkowy UPDATE Django](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#update),
[serializery DRF](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer).
