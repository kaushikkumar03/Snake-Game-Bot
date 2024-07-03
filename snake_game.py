import random

import pygame

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 17) * SIZE
        self.y = random.randint(1, 11) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    # Arrays make it easier for PyTorch to train the bot
    def get_direction_vector(self):
        direction_vector = [0, 0, 0, 0]
        if self.direction == 'up':
            direction_vector[0] = 1
        elif self.direction == 'down':
            direction_vector[1] = 1
        elif self.direction == 'left':
            direction_vector[2] = 1
        elif self.direction == 'right':
            direction_vector[3] = 1
        return direction_vector

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


def play_sound(sound):
    sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
    pygame.mixer.Sound.play(sound)


def play_bgm():
    pygame.mixer.music.load("resources/bg_music_1.mp3")
    pygame.mixer.music.play(-1, 0)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.surface = pygame.display.set_mode((720, 480))

        pygame.mixer.init()
        play_bgm()

        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (100, 200))
        line2 = font.render("To play again press Enter. To exit, press Escape.", True, (255, 255, 255))
        self.surface.blit(line2, (100, 250))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (600, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True

        return False

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        pause = False

        #Collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        #Collision with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                play_sound("crash")
                pause = True

        #Collision with game window
        if not (0 <= self.snake.x[0] <= 720 and 0 <= self.snake.y[0] <= 480):
            play_sound('crash')
            pause = True

        return pause

    # The following code block implements the game in the vanilla version;
    # In the Snake BOT project, the game is run using RL_Environment (RL_Environment.py is the equivalent of main.py).
    """
    import time
    
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.2)"""
