class Motion:
    def __init__(self):
        self.vertical_displacement = 0  # For vertical (Y-axis) motion due to gravity or jump
        self.gravity_force = 0.7        # Gravity effect value
        self.rect = None
        self.speed = 5
        self.last_jump_time = 0

    def apply_gravity(self, rect):
        # Apply gravity effect on vertical displacement if player is in air
        if rect.bottom < ground:
            self.vertical_displacement -= self.gravity_force
            rect.bottom -= self.vertical_displacement
        # Ensure the player does not fall below ground level
        else:
            rect.bottom = ground
            self.vertical_displacement = 0

    def jump(self, interval=0, jump_height=16):
        current_time = tm.time()
        # Apply upward force if player is on the ground
        if self.rect.bottom == ground:
            # check if the time passed after the last jump is more than the interval
            if current_time - self.last_jump_time >= interval:
                self.vertical_displacement = jump_height
                self.rect.bottom -= self.vertical_displacement
                self.last_jump_time = current_time

    def move_horizontal(self, direction, border=False):
        # Move left or right on the X-axis
        if direction == "left":
            # To prevent the rect to go beyond the window border
            if border:
                if self.rect.left >= 0:
                    self.rect.left -= self.speed
            else:
                self.rect.left -= self.speed
        elif direction == "right":
            if border:
                if self.rect.right <= display_size[0]:
                    self.rect.right += self.speed
            else:
                self.rect.right += self.speed
