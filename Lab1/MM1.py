# Etraf first project -- M/M/1 queue simulation

import random
import time

# ---- Parameters ----
LAMBDA = 2.0   # arrival rate
MU = 4.0       # service rate
MAX_TIME = 20  # simulation time limit

ARRIVAL = "arrival"
DEPARTURE = "departure"


# ---- Helper: exponential random variable ----
def exp_time(rate):
    return random.expovariate(rate)

# ---- Function to simulate the server ----
def server():
    # ---- Initial state ----
    current_time = 0.0
    event_list = [(0.0, ARRIVAL)]  # bootstrap
    queue = []
    server_busy = False

    # ---- Metrics ----
    last_event_time = 0.0

    area_queue = 0.0       # integral of queue length
    area_busy = 0.0        # integral of server busy (0/1)

    total_waiting_time = 0.0
    total_system_time = 0.0
    num_departures = 0

    # ---- Main simulation loop ----
    while current_time < MAX_TIME:

        # time.sleep(0.2)

        # 1. Get next event
        event_list.sort()  # keep sorted by time
        event_time, event_type = event_list.pop(0)

        time_since_last = current_time - last_event_time

        last_event_time = current_time

        area_queue += len(queue) * time_since_last
        area_busy += (1 if server_busy else 0) * time_since_last

        current_packet_arrival = 0

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

            # one packet finished
            num_departures += 1

            # system time = now - when it arrived
            system_time = current_time - current_packet_arrival
            total_system_time += system_time

        # ---- Try to start service ----
        if not server_busy and len(queue) > 0:
            arrival_time = queue.pop(0)

            waiting_time = current_time - arrival_time
            total_waiting_time += waiting_time

            current_packet_arrival = arrival_time

            server_busy = True

            next_departure = current_time + exp_time(MU)
            event_list.append((next_departure, DEPARTURE))

        # ---- Debug print (VERY useful at first) ----
        print(f"time={current_time:.3f}, event={event_type}, queue={len(queue)}, busy={server_busy}")
    
    avg_queue_length = area_queue / current_time
    utilization = area_busy / current_time
    avg_waiting_time = total_waiting_time / num_departures if num_departures > 0 else 0
    avg_system_time = total_system_time / num_departures if num_departures > 0 else 0

    return avg_queue_length, utilization, avg_waiting_time, avg_system_time

# ---- main ----
def main():

    avg_queue_length, utilization, avg_waiting_time, avg_system_time = server()

    print("\n--- Results ---")

    print(f"Average queue length (Lq): {avg_queue_length:.3f}")
    print(f"Server utilization (rho): {utilization:.3f}")
    print(f"Average waiting time (Wq): {avg_waiting_time:.3f}")
    print(f"Average system time (W): {avg_system_time:.3f}")

if __name__=="__main__":
    main()