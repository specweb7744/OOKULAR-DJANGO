# RailsSpace → OOKULAR

Źródłem są dostarczone zdjęcia spisu treści książki „RailsSpace”, strony spisu 5–12.
Nie jest to analiza pełnej treści rozdziałów ani przeniesienie kodu Ruby do Pythona.
Wykorzystujemy widoczny porządek zagadnień i przekładamy go na architekturę OOKULAR.

| Rozdziały widoczne na zdjęciach | Odpowiednik w OOKULAR | Zastosowanie |
|---|---|---|
| 2. Środowisko, pierwsze strony, URL, widoki i układy | Fundament oraz klient webowy | Konfiguracja, adresy, wspólny układ i nawigacja. |
| 3–4. Modelowanie i rejestrowanie użytkowników | Konta i role | Własny model konta, walidacje, rejestracja, rozdzielenie tożsamości i profilu. |
| 5. Rozpoczynamy testowanie | Sprawdzenie każdej funkcji | Testy dostępu i zachowania powstają wraz z odpowiednią funkcją. |
| 6–7. Logowanie, wylogowanie i zapamiętywanie użytkownika | Konta i sesje | Logowanie web/mobile, wygasanie i unieważnianie sesji, ochrona zmian przez CSRF w web. |
| 8. Aktualizacja informacji użytkownika | Ustawienia konta | Bezpieczna zmiana adresu e-mail i hasła, ponowne uwierzytelnienie przy ważnych zmianach. |
| 9. Profile osobiste | Kreator profilu pracownika | Tagi, suwaki, etapy, szkic, widoczność i osobna projekcja zawodowa. |
| 10. Społeczność i stronicowanie | Oś czasu i katalogi | Zasady publikacji, listy i paginacja. |
| 11. Wyszukiwanie i przeglądanie | Search oraz później Matcher | Frazy, filtry zawodowe, lokalizacja pracy i stronicowanie. Wiek i płeć z przykładu książki nie są kryteriami naszego Matchera. |
| 12. Awatary | Media profilu | Weryfikacja typu i rozmiaru pliku, usuwanie metadanych, kontrola widoczności. |
| 13. E-mail | Konta, powiadomienia i integracje | Weryfikacja e-mail i link jednorazowy do ustawienia nowego hasła; hasła nie są wysyłane pocztą. |
| 14. Znajomości | Relacje i wiadomości | Obserwowanie, zaproszenia, blokady, uprawnienia uczestników rozmów. |
| 15. Blogi i REST | Artykuły oraz API | Publikacja i edycja treści, wspólny kontrakt danych dla klientów. |
| 16. Komentarze, Ajax i efekty wizualne | Społeczność i interfejs | Komentarze, aktualizacja części ekranu, stany błędów i subtelne animacje. |
| 17. Produkcja, skalowanie i administracja | Utrzymanie | Kopie zapasowe, monitoring, proces wdrożeń i pomiar wydajności. |

OOKULAR rozszerza ten schemat o firmy, oferty pracy, własny Matcher, edukację, punkty i BLIK.
Prywatność i moderacja są uwzględniane od pierwszych funkcji.

Materiały wejściowe: osiem zdjęć `image-1788824239934.jpg`,
`image-1788824257287.jpg`, `image-1788824266014.jpg`,
`image-1788824277933.jpg`, `image-1788824286630.jpg`,
`image-1788824302124.jpg`, `image-1788824309803.jpg`,
`image-1788824319770.jpg`. Zdjęcia nie są dołączane do publicznego repozytorium.
