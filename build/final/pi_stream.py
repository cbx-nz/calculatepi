import os
import json
from decimal import Decimal, getcontext

# === Settings ===
DIGITS_PER_RUN = 5000         # Digits to calculate this run
LINE_LENGTH = 1000            # Digits per line in output file
STATE_FILE = "pi_state.json"
LEFTOVER_FILE = "pi_leftover.json"
OUTPUT_FILE = "pi_output.txt"


def load_json_file(path):
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"[WARN] {path} is corrupt or empty. Resetting.")
            return {}
    return {}


def chudnovsky_decimal(n_terms):
    getcontext().prec += 10  # Extra precision for internal steps

    C = 426880 * Decimal(10005).sqrt()
    M = Decimal(1)
    L = Decimal(13591409)
    X = Decimal(1)
    K = Decimal(6)
    S = Decimal(L)

    for i in range(1, n_terms):
        M = (M * (K ** 3 - 16 * K)) / (Decimal(i) ** 3)
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12

    pi = C / S
    getcontext().prec -= 10
    return +pi


def main():
    # === Load state ===
    state = load_json_file(STATE_FILE)
    leftover = load_json_file(LEFTOVER_FILE).get("digits", "")
    total_digits = state.get("digits", 0)

    # === Set required precision ===
    digits_needed = total_digits + DIGITS_PER_RUN + 2
    getcontext().prec = digits_needed + 10  # extra margin

    # === Estimate number of terms ===
    terms = digits_needed // 14 + 5
    pi = chudnovsky_decimal(terms)

    pi_str = str(pi)

    if total_digits == 0:
        # First run — include "3." in buffer
        buffer = pi_str  # includes "3."
    else:
        # Subsequent runs — skip "3."
        buffer = leftover + pi_str[2 + total_digits:]

    written = 0

    # === Write to file in chunks ===
    with open(OUTPUT_FILE, "a") as f:
        while len(buffer) >= LINE_LENGTH:
            f.write(buffer[:LINE_LENGTH] + "\n")
            buffer = buffer[LINE_LENGTH:]
            written += LINE_LENGTH
            print(f"Wrote 1000 digits, total this run: {written}")

    # === Save leftover and new state ===
    with open(LEFTOVER_FILE, "w") as f:
        json.dump({"digits": buffer}, f)

    with open(STATE_FILE, "w") as f:
        json.dump({"digits": total_digits + written}, f)

    print(f"\n✅ Done. Wrote {written} digits, {len(buffer)} digits buffered for next run.")


if __name__ == "__main__":
    main()