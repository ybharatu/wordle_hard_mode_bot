import sys
import random
from collections import Counter

def user_guess(valid_word_list, required_letters):
    while True:
        # Ask the user to enter a 5-letter word
        user_input = input("Enter a 5-letter word: ").strip().lower()

        # Check if the input is exactly 5 letters long
        if len(user_input) != 5:
            print("Please enter a word with exactly 5 letters.")
            continue

        flag = 0
        for i in required_letters:
            if i not in user_input:
                print("Hard Mode Enabled. Need to use the letter: " + i)
                flag = 1
                continue
        if flag:
            continue

        # Check if the input is in the valid_word_list
        if user_input.lower() in valid_word_list:
            #print("Valid guess! You entered:", user_input)
            return user_input
        else:
            print("Invalid guess. Try again with a valid word.")

def get_missing_letters(word1, word2):
    # Convert the words to lowercase for case-insensitive comparison
    word1 = word1.lower()
    word2 = word2.lower()

    # Use Counter to get the frequency of each letter in both words
    freq_word1 = Counter(word1)
    freq_word2 = Counter(word2)

    # Find the difference in frequencies
    missing_letters_freq = freq_word1 - freq_word2

    # Convert the missing letters with frequencies back to a string
    result = ''.join([letter * count for letter, count in missing_letters_freq.items()])
    result = [letter * count for letter, count in missing_letters_freq.items()]

    return result

def get_matching_letters(word1, word2):
    # Ensure both words are of the same length
    if len(word1) != len(word2):
        raise ValueError("Words must be of the same length.")

    # Convert the words to lowercase for case-insensitive comparison
    word1 = word1.lower()
    word2 = word2.lower()

    # Use a list comprehension to get matching letters at the same position
    matching_letters = [char1 for char1, char2 in zip(word1, word2) if char1 == char2]

    # Convert the list of matching letters back to a string
    result = ''.join(matching_letters)
    result = matching_letters

    return result

def get_shared_letters(word1, word2):
    # Ensure both words are of the same length
    if len(word1) != len(word2):
        raise ValueError("Words must be of the same length.")

    # Convert the words to lowercase for case-insensitive comparison
    word1 = word1.lower()
    word2 = word2.lower()

    # Use a set to find the unique letters that both words share
    shared_letters = set(word1) & set(word2)

    # Exclude letters at the same position
    matching_positions = [i for i, (char1, char2) in enumerate(zip(word1, word2)) if char1 == char2]
    shared_letters -= set(word1[i] for i in matching_positions)

    # Convert the set of shared letters back to a string
    result = shared_letters
    #result = ''.join(sorted(shared_letters))

    return result

def verify_guess(correct_word, guess, misplaced, wrong_letters, matched, solved):
    # Check if word is correct
    if guess == correct_word:
        print("Congrats, that is correct")
        print("The word is " + guess)
        solved = 1

    # Check which letters are incorrect
    # missing_letters = get_missing_letters(guess, correct_word)
    # matched_letters = get_matching_letters(guess, correct_word)
    # shared_letters = get_shared_letters(guess, correct_word)
    correct_letters = {
        letter for letter, correct in zip(guess, correct_word) if letter == correct
    }
    correct = list(correct_letters)
    misplaced_letters = set(guess) & set(correct_word) - correct_letters
    misplaced = list(misplaced_letters)
    wrong_letters = list(set(guess) - set(correct_word))

    # correct_letters = list(set(list(shared_letters) + correct_letters))
    # matched = list(set(matched + list(matched_letters)))
    # wrong_letters = list(set(list(missing_letters) + wrong_letters))
    print("Matched Letters: " + str(correct))
    print("Incorrect Letters: " + str(wrong_letters))
    print("Misplaced Letters: " + str(misplaced))



    # print("Is it solved? " + str(solved))
    return misplaced, wrong_letters, correct, solved

if __name__ == "__main__":
    # Gets all allowed words
    valid_words_file = "valid_wordle_words.txt"

    # Selects a secret word to be guessed (Will make this a function later)
    correct_word = "house"

    # Sets initial Values of Variables
    current_chance = 0
    max_chances = 6
    solved = 0

    misplaced_letters = []
    wrong_letters = []
    matched_letters = []
    required_letters = []

    # Open the file in read mode
    with open(valid_words_file, 'r') as file:
        # Read lines from the file and create a list of words
        valid_word_list = [line.strip() for line in file]

    # Print the list of words
    #print(valid_word_list)

    while (current_chance < max_chances and not solved):
        # Takes in a guess from the user/bot
        required_letters = misplaced_letters + matched_letters
        guess = user_guess(valid_word_list, required_letters)
        misplaced_letters, wrong_letters, matched_letters, solved = verify_guess(correct_word, guess, misplaced_letters, wrong_letters, matched_letters, solved)
        print(misplaced_letters)
        print(matched_letters)
        print(wrong_letters)




