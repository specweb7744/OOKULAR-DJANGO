# Konta i role

Status: **podblok rejestracji i logowania wdrożony w kodzie**.

Django-allauth 65.19.2: rejestracja obu ról, potwierdzenie i zmiana e-maila,
logowanie, wylogowanie, reset i zmiana hasła. Konto, rola i adres e-mail zapisują
się w jednej transakcji. Publiczny formularz nie przyjmuje uprawnień staff.

HTML: `/konta/`; własne konto: `/konto/`; aplikacja natywna: `/api/auth/app/v1/`.
HasVerifiedAccount chroni prywatne API, MobileSessionAuthentication sprawdza
również hash sesji po zmianie hasła. Nie zastępuj tej klasy standardowym
XSessionTokenAuthentication z allauth bez ponownego sprawdzenia unieważniania sesji.

Testy: `tests.py`, `test_auth.py`, `test_client.py`.
[Opis kont i uruchomienie](../../../docs/06-konta.md).
