import pygame
import sys
import random

class Snake:
    def __init__(self, cell_size, color=(0, 255, 0), start_pos=(100, 100)):
        self.cell_size = cell_size
        self.color = color
        self.direction = (cell_size, 0)
        self.body = [start_pos, (start_pos[0] - cell_size, start_pos[1]), (start_pos[0] - 2*cell_size, start_pos[1])]

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
            pygame.draw.rect(screen, self.color, pygame.Rect(segment[0], segment[1], self.cell_size, self.cell_size))

    def check_portal_collision(self, portal):
        head = self.body[0]
        return head == portal.position

    def check_snake_collision(self, other_snake):
        head = self.body[0]
        return head in other_snake.body

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

    def display_score(self, screen, position='left', player_num=None):
        font = pygame.font.Font(None, 36)
        if player_num:
            text = font.render(f"J{player_num}: {self.score}", True, white)
        else:
            text = font.render(f"Score: {self.score}", True, white)

        if position == 'left':
            screen.blit(text, (10, 10))
        else:  # right
            text_rect = text.get_rect()
            screen.blit(text, (width - text_rect.width - 10, 10))

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

def choose_game_mode():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2

        screen.fill(black)
        font = pygame.font.Font(None, 36)
        text = font.render("Choisissez le mode de jeu:", True, white)
        screen.blit(text, (width//4, height//2 - 50))
        text = font.render("1 - Un joueur", True, white)
        screen.blit(text, (width//4, height//2))
        text = font.render("2 - Deux joueurs", True, white)
        screen.blit(text, (width//4, height//2 + 50))
        pygame.display.flip()

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

def game_over_screen(winner=None):
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
        if winner:
            draw_centered_text(screen, winner, font, white, -30)
            draw_centered_text(screen, "Appuyez sur R pour rejouer ou sur Q pour quitter.", font, white, 30)
        else:
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

game_mode = choose_game_mode()
difficulty, fps = choose_difficulty()

snake1 = Snake(cell_size, green, (100, 100))
food = Food(cell_size)
score1 = Score()
obstacles = []
power_ups = []
num_power_ups = 3

# Initialiser le deuxième serpent en mode 2 joueurs
if game_mode == 2:
    snake2 = Snake(cell_size, blue, (width - 100, height - 100))
    score2 = Score()
    snake1_alive = True
    snake2_alive = True
else:
    snake2 = None

for _ in range(num_power_ups):
    power_up = PowerUp(cell_size)
    power_ups.append(power_up)

if difficulty == "Moyen" or difficulty == "Difficile":
    num_obstacles = 10 if difficulty == "Moyen" else 20
    for _ in range(num_obstacles):
        obstacle = Obstacle(cell_size)
        obstacles.append(obstacle)

portal = Porte(cell_size, (width - cell_size, height // 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Contrôles Joueur 1 (flèches)
            if event.key == pygame.K_UP:
                snake1.change_direction((0, -cell_size))
            elif event.key == pygame.K_DOWN:
                snake1.change_direction((0, cell_size))
            elif event.key == pygame.K_LEFT:
                snake1.change_direction((-cell_size, 0))
            elif event.key == pygame.K_RIGHT:
                snake1.change_direction((cell_size, 0))

            # Contrôles Joueur 2 (ZQSD)
            if game_mode == 2:
                if event.key == pygame.K_z:
                    snake2.change_direction((0, -cell_size))
                elif event.key == pygame.K_s:
                    snake2.change_direction((0, cell_size))
                elif event.key == pygame.K_q:
                    snake2.change_direction((-cell_size, 0))
                elif event.key == pygame.K_d:
                    snake2.change_direction((cell_size, 0))

    # Déplacer les serpents
    if game_mode == 1:
        snake1.move()
    else:
        if snake1_alive:
            snake1.move()
        if snake2_alive:
            snake2.move()

    # Vérifier les collisions pour le mode 1 joueur
    if game_mode == 1:
        if snake1.check_collision(obstacles, width, height):
            score1.reset_score()
            if not game_over_screen():
                pygame.quit()
                sys.exit()
            else:
                snake1 = Snake(cell_size, green, (100, 100))
                food = Food(cell_size)
                obstacles = []
                if difficulty == "Moyen" or difficulty == "Difficile":
                    num_obstacles = 10 if difficulty == "Moyen" else 20
                    for _ in range(num_obstacles):
                        obstacle = Obstacle(cell_size)
                        obstacles.append(obstacle)

        if snake1.check_food_collision(food):
            snake1.grow()
            food.generate_position()
            score1.increase_score(10)

    # Vérifier les collisions pour le mode 2 joueurs
    else:
        # Vérifier collisions Joueur 1
        if snake1_alive:
            if snake1.check_collision(obstacles, width, height) or (snake2_alive and snake1.check_snake_collision(snake2)):
                snake1_alive = False

        # Vérifier collisions Joueur 2
        if snake2_alive:
            if snake2.check_collision(obstacles, width, height) or (snake1_alive and snake2.check_snake_collision(snake1)):
                snake2_alive = False

        # Fin de partie si au moins un serpent est mort
        if not snake1_alive or not snake2_alive:
            winner_message = ""
            if not snake1_alive and not snake2_alive:
                winner_message = "Match nul!"
            elif snake1_alive:
                winner_message = "Joueur 1 (Vert) gagne!"
            else:
                winner_message = "Joueur 2 (Bleu) gagne!"

            score1.reset_score()
            score2.reset_score()

            if not game_over_screen(winner_message):
                pygame.quit()
                sys.exit()
            else:
                # Réinitialiser le jeu
                game_mode = choose_game_mode()
                difficulty, fps = choose_difficulty()
                snake1 = Snake(cell_size, green, (100, 100))
                food = Food(cell_size)
                score1 = Score()
                obstacles = []

                if game_mode == 2:
                    snake2 = Snake(cell_size, blue, (width - 100, height - 100))
                    score2 = Score()
                    snake1_alive = True
                    snake2_alive = True
                else:
                    snake2 = None

                if difficulty == "Moyen" or difficulty == "Difficile":
                    num_obstacles = 10 if difficulty == "Moyen" else 20
                    for _ in range(num_obstacles):
                        obstacle = Obstacle(cell_size)
                        obstacles.append(obstacle)

        # Nourriture pour Joueur 1
        if snake1_alive and snake1.check_food_collision(food):
            snake1.grow()
            food.generate_position()
            score1.increase_score(10)

        # Nourriture pour Joueur 2
        if snake2_alive and snake2.check_food_collision(food):
            snake2.grow()
            food.generate_position()
            score2.increase_score(10)

    screen.fill(black)

    # Dessiner les éléments
    if game_mode == 1 or snake1_alive:
        snake1.draw(screen)
    if game_mode == 2 and snake2_alive:
        snake2.draw(screen)

    food.draw(screen)
    portal.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    # Afficher les scores
    if game_mode == 1:
        score1.display_score(screen)
    else:
        score1.display_score(screen, 'left', 1)
        score2.display_score(screen, 'right', 2)

    pygame.display.flip()
    pygame.time.Clock().tick(fps)
