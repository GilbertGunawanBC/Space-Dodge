import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("Assets/bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_IMG = pygame.image.load("Assets/spaceship.png")
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_VEL = 5


ASTEROID_IMG = pygame.image.load("Assets/Asteroid.png")
STAR_WIDTH, STAR_HEIGHT = 20, 45
ASTEROID_IMG = pygame.transform.scale(ASTEROID_IMG, (STAR_WIDTH, STAR_HEIGHT))
STAR_VEL = 1

BULLET_IMG = pygame.image.load("Assets/bullet.png")
BULLET_WIDTH, BULLET_HEIGHT = 10, 20
BULLET_IMG = pygame.transform.scale(BULLET_IMG, (BULLET_WIDTH, BULLET_HEIGHT))
BULLET_VEL = 7
bullets = []

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw player
    WIN.blit(PLAYER_IMG, (player.x, player.y))

    # Draw stars
    for star in stars:
        WIN.blit(ASTEROID_IMG, (star.x, star.y))

    for bullet in bullets:
        WIN.blit(BULLET_IMG, (bullet.x, bullet.y))

    pygame.display.update()

def shoot(player):
    bullet = pygame.Rect(player.x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player.y, BULLET_WIDTH, BULLET_HEIGHT)
    bullets.append(bullet)

def main():
    pygame.mixer.music.load("Assets/n-Dimensions.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)

    hit_sound = pygame.mixer.Sound("Assets/Explosion2.wav")
    hit_sound.set_volume(1.0)

    explode_sound = pygame.mixer.Sound("Assets/Explosion18.wav")
    explode_sound.set_volume(1.0)

    shoot_sound = pygame.mixer.Sound("Assets/Laser_Shoot16.wav")
    shoot_sound.set_volume(1.0)

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 5000
    star_count = 0

    stars = []
    hit = False

    global STAR_VEL

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            star_add = random.randint(3, 10)
            for i in range(star_add):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, - STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append({"rect": star, "hits": 0})

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(player)
                    shoot_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        elif keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL
        elif keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL

        for bullet in bullets[:]:
            bullet.y -= BULLET_VEL
            if bullet.y + bullet.height < 0:
                bullets.remove(bullet)

        for bullet in bullets[:]:
            for star in stars[:]:
                if bullet.colliderect(star["rect"]):
                    star["hits"] += 1
                    hit_sound.play()
                    bullets.remove(bullet)
                    if star["hits"] >= 5:
                        explode_sound.play()
                        stars.remove(star)
                    break

        for star in stars[:]:
            star["rect"].y += STAR_VEL
            if star["rect"].y > HEIGHT:
                stars.remove(star)
                STAR_VEL += 0.03
                star_add_increment -= 20 
                if star_add_increment < 500:
                    star_add_increment = 500
            elif star["rect"].y + star["rect"].height >= player.y and star["rect"].colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("YOU LOST", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        draw(player, elapsed_time, [star["rect"] for star in stars])

    pygame.quit()

if __name__ == "__main__":
    main()