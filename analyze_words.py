import matplotlib.pyplot as plt
from collections import Counter

def read_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        numbers = []
        for line in lines:
            # Split the line by spaces
            parts = line.strip().split()
            if parts:
                try:
                    # Extract the last value (ending number)
                    number = float(parts[-1])
                    numbers.append(number)
                except ValueError:
                    pass  # Ignore lines without valid numbers
    return numbers

def create_bar_graph(numbers):
    # Count occurrences of each value
    value_counts = Counter(numbers)

    # Extract unique values and their counts
    unique_values, counts = zip(*value_counts.items())

    # Create a bar graph
    plt.bar(unique_values, counts)
    plt.xlabel("Recorded Values")
    plt.ylabel("Occurrences")
    plt.title("Occurrences of Recorded Values in 'word_list_history.txt'")

    # Add text labels above each bar
    for x, y in zip(unique_values, counts):
        plt.text(x, y, str(y), ha='center', va='bottom')

    plt.show()

def main():
    file_path = 'word_list_history.txt'
    numbers = read_numbers_from_file(file_path)
	
	# Calculate mean, median, and range
    mean_value = sum(numbers) / len(numbers)
    sorted_numbers = sorted(numbers)
    median_value = sorted_numbers[len(sorted_numbers) // 2]
    range_value = max(numbers) - min(numbers)

    print(f"Mean: {mean_value:.2f}")
    print(f"Median: {median_value:.2f}")

    # Create the bar graph
    create_bar_graph(numbers)

if __name__ == "__main__":
    main()

