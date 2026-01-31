import pygame
import sys
import random

class Snake:
    def __init__(self, cell_size, start_pos=(100, 100), color=(0, 255, 0)):
        self.cell_size = cell_size
        self.direction = (cell_size, 0)
        self.body = [start_pos, (start_pos[0] - cell_size, start_pos[1]), (start_pos[0] - 2*cell_size, start_pos[1])]
        self.color = color
        self.alive = True

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
        if self.alive:
            for segment in self.body:
                pygame.draw.rect(screen, self.color, pygame.Rect(segment[0], segment[1], self.cell_size, self.cell_size))

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
    def __init__(self, player_number=1):
        self.score = 0
        self.player_number = player_number

    def increase_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def display_score(self, screen, position=None):
        font = pygame.font.Font(None, 36)
        text = font.render(f"P{self.player_number}: {self.score}", True, white)
        if position:
            screen.blit(text, position)
        else:
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
                    return "Facile", fps_facile, 1
                elif event.key == pygame.K_F2:
                    return "Moyen", fps_moyen, 1
                elif event.key == pygame.K_F3:
                    return "Difficile", fps_difficile, 1
                elif event.key == pygame.K_F4:
                    return "Facile", fps_facile, 2
                elif event.key == pygame.K_F5:
                    return "Facile", fps_facile, 4

        screen.fill(black)
        font = pygame.font.Font(None, 36)
        text = font.render("Choisissez le niveau de difficulté:", True, white)
        screen.blit(text, (width//4, height//2 - 100))
        text = font.render("F1 - Facile (1 joueur)", True, white)
        screen.blit(text, (width//4, height//2 - 50))
        text = font.render("F2 - Moyen (1 joueur)", True, white)
        screen.blit(text, (width//4, height//2))
        text = font.render("F3 - Difficile (1 joueur)", True, white)
        screen.blit(text, (width//4, height//2 + 50))
        text = font.render("F4 - Mode 2 joueurs", True, white)
        screen.blit(text, (width//4, height//2 + 100))
        text = font.render("F5 - Mode 4 joueurs", True, white)
        screen.blit(text, (width//4, height//2 + 150))
        pygame.display.flip()

def draw_centered_text(screen, text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2 + y_offset)
    screen.blit(text_surface, text_rect)

def check_snake_collision(snake, other_snakes):
    head = snake.body[0]
    for other_snake in other_snakes:
        if other_snake != snake and other_snake.alive:
            if head in other_snake.body:
                return True
    return False

def generate_food_position_avoiding_snakes(food, snakes):
    while True:
        food.generate_position()
        position_valid = True
        for snake in snakes:
            if snake.alive and food.position in snake.body:
                position_valid = False
                break
        if position_valid:
            break

def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(black)
        font = pygame.font.Font(None, 36)
        draw_centered_text(screen, "Game Over! Appuyez sur R pour rejouer ou sur Q pour quitter.", font, white)
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

difficulty, fps, num_players = choose_difficulty()

# Configuration des positions et couleurs pour chaque joueur
player_configs = [
    {"pos": (100, 100), "color": pink},
    {"pos": (width - 100, 100), "color": cyan},
    {"pos": (100, height - 100), "color": orange},
    {"pos": (width - 100, height - 100), "color": purple}
]

# Score positions (coins de l'écran)
score_positions = [
    (10, 10),  # Haut gauche
    (width - 120, 10),  # Haut droit
    (10, height - 50),  # Bas gauche
    (width - 120, height - 50)  # Bas droit
]

# Initialisation des serpents et scores
snakes = []
scores = []
for i in range(num_players):
    snake = Snake(cell_size, player_configs[i]["pos"], player_configs[i]["color"])
    snakes.append(snake)
    score = Score(i + 1)
    scores.append(score)

food = Food(cell_size)
generate_food_position_avoiding_snakes(food, snakes)

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

# Boucle de jeu principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Contrôles Joueur 1 - Flèches directionnelles
            if event.key == pygame.K_UP and snakes[0].alive:
                snakes[0].change_direction((0, -cell_size))
            elif event.key == pygame.K_DOWN and snakes[0].alive:
                snakes[0].change_direction((0, cell_size))
            elif event.key == pygame.K_LEFT and snakes[0].alive:
                snakes[0].change_direction((-cell_size, 0))
            elif event.key == pygame.K_RIGHT and snakes[0].alive:
                snakes[0].change_direction((cell_size, 0))

            # Contrôles Joueur 2 - ZQSD
            if num_players >= 2:
                if event.key == pygame.K_z and snakes[1].alive:
                    snakes[1].change_direction((0, -cell_size))
                elif event.key == pygame.K_s and snakes[1].alive:
                    snakes[1].change_direction((0, cell_size))
                elif event.key == pygame.K_q and snakes[1].alive:
                    snakes[1].change_direction((-cell_size, 0))
                elif event.key == pygame.K_d and snakes[1].alive:
                    snakes[1].change_direction((cell_size, 0))

            # Contrôles Joueur 3 - IJKL
            if num_players >= 3:
                if event.key == pygame.K_i and snakes[2].alive:
                    snakes[2].change_direction((0, -cell_size))
                elif event.key == pygame.K_k and snakes[2].alive:
                    snakes[2].change_direction((0, cell_size))
                elif event.key == pygame.K_j and snakes[2].alive:
                    snakes[2].change_direction((-cell_size, 0))
                elif event.key == pygame.K_l and snakes[2].alive:
                    snakes[2].change_direction((cell_size, 0))

            # Contrôles Joueur 4 - Pavé numérique 8456
            if num_players >= 4:
                if event.key == pygame.K_KP8 and snakes[3].alive:
                    snakes[3].change_direction((0, -cell_size))
                elif event.key == pygame.K_KP5 and snakes[3].alive:
                    snakes[3].change_direction((0, cell_size))
                elif event.key == pygame.K_KP4 and snakes[3].alive:
                    snakes[3].change_direction((-cell_size, 0))
                elif event.key == pygame.K_KP6 and snakes[3].alive:
                    snakes[3].change_direction((cell_size, 0))

    # Déplacer tous les serpents vivants
    for snake in snakes:
        if snake.alive:
            snake.move()

    # Vérifier les collisions pour chaque serpent
    for i, snake in enumerate(snakes):
        if not snake.alive:
            continue

        # Collision avec les murs ou son propre corps
        if snake.check_collision(obstacles, width, height):
            snake.alive = False
            continue

        # Collision avec les autres serpents (mode multijoueur)
        if num_players > 1 and check_snake_collision(snake, snakes):
            snake.alive = False
            continue

        # Collision avec la nourriture
        if snake.check_food_collision(food):
            snake.grow()
            generate_food_position_avoiding_snakes(food, snakes)
            scores[i].increase_score(10)

    # Vérifier s'il reste des serpents vivants
    alive_snakes = [s for s in snakes if s.alive]

    # En mode multijoueur, vérifier s'il y a un gagnant
    if num_players > 1:
        if len(alive_snakes) == 0:
            # Tous les serpents sont morts
            if not game_over_screen():
                pygame.quit()
                sys.exit()
            else:
                # Réinitialiser le jeu
                snakes = []
                scores = []
                for i in range(num_players):
                    snake = Snake(cell_size, player_configs[i]["pos"], player_configs[i]["color"])
                    snakes.append(snake)
                    score = Score(i + 1)
                    scores.append(score)
                food = Food(cell_size)
                generate_food_position_avoiding_snakes(food, snakes)
                obstacles = []
                if difficulty == "Moyen" or difficulty == "Difficile":
                    num_obstacles = 10 if difficulty == "Moyen" else 20
                    for _ in range(num_obstacles):
                        obstacle = Obstacle(cell_size)
                        obstacles.append(obstacle)
        elif len(alive_snakes) == 1:
            # Un seul serpent survivant - afficher le gagnant
            winner_index = snakes.index(alive_snakes[0])
            screen.fill(black)
            font = pygame.font.Font(None, 72)
            draw_centered_text(screen, f"Joueur {winner_index + 1} gagne!", font, alive_snakes[0].color)
            pygame.display.flip()
            pygame.time.wait(3000)

            if not game_over_screen():
                pygame.quit()
                sys.exit()
            else:
                # Réinitialiser le jeu
                snakes = []
                scores = []
                for i in range(num_players):
                    snake = Snake(cell_size, player_configs[i]["pos"], player_configs[i]["color"])
                    snakes.append(snake)
                    score = Score(i + 1)
                    scores.append(score)
                food = Food(cell_size)
                generate_food_position_avoiding_snakes(food, snakes)
                obstacles = []
                if difficulty == "Moyen" or difficulty == "Difficile":
                    num_obstacles = 10 if difficulty == "Moyen" else 20
                    for _ in range(num_obstacles):
                        obstacle = Obstacle(cell_size)
                        obstacles.append(obstacle)
    else:
        # Mode solo
        if len(alive_snakes) == 0:
            scores[0].reset_score()
            if not game_over_screen():
                pygame.quit()
                sys.exit()
            else:
                snakes = [Snake(cell_size, player_configs[0]["pos"], player_configs[0]["color"])]
                food = Food(cell_size)
                generate_food_position_avoiding_snakes(food, snakes)
                obstacles = []
                if difficulty == "Moyen" or difficulty == "Difficile":
                    num_obstacles = 10 if difficulty == "Moyen" else 20
                    for _ in range(num_obstacles):
                        obstacle = Obstacle(cell_size)
                        obstacles.append(obstacle)

    # Affichage
    screen.fill(black)

    # Dessiner tous les serpents
    for snake in snakes:
        snake.draw(screen)

    food.draw(screen)
    portal.draw(screen)

    for obstacle in obstacles:
        obstacle.draw(screen)

    # Afficher les scores
    for i, score in enumerate(scores):
        score.display_score(screen, score_positions[i])

    pygame.display.flip()
    pygame.time.Clock().tick(fps)
