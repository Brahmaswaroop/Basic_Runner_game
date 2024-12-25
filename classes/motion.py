import time as tm

class Motion:
    def __init__(self, ground):
        self.vertical_displacement = 0  # For vertical (Y-axis) motion due to gravity or jump
        self.gravity_force = 0.7        # Gravity effect value
        self.speed = 0
        self.last_jump_time = 0

        self.screen = None
        self.rect = None
        self.ground = ground

    def apply_gravity(self):
        # Apply gravity effect on vertical displacement if player is in air
        if self.rect.bottom < self.ground:
            self.vertical_displacement -= self.gravity_force
            self.rect.bottom -= self.vertical_displacement
        # Ensure the player does not fall below ground level
        else:
            self.rect.bottom = self.ground
            self.vertical_displacement = 0

    def jump(self, interval=0, jump_height=16):
        # Check if player is on the ground and can jump
        if self.rect.bottom == self.ground and tm.time() - self.last_jump_time >= interval:
            self.vertical_displacement = jump_height
            self.rect.bottom -= self.vertical_displacement
            self.last_jump_time = tm.time()


    def move_horizontal(self, direction, border=False):
        # To prevent the rect to go beyond the window border
        if border:
            self.rect.clamp_ip(self.screen.get_rect())
        # Move left or right on the X-axis
        if direction == "left":
            self.rect.move_ip(-self.speed, 0)
        elif direction == "right":
            self.rect.move_ip(self.speed, 0)

