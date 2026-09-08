# Interfejs OOKULAR — kierunek dla web i mobile

Status: założenia wizualne i funkcjonalne; finalne ekrany nie są jeszcze wykonane.

OOKULAR ma mieć elegancki, nowoczesny interfejs o jakości aplikacji systemowej:
dopracowane proporcje, czytelne warstwy, zaokrąglenia, subtelne wypukłości i
płynne reakcje na dotyk. Spójność obejmuje również błędy, puste listy, postęp
zapisywania oraz widoki na małych ekranach.

Podstawą będą wspólne reguły kolorów, typografii, odstępów i komponentów — podejście
opisane także w [zasadach projektowania Base44](https://docs.base44.com/Building-your-app/Design-foundations-and-layout).
Base44 jest źródłem inspiracji projektowych. Backend projektu powstaje w Django.

## Układ portalu

| Powierzchnia | Główne bloki |
|---|---|
| Publiczna strona główna | Oś czasu i ogłoszenia; wejścia do artykułów oraz edukacji; główne logowanie pracownika. |
| Mniejsze wejście „Dla pracodawców” | Informacje, cennik, logowanie i panel firmowy. |
| Panel pracownika | Postęp profilu, kreator, oferty i dopasowania, wiadomości, ustawienia prywatności. |
| Panel pracodawcy | Firma, wymagania stanowiska, wyszukiwanie naturalną frazą i jawne filtry, dopasowania z uzasadnieniami. |
| Mobile | Te same zadania, układ dopasowany do dotyku; kreator podzielony na krótsze kroki. |

## Wspólne elementy

- Tokeny kolorów, odstępów, typografii, zaokrągleń, cieni i ruchu.
- Karty wpisu, profilu, oferty i dopasowania; przyciski i pola z rozpoznawalnymi stanami.
- Kreator: widoczny etap, zapis szkicu, cofanie i wznawianie; wybory ABC, tagi oraz suwaki
  stosowane zgodnie z sensem danego pytania.
- Widoczny fokus klawiatury, odpowiedni kontrast, duże pola dotykowe i respektowanie
  preferencji ograniczenia animacji.
- Oryginalne logo OOKULAR i jego subtelny globus należy włączyć z zatwierdzonych plików marki.
  Spis treści książki nie zawiera tych plików; nie tworzymy zastępczego logo.

Szczegółowe kolory zostaną dopasowane do zatwierdzonego logo. Kierunek roboczy:
głęboki granat, niebieski/turkus i jasne powierzchnie, z oszczędnym akcentem barwnym.
Wersja webowa i mobilna współdzielą język wizualny, ale nawigację dopasowujemy do urządzenia.
