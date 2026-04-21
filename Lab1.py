# Etraf first project -- Poisson Proccess Simulation

import os
import random
import math
import matplotlib.pyplot as plt

# Funtion for counting events and build histograms out of the delta t generated in main
def hist(arrival_times):
    # Step 1: count events per unit interval
    events_per_interval = {}

    for t in arrival_times:
        interval = int(t)  # floor → which unit interval

        if interval in events_per_interval:
            events_per_interval[interval] += 1
        else:
            events_per_interval[interval] = 1

    # Convert dict → list
    counts = list(events_per_interval.values())

    # Step 2: build histogram manually
    histogram = {}

    for k in counts:
        if k in histogram:
            histogram[k] += 1
        else:
            histogram[k] = 1

    return histogram

# Function for saving results into an output file
def save_histogram(histogram, lamb):
    filename = f"data/histogram_lambda_{lamb}.csv"

    with open(filename, "w") as f:
        f.write("k,frequency\n")
        for k in sorted(histogram.keys()):
            f.write(f"{k},{histogram[k]}\n")

# Function for plotting the Histograms generated
def plot_histogram(histogram, lamb):
    # Total number of intervals
    total_intervals = sum(histogram.values())

    # Sort k values
    k_values = sorted(histogram.keys())

    # Experimental probabilities
    experimental_probs = [histogram[k] / total_intervals for k in k_values]

    # Theoretical Poisson probabilities
    theoretical_probs = [
        (lamb**k * math.exp(-lamb)) / math.factorial(k)
        for k in k_values
    ]

    # Plot
    plt.bar(k_values, experimental_probs, label="Experimental", alpha=0.6)
    plt.plot(k_values, theoretical_probs, marker='o', label="Poisson (theoretical)")

    plt.xlabel("k (events per interval)")
    plt.ylabel("Probability")
    plt.title(f"Poisson Process (λ = {lamb})")
    plt.legend()

    # unique filename
    plt.savefig(f"plots/poisson_lambda_{lamb}.png")

    plt.clf()  # clear figure

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

def main():
    os.makedirs("plots", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Parâmetros
    N = 500
    lambdas = [0.5, 1.0, 5.0, 10.0, 50.0]

    for lamb in lambdas:
        event_gen(N, lamb)

if __name__=="__main__":
    main()
