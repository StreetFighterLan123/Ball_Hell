import pygame, time, os, sys, random, math

# The background is the same as the icon, looks cool, maybe change it later idk.
pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('hell.png')

pygame.display.set_caption("Ball Hell")
pygame.display.set_icon(pygame.image.load('hell.png'))
# For FPS

clock = pygame.time.Clock()


def get_high_score():
    # Default high score
    high_score = 0

    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        print("The high score is", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")

    return high_score


def save_high_score(new_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")


high_score = get_high_score()
high_score_font = pygame.font.Font('freesansbold.ttf', 24)

def high_score_show():
    global high_score
    global high_score_font
    high_score_text = high_score_font.render(f'High Score: {str(high_score)}', True, (255, 192, 203))
    screen.blit(high_score_text, (340, 100))

# I didn't make the function before because I didn't know the pygame BLEND function.
def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image


# Line for the end of the game.
def line(x):
    for x in range(0, x):
        print("                                ")

# Character
orig_Img = pygame.image.load('player.png')
orig_Img = colorize(orig_Img, (255, 192, 203))
playerImg = pygame.transform.scale(orig_Img, (30, 30))
playerX = 380
playerY = 530
playerX_vel = 0
playerY_vel = 0  # Keep the Y_vel just in case.


def player(x, y):
    screen.blit(playerImg, (x, y))


# Balls

ballImg = []
ballX = []
ballY = []
ballY_vel = []
num_of_balls = 10


def ball_thing():
    for i in range(num_of_balls):
        ballImg.append(pygame.image.load('ball.png'))
        ballX.append(random.randint(0, 775))
        ballY.append(20)
        ballY_vel.append(10)


ball_thing()


def ball(x, y, i):
    screen.blit(ballImg[i], (x, y))


# Collision Function


# Score Function
score = 0

font = pygame.font.Font('freesansbold.ttf', 32)


def score_disp():
    score_text = font.render(f'Score: {round(score)}', True, (255, 192, 203))
    screen.blit(score_text, (350, 50))


# Fix this later! Use the bad one I wrote before for now...or forever...
def is_collided_with(sprite_one, sprite_two):
    return sprite_one.rect.colliderect(sprite_two.rect)


# Music that I stole.
pygame.mixer.music.load("adventure.wav")
pygame.mixer.music.play(-1)

# Boop sound
boop_sound = pygame.mixer.Sound('boop.wav')

running = True

# Achievement Variables and Font
ten_once = True
ten_count = 0
ten_sound = True

thirty_once = True
thirty_count = 0
thirty_sound = True

fifty_once = True
fifty_count = 0
fifty_sound = True

hundred_once = True
hundred_count = 0
hundred_sound = True

# Keep the achieve font the same for everything! Because all the achievements are going to be the same size and place.
achieve_font = pygame.font.Font('freesansbold.ttf', 18)

x_vel_base = 25
while running:
    if round(score) > high_score:
        save_high_score(round(score))
    playerX_vel = 0
    playerY_vel = 0
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    # For the player movement that's going to happen later on.
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        playerX_vel = x_vel_base

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        playerX_vel = -x_vel_base

    playerX -= playerX_vel
    playerY -= playerY_vel

    for i in range(num_of_balls):
        ballY[i] += ballY_vel[i]
        ball(ballX[i], ballY[i], i)
        # if collision:
        #    running = False
        #    sys.exit()
        if ballY[i] > 660:
            ball_thing()
            ballY[i] = 10
            ballX[i] = random.randint(0, 775)
            ballY_vel[i] += 0.25
            score += 0.1
        if abs(ballX[i] - playerX) < 20 and abs(ballY[i] - playerY) < 70:
            running = False
            line(50)
            print(f'Your score was: {round(score)}')
            break
            sys.exit()
    if playerX < 0:
        playerX = 0
    if playerX > 738:
        playerX = 738

    # Check for achievements.
    if round(score) >= 10 and ten_once and ten_count < 100:
        achieve_text = achieve_font.render('Noob: Get 10 points', True, (127, 255, 212))
        screen.blit(achieve_text, (100, 10))
        ten_count += 1
        if ten_sound:
            pygame.mixer.Sound.play(boop_sound)
            ten_sound = False
    if round(score) >= 30 and thirty_once and thirty_count < 100:
        achieve_text = achieve_font.render('Decent: Nice, keep going!', True, (127, 255, 212))
        screen.blit(achieve_text, (100, 10))
        thirty_count += 1
        if thirty_sound:
            pygame.mixer.Sound.play(boop_sound)
            thirty_sound = False
    if round(score) >= 50 and fifty_once and fifty_count < 100:
        achieve_text = achieve_font.render("Pro: You're amazing.", True, (127, 255, 212))
        screen.blit(achieve_text, (100, 10))
        fifty_count += 1
        if fifty_sound:
            pygame.mixer.Sound.play(boop_sound)
            fifty_sound = False
    if round(score) >= 100 and hundred_once and hundred_count < 100:
        achieve_text = achieve_font.render("Hacker: You've somehow hacked the game!", True, (127, 255, 212))
        screen.blit(achieve_text, (100, 10))
        hundred_count += 1
        if hundred_sound:
            pygame.mixer.Sound.play(boop_sound)
            hundred_sound = False
    score_disp()
    high_score_show()
    player(playerX, playerY)
    clock.tick(30)
    # print(playerX) for development
    pygame.display.update()
