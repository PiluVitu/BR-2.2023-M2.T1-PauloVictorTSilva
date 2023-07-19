import pygame

from dino_runner.utils.constants import (
    BG,
    ICON,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    FPS,
)

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.osbstacles.obstacle_maneger import ObstacleManeger

FONT_STYLE = "dino_runner/assets/Other/JetBrainsMono-Bold.ttf"
COLORS = {"background": (255, 255, 255), "text": (0, 0, 0)}


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.current_score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManeger()

    def print_on_screen(self, font_size, data, color, position):
        font = pygame.font.Font(FONT_STYLE, font_size)
        text = font.render(data, True, color)
        text_rect = text.get_rect()
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def reset_game_score_and_game_speed(self):
        self.score = 0
        self.game_speed = 20

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacle()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        self.current_score = self.score
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(COLORS["background"])
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.print_on_screen(22, f"Score: {self.score}", COLORS["text"], (1000, 50))

    def show_menu(self):
        self.screen.fill(COLORS["background"])
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.print_on_screen(
                22,
                "Press any key to start",
                COLORS["text"],
                (half_screen_width, half_screen_height),
            )
        else:
            self.screen.blit(
                ICON,
                (half_screen_width - ICON.get_width() / 2, half_screen_height - 140),
            )

            if self.death_count > 1:
                self.print_on_screen(
                    22,
                    f"You went from vasco {self.death_count} time",
                    COLORS["text"],
                    ((half_screen_width, half_screen_height)),
                )
                self.print_on_screen(
                    22,
                    f"Your score is: {self.current_score}",
                    COLORS["text"],
                    ((half_screen_width, half_screen_height + 30)),
                )
                self.print_on_screen(
                    22,
                    "Press any key to restart",
                    COLORS["text"],
                    ((half_screen_width, half_screen_height + 60)),
                )
                self.reset_game_score_and_game_speed()
            else:
                self.print_on_screen(
                    22,
                    "You went from vasco",
                    COLORS["text"],
                    ((half_screen_width, half_screen_height)),
                )
                self.print_on_screen(
                    22,
                    f"Your score is: {self.current_score}",
                    COLORS["text"],
                    ((half_screen_width, half_screen_height + 30)),
                )
                self.print_on_screen(
                    22,
                    "Press any key to restart",
                    COLORS["text"],
                    ((half_screen_width, half_screen_height + 60)),
                )
                self.reset_game_score_and_game_speed()

        pygame.display.update()
        self.handle_event_on_menu()

    def handle_event_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
