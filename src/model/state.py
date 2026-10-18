from .placement import Placement

class State:
    def __init__(self, placements: dict[str, Placement]):
        self.placements: dict[str, Placement] = placements

    def copy(self) -> "State":
        return State({
            vehicle_id: Placement(
                loaded=p.loaded,
                x=p.x,
                y=p.y,
                rotated=p.rotated
            )
            for vehicle_id, p in self.placements.items()
        })