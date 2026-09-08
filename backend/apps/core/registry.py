"""Internal map. Planned entries expose no business endpoints."""

MODULES = [
    {
        "id": "core",
        "title": "Fundament",
        "status": "foundation",
        "phase": 0,
        "dependencies": [],
        "responsibility": "Konfiguracja, diagnostyka działania, wspólne API i katalog modułów.",
    },
    {
        "id": "accounts",
        "title": "Konta i role",
        "status": "implemented",
        "phase": 1,
        "dependencies": ["core"],
        "responsibility": "Rejestracja pracownika i pracodawcy, potwierdzanie e-mail, "
        "logowanie, reset hasła oraz sesje web i mobilne.",
    },
    {
        "id": "taxonomy",
        "title": "Słowniki i kryteria",
        "status": "planned",
        "phase": 2,
        "dependencies": ["core"],
        "responsibility": "Wersjonowane słowniki umiejętności, uprawnień i warunków pracy; "
        "oddzielenie informacji prywatnych od kryteriów zawodowych.",
    },
    {
        "id": "profiles",
        "title": "Kreator profilu pracownika",
        "status": "planned",
        "phase": 2,
        "dependencies": ["accounts", "taxonomy", "privacy"],
        "responsibility": "Wieloetapowy kreator, szkic i wznawianie, tagi, suwaki, "
        "doświadczenie oddzielone od umiejętności, kontrolowana publikacja "
        "profilu.",
    },
    {
        "id": "organizations",
        "title": "Firmy i członkostwa",
        "status": "planned",
        "phase": 3,
        "dependencies": ["accounts", "privacy"],
        "responsibility": "Profil firmy, weryfikacja oraz członkostwa i uprawnienia "
        "rekruterów. Rola pracodawcy nie daje automatycznie dostępu do "
        "każdej firmy.",
    },
    {
        "id": "jobs",
        "title": "Oferty i aplikacje",
        "status": "planned",
        "phase": 3,
        "dependencies": ["organizations", "taxonomy", "profiles"],
        "responsibility": "Wymagania stanowiska, warunki zatrudnienia i zgłoszenia kandydatów.",
    },
    {
        "id": "feed",
        "title": "Oś czasu i ogłoszenia",
        "status": "planned",
        "phase": 4,
        "dependencies": ["accounts", "moderation"],
        "responsibility": "Publiczna oś czasu, zwykłe wpisy i ogłoszenia. Widoczność, "
        "publikacja i moderacja; promowanie uruchamiane przez billing.",
    },
    {
        "id": "content",
        "title": "Artykuły branżowe",
        "status": "planned",
        "phase": 4,
        "dependencies": ["accounts", "moderation"],
        "responsibility": "Treści redakcyjne, kategorie, autorzy i publikacja artykułów "
        "dostępnych bez konta.",
    },
    {
        "id": "education",
        "title": "Edukacja",
        "status": "planned",
        "phase": 7,
        "dependencies": ["content"],
        "responsibility": "Katalog materiałów i ofert edukacyjnych oraz ewidencja prowizji "
        "po ustaleniu modelu rozliczeń.",
    },
    {
        "id": "search",
        "title": "Wyszukiwarka",
        "status": "planned",
        "phase": 5,
        "dependencies": ["profiles", "jobs", "taxonomy", "privacy"],
        "responsibility": "Frazy, filtry i paginacja; następnie semantyka. Pobiera tylko "
        "dozwoloną, opublikowaną projekcję zawodową.",
    },
    {
        "id": "matching",
        "title": "Silnik dopasowania",
        "status": "planned",
        "phase": 6,
        "dependencies": ["profiles", "jobs", "taxonomy", "privacy"],
        "responsibility": "Własne, wersjonowane reguły dopasowania do stanowiska, "
        "uzasadnienia i brak danych. Bez arbitralnego wyniku ani oceny "
        "wartości człowieka.",
    },
    {
        "id": "social",
        "title": "Relacje i reakcje",
        "status": "planned",
        "phase": 7,
        "dependencies": ["accounts", "privacy", "moderation"],
        "responsibility": "Obserwowanie, zaproszenia, blokady i reakcje. Zasady ocen i "
        "weryfikacji wymagają osobnej implementacji.",
    },
    {
        "id": "messaging",
        "title": "Wiadomości",
        "status": "planned",
        "phase": 7,
        "dependencies": ["accounts", "social", "moderation"],
        "responsibility": "Rozmowy i uczestnicy; dostęp wyłącznie do własnych rozmów. "
        "Blokady i zgłoszenia.",
    },
    {
        "id": "notifications",
        "title": "Powiadomienia",
        "status": "planned",
        "phase": 7,
        "dependencies": ["accounts", "privacy"],
        "responsibility": "Preferencje i dostarczanie powiadomień w aplikacji, e-mailem oraz push.",
    },
    {
        "id": "billing",
        "title": "Punkty, BLIK i rozliczenia",
        "status": "planned",
        "phase": 8,
        "dependencies": ["accounts"],
        "responsibility": "Portfel punktów i dziennik operacji; potwierdzenia płatności, "
        "zwroty, idempotencja i promocje. Dostawca niepodłączony.",
    },
    {
        "id": "moderation",
        "title": "Moderacja i zgłoszenia",
        "status": "planned",
        "phase": 1,
        "dependencies": ["accounts"],
        "responsibility": "Decyzje moderatorów, zgłoszenia i audyt. Podstawowe zasady "
        "dostępu obowiązują od pierwszych funkcji.",
    },
    {
        "id": "privacy",
        "title": "Prywatność i widoczność",
        "status": "planned",
        "phase": 1,
        "dependencies": ["accounts"],
        "responsibility": "Cele użycia danych, zakresy widoczności, eksport i usuwanie oraz "
        "projekcja informacji dopuszczonych do dopasowania.",
    },
    {
        "id": "integrations",
        "title": "Integracje zewnętrzne",
        "status": "planned",
        "phase": 9,
        "dependencies": ["core"],
        "responsibility": "Adaptery usług AI, poczty, push i płatności. Klucze tylko po "
        "stronie serwera; brak zewnętrznych wywołań w szkielecie.",
    },
]
