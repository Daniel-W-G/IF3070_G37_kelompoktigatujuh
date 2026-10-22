from time import perf_counter

from ..utils import random_state, generate_neighbors, objective, is_valid


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