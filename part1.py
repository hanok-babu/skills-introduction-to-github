import sys
import random
import pygame

VW, VH = 1000, 800
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

MODE_CRICKET = "HAND_CRICKET"
MODE_MAZE = "MAZE"

LVL_EASY = "Easy"
LVL_MED = "Medium"
LVL_HARD = "Hard"


class SimpleBtn:
    def __init__(self, xywh, txt, col_bg, col_fg=WHITE, fnt=None, brd=2):
        self.rect = pygame.Rect(xywh)
        self.txt = txt
        self.col_bg = col_bg
        self.col_fg = col_fg
        self.fnt = fnt
        self.brd = brd

    def draw(self, scr):
        pygame.draw.rect(scr, self.col_bg, self.rect)
        pygame.draw.rect(scr, BLACK, self.rect, self.brd)
        t = self.fnt.render(self.txt, True, self.col_fg)
        scr.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, e):
        return (e.type == pygame.MOUSEBUTTONDOWN
                and e.button == 1
                and self.rect.collidepoint(e.pos))


def put_text(scr, txt, x, y, fnt, col):
    scr.blit(fnt.render(txt, True, col), (x, y))


def draw_panel(scr, r, col=WHITE):
    pygame.draw.rect(scr, (0, 0, 0), r)
    pygame.draw.rect(scr, col, r, 2)


class MenuScreen:
    def __init__(self, app):
        self.app = app
        self.btn1 = SimpleBtn((VW // 2 - 200, 270, 400, 70),
                              "Play Hand Cricket", GREEN, fnt=self.app.font_m)
        self.btn2 = SimpleBtn((VW // 2 - 200, 360, 400, 70),
                              "Play Maze Runner", ORANGE, fnt=self.app.font_m)
        self.btn3 = SimpleBtn((VW // 2 - 120, 460, 240, 60),
                              "Exit", RED, fnt=self.app.font_m)

    def loop(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.btn1.clicked(e):
                self.app.go_diff(MODE_CRICKET)
            if self.btn2.clicked(e):
                self.app.go_diff(MODE_MAZE)
            if self.btn3.clicked(e):
                pygame.quit()
                sys.exit()

        self.app.screen.blit(self.app.bg_menu, (0, 0))
        t = self.app.font_x.render("Dual Games", True, WHITE)
        self.app.screen.blit(t, t.get_rect(center=(VW // 2, 150)))
        s = self.app.font_m.render("Choose a game to start", True, GRAY)
        self.app.screen.blit(s, s.get_rect(center=(VW // 2, 200)))

        self.btn1.draw(self.app.screen)
        self.btn2.draw(self.app.screen)
        self.btn3.draw(self.app.screen)

        pygame.display.flip()
        self.app.clock.tick(FPS)


class DiffScreen:
    def __init__(self, app):
        self.app = app
        self.opts = [
            SimpleBtn((VW // 2 - 300, 300, 180, 70),
                      LVL_EASY, BLUE, fnt=self.app.font_m),
            SimpleBtn((VW // 2 - 90,  300, 180, 70),
                      LVL_MED,  BLUE, fnt=self.app.font_m),
            SimpleBtn((VW // 2 + 120, 300, 180, 70),
                      LVL_HARD, BLUE, fnt=self.app.font_m),
        ]
        self.btn_go = SimpleBtn((VW // 2 - 120, 400, 240, 70),
                                "Start", BLUE, fnt=self.app.font_m)
        self.btn_back = SimpleBtn((self.app.screen.get_width() - 160, 20, 140, 48),
                                  "Back", GRAY, fnt=self.app.font_m)
        self.sel = None

    def loop(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.btn_back.clicked(e):
                self.app.go_menu()
            for b in self.opts:
                if b.clicked(e):
                    self.sel = b.txt
            if self.btn_go.clicked(e) and self.sel is not None:
                self.app.start_game(self.sel)

        self.app.screen.blit(self.app.bg_menu, (0, 0))
        t = self.app.font_l.render("Select Difficulty", True, WHITE)
        self.app.screen.blit(t, t.get_rect(center=(VW // 2, 200)))

        for b in self.opts:
            b.draw(self.app.screen)
            if self.sel == b.txt:
                pygame.draw.rect(self.app.screen, WHITE, b.rect, 4)

        if self.sel is None:
            old = self.btn_go.col_bg
            self.btn_go.col_bg = GRAY
            self.btn_go.draw(self.app.screen)
            self.btn_go.col_bg = old
        else:
            self.btn_go.draw(self.app.screen)

        self.btn_back.draw(self.app.screen)
        pygame.display.flip()
        self.app.clock.tick(FPS)


class TinyApp:
    def __init__(self, scr, clk, bg1, bg2, bg3, bg4):
        self.screen = scr
        self.clock = clk
        self.bg_menu = bg1
        self.bg_cricket = bg2
        self.bg_maze = bg3
        self.bg_results = bg4

        self.font_s = pygame.font.SysFont(None, 22)
        self.font_m = pygame.font.SysFont(None, 30)
        self.font_l = pygame.font.SysFont(None, 42)
        self.font_x = pygame.font.SysFont(None, 56)

        self.state = "MENU"
        self.mode = None
        self.diff = None
        self.ctrl = None
        self.last_result = None

        self.menu = MenuScreen(self)
        self.diff_scr = DiffScreen(self)
        self.res_scr = ResultScreen(self)

    def run(self):
        while True:
            if self.state == "MENU":
                self.menu.loop()
            elif self.state == "DIFFICULTY":
                self.diff_scr.loop()
            elif self.state == "GAME":
                if self.ctrl is None:
                    self.go_menu()
                else:
                    self.ctrl.loop()
            elif self.state == "RESULT":
                self.res_scr.loop()
            else:
                self.go_menu()

    def go_menu(self):
        self.state = "MENU"
        self.mode = None
        self.diff = None
        self.ctrl = None
        self.last_result = None

    def go_diff(self, mode):
        self.mode = mode
        self.diff = None
        self.state = "DIFFICULTY"

    def start_game(self, d):
        self.diff = d
        if self.mode == MODE_CRICKET:
            self.ctrl = HandCricket(self, d)
        elif self.mode == MODE_MAZE:
            self.ctrl = MazeRunner(self, d)
        self.state = "GAME"

    def end_game(self, data):
        self.last_result = data
        self.state = "RESULT"


def main():
    pygame.init()
    scr = pygame.display.set_mode((VW, VH))
    pygame.display.set_caption(
        "Dual Games: Hand Cricket + Maze Runner (Beginner)")
    clk = pygame.time.Clock()

    img_menu = pygame.image.load("bg.png").convert()
    img_cri = pygame.image.load("cricket.png").convert()
    img_maze = pygame.image.load("maze.png").convert()
    img_res = pygame.image.load("results.png").convert()

    bg1 = pygame.transform.scale(img_menu, (VW, VH))
    bg2 = pygame.transform.scale(img_cri, (VW, VH))
    bg3 = pygame.transform.scale(img_maze, (VW, VH))
    bg4 = pygame.transform.scale(img_res, (VW, VH))

    app = TinyApp(scr, clk, bg1, bg2, bg3, bg4)
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
