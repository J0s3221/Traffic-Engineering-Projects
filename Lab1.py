#Etraf first project -- Poisson Proccess Simulation

import random
import math

def main():
    # Parâmetros
    N = 500
    lamb = 5

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

    # Mostrar primeiros resultados
    print("Primeiros 10 intervalos dt:")
    print(dt_list[:10])

    print("\nPrimeiros 10 tempos de chegada:")
    print(arrival_times[:10])

def hist(): 
    print("") # here: make the histograms and output them in a excel file

if __name__=="__main__":
    main()
