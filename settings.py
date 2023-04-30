class Settings:
    def __init__(self):
        self.bg_color = (0, 150, 200)
        self.width = 1390
        self.height = 700
        self.ship_speed_factor = 1.5
        # Bullet settings
        self.bullet_speed_factor = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 60, 60)
        self.bullets_allowed = 3
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.ship_limit = 3
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1.5
        self.alien_speed_factor = 0.5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.alien_points = 100

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)
        print(self.alien_points)