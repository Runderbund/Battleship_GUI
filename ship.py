class Ship:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.hits = [False] * size

    def hit(self, idx: int) -> bool:
        self.hits[idx] = True
        return all(self.hits)

    def is_sunk(self) -> bool:
        return all(self.hits)

