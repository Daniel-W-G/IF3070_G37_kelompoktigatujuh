import random
from ..utils import *
from ..import model


def generate_population(size, vehicles, ship, rng=None):
    if rng is None:
        rng = random.Random()
    population = []

    for _ in range(size):
        state = random_state(vehicles, ship, rng)
        population.append(state)

    return population


def select_parents(population, vehicles, rng=None):
    if rng is None:
        rng = random.Random()

    if not population:
        raise ValueError("populasi tak boleh kosong")

    fitness_scores = [objective(state, vehicles) for state in population]

    if sum(fitness_scores) == 0:
        return rng.choices(population, k=2)

    return rng.choices(population, weights=fitness_scores, k=2)


def crossover(parent1, parent2, vehicles, ship, rng=None):
    if rng is None:
        rng = random.Random()
    chance: float = 0.5
    parent1 = parent1.copy()
    parent2 = parent2.copy()
    child = State({id: Placement() for id in vehicles})

    for id in vehicles:
        if rng.random() < chance:
            child.placements[id] = parent1.placements[id]
        else:
            child.placements[id] = parent2.placements[id]

    if not is_valid(child, vehicles, ship):
        return random_state(vehicles, ship, rng)

    return child


def mutate(state, vehicles, ship, mutation_rate=0.1, rng=None):
    if rng is None:
        rng = random.Random()
    new_state = state.copy()

    for id in vehicles:
        if rng.random() < mutation_rate:
            p = Placement(rotated=rng.choice([False, True]))
            w, l = get_dimensions(vehicles[id], p)

            if w > ship.width or l > ship.length:
                continue

            p.loaded = True
            p.x = rng.randint(0, ship.width - w)
            p.y = rng.randint(0, ship.length - l)
            new_state.placements[id] = p

    if not is_valid(new_state, vehicles, ship):
        return random_state(vehicles, ship, rng)

    return new_state



def genetic_algorithm(vehicles, ship, state=None, population_size=50, generations=100, mutation_rate=0.1, rng=None):
    if rng is None:
        rng = random.Random()
    if state is not None:
        population = [state.copy()]
    else:
        population = []
    population.extend(generate_population(population_size-len(population), vehicles, ship, rng))

    for _ in range(generations):
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, vehicles, rng)
            child1 = crossover(parent1, parent2, vehicles, ship, rng)
            child2 = crossover(parent2, parent1, vehicles, ship, rng)

            child1 = mutate(child1, vehicles, ship, mutation_rate, rng)
            child2 = mutate(child2, vehicles, ship, mutation_rate, rng)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    best_state = max(population, key=lambda s: objective(s, vehicles))
    return best_state



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

    final_state = genetic_algorithm(
        vehicles,
        ship,
        population_size=50,
        generations=100,
        mutation_rate=0.1
    )

    print("Total shipping fee:", objective(final_state, vehicles))
    print("Total berat:", total_weight(final_state, vehicles))
    print("State valid:", is_valid(final_state, vehicles, ship))

    for vehicle_id, placement in final_state.placements.items():
        if placement.loaded:
            print(
                vehicle_id,
                "posisi:", (placement.x, placement.y),
                "rotated:", placement.rotated
            )
        else:
            print(vehicle_id, "tidak dimuat")
