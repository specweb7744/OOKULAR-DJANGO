# Silnik dopasowania

Status: **zaplanowany moduł — funkcje jeszcze niewdrożone**.

Własne, wersjonowane reguły dopasowania do stanowiska, uzasadnienia i brak danych. Bez arbitralnego wyniku ani oceny wartości człowieka.

Etap: 6. Zależności: `profiles`, `jobs`, `taxonomy`, `privacy`.

Szczegóły granic i kryteria ukończenia: [mapa modułów](../../../docs/01-bloki.md) i [etapy](../../../docs/04-etapy.md).

Dodając funkcję, umieszczaj modele i logikę w tym module, a cienkie widoki HTTP w jego `views.py`. Publiczny endpoint wymaga jawnej decyzji o widoczności. Import modułu nie może wysyłać wiadomości, naliczać opłat ani uruchamiać AI.
