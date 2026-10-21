import math
import random
from ..utils import *
from time import perf_counter
import json
from pathlib import Path
import matplotlib.pyplot as plt
from ..visualisasi import plot_state
from datetime import datetime


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
    probability_history = []  # e^(dE/T), None kalo neighbor lebih baik
    worse_considered = 0
    worse_accepted = 0
    stuck_count = 0  # hitung neighbor lebih buruk yang ditolak
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
                if delta < 0:
                    worse_considered += 1
                if probability > random.random():
                    current, current_value = neighbor, current_value + delta
                    if delta < 0:
                        worse_accepted += 1
                else:
                    stuck_count += 1

        value_history.append(current_value)
        T *= alpha

    return {
        "initial_state": initial_state,
        "final_state": current, # mengembalikan state saat berhenti, bukan best-so-far
        "final_score": current_value,
        "value_history": value_history,
        "temperature_history": temperature_history,
        "probability_history": probability_history,
        "stuck_count": stuck_count,
        "worse_considered": worse_considered,
        "worse_accepted": worse_accepted,
        "iterations": iterations,
        "duration_seconds": perf_counter() - start_time,
        "seed": seed,
        "T0": T0,
        "alpha": alpha,
        "T_min": T_min,
        "max_iter": max_iter
    }



def SA_out(vehicles, ship, T0: float, alpha: float, T_min: float, max_iter: int, seed: int):
    result = simulated_annealing(vehicles, ship, T0, alpha, T_min, max_iter, seed)
    def to_dict(state):
        data = {}
        for id, p in state.placements.items():
            data[id] = {
                "loaded": p.loaded,
                "x": p.x,
                "y": p.y,
                "rotated": p.rotated
            }
        return data

    output = {
        "initial_state": to_dict(result["initial_state"]),
        "final_state": to_dict(result["final_state"]),
        "initial_score": result["value_history"][0],
        "final_score": result["final_score"],
        "value_history": result["value_history"],
        "temperature_history": result["temperature_history"],
        "probability_history": result["probability_history"],
        "stuck_count": result["stuck_count"],
        "worse_considered": result["worse_considered"],
        "worse_accepted": result["worse_accepted"],
        "iterations": result["iterations"],
        "duration_seconds": result["duration_seconds"],
        "seed": result["seed"],
        "T0": result["T0"],
        "alpha": result["alpha"],
        "T_min": result["T_min"],
        "max_iter": result["max_iter"]
    }


    output_path = Path(__file__).resolve().parents[2] / "output" / "SA"
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = (f"SA_seed{seed}_iter{max_iter}_{timestamp}.json")
    file_path = output_path / filename
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)


    initial_result = plot_state(result["initial_state"], vehicles, ship, "SA - State Awal")
    final_result = plot_state(result["final_state"], vehicles, ship, "SA - State Akhir")

    initial_result.savefig(
        output_path / f"{file_path.stem}_initial.png",
        dpi=200, bbox_inches="tight"
    )
    final_result.savefig(
        output_path / f"{file_path.stem}_final.png",
        dpi=200, bbox_inches="tight"
    )

    plt.close(initial_result)
    plt.close(final_result)

    return output