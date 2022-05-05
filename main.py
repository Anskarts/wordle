import pygame, random
from sys import exit
from wordlist import WORDS

pygame.init()
pygame.font.init()

attempt = ""
attempts = []
GAMEOVER = False

GRAY = (70, 70, 80)
GREEN = (6, 214, 160)
YELLOW = (255, 209, 102)

ANSWER = random.choice(WORDS).upper()

HEIGHT, WIDTH = 700, 600
SIZE = 72

FONT = pygame.font.Font("FreeSansBold.otf", SIZE)

pygame.display.set_caption("Wordle Game!")
pygame.display.set_icon(pygame.image.load("icon.png"))
window = pygame.display.set_mode((WIDTH, HEIGHT))

logo = pygame.image.load("logo.png")
logo_surface = logo.get_rect(center= (WIDTH//2, 16))

instructions = pygame.image.load("instructions.png")
instructions_surface = instructions.get_rect(center= (80, HEIGHT//2-10))

def determine_color(attempt, j):
	""" Determining the color of the square we're checking """
	letter = attempt[j]
	if letter == ANSWER[j]:
		return GREEN
	if letter in ANSWER:
		n_target = ANSWER.count(letter)
		n_correct = 0
		n_occurrence = 0
		for i in range(5):
			if attempt[i] == letter:
				if i <= j:
					n_occurrence += 1
				if letter == ANSWER[i]:
					n_correct += 1
		if n_target - n_correct - n_occurrence >= 0:
			return YELLOW
	return GRAY


def game_over():
	""" Shows the correct answer """
	if len(attempts) == 6 and attempts[-1] != ANSWER:
		GAMEOVER = True
		word = FONT.render(ANSWER, False, GRAY)
		surface = word.get_rect(center= (WIDTH//2, HEIGHT-100//2-10))
		window.blit(word, surface)


def draw_rect():
		""" Responsible for drawing the squares/text of the game """
		y = 100
		for i in range(6):
			x = 100
			for j in range(5):
				# Drawing the squares
				square = pygame.Rect(x, y, SIZE, SIZE)
				pygame.draw.rect(window, GRAY, square, width=2, border_radius=4)

				# Drawing the letters/words which have already been guessed
				if i < len(attempts):
					color = determine_color(attempts[i], j)
					pygame.draw.rect(window, color, square, border_radius=4)
					letter = FONT.render(attempts[i][j].upper(), False, "White")
					surface = letter.get_rect(center= (x+SIZE//2, y+SIZE//2))
					window.blit(letter, surface)

				# Drawing the user input
				if i == len(attempts) and j < len(attempt):
					letter = FONT.render(attempt[j].upper(), False, GRAY)
					surface = letter.get_rect(center= (x+SIZE//2, y+SIZE//2))
					window.blit(letter, surface)

				x += SIZE + 10

			y += SIZE + 10


def main():
	""" The main function containing the animation loop """
	global attempt, attempts, ANSWER, GAMEOVER
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.KEYDOWN:			
				if len(attempt) < 5 and not GAMEOVER:	# Getting the user's input
						attempt += event.unicode.upper()

				if event.key == pygame.K_RETURN:		# Handling the user's return press
					if len(attempt) == 5 and attempt.lower() in WORDS:
						attempts.append(attempt)
						GAMEOVER = True if attempt == ANSWER else False
						attempt = ""

				if event.key == pygame.K_BACKSPACE:		# Correcting the user's input
					if len(attempt) > 0:
						attempt = attempt[:-2]

				if event.key == pygame.K_SPACE:			# SPACEBAR to restart the game
					GAMEOVER = False
					ANSWER = random.choice(WORDS).upper()
					attempt = ""
					attempts = []

		window.fill("White")
		window.blit(logo, logo_surface)
		window.blit(instructions, instructions_surface)
		draw_rect()
		game_over()
		pygame.display.flip()

if __name__ == "__main__":
	main()
