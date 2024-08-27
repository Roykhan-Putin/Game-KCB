import pygame
import random
import sys
import math

# Inisialisasi pygame
pygame.init()

# Dimensi layar
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Typing Game")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 24)

# Waktu permainan
clock = pygame.time.Clock()

# Muat gambar pesawat
plane_image = pygame.image.load('data/plane/plane.png')
plane_width = plane_image.get_width()
plane_height = plane_image.get_height()

# Muat gambar background
background_image = pygame.image.load('data/background/background.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Posisi pesawat di tengah bawah layar
plane_x = SCREEN_WIDTH // 2 - plane_width // 2
plane_y = SCREEN_HEIGHT - plane_height

# Muat gambar pesawat alien (musuh)
alien_image = pygame.image.load('data/alien/alien.png')
alien_width = alien_image.get_width()
alien_height = alien_image.get_height()

moving_sprites = pygame.sprite.Group()

# Daftar soal yang dibuat secara custom
custom_problems = [
    ("2 + 3 * 5", "17"),
    ("15 / 3 + 2", "7"),
    ("(6 + 4) * 2", "20"),
    ("10 - 2 * 3", "4"),
    ("8 + 2 * (5 - 3)", "12"),
    ("25 / 5 + 9", "14"),
    ("50 - 6 * 8", "2"),
    ("(12 + 8) / 4", "5")
]

enemy_speed = 1
level = 1
enemies_destroyed = 0
enemies_to_next_level = 5

# Fungsi untuk memilih soal acak dari daftar
def get_custom_problem():
    return random.choice(custom_problems)

# Class Enemy (Pesawat Alien + Soal di bawahnya)
class Enemy:
    def __init__(self, question, answer, x, y, speed):
        self.question = question
        self.answer = str(answer)
        self.x = x
        self.y = y
        self.speed = speed
        self.calculate_direction()  # Menghitung arah gerakan ke pesawat

    # Menghitung vektor arah musuh menuju pesawat
    def calculate_direction(self):
        delta_x = plane_x + plane_width // 2 - self.x
        delta_y = plane_y + plane_height // 2 - self.y
        distance = math.sqrt(delta_x**2 + delta_y**2)
        self.dir_x = delta_x / distance
        self.dir_y = delta_y / distance

    def move(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

    def draw(self, screen):
        screen.blit(alien_image, (self.x, self.y))
        enemy_text = small_font.render(self.question, True, RED)
        screen.blit(enemy_text, (self.x, self.y + alien_height + 5))

def increase_level():
    global level, enemy_speed, enemies_to_next_level
    level += 1
    enemy_speed += 0.5
    enemies_to_next_level += 5

def draw_text(screen, text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def game_loop():
    global enemies_destroyed
    enemies = []
    score = 0
    input_text = ''
    game_over = False
    spawn_rate = 3000
    pygame.time.set_timer(pygame.USEREVENT, spawn_rate)

    while not game_over:
        screen.blit(background_image, (0, 0))  # Gambar background di setiap frame

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                question, answer = get_custom_problem()
                new_enemy = Enemy(question, answer, random.randint(50, SCREEN_WIDTH - 150), 0, enemy_speed)
                enemies.append(new_enemy)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for enemy in enemies:
                        if input_text == enemy.answer:
                            enemies.remove(enemy)
                            score += 1
                            enemies_destroyed += 1
                            if enemies_destroyed >= enemies_to_next_level:
                                increase_level()
                                enemies_destroyed = 0
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # Gerakkan dan gambar musuh
        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)
            if enemy.y >= plane_y:
                game_over = True

        screen.blit(plane_image, (plane_x, plane_y))

        draw_text(screen, f"Score: {score}", 10, 10, WHITE)
        draw_text(screen, input_text, 10, SCREEN_HEIGHT - 50, GREEN)

        pygame.display.flip()
        clock.tick(60)

        if game_over:
            draw_text(screen, "Game Over", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, RED)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

# Mulai permainan
game_loop()
