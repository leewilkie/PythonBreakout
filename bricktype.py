class BrickType:
    def __init__(self, sprite_idx, hits):
        self.sprite_idx = sprite_idx  # index of the sprite to use for this brick type
        self.hits = hits      # number of hits required to break this brick
