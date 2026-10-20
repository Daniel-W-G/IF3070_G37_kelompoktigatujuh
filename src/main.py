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
    parser.add_argument("algorithm", choices=["ga", "hc", "sa", "all"])
    args = parser.parse_args()

    def run_ga():
        output_GA_control= GA_out(vehicles, ship, population, iteration, mutation)
        for i in range(3):
            output_GA_I1= GA_out(vehicles, ship, population, iteration_i1, mutation)
            output_GA_I2= GA_out(vehicles, ship, population, iteration_i2, mutation)
            output_GA_I3= GA_out(vehicles, ship, population, iteration_i3, mutation)

            output_GA_P1= GA_out(vehicles, ship, population_p1, iteration, mutation)
            output_GA_P2= GA_out(vehicles, ship, population_p2, iteration, mutation)
            output_GA_P3= GA_out(vehicles, ship, population_p3, iteration, mutation)
        return


    if args.algorithm == "hc":
        pass

    elif args.algorithm == "sa":
        pass

    elif args.algorithm == "ga":
        run_ga()

    elif args.algorithm == "all":
        
        run_ga()