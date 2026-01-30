import pygame
import sys
import random
import os

class Snake:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.direction = (cell_size, 0)
        self.body = [(100, 100), (90, 100), (80, 100)]

    def move(self):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def change_direction(self, new_direction):
        if (
            (new_direction == (0, -self.cell_size) and self.direction != (0, self.cell_size)) or
            (new_direction == (0, self.cell_size) and self.direction != (0, -self.cell_size)) or
            (new_direction == (-self.cell_size, 0) and self.direction != (self.cell_size, 0)) or
            (new_direction == (self.cell_size, 0) and self.direction != (-self.cell_size, 0))
        ):
            self.direction = new_direction

    def check_collision(self, obstacles, width, height):
        head = self.body[0]
        if (
            head[0] < 0
            or head[0] >= width
            or head[1] < 0
            or head[1] >= height
            or head in self.body[1:]
        ):
            return True

        for obstacle in obstacles:
            if head == obstacle.position:
                return True
        return False

    def check_food_collision(self, food):
        return self.body[0] == food.position

    def grow(self):
        self.body.append((0, 0))

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, green, pygame.Rect(segment[0], segment[1], self.cell_size, self.cell_size))

    def check_portal_collision(self, portal):
        head = self.body[0]
        return head == portal.position

class Food:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.position = (0, 0)
        self.generate_position()

    def generate_position(self):
        self.position = (random.randrange(0, width, self.cell_size), random.randrange(0, height, self.cell_size))

    def draw(self, screen):
        pygame.draw.rect(screen, red, pygame.Rect(self.position[0], self.position[1], self.cell_size, self.cell_size))

class Obstacle:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.position = (0, 0)
        self.generate_position()

    def generate_position(self):
        self.position = (random.randrange(0, width, self.cell_size), random.randrange(0, height, self.cell_size))

    def draw(self, screen):
        pygame.draw.rect(screen, gray, pygame.Rect(self.position[0], self.position[1], self.cell_size, self.cell_size))

class Score:
    def __init__(self):
        self.score = 0

    def increase_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def display_score(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, white)
        screen.blit(text, (10, 10))

class PowerUp:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.position = (0, 0)
        self.active = False
        self.duration = 0
        self.generate_position()

    def generate_position(self):
        self.position = (random.randrange(0, width, self.cell_size), random.randrange(0, height, self.cell_size))

    def activate(self, duration):
        self.active = True
        self.duration = duration

    def deactivate(self):
        self.active = False
        self.duration = 0

    def update(self):
        if self.active:
            self.duration -= 1
            if self.duration <= 0:
                self.deactivate()

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, green, pygame.Rect(self.position[0], self.position[1], self.cell_size, self.cell_size))

class Porte:
    def __init__(self, cell_size, position):
        self.cell_size = cell_size
        self.position = position

    def draw(self, screen):
        pygame.draw.rect(screen, blue, pygame.Rect(self.position[0], self.position[1], self.cell_size, self.cell_size))

def choose_difficulty():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    return "Facile", fps_facile
                elif event.key == pygame.K_F2:
                    return "Moyen", fps_moyen
                elif event.key == pygame.K_F3:
                    return "Difficile", fps_difficile

        screen.fill(black)
        font = pygame.font.Font(None, 36)
        text = font.render("Choisissez le niveau de difficulté:", True, white)
        screen.blit(text, (width//4, height//2 - 50))
        text = font.render("F1 - Facile", True, white)
        screen.blit(text, (width//4, height//2))
        text = font.render("F2 - Moyen", True, white)
        screen.blit(text, (width//4, height//2 + 50))
        text = font.render("F3 - Difficile", True, white)
        screen.blit(text, (width//4, height//2 + 100))
        pygame.display.flip()

def draw_centered_text(screen, text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2 + y_offset)
    screen.blit(text_surface, text_rect)

def game_over_screen(final_score):
    save_high_score(final_score)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_m:
                    return "menu"

        screen.fill(black)
        font = pygame.font.Font(None, 36)
        draw_centered_text(screen, "Game Over!", font, white, -50)
        draw_centered_text(screen, f"Score: {final_score}", font, yellow, 0)
        draw_centered_text(screen, "R - Rejouer | M - Menu | Q - Quitter", font, white, 50)
        pygame.display.flip()

def load_high_scores():
    scores_file = os.path.join(os.path.dirname(__file__), "high_scores.txt")
    scores = []
    if os.path.exists(scores_file):
        with open(scores_file, "r") as f:
            for line in f:
                try:
                    scores.append(int(line.strip()))
                except ValueError:
                    pass
    return sorted(scores, reverse=True)[:10]

def save_high_score(score):
    scores_file = os.path.join(os.path.dirname(__file__), "high_scores.txt")
    scores = load_high_scores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:10]
    with open(scores_file, "w") as f:
        for s in scores:
            f.write(f"{s}\n")

def show_high_scores():
    scores = load_high_scores()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return

        screen.fill(black)
        title_font = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)

        draw_centered_text(screen, "HIGH SCORES", title_font, yellow, -250)

        if not scores:
            draw_centered_text(screen, "Aucun score enregistré", font, white, 0)
        else:
            for i, s in enumerate(scores):
                y_offset = -150 + i * 40
                rank_text = f"{i + 1}. {s} points"
                color = yellow if i == 0 else white
                draw_centered_text(screen, rank_text, font, color, y_offset)

        draw_centered_text(screen, "Appuyez sur Entrée ou Échap pour revenir", font, gray, 300)
        pygame.display.flip()

def show_menu():
    menu_options = ["Jouer", "High Scores", "Quitter"]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return "play"
                    elif selected == 1:
                        return "highscores"
                    elif selected == 2:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "highscores"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

        screen.fill(black)

        title_font = pygame.font.Font(None, 100)
        draw_centered_text(screen, "SNAKE GAME", title_font, green, -200)

        menu_font = pygame.font.Font(None, 48)
        for i, option in enumerate(menu_options):
            y_offset = -20 + i * 60
            if i == selected:
                color = yellow
                prefix = "> "
                suffix = " <"
            else:
                color = white
                prefix = "  "
                suffix = "  "
            draw_centered_text(screen, f"{prefix}{i + 1}. {option}{suffix}", menu_font, color, y_offset)

        hint_font = pygame.font.Font(None, 28)
        draw_centered_text(screen, "Utilisez les flèches + Entrée ou les touches 1-3", hint_font, gray, 200)

        pygame.display.flip()

pygame.init()

width, height = 1080, 900
cell_size = 20
fps_facile = 5
fps_moyen = 10
fps_difficile = 20

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
purple = (128, 0, 128)
cyan = (0, 255, 255)
pink = (255, 192, 203)
brown = (165, 42, 42)
magenta = (255, 0, 255)
lime = (0, 255, 0)
teal = (0, 128, 128)
navy = (0, 0, 128)
olive = (128, 128, 0)
maroon = (128, 0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

def init_game(difficulty):
    snake = Snake(cell_size)
    food = Food(cell_size)
    score = Score()
    obstacles = []
    power_ups = []
    num_power_ups = 3

    for _ in range(num_power_ups):
        power_up = PowerUp(cell_size)
        power_ups.append(power_up)

    if difficulty == "Moyen" or difficulty == "Difficile":
        num_obstacles = 10 if difficulty == "Moyen" else 20
        for _ in range(num_obstacles):
            obstacle = Obstacle(cell_size)
            obstacles.append(obstacle)

    portal = Porte(cell_size, (width - cell_size, height // 2))
    return snake, food, score, obstacles, power_ups, portal

def game_loop(snake, food, score, obstacles, portal, fps, difficulty):
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -cell_size))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, cell_size))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-cell_size, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((cell_size, 0))

        snake.move()

        if snake.check_collision(obstacles, width, height):
            final_score = score.score
            result = game_over_screen(final_score)
            if result == "menu":
                return "menu"
            elif result:
                snake, food, score, obstacles, _, portal = init_game(difficulty)
            else:
                pygame.quit()
                sys.exit()

        if snake.check_food_collision(food):
            snake.grow()
            food.generate_position()
            score.increase_score(10)

        screen.fill(black)

        snake.draw(screen)
        food.draw(screen)
        portal.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        score.display_score(screen)

        pygame.display.flip()
        clock.tick(fps)

def main():
    while True:
        menu_choice = show_menu()

        if menu_choice == "highscores":
            show_high_scores()
        elif menu_choice == "play":
            difficulty, fps = choose_difficulty()
            snake, food, score, obstacles, power_ups, portal = init_game(difficulty)
            result = game_loop(snake, food, score, obstacles, portal, fps, difficulty)
            if result != "menu":
                break

if __name__ == "__main__":
    main()
