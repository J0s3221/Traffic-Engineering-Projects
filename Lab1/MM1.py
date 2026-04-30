# Etraf first project -- M/M/1 queue simulation

import random
import time

# ---- Parameters ----
LAMBDA = 4.0   # arrival rate
MU = 8.0       # service rate
MAX_TIME = 100000

ARRIVAL = "arrival"
DEPARTURE = "departure"

# ---- helper function give exponential rate ----
def exp_time(rate):
    return random.expovariate(rate)

# ---- function that simulates the server ----
def server():

    # ---- System state ----
    current_time = 0.0
    event_list = [(0.0, ARRIVAL)]  # first arrival
    queue = []                     # waiting packets (stores arrival times)
    server_busy = False

    # ---- Metrics ----
    last_event_time = 0.0

    area_queue = 0.0   # integral of queue length over time
    area_busy = 0.0    # integral of server utilization

    total_waiting_time = 0.0
    total_system_time = 0.0
    num_departures = 0

    # ---- Main simulation loop ----
    while current_time < MAX_TIME:

        # 1. Get next event (earliest in time)
        event_list.sort()
        event_time, event_type = event_list.pop(0)

        # 2. Update time-dependent statistics BEFORE changing state
        time_since_last = event_time - last_event_time

        area_queue += len(queue) * time_since_last
        area_busy += (1 if server_busy else 0) * time_since_last

        # advance simulation clock
        current_time = event_time
        last_event_time = current_time

        # ---- ARRIVAL EVENT ----
        if event_type == ARRIVAL:

            # packet arrives → joins queue
            queue.append(current_time)

            # schedule next arrival (Poisson process)
            next_arrival = current_time + exp_time(LAMBDA)
            event_list.append((next_arrival, ARRIVAL))

        # ---- DEPARTURE EVENT ----
        elif event_type == DEPARTURE:

            # packet finished service → server becomes free
            server_busy = False
            num_departures += 1

        # ---- START SERVICE IF POSSIBLE ----
        if not server_busy and len(queue) > 0:

            # take next packet (FIFO)
            arrival_time = queue.pop(0)

            # compute waiting time
            waiting_time = current_time - arrival_time
            total_waiting_time += waiting_time

            # generate service time
            service_time = exp_time(MU)

            # total time in system = waiting + service
            total_system_time += waiting_time + service_time

            # server becomes busy
            server_busy = True

            # schedule departure
            next_departure = current_time + service_time
            event_list.append((next_departure, DEPARTURE))

        # ---- Debug ----
        print(f"time={current_time:.3f}, event={event_type}, queue={len(queue)}, busy={server_busy}")

    # ---- Final metrics ----
    avg_queue_length = area_queue / current_time
    utilization = area_busy / current_time
    avg_waiting_time = total_waiting_time / num_departures if num_departures > 0 else 0
    avg_system_time = total_system_time / num_departures if num_departures > 0 else 0

    return avg_queue_length, utilization, avg_waiting_time, avg_system_time


def main():
    avg_queue_length, utilization, avg_waiting_time, avg_system_time = server()

    print("\n--- Results ---")
    print(f"Average queue length (Lq): {avg_queue_length:.3f}")
    print(f"Server utilization (rho): {utilization:.3f}")
    print(f"Average waiting time (Wq): {avg_waiting_time:.3f}")
    print(f"Average system time (W): {avg_system_time:.3f}")


if __name__ == "__main__":
    main()