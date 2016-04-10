class Agent(object):
    def __init__(
        self,
        character_id,
        character_name,
        ships_destroyed,
            isk_destroyed):
        self.character_id = character_id
        self.character_name = character_name
        self.ships_destroyed = ships_destroyed
        self.isk_destroyed = isk_destroyed
