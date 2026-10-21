from .search.SA import SA_out
from .search.GA import GA_out
from .import model
import argparse



# Deklarasi Variabel -------------------------------------------------------------------------------------------------------#


vehicles = {
        "V1": model.Vehicle("V1", 2, 3, 150, 20, 5),
        "V2": model.Vehicle("V2", 3, 2, 150, 15, 2),
        "V3": model.Vehicle("V3", 1, 1, 50, 10, 1),
        "V4": model.Vehicle("V4", 2, 2, 120, 23, 3),
        "V5": model.Vehicle("V5", 4, 1, 200, 9, 1),
    }

ship = model.Ship(3, 5, 50)










# khusus SA

sa_T0 = 500             # temperatur awal
sa_alpha = 0.995        # T <- alpha * T tiap iterasi
sa_T_min = 1.0          # T < T_min dianggap T ~ 0 -> berhenti
sa_max_iter = 3000      # limit iterasi
sa_seeds = [1, 2, 3]  

# khusus GA

# control
population = 100
iteration = 100
mutation = 0.1

# iteration change
iteration_i1 = 50
iteration_i2 = 200
iteration_i3 = 500

# population change
population_p1 = 50
population_p2 = 200
population_p3 = 500



# Main ----------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", nargs="?", choices=["ga", "hc", "sa", "all"], default="all")
    args = parser.parse_args()

    def run_ga():
        GA_out(vehicles, ship, population, iteration, mutation)
        for i in range(3):
            GA_out(vehicles, ship, population, iteration_i1, mutation)
            GA_out(vehicles, ship, population, iteration_i2, mutation)
            GA_out(vehicles, ship, population, iteration_i3, mutation)

            GA_out(vehicles, ship, population_p1, iteration, mutation)
            GA_out(vehicles, ship, population_p2, iteration, mutation)
            GA_out(vehicles, ship, population_p3, iteration, mutation)
        return

    def run_sa():
        for seed in sa_seeds:
            out = SA_out(vehicles, ship, sa_T0, sa_alpha, sa_T_min, sa_max_iter, seed)
            print(f"SA seed={seed} final={out['final_score']} iter={out['iterations']} "
                  f"stuck={out['stuck_count']} durasi={out['duration_seconds']:.2f}s")
        return

    if args.algorithm == "hc":
        pass

    elif args.algorithm == "sa":
        run_sa()

    elif args.algorithm == "ga":
        run_ga()

    elif args.algorithm == "all":
        
        run_sa()
        run_ga()