# Etraf first project -- M/M/1 queue simulation

import random

# ---- Parameters ----
LAMBDA = 2.0   # arrival rate
MU = 3.0       # service rate
MAX_TIME = 20  # simulation time limit

ARRIVAL = "arrival"
DEPARTURE = "departure"


# ---- Helper: exponential random variable ----
def exp_time(rate):
    return random.expovariate(rate)


# ---- Initial state ----
current_time = 0.0
event_list = [(0.0, ARRIVAL)]  # bootstrap
queue = []
server_busy = False


# ---- Main simulation loop ----
while current_time < MAX_TIME:

    # 1. Get next event
    event_list.sort()  # keep sorted by time
    event_time, event_type = event_list.pop(0)

    # 2. Advance time
    current_time = event_time

    # ---- Handle ARRIVAL ----
    if event_type == ARRIVAL:
        queue.append(current_time)  # store arrival time (useful later)

        # Schedule next arrival
        next_arrival = current_time + exp_time(LAMBDA)
        event_list.append((next_arrival, ARRIVAL))

    # ---- Handle DEPARTURE ----
    elif event_type == DEPARTURE:
        server_busy = False

    # ---- Try to start service ----
    if not server_busy and len(queue) > 0:
        queue.pop(0)  # FIFO

        server_busy = True

        # Schedule departure
        next_departure = current_time + exp_time(MU)
        event_list.append((next_departure, DEPARTURE))

    # ---- Debug print (VERY useful at first) ----
    print(f"time={current_time:.3f}, event={event_type}, queue={len(queue)}, busy={server_busy}")