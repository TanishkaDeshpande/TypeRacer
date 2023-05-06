import pygame
import random
import time

# initialize pygame
pygame.init()

# set up the window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Racers")

# set up the fonts
font = pygame.font.SysFont("comicsansms", 32)
font_small = pygame.font.SysFont("comicsansms", 16)

# set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set up the game clock
clock = pygame.time.Clock()

# load the words from the file
with open("words.txt", "r") as f:
    words = f.readlines()
    words = [word.strip() for word in words]

# set up the game
class Game:
    def __init__(self):
        self.word = random.choice(words)
        self.word_index = 0
        self.input_text = ""
        self.start_time = None
        self.elapsed_time = None
        self.is_running = False
        self.is_finished = False
    
    def start(self):
        self.is_running = True
        self.start_time = time.time()

    def stop(self):
        self.is_running = False
        self.elapsed_time = round(time.time() - self.start_time, 2)
        self.is_finished = True
    
    def get_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            if self.input_text == self.word:
                self.stop()
            else:
                self.input_text = ""
        elif event.unicode.isalpha():
            self.input_text += event.unicode
    
    def update(self):
        if self.is_running:
            if self.word_index == len(self.word):
                self.stop()
            elif self.input_text == self.word[:self.word_index+1]:
                self.word_index += 1
    
    def render(self):
        window.fill(WHITE)
        
        # display the word to type
        word_text = font.render(self.word, True, BLACK)
        window.blit(word_text, (50, 100))
        
        # display the user's input
        input_text = font.render(self.input_text, True, BLACK)
        window.blit(input_text, (50, 150))
        
        # display the time elapsed
        if self.is_running:
            elapsed_time = round(time.time() - self.start_time, 2)
        else:
            elapsed_time = self.elapsed_time
        time_text = font_small.render("Time: " + str(elapsed_time), True, BLACK)
        window.blit(time_text, (WIDTH - 100, 50))
        
        # display the game over message
        if self.is_finished:
            if self.input_text == self.word:
                game_over_text = font.render("You win!", True, BLACK)
            else:
                game_over_text = font.render("You lose!", True, BLACK)
            window.blit(game_over_text, (50, 250))
        
        pygame.display.update()

game = Game()

# run the game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            game.get_input(event)
