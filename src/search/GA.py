import random
from ..utils import *
from time import perf_counter
import json
from pathlib import Path
import matplotlib.pyplot as plt
from ..visualisasi import plot_state
from datetime import datetime



def generate_population(size, vehicles, ship):
    population = []
    for i in range(size):
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
    ids = list(vehicles)
    if len(ids) < 2:
        return parent1.copy()
    cut = random.randint(1, len(ids) - 1)
    parent1 = parent1.copy()
    parent2 = parent2.copy()
    child = State({id: Placement() for id in vehicles})
    for index, id in enumerate(ids):
        if index < cut:
            child.placements[id] = parent1.placements[id]
        else:
            child.placements[id] = parent2.placements[id]
    if not is_valid(child, vehicles, ship):
        return random.choice([parent1, parent2]).copy()
    return child


def mutate(state, vehicles, ship, mutation_rate=0.1):
    temp_state = state.copy()
    if random.random() >= mutation_rate or not vehicles:
        return temp_state
    id = random.choice(list(vehicles))
    if random.choice([True, False]):
        p = Placement(
            loaded=True,
            rotated=random.choice([False, True])
        )
        w, l = get_dimensions(vehicles[id], p)
        if w > ship.width or l > ship.length:
            return temp_state
        p.x = random.randint(0, ship.width - w)
        p.y = random.randint(0, ship.length - l)
    else:
        p = Placement(
            loaded=False,
            rotated=temp_state.placements[id].rotated
        )
    temp_state.placements[id] = p
    if not is_valid(temp_state, vehicles, ship):
        return state.copy()
    return temp_state



def genetic_algorithm(vehicles, ship, population_size, iterations, mutation_rate):
    start_time = perf_counter()
    population = generate_population(population_size, vehicles, ship)
    initial_population = [s.copy() for s in population]
    scores = [objective(s, vehicles) for s in population]
    max_history = [max(scores)]
    average_history = [sum(scores) / len(scores)]

    for _ in range(iterations):
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
    "iterations": iterations,
    "mutation_rate": mutation_rate,
    "duration_seconds": perf_counter() - start_time
}



def GA_out(vehicles, ship, population_size: int, iterations: int, mutation_rate: float):
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

    outputs = []
    output_path = Path(__file__).resolve().parents[2] / "output" / "GA"
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    base_name = f"GA_pop{population_size}_gen{iterations}_{timestamp}"

    for i in range(3):
        result = genetic_algorithm(
            vehicles, ship, population_size, iterations, mutation_rate
        )
        output = {
            "initial_population": [to_dict(s) for s in result["initial_population"]],
            "final_population": [to_dict(s) for s in result["final_population"]],
            "final_state": to_dict(result["final_state"]),
            "final_score": result["final_score"],
            "max_history": result["max_history"],
            "average_history": result["average_history"],
            "population_size": result["population_size"],
            "iterations": result["iterations"],
            "mutation_rate": result["mutation_rate"],
            "duration_seconds": result["duration_seconds"]
        }
        outputs.append(output)
        run_name = f"{base_name}_run{i + 1}"
        file_path = output_path / f"{run_name}.json"
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)
        initial_state = max(result["initial_population"], key=lambda s: objective(s, vehicles))
        initial_result = plot_state(initial_state, vehicles, ship, f"GA Run {i + 1} - State Terbaik | Populasi Awal \n Populasi: {population_size} | Generasi: {iterations}")
        final_result = plot_state(result["final_state"], vehicles, ship, f"GA Run {i + 1} - State Terbaik | Generasi Terakhir \n Populasi: {population_size} | Generasi: {iterations}")
        initial_result.savefig(output_path / f"{run_name}_initial.png", dpi=200, bbox_inches="tight")
        final_result.savefig(output_path / f"{run_name}_final.png", dpi=200, bbox_inches="tight")
        plt.close(initial_result)
        plt.close(final_result)

    history_result = plot_ga_history(outputs)
    history_result.savefig(
        output_path / f"{base_name}_history.png",
        dpi=200, bbox_inches="tight"
    )

    plt.close(history_result)
    return outputs



def plot_ga_history(results):
    fig, ax = plt.subplots(figsize=(10, 6))

    for index, result in enumerate(results):
        iterations = range(len(result["max_history"]))
        line, = ax.plot(
            iterations,
            result["max_history"],
            label=f"Run {index + 1} maksimum"
        )
        ax.plot(
            iterations,
            result["average_history"],
            color=line.get_color(),
            linestyle="--",
            label=f"Run {index + 1} rata-rata"
        )

    ax.set_title(f"Perkembangan Objective Function GA | Populasi: {results[0]['population_size']} | Generasi: {results[0]['iterations']}")
    ax.set_xlabel("Iterasi")
    ax.set_ylabel("Total Shipping Fee")
    ax.grid(True, alpha=0.3)
    ax.legend(ncol=2)
    fig.tight_layout()
    return fig