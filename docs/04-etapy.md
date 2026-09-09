# Etapy budowy i kryteria ukończenia

To kolejność zależności; nie deklaracja czasu realizacji.

| Etap | Zakres | Co sprawdzamy przed przejściem dalej |
|---|---|---|
| 0 — wykonany | Projekt Django, ustawienia, własny User, role, pierwsze API i katalog domen | Projekt startuje, migracje są spójne, prywatne endpointy odmawiają dostępu osobom nieuprawnionym. |
| 1 — bieżący | Konta web/mobile i zasady dostępu | Rejestracja, weryfikacja e-mail, logowanie, wylogowanie, reset hasła, unieważnianie sesji, ograniczenie prób, numeracja kont; testy obu klientów. |
| 2A — wykonany w kodzie | Prywatny szkic podstawowego profilu | Dane podstawowe, cel zawodowy, zapis i wznowienie przez web/API, odmowa dostępu innym osobom, konflikty równoległych zapisów. |
| 2B | Słowniki i dalsze kroki kreatora | Rozdzielenie doświadczenia i umiejętności, wersja pytań, widoczność każdego zakresu. |
| 3 | Firma i oferta | Zweryfikowane członkostwo rekrutera, wymagania stanowiska, warunki pracy, zgłoszenie kandydata. |
| 4 | Publiczna oś czasu i artykuły | Gość widzi tylko opublikowane treści; tworzenie i edycja mają uprawnienia; działa moderacja. |
| 5 | Wyszukiwarka | Frazy, filtry zawodowe, lokalizacja i paginacja; indeks nie ujawnia prywatnych ani cofniętych profili. |
| 6 | Matcher v1 | Zatwierdzone i wersjonowane kryteria oraz wagi, uzasadnienia, obsługa braków, powtarzalne wyniki dla danych testowych. |
| 7 | Społeczność, wiadomości, edukacja i powiadomienia | Blokady, dostęp uczestników rozmów, preferencje powiadomień i reguły publikacji materiałów. |
| 8 | Punkty, BLIK, promocje i prowizje | Testowe płatności, zwroty, podpisy webhooków, brak podwójnego naliczenia i ewidencja operacji. |
| 9 | Semantyka i dodatkowe AI | Poprawna interpretacja fraz, ograniczony zestaw danych, pomiar jakości, kontrola kosztów i wersji integracji. |
| 10 | Uruchomienie produkcyjne | Kopie zapasowe i odtworzenie, monitoring, dostarczanie poczty, gotowość obsługi zgłoszeń, test obciążenia i ustalone środowisko. |

Prywatność, dostęp i moderacja są pracą przekrojową każdego etapu. Nie czekają na końcowy
moduł. Ekrany web/mobile rosną razem z tymi funkcjami i używają tego samego API.

## Stan bieżącej paczki

Działają rejestracja obu ról, weryfikacja e-mail, logowanie, wylogowanie, reset i zmiana
hasła, sesje mobilne oraz ograniczenie prób. Interfejs kont jest responsywny; klient
TypeScript korzysta z rzeczywistego API. Szczegóły: [blok kont](06-konta.md).

Dodano [prywatny szkic profilu pracownika](08-profil-pracownika.md). Nie ma jeszcze
publikacji, wyszukiwania profili ani pełnego kreatora zawodowego.

Etap 1 ma zakończony podblok uwierzytelniania. Oddzielnie pozostają reguła numeracji
publicznych kont i natywne ekrany. Poczta ma konfigurację SMTP; lokalnie trafia do
konsoli, a w testach do pamięci. Rzeczywistego dostarczania na domenie nie sprawdzono.
`runserver` służy do pracy lokalnej.

Produkcja ma osobną konfigurację wymagającą PostgreSQL, konkretnej listy hostów i mocnego
sekretu. To szablon konfiguracji, a nie dowód spełnienia wszystkich wymagań wdrożenia.

Pierwsze uruchomienie lokalne korzysta z SQLite, aby obejrzeć fundament bez instalacji
bazy. W docelowym środowisku i drugiej ścieżce CI stosujemy PostgreSQL.
Obsługa indeksów pełnotekstowych i pgvector nie została jeszcze zaimplementowana.

## Zgodność środowiska

Projekt jest przygotowany dla Python 3.12 i Django 5.2 LTS.
Django 5.2 jest wydaniem z przedłużonym wsparciem; wymaga nowszego Pythona niż 3.9.
[Django 5.2](https://docs.djangoproject.com/en/5.2/releases/5.2/),
[cykl wsparcia](https://www.djangoproject.com/download/).

Odczyt użytkownika potwierdził Python 3.9.6 na Hostingu Biznes. W odpowiedzi przekazanej
przez użytkownika home.pl wykluczyło na tej usłudze własny interpreter Python 3.12
oraz uruchamianie Django przez WSGI/ASGI; dostawca wskazał VPS lub serwer dedykowany.
Wdrożenie wymaga osobnego, zgodnego środowiska. Nie zakupiono ani nie skonfigurowano VPS,
nie potwierdzono przypisania domeny i nie wykonano wdrożenia produkcyjnego.
