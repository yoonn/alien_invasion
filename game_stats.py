class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_settings):
        """기록을 초기화 합니다."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # 외계인 침공 게임을 비활성 상태로 시작합니다.
        self.game_active = False
        
    def reset_stats(self):
        """게임 도중에 바뀔 수 있는 기록을 초기화합니다."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
