import os
import json
import psutil
import multiprocessing
from multiprocessing import Process, Queue, freeze_support
from mpmath import mp, fsum, fac

DIGITS_PER_RUN = 50000
LINE_LENGTH = 1000
STATE_FILE = 'state.json'
LEFTOVER_FILE = 'leftover.json'
OUTPUT_FILE = 'pi.txt'

def chudnovsky_term(k):
    M = fac(6*k) * (545140134*k + 13591409)
    X = fac(3*k) * (fac(k) ** 3) * (-262537412640768000) ** k
    return M / X

def worker(k_range, queue, cpu_id):
    psutil.Process().cpu_affinity([cpu_id])
    results = [chudnovsky_term(k) for k in k_range]
    queue.put(results)

def main():
    # Load state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            total_digits = json.load(f).get('digits', 0)
    else:
        total_digits = 0

    # Load leftover digits
    if os.path.exists(LEFTOVER_FILE):
        with open(LEFTOVER_FILE, 'r') as f:
            leftover = json.load(f).get('digits', '')
    else:
        leftover = ''

    total_needed = total_digits + DIGITS_PER_RUN
    mp.dps = total_needed + 10  # Extra precision buffer
    term_count = total_needed // 14 + 2  # Estimate terms needed

    # CPU affinity settings: use 1 P-core (CPU 0), 2 E-cores (CPU 4 and 5)
    cpu_ids = [0, 4, 5]
    num_workers = len(cpu_ids)

    # Distribute term indexes among workers
    chunks = [[] for _ in range(num_workers)]
    for i, k in enumerate(range(term_count)):
        chunks[i % num_workers].append(k)

    # Start processes
    queue = Queue()
    processes = []
    for i, chunk in enumerate(chunks):
        p = Process(target=worker, args=(chunk, queue, cpu_ids[i]))
        p.start()
        processes.append(p)

    # Collect results
    all_results = []
    for _ in processes:
        all_results.extend(queue.get())

    for p in processes:
        p.join()

    # Calculate Pi from results
    pi = mp.mpf(426880) * mp.sqrt(10005) / fsum(all_results)
    pi_str = str(pi)

    # Extract only the newly needed digits
    if total_digits == 0:
        digits = pi_str[2:]  # skip "3."
    else:
        digits = pi_str[2 + total_digits:]

    # Combine with leftover from last run
    buffer = leftover + digits
    written = 0

    with open(OUTPUT_FILE, 'a') as f:
        while len(buffer) >= LINE_LENGTH:
            f.write(buffer[:LINE_LENGTH] + '\n')
            buffer = buffer[LINE_LENGTH:]
            written += LINE_LENGTH
            print(f"Wrote 1000 digits, total this run: {written}")

    # Save leftover digits
    with open(LEFTOVER_FILE, 'w') as f:
        json.dump({ 'digits': buffer }, f)

    # Save total written digit count
    with open(STATE_FILE, 'w') as f:
        json.dump({ 'digits': total_digits + written }, f)

    print(f"✅ Done. {written} digits written, {len(buffer)} leftover digits saved.")

if __name__ == '__main__':
    freeze_support()  # Important for Windows multiprocessing
    main()