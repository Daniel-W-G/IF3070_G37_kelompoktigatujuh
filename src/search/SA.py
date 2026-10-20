import math
import random
from ..utils import *
from time import perf_counter



# T geometrik: T <- alpha * T. berhenti kalo T < T_min (anggap T ~ 0) atau iterasi selesai
def simulated_annealing(vehicles, ship, T0, alpha, T_min, max_iter, seed):
    if T0 <= 0 or T_min <= 0 or not 0 < alpha <= 1:
        raise ValueError("T0, T_min harus > 0 dan 0 < alpha <= 1")

    random.seed(seed)
    start_time = perf_counter()

    current = random_state(vehicles, ship)
    current_value = objective(current, vehicles)
    initial_state = current.copy()

    value_history = [current_value]
    temperature_history = []
    probability_history = []  # e^(dE/T), None kalau neighbor lebih baik
    iterations = 0
    T = T0

    for _ in range(max_iter):
        if T < T_min:
            break
        iterations += 1
        temperature_history.append(T)
        probability_history.append(None)

        neighbor = random_neighbor(current, vehicles, ship)
        if neighbor is not None:  # None -> iterasi dilewati
            delta = objective(neighbor, vehicles) - current_value
            if delta > 0:
                current, current_value = neighbor, current_value + delta
            else:
                probability = math.exp(delta / T)
                probability_history[-1] = probability
                if probability > random.random():
                    current, current_value = neighbor, current_value + delta

        value_history.append(current_value)
        T *= alpha

    return {
        "initial_state": initial_state,
        "final_state": current,
        "final_score": current_value,
        "value_history": value_history,
        "temperature_history": temperature_history,
        "probability_history": probability_history,
        "iterations": iterations,
        "duration_seconds": perf_counter() - start_time,
        "seed": seed,
        "T0": T0,
        "alpha": alpha,
        "T_min": T_min,
        "max_iter": max_iter
    }
