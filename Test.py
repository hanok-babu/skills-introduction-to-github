import sys
import random
import pygame

# -------------------- Constants --------------------
WIDTH, HEIGHT = 1000, 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK = (40, 40, 40)
BLUE = (66, 135, 245)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
ORANGE = (243, 156, 18)
PURPLE = (155, 89, 182)
BG1 = (15, 30, 45)   # hand cricket background
BG2 = (10, 10, 20)   # maze background

STATE_MENU = "MENU"
STATE_DIFFICULTY = "DIFFICULTY"
STATE_GAME = "GAME"
STATE_RESULT = "RESULT"

GAME_HAND_CRICKET = "HAND_CRICKET"
GAME_MAZE = "MAZE"

DIFF_EASY = "Easy"
DIFF_MED = "Medium"
DIFF_HARD = "Hard"

# -------------------- Simple UI --------------------


class Button:
    def __init__(self, rect_tuple, text, bg_color, fg_color=WHITE, font=None, radius=10, border=2):
        self.rect = pygame.Rect(rect_tuple)
        self.text = text
        self.bg = bg_color
        self.fg = fg_color
        self.font = font
        self.radius = radius
        self.border = border

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg, self.rect,
                         border_radius=self.radius)
        pygame.draw.rect(surface, BLACK, self.rect,
                         self.border, border_radius=self.radius)
        label_surface = self.font.render(self.text, True, self.fg)
        surface.blit(label_surface, label_surface.get_rect(
            center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False


def draw_label(surface, text, pos_tuple, font, color):
    label_surface = font.render(text, True, color)
    surface.blit(label_surface, pos_tuple)


class MenuScreen:
    def __init__(self, app):
        self.app = app
        self.button_hand = Button(
            (WIDTH//2-200, 270, 400, 70), "Play Hand Cricket", GREEN, font=self.app.FONT_MD)
        self.button_maze = Button(
            (WIDTH//2-200, 360, 400, 70), "Play Maze Runner", ORANGE, font=self.app.FONT_MD)
        self.button_exit = Button(
            (WIDTH//2-120, 460, 240, 60), "Exit", RED, font=self.app.FONT_MD)

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.button_hand.is_clicked(event):
                self.app.goto_difficulty(GAME_HAND_CRICKET)
            if self.button_maze.is_clicked(event):
                self.app.goto_difficulty(GAME_MAZE)
            if self.button_exit.is_clicked(event):
                pygame.quit()
                sys.exit()

        self.app.screen.fill(DARK)
        title_surface = self.app.FONT_XL.render("Dual Games", True, WHITE)
        self.app.screen.blit(
            title_surface, title_surface.get_rect(center=(WIDTH//2, 150)))
        subtitle_surface = self.app.FONT_MD.render(
            "Choose a game to start", True, GRAY)
        self.app.screen.blit(
            subtitle_surface, subtitle_surface.get_rect(center=(WIDTH//2, 200)))
        self.button_hand.draw(self.app.screen)
        self.button_maze.draw(self.app.screen)
        self.button_exit.draw(self.app.screen)
        pygame.display.flip()
        self.app.clock.tick(FPS)


class DifficultyScreen:
    def __init__(self, app):
        self.app = app
        self.buttons = [
            Button((WIDTH//2-300, 300, 180, 70),
                   DIFF_EASY, BLUE, font=self.app.FONT_MD),
            Button((WIDTH//2 - 90, 300, 180, 70),
                   DIFF_MED,  BLUE, font=self.app.FONT_MD),
            Button((WIDTH//2+120, 300, 180, 70),
                   DIFF_HARD, BLUE, font=self.app.FONT_MD),
        ]
        self.button_start = Button(
            (WIDTH//2-120, 400, 240, 70), "Start", BLUE, font=self.app.FONT_MD)
        self.button_back = Button((self.app.screen.get_width(
        ) - 160, 20, 140, 48), "Back", GRAY, font=self.app.FONT_MD)
        self.selected_text = None

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.button_back.is_clicked(event):
                self.app.goto_menu()
            for b in self.buttons:
                if b.is_clicked(event):
                    self.selected_text = b.text
            if self.button_start.is_clicked(event) and self.selected_text is not None:
                self.app.start_game(self.selected_text)

        self.app.screen.fill(DARK)
        title_surface = self.app.FONT_LG.render(
            "Select Difficulty", True, WHITE)
        self.app.screen.blit(
            title_surface, title_surface.get_rect(center=(WIDTH//2, 200)))
        for b in self.buttons:
            if self.selected_text == b.text:
                orig = b.bg
                b.bg = PURPLE
                b.draw(self.app.screen)
                b.bg = orig
                pygame.draw.rect(self.app.screen, WHITE,
                                 b.rect, 3, border_radius=10)
            else:
                b.draw(self.app.screen)
        if self.selected_text is None:
            old = self.button_start.bg
            self.button_start.bg = GRAY
            self.button_start.draw(self.app.screen)
            self.button_start.bg = old
        else:
            self.button_start.draw(self.app.screen)
        self.button_back.draw(self.app.screen)
        pygame.display.flip()
        self.app.clock.tick(FPS)


class ResultScreen:
    def __init__(self, app):
        self.app = app
        self.button_play_again = Button(
            (WIDTH//2-360, 560, 220, 60), "Play Again", GREEN,  font=self.app.FONT_MD)
        self.button_change_diff = Button(
            (WIDTH//2-110, 560, 220, 60), "Change Difficulty", ORANGE, font=self.app.FONT_MD)
        self.button_menu = Button(
            (WIDTH//2+140, 560, 220, 60), "Back to Menu", BLUE,  font=self.app.FONT_MD)

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.button_play_again.is_clicked(event):
                self.app.start_game(self.app.difficulty)
            if self.button_change_diff.is_clicked(event):
                self.app.state = STATE_DIFFICULTY
            if self.button_menu.is_clicked(event):
                self.app.goto_menu()

        self.app.screen.fill(DARK)
        title_surface = self.app.FONT_LG.render("Results", True, WHITE)
        self.app.screen.blit(
            title_surface, title_surface.get_rect(center=(WIDTH//2, 120)))

        payload = self.app.result_payload or {}
        y = 200
        x = WIDTH//2 - 280
        for key in payload:
            val = payload[key]
            color = WHITE if key == "Game" else (220, 220, 220)
            draw_label(self.app.screen,
                       f"{key}: {val}", (x, y), self.app.FONT_LG, color)
            y += 40

        self.button_play_again.draw(self.app.screen)
        self.button_change_diff.draw(self.app.screen)
        self.button_menu.draw(self.app.screen)
        pygame.display.flip()
        self.app.clock.tick(FPS)

# -------------------- App --------------------


class App:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.FONT_SM = pygame.font.SysFont(None, 22)
        self.FONT_MD = pygame.font.SysFont(None, 30)
        self.FONT_LG = pygame.font.SysFont(None, 42)
        self.FONT_XL = pygame.font.SysFont(None, 56)

        self.state = STATE_MENU
        self.selected_game = None
        self.difficulty = None
        self.game_obj = None
        self.result_payload = None

        self.menu = MenuScreen(self)
        self.diff = DifficultyScreen(self)
        self.result = ResultScreen(self)

    def run(self):
        while True:
            if self.state == STATE_MENU:
                self.menu.loop()
            elif self.state == STATE_DIFFICULTY:
                self.diff.loop()
            elif self.state == STATE_GAME:
                if self.game_obj is None:
                    self.goto_menu()
                else:
                    self.game_obj.loop()
            elif self.state == STATE_RESULT:
                self.result.loop()
            else:
                self.goto_menu()

    def goto_menu(self):
        self.state = STATE_MENU
        self.selected_game = None
        self.difficulty = None
        self.game_obj = None
        self.result_payload = None

    def goto_difficulty(self, game_type):
        self.selected_game = game_type
        self.difficulty = None
        self.state = STATE_DIFFICULTY

    def start_game(self, difficulty_text):
        self.difficulty = difficulty_text
        if self.selected_game == GAME_HAND_CRICKET:
            self.game_obj = HandCricketGame(self, difficulty_text)
        elif self.selected_game == GAME_MAZE:
            self.game_obj = MazeRunnerGame(self, difficulty_text)
        self.state = STATE_GAME

    def finish_game(self, payload_dict):
        self.result_payload = payload_dict
        self.state = STATE_RESULT

# -------------------- Entry Point --------------------


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dual Games: Hand Cricket + Maze Runner")
    clock = pygame.time.Clock()
    app = App(screen, clock)
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
