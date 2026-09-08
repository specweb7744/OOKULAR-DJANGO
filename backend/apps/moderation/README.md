# Moderacja i zgłoszenia

Status: **zaplanowany moduł — funkcje jeszcze niewdrożone**.

Decyzje moderatorów, zgłoszenia i audyt. Podstawowe zasady dostępu obowiązują od pierwszych funkcji.

Etap: 1. Zależności: `accounts`.

Szczegóły granic i kryteria ukończenia: [mapa modułów](../../../docs/01-bloki.md) i [etapy](../../../docs/04-etapy.md).

Dodając funkcję, umieszczaj modele i logikę w tym module, a cienkie widoki HTTP w jego `views.py`. Publiczny endpoint wymaga jawnej decyzji o widoczności. Import modułu nie może wysyłać wiadomości, naliczać opłat ani uruchamiać AI.
