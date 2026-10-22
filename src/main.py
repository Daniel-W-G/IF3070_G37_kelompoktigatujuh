from .search.GA import GA_out
from .search.HC import hill_climbing
from .search.SA import SA_out
from .import model
import argparse
import matplotlib.pyplot as plt
from .visualisasi import plot_state
from pathlib import Path
from datetime import datetime
import json
import random



# Deklarasi Variabel -------------------------------------------------------------------------------------------------------#


vehicles = {
        "V1": model.Vehicle("V1", 2, 3, 200, 15, 5),
        "V2": model.Vehicle("V2", 3, 7, 350, 25, 2),
        "V3": model.Vehicle("V3", 1, 1, 50, 10, 1),
        "V4": model.Vehicle("V4", 2, 4, 200, 15, 3),
        "V5": model.Vehicle("V5", 10, 3, 500, 40, 5),
        "V6": model.Vehicle("V6", 8, 4, 400, 35, 5),
        "V7": model.Vehicle("V7", 1, 5, 150, 15, 2),
        "V8": model.Vehicle("V8", 5, 5, 250, 20, 1),
        "V9": model.Vehicle("V9", 1, 6, 150, 15, 3),
        "V10": model.Vehicle("V10", 7, 2, 300, 25, 1),
    }

ship = model.Ship(5, 15, 100)











# khusus GA

# control
population = 100
iteration = 100
mutation = 0.1

# iteration change
iteration_i1 = 10
iteration_i2 = 50
iteration_i3 = 200

# population change
population_p1 = 10
population_p2 = 50
population_p3 = 200



# khusus SA

sa_T0 = 800
sa_alpha = 0.998
sa_T_min = 1.0
sa_max_iter = 5000
sa_seeds = [1, 2, 3]



# Main ----------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", nargs="?", choices=["ga", "hc", "sa", "all"], default="all")
    parser.add_argument("--seed", type=int, default=None, help="Seed untuk mengulang pembentukan state awal Hill-climbing.")
    args = parser.parse_args()

    def run_ga():
        GA_out(vehicles, ship, population, iteration, mutation)

        GA_out(vehicles, ship, population, iteration_i1, mutation)
        GA_out(vehicles, ship, population, iteration_i2, mutation)
        GA_out(vehicles, ship, population, iteration_i3, mutation)

        GA_out(vehicles, ship, population_p1, iteration, mutation)
        GA_out(vehicles, ship, population_p2, iteration, mutation)
        GA_out(vehicles, ship, population_p3, iteration, mutation)
        return


    def run_hc():
        if args.seed is not None:
            random.seed(args.seed)
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
        fig, ax = plt.subplots(figsize=(8,5))
        steps = range(len(result["history"]))

        ax.plot(steps, result["history"], marker="o")
        ax.set_xticks(list(steps))
        ax.set_xlabel("Iterasi pemeriksaan (0 = state awal)")
        ax.set_ylabel("Total Shipping Fee")
        ax.set_title("Perkembangan Nilai Objektif - Hill-climbing")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        project_root = Path(__file__).resolve().parent.parent
        output_dir = project_root / "output" / "hc" / run_id
        output_dir.mkdir(parents=True, exist_ok=True)

        initial_fig.savefig(
            output_dir / "state_awal.png", dpi=150, bbox_inches="tight"
        )
        final_fig.savefig(
            output_dir / "state_akhir.png", dpi=150, bbox_inches="tight"
        )
        fig.savefig(
            output_dir / "grafik_objektif.png", dpi=150, bbox_inches="tight"
        )

        print(f"Gambar tersimpan di: {output_dir}")

        summary = {

            "seed": args.seed,
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


        plt.show()

    def run_sa():
        for seed in sa_seeds:
            out = SA_out(vehicles, ship, sa_T0, sa_alpha, sa_T_min, sa_max_iter, seed)
            print(f"SA seed={seed} awal={out['initial_score']} akhir={out['final_score']} "
                  f"iter={out['iterations']} stuck={out['stuck_count']} durasi={out['duration_seconds']:.2f}s")
        return


    if args.algorithm == "hc":
        run_hc()

    elif args.algorithm == "sa":
        run_sa()

    elif args.algorithm == "ga":
        run_ga()

    elif args.algorithm == "all":
        run_hc()
        run_ga()
        run_sa()