# OOKULAR — klient webowy

Status: zaplanowana powierzchnia aplikacji; w tym etapie nie ma jeszcze interfejsu portalu.

Publiczne ekrany: strona główna z osią czasu i ogłoszeniami, artykuły branżowe, edukacja.
Główne wejście do konta prowadzi pracownika. Mniejsze wejście „Dla pracodawców” prowadzi do informacji, cennika i panelu firmowego.

Ekrany po zalogowaniu: kreator profilu, profil, ustawienia widoczności, oferty i dopasowania, wiadomości oraz powiadomienia.
Panel pracodawcy: firma, rekruterzy, wymagania stanowiska, wyszukiwarka i lista dopasowań.

API: `/api/v1/`; współdzielony klient w `packages/api-client`.
W pierwszym wdrożeniu web najlepiej utrzymać API pod tym samym adresem domenowym.
Tożsamość i reguły dopasowania należą do Django; nie powielamy ich w przeglądarce.

Styl: [system interfejsu](../../docs/03-interfejs.md).
