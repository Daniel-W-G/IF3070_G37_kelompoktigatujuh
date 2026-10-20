import random
from .model.state import State
from .model.placement import Placement



def get_dimensions(vehicle, placement):
    if placement.rotated:
        return vehicle.length, vehicle.width
    return vehicle.width, vehicle.length


def objective(state, vehicles): # <---------------------------------------------------------------------------------------------------------------------------- penting
    total = 0
    for id, p in state.placements.items():
        if p.loaded:
            total += vehicles[id].shipping_fee
            # total += (1/vehicles[id].eta) buat minimize)

    return total


def total_weight(state, vehicles): 
    total = 0
    for id, p in state.placements.items():
        if p.loaded:
            total += vehicles[id].weight

    return total

# ngecek state valid nggak:
# - ID kendaraan di state.placements = ID di vehicles
# - Total berat <= ship.max_capacity
# - Kendaraan yg ga loaded -> 0 harus x dan y nya None
# - Kendaraan yg loaded -> x dan y hrs int
# - Letak kendaraan gaboleh
# note: function random_state dan generate_neighbors udh ada validasi is_valid di dalamnya, jadi ga perlu di luar lagi
def is_valid(state, vehicles, ship): 
    if state.placements.keys() != vehicles.keys():
        return False
    if total_weight(state, vehicles) > ship.max_capacity:
        return False

    occupied = set()

    for id, p in state.placements.items():
        if not p.loaded:
            if p.x is not None or p.y is not None:
                return False
            continue
        if type(p.x) is not int or type(p.y) is not int:
            return False

        w, l = get_dimensions(vehicles[id], p)

        if (p.x < 0 or p.y < 0 or p.x + w > ship.width or p.y + l > ship.length):
            return False

        for x in range(p.x, p.x + w):
            for y in range(p.y, p.y + l):
                if (x, y) in occupied:
                    return False
                occupied.add((x, y))
    return True


def random_state(vehicles, ship): 
    state = State({id: Placement() for id in vehicles})
    ids = list(vehicles)
    random.shuffle(ids)
    chance: float = 0.5 # ubah kemungkinan dilewat -> gadimasukin ke kapal
    tries: int = 50 # maks nyoba x kali orientasi & posisi acak

    for id in ids:
        if random.random() < chance: 
            continue

        for _ in range(tries): 
            p = Placement(rotated=random.choice([False, True]))
            w, l = get_dimensions(vehicles[id], p)

            if w > ship.width or l > ship.length:
                continue

            p.loaded = True
            p.x = random.randint(0, ship.width - w)
            p.y = random.randint(0, ship.length - l)
            state.placements[id] = p

            if is_valid(state, vehicles, ship):
                break

            state.placements[id] = Placement()

    return state


def generate_neighbors(state, vehicles, ship): # return array semua neighbor state yg valid dari state sekarang
    neighbors = []

    def add_if_valid(candidate):
        if is_valid(candidate, vehicles, ship):
            neighbors.append(candidate)

    for id, p in state.placements.items():
        w, l = get_dimensions(vehicles[id], p)
        for x in range(ship.width - w + 1):
            for y in range(ship.length - l + 1):
                if p.loaded and (p.x, p.y) == (x, y):
                    continue

                candidate = state.copy()
                candidate.placements[id] = Placement(
                    True, x, y, p.rotated
                )
                add_if_valid(candidate)

        if p.loaded:
            candidate = state.copy()
            candidate.placements[id] = Placement(
                rotated=p.rotated
            )
            add_if_valid(candidate)
 
        candidate = state.copy()
        candidate.placements[id].rotated = not p.rotated
        add_if_valid(candidate)

    ids = list(vehicles)

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            first_id, second_id = ids[i], ids[j]
            first = state.placements[first_id]
            second = state.placements[second_id]

            if not first.loaded and not second.loaded:
                continue

            candidate = state.copy()
            candidate.placements[first_id] = Placement(
                second.loaded, second.x, second.y, first.rotated
            )
            candidate.placements[second_id] = Placement(
                first.loaded, first.x, first.y, second.rotated
            )
            add_if_valid(candidate)

    return neighbors


def random_neighbor(state, vehicles, ship):
    neighbors = generate_neighbors(state, vehicles, ship)
    if neighbors:
        return random.choice(neighbors)

    return None