"""
BAKERY - Producer/Consumer Problem (easy version)

    Baker    = PRODUCER  (makes bread and puts it on the shelf)
    Customer = CONSUMER  (takes bread from the shelf and buys it)
    Shelf    = BUFFER    (has limited space)

Rules:
    1. Shelf FULL   -> baker must WAIT
    2. Shelf EMPTY  -> customer must WAIT
    3. Only ONE person can touch the shelf at a time

Run in terminal :  python bakery.py
Run with website:  python app.py
"""

import threading
import time
import random

# ---------- Settings ----------
SHELF_SIZE = 5      # shelf can hold 5 breads
BAKE_TIME = 1.5     # seconds a baker takes to make 1 bread
BUY_TIME = 1.5      # seconds a customer takes before buying

# ---------- Shared things ----------
shelf = []                                # breads on the shelf right now
empty = threading.Semaphore(SHELF_SIZE)   # counts EMPTY spaces on the shelf
full = threading.Semaphore(0)             # counts BREADS on the shelf
lock = threading.Lock()                   # only ONE person at a time

# ---------- Info for the website ----------
running = False     # becomes True when Start is pressed
status = {}         # what each person is doing
messages = []       # last few things that happened
baked = 0           # total breads baked
sold = 0            # total breads sold


def say(text):
    print(text)
    messages.append(text)
    del messages[:-8]          # keep only the last 8 messages


def baker(name):
    """PRODUCER: bakes bread and puts it on the shelf."""
    global baked
    number = 0
    while True:
        while not running:                     # wait until Start is pressed
            time.sleep(0.1)

        status[name] = "baking"
        time.sleep(random.uniform(0.6, 1.4) * BAKE_TIME)   # baking takes time
        number += 1
        bread = f"Bread-{name[-1]}.{number}"

        # Step 1: is there an empty space? If not, wait.
        if not empty.acquire(blocking=False):
            status[name] = "waiting"
            say(f"{name}: shelf is FULL, waiting...")
            empty.acquire()

        # Step 2: lock the shelf, put the bread, unlock (automatic)
        with lock:
            shelf.append(bread)
            baked += 1
            say(f"{name} put {bread} on the shelf  ({len(shelf)} on shelf)")

        # Step 3: tell customers there is one more bread
        full.release()


def customer(name):
    """CONSUMER: takes bread from the shelf and buys it."""
    global sold
    while True:
        while not running:
            time.sleep(0.1)

        status[name] = "shopping"
        time.sleep(random.uniform(0.6, 1.4) * BUY_TIME)    # deciding what to buy

        # Step 1: is there any bread? If not, wait.
        if not full.acquire(blocking=False):
            status[name] = "waiting"
            say(f"{name}: shelf is EMPTY, waiting...")
            full.acquire()

        # Step 2: lock the shelf, take the bread, unlock (automatic)
        with lock:
            bread = shelf.pop(0)
            sold += 1
            say(f"{name} bought {bread}  ({len(shelf)} on shelf)")

        # Step 3: tell bakers there is one more empty space
        empty.release()


_started = False


def start_all():
    """Create 2 bakers and 3 customers (each one is a thread)."""
    global _started
    if _started:
        return
    _started = True
    for i in (1, 2):
        threading.Thread(target=baker, args=(f"Baker {i}",), daemon=True).start()
    for i in (1, 2, 3):
        threading.Thread(target=customer, args=(f"Customer {i}",), daemon=True).start()


# ---------- Terminal mode ----------
if __name__ == "__main__":
    print("=== Bakery (runs for 15 seconds) ===")
    running = True
    start_all()
    time.sleep(15)
    print("=== Done ===")
