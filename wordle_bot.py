from itertools import product

# Gets all allowed words
valid_words_file = "valid_wordle_words.txt"

# Open the file in read mode
with open(valid_words_file, 'r') as file:
    # Read lines from the file and create a list of words
    all_current_words = [line.strip() for line in file]

# Function to generate all combinations of Black, Yellow, and Green letters
def generate_combinations():
    # Define the set of letters to use
    letters = "YGB"

    # Generate all combinations of a 5-letter string using the specified letters
    combinations = [''.join(combination) for combination in product(letters, repeat=5)]

    return combinations

def remove_misplaced_words(current_words, letter, pos):
    filtered_words = []

    for word in current_words:
        if word[pos] != letter and letter in word:
            filtered_words.append(word)

    return filtered_words

def include_matched_words(current_words, letter, pos):
    filtered_words = []

    for word in current_words:
        if word[pos] == letter:
            filtered_words.append(word)

    return filtered_words

def remove_wrong_letters(current_words, letter):
    filtered_words = []

    for word in current_words:
        if letter not in word:
            filtered_words.append(word)

    print(len(current_words))
    print(len(filtered_words))

    return filtered_words


def update_current_words(current_words, word, comb):
    cnt = 0
    new_current_words = current_words

    for letter, status in zip(word, comb):
        #print(letter)
        #print(status)
        if status == "Y":
            new_current_words = remove_misplaced_words(new_current_words, letter, cnt)
        if status == "B":
            new_current_words = remove_wrong_letters(new_current_words, letter)
        if status == "G":
            new_current_words = include_matched_words(new_current_words, letter, cnt)
        cnt += 1

    return new_current_words

def assign_scores(all_current_words):
    current_word_dict = dict()
    new_current_words = all_current_words

    all_combinations = generate_combinations()
    # 14855 is total allowed words
    for word in all_current_words:
        total_matches = 0
        for comb in all_combinations:
            #print(word)
            #print(comb)
            #print(len(new_current_words))
            new_current_words = update_current_words(all_current_words, word, comb)
            #print(len(new_current_words))

            ## Treating all matches the same. Can adjust this for word frequencies
            total_matches += len(new_current_words)
            #print(total_matches)
            #print(new_current_words)

        print(word + " " + str(total_matches) + " matches")
        current_word_dict[word] = total_matches
        break

    print(current_word_dict)
    return current_word_dict

if __name__ == "__main__":

    current_word_dict = assign_scores(all_current_words)

