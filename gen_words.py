import pandas as pd

# Step 2: Read the input text file line by line
input_file = 'input.txt'
output_file = '.csv'

data = []

with open(input_file, 'r') as file:
    for line in file:
        # Step 3: Parse each line to extract word_no, word, and clue
        word_no, word, clue = line.strip().split(':')
        # Step 4: Store the parsed data in a list of dictionaries
        data.append({'word_no': word_no, 'words': word, 'clue': clue})

# Step 5: Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Step 6: Write the DataFrame to a CSV file
df.to_csv(output_file, index=False)