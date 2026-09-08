# OOKULAR — klient web

Działający podblok kont znajduje się w `backend/templates` i `backend/static/accounts`.
Django renderuje formularze rejestracji, logowania, potwierdzania e-mail i odzyskiwania
hasła. Formularze działają bez JS; JS dodaje pokazanie/ukrycie hasła. CSS ma układ
na komputer i telefon. Nie ma zewnętrznych fontów, trackerów ani gotowych kont demo.

Główne wejście do rejestracji prowadzi pracownika, mniejszy link — pracodawcę.
Formularz pozwala jawnie zmienić rolę przed rejestracją. Logowanie jest wspólne.
Po zalogowaniu użytkownik widzi wyłącznie własny adres i role, zmianę danych konta
oraz wylogowanie. Całość kończy się na tym podbloku.

[Uruchomienie i trasy](../../docs/06-konta.md).
Oś czasu, kreator profilu, oferty i wiadomości pozostają kolejnymi etapami.
