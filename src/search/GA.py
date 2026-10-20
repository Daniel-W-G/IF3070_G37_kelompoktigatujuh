import random
from ..utils import *
from ..import model
from time import perf_counter
import json
from pathlib import Path


def generate_population(size, vehicles, ship):
    population = []

    for _ in range(size):
        state = random_state(vehicles, ship)
        population.append(state)

    return population



def select_parents(population, vehicles):

    if not population:
        raise ValueError("populasi tak boleh kosong")

    fitness_scores = [objective(state, vehicles) for state in population]

    if sum(fitness_scores) == 0:
        return random.choices(population, k=2)

    return random.choices(population, weights=fitness_scores, k=2)



def crossover(parent1, parent2, vehicles, ship):
    chance: float = 0.5
    parent1 = parent1.copy()
    parent2 = parent2.copy()
    child = State({id: Placement() for id in vehicles})

    for id in vehicles:
        if random.random() < chance:
            child.placements[id] = parent1.placements[id]
        else:
            child.placements[id] = parent2.placements[id]

    if not is_valid(child, vehicles, ship):
        return random_state(vehicles, ship)

    return child



def mutate(state, vehicles, ship, mutation_rate=0.1):
    new_state = state.copy()

    for id in vehicles:
        if random.random() < mutation_rate:
            p = Placement(rotated=random.choice([False, True]))
            w, l = get_dimensions(vehicles[id], p)

            if w > ship.width or l > ship.length:
                continue

            p.loaded = True
            p.x = random.randint(0, ship.width - w)
            p.y = random.randint(0, ship.length - l)
            new_state.placements[id] = p

    if not is_valid(new_state, vehicles, ship):
        return random_state(vehicles, ship)

    return new_state



def genetic_algorithm(vehicles, ship, population_size, generations, mutation_rate):
    start_time = perf_counter()

    population = []
    population.extend(generate_population(population_size-len(population), vehicles, ship))

    initial_population = [s.copy() for s in population]
    scores = [objective(s, vehicles) for s in population]
    max_history = [max(scores)]
    average_history = [sum(scores) / len(scores)]

    for _ in range(generations):
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, vehicles)
            child1 = crossover(parent1, parent2, vehicles, ship)
            child2 = crossover(parent2, parent1, vehicles, ship)

            child1 = mutate(child1, vehicles, ship, mutation_rate)
            child2 = mutate(child2, vehicles, ship, mutation_rate)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population
        scores = [objective(s, vehicles) for s in population]
        max_history.append(max(scores))
        average_history.append(sum(scores) / len(scores))

    best_state = max(population, key=lambda s: objective(s, vehicles))
    return {
    "initial_population": initial_population,
    "final_population": population,
    "final_state": best_state,
    "final_score": objective(best_state, vehicles),
    "max_history": max_history,
    "average_history": average_history,
    "population_size": population_size,
    "generations": generations,
    "mutation_rate": mutation_rate,
    "duration_seconds": perf_counter() - start_time
}



def GA_out(vehicles, ship, population_size: int, generations: int, mutation_rate: float):
    result = genetic_algorithm(vehicles, ship, population_size, generations, mutation_rate)

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
        "initial_population": [to_dict(s) for s in result["initial_population"]],
        "final_population": [to_dict(s) for s in result["final_population"]],
        "final_state": to_dict(result["final_state"]),
        "final_score": result["final_score"],
        "max_history": result["max_history"],
        "average_history": result["average_history"],
        "population_size": result["population_size"],
        "generations": result["generations"],
        "mutation_rate": result["mutation_rate"],
        "duration_seconds": result["duration_seconds"]  
    }



    output_path = Path(__file__).resolve().parents[2] / "output"
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / "GA_output.json"
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)

    return output






# --------------------------------testing---------------------------------#


if __name__ == "__main__":
    vehicles = {
        "V1": model.Vehicle("V1", 2, 3, 100, 20, 5),
        "V2": model.Vehicle("V2", 3, 2, 150, 15, 2),
        "V3": model.Vehicle("V3", 1, 1, 50, 10, 1),
        "V4": model.Vehicle("V4", 2, 2, 120, 23, 3),
        "V5": model.Vehicle("V5", 4, 1, 200, 9, 1),
    }

    ship = model.Ship(5, 20, 50)

    population = 100
    iterations = 50
    mutation = 0.1

    output = GA_out(vehicles, ship, population, iterations, mutation)

