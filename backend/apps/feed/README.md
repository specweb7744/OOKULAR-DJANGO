# Oś czasu i ogłoszenia

Status: **zaplanowany moduł — funkcje jeszcze niewdrożone**.

Publiczna oś czasu, zwykłe wpisy i ogłoszenia. Widoczność, publikacja i moderacja; promowanie uruchamiane przez billing.

Etap: 4. Zależności: `accounts`, `moderation`.

Szczegóły granic i kryteria ukończenia: [mapa modułów](../../../docs/01-bloki.md) i [etapy](../../../docs/04-etapy.md).

Dodając funkcję, umieszczaj modele i logikę w tym module, a cienkie widoki HTTP w jego `views.py`. Publiczny endpoint wymaga jawnej decyzji o widoczności. Import modułu nie może wysyłać wiadomości, naliczać opłat ani uruchamiać AI.
