### File management ###
import json
import pygame
import random
import sys
import math

# Define file paths
filtered_word_bank_file = "filtered_and_modified_words_dictionary.json"
pangrams_file = "pangrams.json"

# Initialize objects to store the data
filtered_word_bank_data = {}
pangrams_data = {}

# Load data from JSON files
for name, file_path in [("filtered_word_bank", filtered_word_bank_file), ("pangrams", pangrams_file)]:
    try:
        with open(file_path, 'r') as json_file:
            if name == "filtered_word_bank":
                filtered_word_bank_data = json.load(json_file)
            elif name == "pangrams":
                pangrams_data = json.load(json_file)
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading '{file_path}': {str(e)}")

with open("google-10000-english-no-swears.txt", "r") as file:
    word_list = set(word.strip() for word in file.readlines())



### Game setup ###
# Pick a pangram and create the board with it
pangram = random.choice(pangrams_data)
print(pangram)
letter_list = list(set(pangram))

# Pick center letter
center_tile = random.choice(letter_list)
print(center_tile)
outside_tiles = [letter for letter in letter_list if letter != center_tile]

# Create possible solutions
filtered_words_with_valid_letters = []

for word in filtered_word_bank_data:
    # Check if all letters in the word are in the letter list
    if all(letter in letter_list for letter in word) and center_tile in word:
        filtered_words_with_valid_letters.append(word)

total_points = 0

# Add up points for each word from the dictionary
for word in filtered_words_with_valid_letters:
    # Check if the word exists in the dictionary and retrieve its point value
    if word in filtered_word_bank_data:
        word_points = filtered_word_bank_data[word]
        total_points += word_points
print(f"Total Points: {total_points}")

common_pangrams = []

common_points = 0
# Add up points for common words
for word in filtered_words_with_valid_letters:
# Check if the word exists in both dictionaries and retrieve its point value
    if word in filtered_word_bank_data:
        if word in word_list:
            word_points = filtered_word_bank_data[word]
            common_points += word_points
            if len(set(word)) == 7:
                common_pangrams.append(word)
print(len(common_pangrams))

print(f"Common Points: {common_points}")


### Interface and gameplay ###
# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 48
font = pygame.font.Font(None, FONT_SIZE)

# Define the radius and center coordinates for the circle
circle_radius = 150
center_x = 375
center_y = 450
angle_increment = 60

# Screen setup
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spelling Bee")

# Word management/tracking
current_word = ""
correct_words = []

# Position to display correct words
correct_words_x = 700
correct_words_y = 100
correct_words_spacing = 40

# Separate lists for each column of correct words
correct_words_column1 = []
correct_words_column2 = []
max_words_per_column = 20

# Create an empty input box
input_box = pygame.Rect(100, 100, 550, 75)
input_color = pygame.Color('lightskyblue1')
input_text = ""
input_active = True

# Score management
score = 0

# Game window
def draw_board():
    screen.fill(WHITE)

    # Draw circles
    pygame.draw.circle(screen, (222, 184, 135), (center_x, center_y), 75)  # Light Brown Circle

    # Display the center tile
    center_text = font.render(center_tile, True, BLACK)
    center_text_rect = center_text.get_rect(center=(center_x, center_y))
    screen.blit(center_text, center_text_rect)

    # Display letters in a circle around the center
    for i, letter in enumerate(outside_tiles):
        angle = math.radians(i * angle_increment)
        x = center_x + circle_radius * math.cos(angle)
        y = center_y + circle_radius * math.sin(angle)
        
        pygame.draw.circle(screen, (176, 226, 255), (int(x), int(y)), 75)  # Light Blue Circle
        text = font.render(letter, True, BLACK)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    # Draw the input box
    pygame.draw.rect(screen, input_color, input_box, 5)
    input_surface = font.render(input_text, True, BLACK)
    screen.blit(input_surface, (input_box.x + 10, input_box.y + 20))

    # Draw goal score
    goal_score_text = font.render(f"Goal score: {common_points}", True, BLACK)
    goal_score_rect = goal_score_text.get_rect(topleft=(1100, 20))
    screen.blit(goal_score_text, goal_score_rect)

    # Draw goal pangrams
    goal_pangram_text = font.render(f"Goal pangrams: {len(common_pangrams)}", True, BLACK)
    goal_pangram_rect = goal_score_text.get_rect(topleft=(10, 850))
    screen.blit(goal_pangram_text, goal_pangram_rect)

     # Display correct words in two columns
    for i, word in enumerate(correct_words):
        column = i // max_words_per_column  # Determine the column (0 or 1)
        x_position = correct_words_x + (column * correct_words_spacing * 6)
        y_position = correct_words_y + (i % max_words_per_column) * correct_words_spacing

        if len(set(word)) == 7:
            font_color = (176, 226, 255)  # Light Blue if all 7 unique letters
        elif word in word_list:
            font_color = BLACK
        else:
            font_color = (222, 184, 135)  # Brown if rare

        word_text = font.render(word, True, font_color)
        word_rect = word_text.get_rect(x=x_position, y=y_position)
        screen.blit(word_text, word_rect)


    # Display the score in the top left corner
    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(topleft=(20, 20))
    screen.blit(score_text, score_rect)
    
def main():
    global input_text
    global input_active
    global score
    global correct_words

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        # Process the word when the user presses Enter
                        if input_text in filtered_words_with_valid_letters and input_text not in correct_words:
                            correct_words.append(input_text)
                            correct_words.sort()
                            word_points = filtered_word_bank_data[input_text]
                            score += word_points
                        input_text = ""  # Clear the current word
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character when the user presses Backspace
                        input_text = input_text[:-1]
                    elif event.unicode.isalpha() and event.unicode in letter_list:
                        # Add valid characters to the current word
                        input_text += event.unicode

        draw_board()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()