class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        
        # Alien settings.
        self.fleet_drop_speed = 50

        # item 설정
        self.item_margin = 30

        # item 속도를 높이는 설정
        self.item_scale = 1.3

        # 게임 속도를 높이는 설정
        self.speedup_scale = 1.1
        # 외계인 점수를 높이는 설정
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """게임 도중에 바뀔 수 있는 설정을 초기화 합니다."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.item_speed_factor = 1

        # fleet_direction 이 1이면 오른쪽, -1이면 왼쪽입니다.
        self.fleet_direction = 1

        # 점수 설정
        self.alien_points = 50

    def increase_speed(self):
        """속도 설정과 외계인 점수를 올립니다."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.item_speed_factor *= self.item_scale

        self.alien_points = int(self.alien_points * self.score_scale)