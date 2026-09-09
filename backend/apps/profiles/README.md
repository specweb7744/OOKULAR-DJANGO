# Kreator profilu pracownika

Status: **częściowo wdrożony — prywatny szkic podstaw i celu zawodowego**.

Formularz `/konto/profil/` i GET/PATCH `/api/v1/me/employee-profile/` obsługują imię
lub pseudonim, miejscowość, szukane stanowisko i cel zawodowy. Zapis jest częściowy,
prywatny i chroniony przed nadpisaniem nowszej wersji. Każdy odczyt i zapis wymaga
aktywnego, zweryfikowanego konta z rolą pracownika; dotyczy wyłącznie właściciela.

Tagi, suwaki, doświadczenie oddzielone od umiejętności i kontrolowana publikacja
profilu pozostają kolejnymi krokami. Dane tego szkicu nie trafiają do Matchera.

Implementacja i scenariusze: [podstawowy profil](../../../docs/08-profil-pracownika.md).

Etap: 2A. Obecna zależność: `accounts`. Kolejne kroki wykorzystają `taxonomy` i `privacy`.

Szczegóły granic i kryteria ukończenia: [mapa modułów](../../../docs/01-bloki.md) i [etapy](../../../docs/04-etapy.md).

Dodając funkcję, umieszczaj modele i logikę w tym module, a cienkie widoki HTTP w jego `views.py`. Publiczny endpoint wymaga jawnej decyzji o widoczności. Import modułu nie może wysyłać wiadomości, naliczać opłat ani uruchamiać AI.
