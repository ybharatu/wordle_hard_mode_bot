from itertools import product
import random
import copy
from wordfreq import word_frequency

# Can look at this link to help connect to the NYT
# https://devsblog.hashnode.dev/wordle-bot-python

# Gets all allowed words
valid_words_file = "valid_wordle_words.txt"

# Open the file in read mode
with open(valid_words_file, 'r') as file:
    # Read lines from the file and create a list of words
    all_current_words = [line.strip() for line in file]

def read_word_frequencies(file_path):
    word_frequencies = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    word = parts[0]
                    frequency = float(parts[1])
                    word_frequencies[word] = frequency
                else:
                    print(f"Ignoring invalid line: {line}")

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return word_frequencies

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

    return filtered_words

def remove_wrong_letters_pos(current_words, letter, pos):
    filtered_words = []

    for word in current_words:
        if word[pos] != letter:
            filtered_words.append(word)

    return filtered_words


def update_current_words(current_words, word, comb):
    cnt = 0
    combos = []
    for letter, status in zip(word, comb):
        combos.append(letter + status)
        if status == "Y":
            current_words = remove_misplaced_words(current_words, letter, cnt)
        if status == "B":
            if (letter + "G") in combos:
                current_words = remove_wrong_letters_pos(current_words, letter, cnt)
            elif (letter + "Y") in combos:
                current_words = remove_wrong_letters_pos(current_words, letter, cnt)
            else:
                current_words = remove_wrong_letters(current_words, letter)
        if status == "G":
            current_words = include_matched_words(current_words, letter, cnt)
        cnt += 1

    return current_words

def calculate_total_sum(word_dict, word_list):
    total_sum = sum(word_dict.get(word, 0) for word in word_list)
    return total_sum

def assign_scores(new_current_words):
    current_word_dict = dict()
    #new_current_words = all_current_words
    iterate_words = new_current_words

    all_combinations = generate_combinations()
    # 14855 is total allowed words
    for word in iterate_words:
        total_matches = 0

        for comb in all_combinations:
            new_current_words = iterate_words
            #print(word)
            #print(comb)
            old = len(new_current_words)

            new_current_words = update_current_words(new_current_words, word, comb)
            comb_prob = len(new_current_words) / old
            new = len(new_current_words) * comb_prob
            #new = calculate_total_sum(freq_dict, new_current_words)
            #print(new)

            ## Treating all matches the same. Can adjust this for word frequencies
            #print(total_matches)
            #print(new)
            total_matches += new
            #print(total_matches)
            #print(new_current_words)

        #print(word + " " + str(total_matches) + " matches")
        #print(word + " " + str(word_frequency(word, 'en')))
        current_word_dict[word] = total_matches

    #sorted_items = sorted(current_word_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_items = dict(sorted(current_word_dict.items(), key=lambda item: item[1]))
    #print(sorted_items)
    return current_word_dict

def words_above_benchmark(word_dict, benchmark):
    above_benchmark_words = [word for word, value in word_dict.items() if value > benchmark]
    return above_benchmark_words

def words_below_benchmark(word_dict, benchmark):
    above_benchmark_words = [word for word, value in word_dict.items() if value < benchmark]
    return above_benchmark_words

def read_file_and_create_dict(file_path):
    word_dict = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 3:
                    word = parts[0]
                    number = float(parts[1])
                    word_dict[word] = number
                else:
                    print(f"Ignoring invalid line: {line}")

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Sort the dictionary based on values in ascending order
    sorted_word_dict = dict(sorted(word_dict.items(), key=lambda item: item[1]))

    return sorted_word_dict

def get_feedback(word):
    while True:
        user_input = input(f"Enter a 5-letter string with B, G, or Y for the word '{word}': ").strip().upper()

        if len(user_input) == 5 and all(letter in "BGY" for letter in user_input):
            return user_input
        else:
            print("Invalid input. Please enter a 5-letter string with B, G, or Y.")

def get_feedback_env(word, correct_word):
    result = ""

    for i in range(len(word)):
        if word[i] == correct_word[i]:
            result += "G"  # Same letter in the same position
        elif word[i] in correct_word:
            result += "Y"  # Same letter, but different position
        else:
            result += "B"  # Letter not in the correct word
    #print(result)
    return result

def wordle_env(correct_word):
    return_val = play_wordle_bot(correct_word)
    return return_val

def play_wordle_bot(correct_word):
    file_path = "word_frequencies_updated.txt"
    frequency_dict = read_word_frequencies(file_path)
    most_likely_words = words_above_benchmark(frequency_dict, 5.0e-07)
    most_likely_matches = read_file_and_create_dict("matches.txt")
    best_matches = words_below_benchmark(most_likely_matches, 300)
    # print(len(all_current_words))
    # print(len(most_likely_words))
    # print(len(best_matches))
    starting_word = random.choice(best_matches)
    #starting_word = best_matches[0]
    # print(starting_word)
    all_guesses = []

    all_combinations = generate_combinations()
    for i in range(30):
        # if (len(most_likely_words) == 1):
        #     print("YOU FOUND THE WORD! It is: " + most_likely_words[0])
        #     break
        all_guesses.append(starting_word)
        comb = get_feedback_env(starting_word, correct_word)
        if (comb.lower() == "ggggg"):
            #print("CORRECT. The word is: " + starting_word)
            break
        #print(len(most_likely_words))
        most_likely_words = update_current_words(most_likely_words, starting_word, comb)
        #print(len(most_likely_words))
        current_word_dict = assign_scores(most_likely_words)
        #print(starting_word)
        #print(current_word_dict)
        starting_word = min(current_word_dict, key=current_word_dict.get)
        # starting_word = current_word_dict.keys()[0]
        #print("New starting word is " + starting_word)

    #print(all_guesses)
    # with open("example.txt", "a") as file:
    #     file.write(all_guesses)
    #     file.write("\n")
    all_guesses.append(len(all_guesses))
    return all_guesses
    # play_wordle(best_mat)
    # print(most_likely_words)
    # print(frequency_dict)
    # current_word_dict = assign_scores(most_likely_words, frequency_dict, most_likely_matches)

if __name__ == "__main__":

    # Open the file in read mode
    with open("answer_list.txt", 'r') as file:
        # Read lines from the file and create a list of words
        answer_list = [line.strip() for line in file]
    #chosen_answer = random.choice(answer_list)
    #chosen_answer = "wooer"
    #print(chosen_answer)

    for chosen_answer in answer_list:
        try:
            all_guesses = wordle_env(chosen_answer)
            #print(all_guesses)

        except:
            print(chosen_answer + " does not work")
            with open("example2.txt", "a") as file:
                file.write(chosen_answer + " does not work")
                file.write("\n")
        finally:
            print(str(all_guesses))
            with open("example2.txt", "a") as file:
                file.write(str(all_guesses))
                file.write("\n")

