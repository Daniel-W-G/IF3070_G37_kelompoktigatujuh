import json
import random
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt

from ..utils import random_state, generate_neighbors, objective, is_valid
from ..visualisasi import plot_state


def hill_climbing(vehicles, ship, initial_state=None):
    """Steepest ascent: tetangga dengan nilai lebih tinggi. Pencatatan setiap putaran pemeriksaan."""
    started = perf_counter()

    if initial_state is None:
        current = random_state(vehicles, ship)
    else:
        current = initial_state.copy()

    if not is_valid(current, vehicles, ship):
        raise ValueError("State awal tidak valid.")

    start_state = current.copy()
    current_score = objective(current, vehicles)
    history = [current_score]
    iterations = 0
    accepted_moves = 0

    while True:
        iterations += 1
        neighbors = generate_neighbors(current, vehicles, ship)

        if not neighbors:
            history.append(current_score)
            stop_reason = "Tidak ada tetangga valid."
            break

        best = max(neighbors, key=lambda state: objective(state, vehicles))
        best_score = objective(best, vehicles)

        if best_score <= current_score:
            history.append(current_score)
            stop_reason = "Tidak ada tetangga dengan nilai lebih tinggi."
            break

        current = best
        current_score = best_score
        accepted_moves += 1
        history.append(current_score)

    return {
        "initial_state": start_state,
        "final_state": current.copy(),
        "initial_score": history[0],
        "final_score": current_score,
        "history": history,
        "iterations": iterations,
        "accepted_moves": accepted_moves,
        "duration_seconds": perf_counter() - started,
        "stop_reason": stop_reason,
    }

def _create_experiment_dir():
    output_root = Path(__file__).resolve().parents[2] / "output" / "hc"
    output_root.mkdir(parents=True, exist_ok=True)

    experiment_numbers = []

    for folder in output_root.iterdir():
        if not folder.is_dir():
            continue

        prefix, separator, number = folder.name.rpartition("_")

        if prefix == "eksperimen" and separator and number.isdecimal():
            experiment_numbers.append(int(number))

    next_number = max(experiment_numbers, default=0) + 1
    output_dir = output_root / f"eksperimen_{next_number}"
    output_dir.mkdir()

    return output_dir

def HC_out(vehicles, ship, seed=None):
    if seed is not None:
        random.seed(seed)

    result = hill_climbing(vehicles, ship)

    print("Algoritma: Steepest Ascent Hill-climbing")
    print(f"Nilai awal: {result['initial_score']}")
    print(f"Nilai akhir: {result['final_score']}")
    print(f"Jumlah iterasi pemeriksaan: {result['iterations']}")
    print(f"Jumlah perpindahan: {result['accepted_moves']}")
    print(f"Durasi: {result['duration_seconds']:.6f} detik")
    print(f"Alasan berhenti: {result['stop_reason']}")
    print(f"Riwayat nilai: {result['history']}")

    initial_fig = plot_state(
        result["initial_state"], vehicles, ship,
        "State Awal - Steepest Ascent Hill-climbing"
    )
    final_fig = plot_state(
        result["final_state"], vehicles, ship,
        "State Akhir - Steepest Ascent Hill-climbing"
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    steps = range(len(result["history"]))

    ax.plot(steps, result["history"], marker="o")
    ax.set_xticks(list(steps))
    ax.set_xlabel("Iterasi pemeriksaan (0 = state awal)")
    ax.set_ylabel("Total Shipping Fee")
    ax.set_title("Perkembangan Nilai Objektif - Hill-climbing")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    output_dir = _create_experiment_dir()

    initial_fig.savefig(
        output_dir / "state_awal.png", dpi=150, bbox_inches="tight"
    )
    final_fig.savefig(
        output_dir / "state_akhir.png", dpi=150, bbox_inches="tight"
    )
    fig.savefig(
        output_dir / "grafik_objektif.png", dpi=150, bbox_inches="tight"
    )

    summary = {
        "seed": seed,
        "algorithm": "Steepest Ascent Hill-climbing",
        "initial_score": result["initial_score"],
        "final_score": result["final_score"],
        "iterations": result["iterations"],
        "accepted_moves": result["accepted_moves"],
        "duration_seconds": result["duration_seconds"],
        "stop_reason": result["stop_reason"],
        "history": result["history"],
    }

    for state_key in ("initial_state", "final_state"):
        summary[state_key] = {
            vehicle_id: {
                "loaded": placement.loaded,
                "x": placement.x,
                "y": placement.y,
                "rotated": placement.rotated,
            }
            for vehicle_id, placement
            in result[state_key].placements.items()
        }

    with (output_dir / "hasil.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    print(f"Hasil tersimpan di: {output_dir}")

    plt.show()

    return result