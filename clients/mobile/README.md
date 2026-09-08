# OOKULAR — klient mobilny

Status: kontrakt i miejsce na klienta; nie jest to jeszcze uruchamialna aplikacja ani APK/IPA.

Korzysta z tych samych kont, profili, treści i reguł dopasowania co web poprzez `/api/v1/`.
Wspólny klient TypeScript jest w `packages/api-client`. Jego publiczne `status()` nie wymaga logowania.
Mobilne uwierzytelnienie będzie wdrożone i sprawdzone w etapie kont; w szkielecie nie udajemy obsługi tokenów.

Proponowany późniejszy klient: React Native / Expo, po zatwierdzeniu zakresu pierwszych ekranów.
Nawigacja funkcjonalna: Start, Oferty, Wiadomości, Profil. Moduł powiadomień jest dostępny z górnego paska.
Po wyborze roli pracodawcy: firma i wyszukiwanie kandydatów, z kontrolą członkostwa po stronie Django.

Szkic profilu zapisuje się na serwerze; po zmianie urządzenia użytkownik wznawia ten sam etap.
Na telefonie nie przechowujemy kluczy usług AI ani płatności.
Nie wywołujemy lokalnego serwera telefonu pod `localhost`, gdy backend działa na komputerze:
środowisko mobilne otrzyma jawnie ustawiony adres osiągalnego API.
