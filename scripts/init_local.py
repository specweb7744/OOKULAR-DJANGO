"""Create local secrets without replacing existing configuration or exposing them."""

import secrets
from pathlib import Path

root = Path(__file__).resolve().parents[1]
target = root / ".env"
if target.exists():
    print("Plik .env już istnieje; zachowano jego zawartość.")
else:
    template = (root / ".env.example").read_text(encoding="utf-8")
    value = template.replace("CHANGE_ME", secrets.token_urlsafe(64)).replace(
        "CHANGE_DB_PASSWORD", secrets.token_hex(24)
    )
    with target.open("x", encoding="utf-8") as output:
        output.write(value)
    target.chmod(0o600)
    print("Utworzono lokalny plik .env z losowymi sekretami.")
