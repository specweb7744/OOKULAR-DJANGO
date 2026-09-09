# Podgląd kont i przygotowanie testu poczty

## Wykonane w tym kroku

Powiększono opisy, etykiety, pomoc do hasła, komunikaty błędów i wejście pracodawcy.
Podstawowy tekst ma 16 px, etykiety 14 px, a pomoc 13 px przy domyślnym rozmiarze
czcionki przeglądarki. Rozmiary zapisano w `rem`. Wybór roli układa się w jedną
lub dwie kolumny zależnie od miejsca wewnątrz formularza. Przycisk pokazywania hasła
aktualizuje nazwę dostępną dla czytnika ekranu. Powiększono pola dotykowe i zapewniono
zawijanie nagłówków oraz stopki na wąskim ekranie.

Podgląd w rozmowie powstał z rzeczywistych odpowiedzi GET Django: logowania,
rejestracji pracownika, rejestracji pracodawcy i odzyskiwania hasła. Pozwala przełączyć
ekran i szerokość. Służy do oceny wyglądu: formularze są nieaktywne i nie zawierają
tokenów CSRF. Rejestracja i wysyłka poczty odbywają się wyłącznie w uruchomionej aplikacji.

Po zmianach przechodzi 48 testów kont, w tym klient TypeScript przeciw serwerowi HTTP.
Kontrola Ruff i składni JavaScript także zakończyła się powodzeniem. Każdy z czterech
ekranów zwrócił HTTP 200. Nie przeprowadzono przeglądu renderowania w przeglądarce ani
testu na fizycznym telefonie: dostępne środowisko podglądu nie obsługuje serwera Django.

## Kolejny krok: środowisko w home.pl

Aktualizacja po diagnostyce: użytkownik potwierdził przez SSH Python 3.9.6, a home.pl
w przekazanej odpowiedzi wykluczyło uruchomienie tego Django na Hostingu Biznes.
Docelowe wdrożenie wymaga VPS lub serwera dedykowanego. Nie wykonano zakupu ani
konfiguracji. Przypisanie domeny do serwera nie zostało potwierdzone.

Zachowujemy home.pl jako dostawcę hostingu, domeny i poczty. Główny adres portalu to
`https://www.ookular.pl`; `ookular.pl` ma do niego przekierowywać. Ta zmiana nie wdraża
aplikacji ani nie zmienia DNS.

Wcześniejszy odczyt na hostingu wskazywał Python 3.9.6 i Django 4.2.30. Trzeba ponownie
sprawdzić wersje w środowisku, z którego faktycznie korzysta proces aplikacji.
Repozytorium i CI używają Python 3.12 oraz Django 5.2. Samo utworzenie nowego venv
nie zmienia wersji interpretera. Django 5.2 nie obsługuje Pythona 3.9:
[oficjalna tabela zgodności](https://docs.djangoproject.com/en/5.2/faq/install/#what-python-version-can-i-use-with-django).

W istniejącym terminalu SSH można wykonać odczyt:

```sh
python3 --version
python3.12 --version
```

Brak polecenia `python3.12` oznacza brak tej nazwy w PATH, a nie dowód, że dostawca
nie udostępnia innej ścieżki. Należy ustalić z home.pl dostęp do Python 3.12,
PostgreSQL i sposobu uruchamiania procesu WSGI/ASGI dla posiadanej usługi.
Po wskazaniu właściwego interpretera należy utworzyć osobne środowisko dla nowej
wersji aplikacji i przejść uruchomienie opisane w README.

## Poczta: dane wymagane przed pierwszą wysyłką

W bieżącym środowisku nie ma skonfigurowanego hosta, użytkownika ani hasła SMTP.
Wzór zmiennych znajduje się w `.env.example`; hasło trafia do ustawień środowiska
serwera, nigdy do repozytorium ani rozmowy.

| Ustawienie | Skąd je wziąć |
|---|---|
| `EMAIL_HOST`, `EMAIL_PORT`, tryb TLS/SSL | Konfiguracja konkretnej skrzynki w panelu home.pl. |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Dane istniejącej skrzynki nadawczej. |
| `DEFAULT_FROM_EMAIL` | Ustalony adres tej skrzynki; nie zakładamy, że `noreply` istnieje. |
| `OOKULAR_PUBLIC_ORIGIN` | `https://www.ookular.pl`, gdy ta wersja aplikacji rzeczywiście obsługuje domenę. |
| Odbiorca testu | Wskazana skrzynka użytkownika, na której można otworzyć otrzymany link. |

Backend poczty: `django.core.mail.backends.smtp.EmailBackend`. Włącza się dokładnie
jeden tryb: `EMAIL_USE_TLS` lub `EMAIL_USE_SSL`, zgodnie z konfiguracją skrzynki.
Samo ustawienie adresu portalu nie uruchamia aplikacji pod tą domeną.

## Przejście przez prawdziwy e-mail

1. W uruchomionym środowisku zarejestrować konto pracownika na wskazanej skrzynce.
2. Otworzyć otrzymany link, potwierdzić adres przyciskiem i zalogować się. Sprawdzić rolę.
3. Wylogować się, poprosić o reset hasła i ustawić nowe hasło z otrzymanego linku.
   Sprawdzić logowanie nowym hasłem i odrzucenie starego oraz ponownego użycia linku.
4. Powtórzyć rejestrację i potwierdzenie dla roli pracodawcy na drugim adresie testowym.
5. Przejść te same ekrany na komputerze i telefonie: bez poziomego przewijania,
   z czytelną pomocą, dostępnymi przyciskami i widocznym fokusem klawiatury.

Powyższe kroki nie zostały jeszcze wykonane na rzeczywistych skrzynkach.
Niezależnie od oczekiwania na serwer dodano w kodzie [podstawowy profil pracownika](08-profil-pracownika.md):
dane podstawowe, cel zawodowy oraz zapis i wznowienie szkicu. Testy realnej poczty
i uruchomienie internetowe nadal pozostają do wykonania.
