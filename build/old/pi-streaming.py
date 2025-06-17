import json
import os
import gmpy2
from gmpy2 import mpz, get_context

DIGITS_PER_RUN = 600000
LINE_LENGTH = 1000

# File paths
STATE_FILE = 'state2.json'
LEFTOVER_FILE = 'leftover2.json'
OUTPUT_FILE = 'pi2.txt'

# Load current state
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
        total_digits = state.get('digits', 0)
else:
    total_digits = 0

# Load leftover
if os.path.exists(LEFTOVER_FILE):
    with open(LEFTOVER_FILE, 'r') as f:
        leftover = json.load(f).get('digits', '')
else:
    leftover = ''

# Set precision
get_context().precision = (total_digits + DIGITS_PER_RUN + 100) * 4  # bits

# Chudnovsky Algorithm
def chudnovsky_pi(n_terms):
    C = 426880 * gmpy2.sqrt(10005)
    M = mpz(1)
    L = mpz(13591409)
    X = mpz(1)
    K = mpz(6)
    S = mpz(L)

    for i in range(1, n_terms):
        M = (M * (K ** 3 - 16 * K)) // (i ** 3)
        L += 545140134
        X *= -262537412640768000
        term = M * L // X
        S += term
        K += 12

    pi = C / S
    return pi

# Estimate number of terms needed
terms_needed = (total_digits + DIGITS_PER_RUN) // 14 + 5
pi = chudnovsky_pi(terms_needed)
pi_str = str(pi)

# Prepare digit buffer
if total_digits == 0:
    # First run — include the "3." prefix
    prefix = "3."
    digits = pi_str[2:]  # skip "3."
    buffer = prefix + leftover + digits
else:
    # Later runs — just digits after already written
    digits = pi_str[2 + total_digits:]  # skip previous digits
    buffer = leftover + digits

written = 0

# Write out lines of 1000 characters
with open(OUTPUT_FILE, 'a') as f:
    while len(buffer) >= LINE_LENGTH:
        line = buffer[:LINE_LENGTH]
        f.write(line + '\n')
        buffer = buffer[LINE_LENGTH:]
        written += LINE_LENGTH
        print(f"Wrote 1000 digits, total this run: {written}")

# Save leftover and updated state
with open(LEFTOVER_FILE, 'w') as f:
    json.dump({ 'digits': buffer }, f)

with open(STATE_FILE, 'w') as f:
    json.dump({ 'digits': total_digits + written }, f)

print(f"\n✅ Done. {written} digits written, {len(buffer)} digits saved for next run.")