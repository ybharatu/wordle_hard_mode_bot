import os
from datetime import datetime

# Function to extract title, content, and date from each file
def extract_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Extracting title
        title = lines[-1].strip().split('"')[1]
        # Extracting content
        content = ''.join(lines[:-1])
        # Extracting date from file name
        date_str = os.path.splitext(os.path.basename(file_path))[0].split('_')
        month_str = date_str[0]
        day_str = date_str[1]
        year_str = date_str[2]
        # Converting month string to month number
        month_dict = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        month_num = month_dict[month_str]
        # Formatting date
        date = f"{year_str}-{month_num}-{day_str}"
        return {'title': title, 'content': content, 'date': date}

# Main function to iterate over .txt files in directory
def main():
    directory = '.'  # Assuming current directory, change it if needed
    for file_name in os.listdir(directory):
#        print(file_name)
        if file_name.endswith('.txt'):
            file_path = os.path.join(directory, file_name)
            poem_info = extract_info(file_path)
            print(poem_info)

if __name__ == "__main__":
    main()

