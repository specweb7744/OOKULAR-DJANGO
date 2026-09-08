# Konta i role

Status: **fundament działa; zakres opisany w głównym README**.

Tożsamość konta i role pracownik/pracodawca. Rejestracja, weryfikacja e-mail, odzyskiwanie dostępu i sesje mobilne są następnym etapem.

Etap: 1. Zależności: `core`.

Szczegóły granic i kryteria ukończenia: [mapa modułów](../../../docs/01-bloki.md) i [etapy](../../../docs/04-etapy.md).

Dodając funkcję, umieszczaj modele i logikę w tym module, a cienkie widoki HTTP w jego `views.py`. Publiczny endpoint wymaga jawnej decyzji o widoczności. Import modułu nie może wysyłać wiadomości, naliczać opłat ani uruchamiać AI.
