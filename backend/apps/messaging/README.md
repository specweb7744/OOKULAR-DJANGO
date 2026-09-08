# Wiadomości

Status: **zaplanowany moduł — funkcje jeszcze niewdrożone**.

Rozmowy i uczestnicy; dostęp wyłącznie do własnych rozmów. Blokady i zgłoszenia.

Etap: 7. Zależności: `accounts`, `social`, `moderation`.

Szczegóły granic i kryteria ukończenia: [mapa modułów](../../../docs/01-bloki.md) i [etapy](../../../docs/04-etapy.md).

Dodając funkcję, umieszczaj modele i logikę w tym module, a cienkie widoki HTTP w jego `views.py`. Publiczny endpoint wymaga jawnej decyzji o widoczności. Import modułu nie może wysyłać wiadomości, naliczać opłat ani uruchamiać AI.
