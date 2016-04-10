class Ship(object):
    def __init__(
        self,
        ship_type_id,
        ship_name,
        ships_destroyed,
            isk_destroyed):
        self.ship_type_id = ship_type_id
        self.ship_name = ship_name
        self.ships_destroyed = ships_destroyed
        self.isk_destroyed = isk_destroyed
