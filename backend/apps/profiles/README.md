# Kreator profilu pracownika

Status: **zaplanowany moduł — funkcje jeszcze niewdrożone**.

Wieloetapowy kreator, szkic i wznawianie, tagi, suwaki, doświadczenie oddzielone od umiejętności, kontrolowana publikacja profilu.

Etap: 2. Zależności: `accounts`, `taxonomy`, `privacy`.

Szczegóły granic i kryteria ukończenia: [mapa modułów](../../../docs/01-bloki.md) i [etapy](../../../docs/04-etapy.md).

Dodając funkcję, umieszczaj modele i logikę w tym module, a cienkie widoki HTTP w jego `views.py`. Publiczny endpoint wymaga jawnej decyzji o widoczności. Import modułu nie może wysyłać wiadomości, naliczać opłat ani uruchamiać AI.
