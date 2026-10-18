class Placement:
    def __init__(self, loaded: bool = False, x: int | None = None, y: int | None = None, rotated: bool = False):
        self.loaded: bool = loaded
        self.x: int | None = x # sistem koordinatnya pokoknya titik pojok kiri dari kendaraan, rotated cuman balikin width dan length dr kendaraan 
        self.y: int | None = y # x & y harus isinya none kalo loaded = false
        self.rotated: bool = rotated