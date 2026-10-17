from .placement import Placement


class State:
    def __init__(self, placements):
        self.placements = placements

    def copy(self):
        return State({
            vehicle_id: Placement(
                loaded=p.loaded,
                x=p.x,
                y=p.y,
                rotated=p.rotated
            )
            for vehicle_id, p in self.placements.items()
        })