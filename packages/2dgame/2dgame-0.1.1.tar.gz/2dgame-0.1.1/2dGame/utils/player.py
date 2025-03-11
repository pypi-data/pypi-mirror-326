class Player:
    def __init__(self, x: int = 0, y: int = 0, health: int = 3):
        self.x = x
        self.y = y
        self._health = health

    @property
    def health(self):
        return self._health if self._health > -1 else 0

    def damage(self, amount: int):
         self._health -= amount

    def heal(self, amount):
        self._health += amount
