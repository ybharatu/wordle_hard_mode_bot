def update_word_frequencies(example_file, word_freq_file):
    # Read words from example.txt
    with open(example_file, 'r') as example_file:
        words_to_update = [word.strip() for word in example_file.readlines()]

    # for w in words_to_update:
    #     print(w)
    # Update frequencies in word_freq.txt
    with open(word_freq_file, 'r') as word_freq_file:
        lines = word_freq_file.readlines()

    updated_lines = []
    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            word = parts[0]
            frequency = float(parts[1])
            if word in words_to_update:
                print("Updating " + word)
                updated_lines.append(f"{word} 6.0e-07\n")
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    # Write the updated content back to word_freq.txt
    with open("word_frequencies_updated.txt", 'w') as updated_file:
        updated_file.writelines(updated_lines)

# Example usage:
update_word_frequencies("b.txt", "word_frequencies.txt")
