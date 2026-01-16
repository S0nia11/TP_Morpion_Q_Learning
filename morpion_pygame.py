import pygame
import sys
import numpy as np
import random
from collections import defaultdict

# ===================== ENVIRONNEMENT =====================
class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros(9, dtype=int)
        self.current_player = 1
        self.winner = None

    def legal_actions(self):
        return [i for i in range(9) if self.board[i] == 0]

    def step(self, action):
        self.board[action] = self.current_player
        self.winner = self.check_winner()
        done = self.winner is not None or len(self.legal_actions()) == 0
        self.current_player *= -1
        return done

    def check_winner(self):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in wins:
            s = self.board[a] + self.board[b] + self.board[c]
            if s == 3: return 1
            if s == -3: return -1
        return None

# ===================== AGENT =====================
class QLearningAgent:
    def __init__(self):
        self.Q = defaultdict(float)

    def act(self, legal_actions):
        return random.choice(legal_actions)

# ===================== INIT PYGAME =====================
pygame.init()
WIDTH, HEIGHT = 420, 520
CELL = 120
BOARD_LEFT = 30
BOARD_TOP = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morpion - Q-learning")

FONT_BIG = pygame.font.SysFont(None, 48)
FONT = pygame.font.SysFont(None, 26)

# ===================== COULEURS =====================
GRID = (40, 40, 40)
X_COLOR = (200, 60, 60)
O_COLOR = (60, 100, 200)

BTN = (200, 230, 255)
BTN_HOVER = (220, 245, 255)
BTN_TEXT = (40, 70, 100)

WHITE = (255,255,255)
BLACK = (0,0,0)

# ===================== IMAGE FOND =====================
background = pygame.image.load("light_blue.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# ===================== BOUTON =====================
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text

    def draw(self):
        color = BTN_HOVER if self.rect.collidepoint(pygame.mouse.get_pos()) else BTN
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        txt = FONT.render(self.text, True, BTN_TEXT)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# ===================== DESSIN PLATEAU =====================
def draw_board(env):
    screen.fill(WHITE)

    for i in range(1,3):
        pygame.draw.line(
            screen, GRID,
            (BOARD_LEFT, BOARD_TOP + i*CELL),
            (BOARD_LEFT + 3*CELL, BOARD_TOP + i*CELL), 3
        )
        pygame.draw.line(
            screen, GRID,
            (BOARD_LEFT + i*CELL, BOARD_TOP),
            (BOARD_LEFT + i*CELL, BOARD_TOP + 3*CELL), 3
        )

    for i in range(9):
        x = BOARD_LEFT + (i % 3) * CELL + CELL//2
        y = BOARD_TOP + (i // 3) * CELL + CELL//2

        if env.board[i] == 1:
            pygame.draw.line(screen, X_COLOR, (x-30,y-30), (x+30,y+30), 4)
            pygame.draw.line(screen, X_COLOR, (x+30,y-30), (x-30,y+30), 4)
        elif env.board[i] == -1:
            pygame.draw.circle(screen, O_COLOR, (x,y), 32, 4)

# ===================== MENU =====================
def menu():
    btn_hvh = Button(110, 190, 200, 45, "Humain vs Humain")
    btn_hva = Button(110, 250, 200, 45, "Humain vs Agent")
    btn_ava = Button(110, 310, 200, 45, "Agent vs Agent")
    btn_quit = Button(110, 370, 200, 45, "Quitter")

    while True:
        screen.blit(background, (0,0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        title = FONT_BIG.render("MORPION", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 110)))

        for btn in [btn_hvh, btn_hva, btn_ava, btn_quit]:
            btn.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_hvh.clicked(event): return 1
            if btn_hva.clicked(event): return 2
            if btn_ava.clicked(event): return 3
            if btn_quit.clicked(event):
                pygame.quit(); sys.exit()

# ===================== JEU =====================
def game_loop(mode):
    env = TicTacToeEnv()
    agent = QLearningAgent()
    env.reset()
    done = False
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if not done and event.type == pygame.MOUSEBUTTONDOWN:

                # Humain vs Humain → les deux joueurs cliquent
                if mode == 1:
                    x,y = event.pos
                    if (BOARD_LEFT <= x <= BOARD_LEFT + 3*CELL and
                        BOARD_TOP <= y <= BOARD_TOP + 3*CELL):
                        col = (x - BOARD_LEFT) // CELL
                        row = (y - BOARD_TOP) // CELL
                        action = row*3 + col
                        if action in env.legal_actions():
                            done = env.step(action)

                # Humain vs Agent → humain = joueur 1
                elif mode == 2 and env.current_player == 1:
                    x,y = event.pos
                    if (BOARD_LEFT <= x <= BOARD_LEFT + 3*CELL and
                        BOARD_TOP <= y <= BOARD_TOP + 3*CELL):
                        col = (x - BOARD_LEFT) // CELL
                        row = (y - BOARD_TOP) // CELL
                        action = row*3 + col
                        if action in env.legal_actions():
                            done = env.step(action)

        # Coups de l'agent
        if not done:
            if mode == 2 and env.current_player == -1:
                done = env.step(agent.act(env.legal_actions()))
            if mode == 3:
                done = env.step(agent.act(env.legal_actions()))

        draw_board(env)

        if done:
            msg = "Match nul"
            if env.winner == 1: msg = "X a gagné"
            if env.winner == -1: msg = "O a gagné"

            txt = FONT_BIG.render(msg, True, BLACK)
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, 430)))

            back = Button(110, 470, 200, 40, "Retour menu")
            back.draw()

            if pygame.mouse.get_pressed()[0] and back.rect.collidepoint(pygame.mouse.get_pos()):
                return

        pygame.display.flip()

# ===================== MAIN =====================
while True:
    mode = menu()
    game_loop(mode)