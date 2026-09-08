# OOKULAR — klient mobilny

Działają wspólne konta i API logowania dla aplikacji natywnej. Responsywne ekrany
webowe można używać w przeglądarce telefonu. Nie ma jeszcze ekranów React Native,
instalowalnej aplikacji ani APK/IPA.

`createMobileAuthClient` w `packages/api-client` obsługuje rejestrację, logowanie,
potwierdzenie e-mail, ponowną wysyłkę, reset i zmianę hasła, sesję, własne konto
oraz wylogowanie. Wstrzyknij magazyn tokenów z Keychain/Keystore, np. przez adapter
przyszłego klienta; kod nie zapisuje ich w localStorage ani w jawnym pliku.

HTTP 401 po rejestracji oznacza oczekiwanie na potwierdzenie. Zachowaj również token
sesji oczekującej. Adresy z wiadomości otwierają formularze Django; po potwierdzeniu
wróć do aplikacji i zaloguj się. Deep linki i ekran natywny są osobnym zadaniem.
Weryfikację można też wykonać API, przekazując klucz z linku.

Adres backendu musi być osiągalny z telefonu; localhost telefonu wskazuje sam telefon.
W produkcji stosuj HTTPS. Żadne klucze poczty ani usług zewnętrznych nie trafiają do aplikacji.
[Kontrakt i scenariusze](../../docs/06-konta.md).
