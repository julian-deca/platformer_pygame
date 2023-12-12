from classItem import Item


class Coin(Item):
    def __init__(self, game, image, width, height, position, value, initial_speed_x):
        super().__init__(game, image, width, height,
                         position, initial_speed_x, "COIN", True, 5)
        self.value = value

    def update(self):
        return super().update()

    def draw(self, screen):
        return super().draw(screen)

    def get_frame(self):
        return super().get_frame()
