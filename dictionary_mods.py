import json

# Read the JSON file
with open('words_dictionary.json', 'r') as json_file:
    data = json.load(json_file)

# Read google file
file_path = "google-10000-english-no-swears.txt"

try:
    with open(file_path, 'r') as file:
        # Read the entire file content into a variable
        file_content = file.read()
except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Create a new dictionary to store the filtered and modified data
filtered_and_modified_data = {}

# Iterate through each word in the dictionary
for word in data.keys():
    # Calculate the length of the word
    word_length = len(word)

    # Check if the word is longer than 3 letters and does not contain 's'
    if word_length > 3 and 's' not in word:
        # Determine the new value based on word length
        if word_length == 4:
            filtered_and_modified_data[word] = 1
        else:
            filtered_and_modified_data[word] = word_length

print(f"Filtered and modified {len(data) - len(filtered_and_modified_data)} words.")

possible_pangrams = []

# Iterate through each word in filtered_and_modified_data
for word in filtered_and_modified_data.keys():
    word_length = len(word)

    # Check if the word is longer than 7 letters and exists in file_content
    if word_length > 7 and word in file_content:
        unique_letters = len(set(word))
        if unique_letters == 7:
            possible_pangrams.append(word)

with open('pangrams.json', 'w') as json_output_file:
    json.dump(possible_pangrams, json_output_file, indent=4)
