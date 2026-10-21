from .search.GA import GA_out
from .import model
import argparse



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



# Main ----------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", nargs="?", choices=["ga", "hc", "sa", "all"], default="all")
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


    if args.algorithm == "hc":
        pass

    elif args.algorithm == "sa":
        pass

    elif args.algorithm == "ga":
        run_ga()

    elif args.algorithm == "all":
        
        run_ga()