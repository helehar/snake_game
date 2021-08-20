import pygame
import random
import math
import time
import sqlite3

STATE_MENU = "menu"
STATE_INGAME = "ingame"
STATE_GAMEOVER = "gameover"
STATE_EXIT = "exit"


class Apple:
    def __init__(self, screen):
        self.appleImg = pygame.image.load('resources/apple.png')
        self.screen = screen

        # start position
        self.apple_x = 499
        self.apple_y = 100

    def move(self):
        self.apple_x = random.randint(0, 768)
        self.apple_y = random.randint(0, 568)

    def draw(self):
        self.screen.blit(self.appleImg, (self.apple_x, self.apple_y))
        pygame.display.flip()


class Snake:
    def __init__(self, screen, length):
        self.screen = screen
        self.length = length
        self.snakeImg = pygame.image.load('resources/snake.png')
        self.direction = 'down'

        # start position
        self.snake_x = [12] * length
        self.snake_y = [12] * length

        # snake crash
        self.game_over = False

    def self_collide(self, x, y):
        for i in range(self.length - 1, 0, -1):
            if self.snake_x[i] == x and self.snake_y[i] == y:
                return True
        return False

    def increase_length(self):
        self.length += 1
        self.snake_x.append(-1)
        self.snake_y.append(-1)

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def reached_wall(self):
        if self.snake_x[0] <= 0:
            self.snake_x[0] = 768
            self.direction = 'left'

        elif self.snake_x[0] >= 768:
            self.snake_x[0] = 0
            self.direction = 'right'


        elif self.snake_y[0] <= 0:
            self.snake_y[0] = 568
            self.direction = 'up'


        elif self.snake_y[0] >= 568:
            self.snake_y[0] = 0
            self.direction = 'down'

    def walk(self):
        self.reached_wall()
        for i in range(self.length - 1, 0, -1):
            self.snake_x[i] = self.snake_x[i - 1]
            self.snake_y[i] = self.snake_y[i - 1]

        if self.direction == 'left':
            self.snake_x[0] -= 32

        if self.direction == 'right':
            self.snake_x[0] += 32

        if self.direction == 'up':
            self.snake_y[0] -= 32

        if self.direction == 'down':
            self.snake_y[0] += 32

        if self.self_collide(self.snake_x[0], self.snake_y[0]):
            self.game_over = True

        if self.game_over == False:
            self.draw()

    def draw(self):
        # RGB - red, green, blue
        self.screen.fill((150, 150, 150))

        for i in range(self.length):
            self.screen.blit(self.snakeImg, (self.snake_x[i], self.snake_y[i]))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

        # Title and Icon
        pygame.display.set_caption("Snake Game")
        self.icon = pygame.image.load('resources/logo.png')
        pygame.display.set_icon(self.icon)

        # Snake
        self.snake = Snake(self.screen, 1)

        # Apple
        self.apple = Apple(self.screen)

        # Score
        self.score_value = 0
        self.font = pygame.font.Font('C:\Windows\Fonts\Calibri.ttf', 32)
        self.textX = 10
        self.textY = 10

        self.first_round = True

        # Game over text
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)

        # score board
        self.score_list = []

        # new game
        self.new_game = True

        # states
        self.state = STATE_INGAME

        self.name = ""

        self.capslock = False

        self.database = " "

    def text_render(self, word, x, y):
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = self.font.render(str(word), True, (0, 0, 0))
        return self.screen.blit(text, (x, y))

    def show_score(self):
        score = self.font.render("Score: " + str(self.score_value), True, (0, 0, 0))
        self.screen.blit(score, (self.textX, self.textY))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER: " + str(self.score_value), True, (54, 107, 20))
        self.screen.blit(over_text, (150, 250))

    def play_again_text(self):
        self.screen.fill((150, 150, 150))
        y_line = 90
        score_board = self.font.render("SCORE BOARD: ", True, (54, 107, 20))
        self.screen.blit(score_board, (150, 80))

        counter = 0
        for score in self.score_list:
            counter += 1
            score_board = self.font.render(str(counter) + ": " + str(score), True, (0, 0, 0))
            y_line += 32
            self.screen.blit(score_board, (150, y_line))

        pygame.draw.line(self.screen, (0, 0, 0), [0, 455], [800, 455], width=1)
        play_again_text = self.font.render("Play again? press enter", True, (54, 107, 20))
        quit_game_text = self.font.render("Exit game? press esc", True, (54, 107, 20))
        self.screen.blit(play_again_text, (150, 470))
        self.screen.blit(quit_game_text, (150, 510))

    def is_collision(self, apple_x, apple_y, snake_x, snake_y):
        distance = math.sqrt((math.pow(apple_x - snake_x, 2)) + (
            math.pow(apple_y - snake_y, 2)))

        if distance < 27:
            return True
        else:
            return False

    def gameover_process_input(self):
        for event in pygame.event.get():
            Letters = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d,
                       pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h,
                       pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
                       pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p,
                       pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
                       pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
                       pygame.K_y, pygame.K_z, pygame.K_1, pygame.K_2,
                       pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                       pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]

            if event.type == pygame.QUIT:
                self.state = STATE_EXIT
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                if event.key == pygame.K_SPACE:
                    self.name += ' '
                if event.key == pygame.K_RETURN:
                    self.state = STATE_MENU
                    self.first_round = True
                    return
                if event.key == pygame.K_CAPSLOCK:
                    if self.capslock:
                        self.capslock = False
                    else:
                        self.capslock = True

                if event.key in Letters and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.name += str(chr(event.key)).upper()

                elif event.key in Letters:
                    if self.capslock:
                        self.name += str(chr(event.key)).upper()
                    else:
                        self.name += str(chr(event.key))

    def gameover_draw(self):
        self.screen.fill((150, 150, 150))
        self.game_over_text()
        self.text_render("Please enter your name: ", 200, 300)

        self.text_render(self.name, 200, 400)
        pygame.display.flip()

    def ingame_process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = STATE_EXIT
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    self.snake.move_left()

                if event.key == pygame.K_RIGHT:
                    self.snake.move_right()

                if event.key == pygame.K_UP:
                    self.snake.move_up()

                if event.key == pygame.K_DOWN:
                    self.snake.move_down()

    def ingame_update(self):
        if self.snake.game_over:
            self.state = STATE_GAMEOVER
            self.first_round = True
            return
        self.snake.walk()

        if self.is_collision(self.apple.apple_x, self.apple.apple_y, self.snake.snake_x[0], self.snake.snake_y[0]):
            self.snake.increase_length()
            self.apple.move()
            self.score_value += 1

    def ingame_draw(self):
        self.apple.draw()
        self.show_score()
        pygame.display.flip()
        time.sleep(0.1)

    def menu_process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = STATE_EXIT
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = STATE_INGAME
                    self.first_round = True
                    self.name = ""
                    self.snake.game_over = False
                    return

                if event.key == pygame.K_ESCAPE:
                    self.state = STATE_EXIT
                    return

    def menu_update(self):
        self.score_list.clear()

        conn = sqlite3.connect('scoreboard.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS score(
                                participant text,
                                scorevalue int
                                )""")
        conn.commit()

        c.execute("INSERT INTO score VALUES(:participant, :scorevalue)",
                  {'participant': self.name, 'scorevalue': self.score_value})
        conn.commit()

        c.execute("""SELECT * FROM score ORDER BY scorevalue DESC LIMIT 10""")

        teller = 30
        for score in c.fetchall():
            teller -= len(score[0])

            score_board_value = score[0] + "-" * teller + str(score[1])
            self.score_list.append(score_board_value)
            teller = 30

        # koden skal egentlig ikke trenge å komme hit, men for sikkerhets skyld
        if len(self.score_list) > 10:
            self.score_list.pop(0)

    def menu_draw(self):
        self.play_again_text()
        pygame.display.flip()

    def run(self):
        running = True

        while running:
            if self.state == STATE_MENU:
                if self.first_round:
                    self.menu_update()
                    self.first_round = False
                self.menu_process_input()
                self.menu_draw()

            if self.state == STATE_INGAME:
                if self.first_round:
                    self.snake.length = 1
                    self.score_value = 0

                    self.snake.draw()
                    self.apple.draw()

                    self.first_round = False
                self.ingame_process_input()
                self.ingame_update()
                self.ingame_draw()

            if self.state == STATE_GAMEOVER:
                self.gameover_process_input()
                self.gameover_draw()

            if self.state == STATE_EXIT:
                running = False


if __name__ == "__main__":
    game = Game()
    game.run()
