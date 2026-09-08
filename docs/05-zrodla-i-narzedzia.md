# Źródła i narzędzia

Zakres sprawdzenia: fundament architektury i granice pierwszej implementacji.
Data sprawdzenia źródeł: 2026-09-07 (UTC).
Nie analizowano pełnej książki, produkcyjnego hostingu ani wydajności przyszłego Matchera.

| Źródło | Co potwierdza lub wnosi |
|---|---|
| Dostarczone zdjęcia spisu treści RailsSpace | Kolejność tematów: środowisko, konta, testy, logowanie, profil, społeczność, wyszukiwanie, media, poczta, relacje, REST i wdrożenie. |
| [OOKULAR-DOCS](https://github.com/specweb7744/OOKULAR-DOCS/blob/main/README.md) | Wizję portalu, cyfrowego portretu człowieka i pięć obszarów opisu. |
| [Django: własny model użytkownika](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/) | Własny User należy ustalić na początku projektu i uwzględnić w pierwszej migracji. Dane domenowe można rozdzielić do osobnych modeli. |
| [Django: obsługiwane wersje](https://www.djangoproject.com/download/) | Status Django 5.2 LTS i horyzont wsparcia. |
| [DRF: uprawnienia](https://www.django-rest-framework.org/api-guide/permissions/) | Sprawdzanie uprawnień i potrzebę filtrowania list według dostępności obiektów. |
| [DRF: uwierzytelnianie](https://www.django-rest-framework.org/api-guide/authentication/) | Rozdzielenie uwierzytelniania i dostępu oraz potrzebę CSRF w logowaniu opartym na sesji. |
| [pgvector](https://github.com/pgvector/pgvector) | Wyszukiwanie podobieństwa wektorów w PostgreSQL; implementacja odłożona do etapu semantyki. |
| [OpenAI API](https://developers.openai.com/api/reference/overview) | Klucze usług należy przechowywać na serwerze, bez umieszczania ich w aplikacji mobilnej i przeglądarce. |
| [Base44: fundamenty projektu interfejsu](https://docs.base44.com/Building-your-app/Design-foundations-and-layout) | Spójne kolory, typografia, odstępy i komponenty. |

## Dobór narzędzi do OOKULAR

| Narzędzie | Zadanie |
|---|---|
| Codex | Tworzenie kodu, podział na moduły, testy i poprawki. |
| GitHub | Istniejące repozytorium, historia zmian i osobna gałąź do przeglądu. |
| Context7 | Dokumentacja bibliotek, gdy jego narzędzia są dostępne. W tej sesji dokumentację sprawdzono bezpośrednio u autorów. |
| Code Tytor: Python | Pomoc przy wyjaśnianiu małych fragmentów Pythona. Wywołany generator nie dostarczył kodu projektu; nie stanowi źródła tej implementacji. |
| Deep Research | Sprawdzenie źródeł i uzasadnienie kluczowych decyzji, w zakresie potrzebnym dla fundamentu. |
| OpenAI Developers | Połączony; przeznaczony do późniejszego adaptera AI. W fundamencie nie utworzono klucza ani płatnego wywołania. |
| Base44 | Inspiracje do wyglądu i wygody obsługi. |

Podział na domeny, kolejność wdrożenia i kształt API są projektem dla OOKULAR.
Nie są twierdzeniem, że książka lub dokumentacja narzędzi narzucają dokładnie taką architekturę.
