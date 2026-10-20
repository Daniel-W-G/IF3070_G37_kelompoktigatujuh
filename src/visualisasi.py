import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .utils import get_dimensions, objective, total_weight


def plot_state(state, vehicles, ship, title="Penempatan Kendaraan"):
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.set_xlim(0, ship.width)
    ax.set_ylim(ship.length, 0)
    ax.set_aspect("equal")

    ax.set_xticks(range(ship.width + 1))
    ax.set_yticks(range(ship.length + 1))
    ax.grid(True, color="lightgray")
    ax.set_axisbelow(True)

    colors = plt.get_cmap("tab20")
    unloaded = []

    for index, vehicle_id in enumerate(vehicles):
        placement = state.placements[vehicle_id]

        if not placement.loaded:
            unloaded.append(vehicle_id)
            continue

        width, length = get_dimensions(
            vehicles[vehicle_id], placement
        )

        rectangle = Rectangle(
            (placement.x, placement.y),
            width,
            length,
            facecolor=colors(index % 20),
            edgecolor="black",
            alpha=0.8
        )
        ax.add_patch(rectangle)

        ax.text(
            placement.x + width / 2,
            placement.y + length / 2,
            vehicle_id,
            ha="center",
            va="center"
        )

    score = objective(state, vehicles)
    weight = total_weight(state, vehicles)

    ax.set_title(
        f"{title}\n"
        f"Shipping fee: {score} | Berat: {weight}/{ship.max_capacity}"
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    if unloaded:
        unloaded_text = ", ".join(unloaded)
    else:
        unloaded_text = "Tidak ada"

    fig.text(
        0.5, 0.03,
        f"Tidak dimuat: {unloaded_text}",
        ha="center",
        wrap=True
    )

    fig.tight_layout(rect=(0, 0.08, 1, 1))
    return fig



#-----------------------------------------testing--------------------------------------------#

if __name__ == "__main__":
    from .model import Vehicle, Ship, Placement, State

    vehicles = {
        "V1": Vehicle("V1", 2, 3, 100, 20, 5),
        "V2": Vehicle("V2", 3, 2, 150, 15, 2),
        "V3": Vehicle("V3", 1, 1, 50, 10, 1)
    }

    ship = Ship(5, 10, 50)

    state = State({
        "V1": Placement(True, 0, 0, False),
        "V2": Placement(True, 0, 3, False),
        "V3": Placement(True, 1, 6, False)
    })

    plot_state(state, vehicles, ship, "Tes Visualisasi State")
    plt.show()