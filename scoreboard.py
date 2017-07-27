import pygame.font


class Scoreboard():
    """점수 표시에 사용할 클래스"""

    def __init__(self, ai_settings, screen, stats):
        """설정을 초기화합니다."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 점수표시에 사용할 폰트를 설정합니다.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 초기 점수 이미지를 중비합니다.
        self.prep_score()

    def prep_score(self):
        """점수를 이미지로 바꿉니다."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color
                                            , self.ai_settings.bg_color)

        # 점수를 화면 오른쪽 위에 표시합니다.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """화면에 점수를 표시합니다."""
        self.screen.blit(self.score_image, self.score_rect)