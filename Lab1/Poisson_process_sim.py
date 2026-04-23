# Etraf first project -- Poisson Proccess Simulation

import sys
import os
import random
import math
import matplotlib.pyplot as plt

# Funtion for counting events and build histograms out of the delta t generated in main
def hist(arrival_times):
    # último intervalo observado
    max_interval = int(arrival_times[-1])

    # contar eventos em TODOS os intervalos, incluindo vazios
    events_per_interval = [0] * (max_interval + 1)

    for t in arrival_times:
        interval = int(t)
        events_per_interval[interval] += 1

    # construir histograma manual
    histogram = {}

    for count in events_per_interval:
        if count in histogram:
            histogram[count] += 1
        else:
            histogram[count] = 1

    return histogram

# Function for saving results into an output file
def save_histogram(histogram, lamb):
    filename = f"data/histogram_lambda_{lamb}.csv"

    with open(filename, "w") as f:
        f.write("k,frequency\n")
        for k in sorted(histogram.keys()):
            f.write(f"{k},{histogram[k]}\n")

# Function for plotting the Histograms generated
def plot_histogram(histogram, lamb, name=None):
    total_intervals = sum(histogram.values())

    k_values = range(0, max(histogram.keys()) + 1)

    experimental_probs = [
        histogram.get(k, 0) / total_intervals
        for k in k_values
    ]

    theoretical_probs = [
        (lamb**k * math.exp(-lamb)) / math.factorial(k)
        for k in k_values
    ]

    plt.bar(k_values, experimental_probs, alpha=0.6, label="Experimental")
    plt.plot(k_values, theoretical_probs, marker='o', label="Poisson (theoretical)")

    plt.xlabel("k")
    plt.ylabel("Probability")
    plt.title(f"Poisson Process (λ={lamb})")
    plt.legend()

    if name is None:
        filename = f"plots/poisson_lambda_{lamb}.png"
    else:
        filename = f"plots/{name}.png"

    plt.savefig(filename)
    plt.clf()

def event_gen(N, lamb):
    # Listas
    dt_list = []       # intervalos entre eventos
    arrival_times = [] # tempos acumulados

    # Tempo inicial
    current_time = 0 

    # Gerar eventos
    for i in range(N):
        u = random.random()  # número uniforme [0,1) Graças a função random usada (meter no relatorio)

        # transformação exponencial
        dt = -math.log(1 - u) / lamb

        dt_list.append(dt)

        current_time += dt
        arrival_times.append(current_time)

    histogram = hist(arrival_times)

    plot_histogram(histogram, lamb)
    save_histogram(histogram, lamb)

    print("Histogram (k events per interval):")
    for k in sorted(histogram.keys()):
        print(f"{k}: {histogram[k]}")


# Function for step 2.3: generates four independent sequences with different lambdas
#                        then it combines the four sequences into one and creates a histogram
def superposition_experiment():
    lambdas = [2, 9, 11, 15]
    T = 10000

    processes = []

    # gerar processos individuais
    for lamb in lambdas:
        arrivals = generate_arrivals_until(T, lamb)
        processes.append(arrivals)

        histogram = hist(arrivals)

        plot_histogram(
            histogram,
            lamb,
            name=f"individual_lambda_{lamb}"
        )

        save_histogram(histogram, lamb)

    # combinar todos
    combined_arrivals = combine_process(processes)

    histogram = hist(combined_arrivals)

    lamb_total = sum(lambdas)

    plot_histogram(
        histogram,
        lamb_total,
        name=f"superposition_lambda_{lamb_total}"
    )

    save_histogram(histogram, lamb_total)

    print(f"\nSuperposed process (λ = {lamb_total})")
    for k in sorted(histogram.keys()):
        print(f"{k}: {histogram[k]}")

#======= Helper functions for superposition ==========
def generate_arrivals(N, lamb):
    arrival_times = []
    current_time = 0

    for _ in range(N):
        u = random.random()
        dt = -math.log(1 - u) / lamb
        current_time += dt
        arrival_times.append(current_time)

    return arrival_times

def generate_arrivals_until(T, lamb):
    arrival_times = []
    current_time = 0.0

    while True:
        u = random.random()
        dt = -math.log(1 - u) / lamb
        current_time += dt

        if current_time > T:
            break

        arrival_times.append(current_time)

    return arrival_times

def combine_process(processes):
    combined = []

    for process in processes:
        combined.extend(process)

    combined.sort()

    return combined

def main():
    os.makedirs("plots", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Parâmetros

    lambdas = [0.5, 1.0, 5.0, 10.0, 50.0]

    # Check argument
    if len(sys.argv) < 2:
        print("Usage: python Lab1.py [1|2]")
        return

    arg = sys.argv[1]

    if arg == "1":
        # 2.2 part
        for lamb in lambdas:
            N = int(1000 * lamb)
            event_gen(N, lamb)

    elif arg == "2":
        # 2.3 part
        superposition_experiment()

    else:
        print("\nInvalid option. Use 1 (Poisson) or 2 (Superposition).")

if __name__=="__main__":
    main()
