import pandas as pd
import random
from word_search_generator import WordSearch
from word_search_generator.mask import BitmapImage
import os
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red

DIFFICULTY_LEVEL = 3  # Example difficulty level

MASK_IMAGES_DIR = "mask_images"
PUZZLES_DIR = "puzzles"

# To generate only one puzzle for now, set the limit to 1 for a single mask image.
# You can restore the original values to generate more puzzles later.
MASK_IMAGES_FILE_NAMES = {
    'hf.png': 1,  # Set to 1 for now; increase for more puzzles per mask
    'git.png': 1,
    'python.png': 1,
    'github.png': 1,
    'VS-CODE.png': 1
}

def create_custom_puzzle_pdf(puzzle, selected_words, selected_clues, puzzle_filename):
    """Create a custom PDF with clues instead of words"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    c = canvas.Canvas(puzzle_filename, pagesize=letter)
    page_width, page_height = letter
    
    # Get the puzzle grid as string
    puzzle_str = str(puzzle)
    lines = puzzle_str.split('\n')
    
    # Find the grid content
    grid_lines = []
    in_grid = False
    
    for line in lines:
        if '───' in line:
            if not in_grid:
                in_grid = True
                # Skip the first border line (don't append it)
            else:
                # Skip the last border line and break
                break
        elif in_grid:
            grid_lines.append(line)
    
    # Set up the document
    c.setFont("Courier-Bold", 16)
    y = page_height - 50
    
    # Title
    title = "WORD SEARCH"
    title_width = c.stringWidth(title)
    c.drawString((page_width - title_width) / 2, y, title)
    y -= 40
    
    # Draw the grid
    c.setFont("Courier", 12)
    line_height = 14
    
    for line in grid_lines:
        if line.strip():
            line_width = c.stringWidth(line)
            c.drawString((page_width - line_width) / 2, y, line)
        y -= line_height
    
    # Add instructions on the same page as grid
    y -= 20
    c.setFont("Courier-Bold", 14)
    instructions = "Find words going NW, S, E, SW, SE, N, NE, and W:"
    instr_width = c.stringWidth(instructions)
    c.drawString((page_width - instr_width) / 2, y, instructions)
    y -= 40
    
    # Add clues in two columns at the bottom of the first page
    # Left column setup
    left_column_x = 50
    right_column_x = page_width // 2 + 147
    clue_y = y
    
    # Left column heading: "CLUES"
    c.setFont("Courier-Bold", 14)
    clues_heading = "CLUES"
    c.drawString(left_column_x, clue_y, clues_heading)
    
    # Right column heading: "WORDS"
    words_heading = "WORDS"
    c.drawString(right_column_x, clue_y, words_heading)
    
    clue_y -= 25
    c.setFont("Courier", 9)  # Slightly smaller font to fit more text
    
    # Left column (clues 1-5)
    current_y = clue_y
    for i in range(min(5, len(selected_words))):
        word = selected_words[i]
        clue = selected_clues[i]
        clue_text = f"{i+1:2d}. {clue}"
        
        # Handle long clues with wrapping for left column
        max_width = (page_width // 2) - 20  # Even more width to prevent cutting
        if c.stringWidth(clue_text) > max_width:
            words = clue_text.split()
            current_line = ""
            
            for word_part in words:
                if c.stringWidth(current_line + word_part + " ") < max_width:
                    current_line += word_part + " "
                else:
                    if current_line:
                        c.drawString(left_column_x, current_y, current_line.strip())
                        current_y -= 11  # Slightly tighter line spacing
                    current_line = "    " + word_part + " "
            
            if current_line:
                c.drawString(left_column_x, current_y, current_line.strip())
        else:
            c.drawString(left_column_x, current_y, clue_text)
        
        current_y -= 13  # Slightly tighter spacing between items
    
    # Right column (words 6-10)
    current_y = clue_y
    for i in range(5, min(10, len(selected_words))):
        word = selected_words[i]
        word_text = f"{i+1:2d}. {word.upper()}"
        
        # Handle long words with wrapping for right column
        max_width = (page_width // 2) - 20  # Even more width to prevent cutting
        if c.stringWidth(word_text) > max_width:
            words = word_text.split()
            current_line = ""
            
            for word_part in words:
                if c.stringWidth(current_line + word_part + " ") < max_width:
                    current_line += word_part + " "
                else:
                    if current_line:
                        c.drawString(right_column_x, current_y, current_line.strip())
                        current_y -= 11  # Slightly tighter line spacing
                    current_line = "    " + word_part + " "
            
            if current_line:
                c.drawString(right_column_x, current_y, current_line.strip())
        else:
            c.drawString(right_column_x, current_y, word_text)
        
        current_y -= 13  # Slightly tighter spacing between items
    
    # Start a new page for answer key only
    c.showPage()
    y = page_height - 50
    
    # Always show answer key title
    c.setFont("Courier-Bold", 14)
    answer_title = "ANSWER KEY"
    answer_title_width = c.stringWidth(answer_title)
    c.drawString((page_width - answer_title_width) / 2, y, answer_title)
    y -= 25
    
    c.setFont("Courier", 10)
    
    # Extract answer key from puzzle string
    puzzle_str = str(puzzle)
    lines = puzzle_str.split('\n')
    
    # Debug: Let's first see what the puzzle output actually looks like
    print("\n=== PUZZLE OUTPUT DEBUG ===")
    answer_section_started = False
    for i, line in enumerate(lines):
        if 'Answer Key' in line:
            answer_section_started = True
            print(f"Line {i}: {repr(line)}")
        elif answer_section_started:
            print(f"Line {i}: {repr(line)}")
            if not line.strip():  # Empty line might end the section
                break
    print("=== END DEBUG ===\n")
    
    # Find the answer key section
    answer_key_found = False
    answer_data = {}
    all_answer_lines = []
    
    for line in lines:
        if 'Answer Key:' in line:
            answer_key_found = True
            # Process this line and continue
            line = line.replace('Answer Key:', '').strip()
            if line:  # If there's content after "Answer Key:"
                all_answer_lines.append(line)
        elif answer_key_found and line.strip():
            all_answer_lines.append(line.strip())
        elif answer_key_found and not line.strip():
            break  # Empty line ends the answer key section
    
    # Combine all answer key lines into one string
    combined_answer_text = ' '.join(all_answer_lines)
    
    if combined_answer_text:
        # Clean all ANSI color codes first
        import re
        clean_text = re.sub(r'\x1b\[[0-9;]*m', '', combined_answer_text)  # Remove ANSI codes
        
        print(f"Combined answer text: {repr(clean_text)}")
        
        # Look for pattern: WORD DIRECTION @ (column, row)
        # Find all matches of pattern: WORD DIRECTION @ (x, y)
        matches = re.findall(r'(\w+(?:\s+\w+)*)\s+(\w+)\s+@\s*\(([^)]+)\)', clean_text)
        
        print(f"Found matches: {matches}")
        
        for match in matches:
            word = match[0].strip()
            direction = match[1].strip()
            coordinates = match[2].strip()
            
            print(f"Match: word={word}, direction={direction}, coords={coordinates}")
            
            # Split coordinates to get column and row
            coords = coordinates.split(',')
            if len(coords) >= 2:
                column = coords[0].strip()
                row = coords[1].strip()
                answer_data[word] = {
                    'direction': direction,
                    'column': column,
                    'row': row
                }
    
    print(f"Final answer_data: {answer_data}")
    
    # Function to calculate end coordinates based on start coordinates, direction, and word length
    def calculate_end_coordinates(start_col, start_row, direction, word_length):
        start_col = int(start_col)
        start_row = int(start_row)
        word_length -= 1  # Subtract 1 because we start counting from the first letter
        
        direction_map = {
            'N': (0, -word_length),    # North: same column, row decreases
            'S': (0, word_length),     # South: same column, row increases
            'E': (word_length, 0),     # East: column increases, same row
            'W': (-word_length, 0),    # West: column decreases, same row
            'NE': (word_length, -word_length),  # Northeast: column increases, row decreases
            'NW': (-word_length, -word_length), # Northwest: column decreases, row decreases
            'SE': (word_length, word_length),   # Southeast: column increases, row increases
            'SW': (-word_length, word_length)   # Southwest: column decreases, row increases
        }
        
        col_offset, row_offset = direction_map.get(direction, (0, 0))
        end_col = start_col + col_offset
        end_row = start_row + row_offset
        
        return end_col, end_row
    
    # Display the answer key in the requested format: no) words - location (direction (@start_col, start_row) to (@end_col, end_row))
    for i, word in enumerate(selected_words, 1):
        original_word = word.upper()
        word_key = word.upper().replace(' ', '')
        
        if y < 50:  # Check for page break
            c.showPage()
            y = page_height - 50
            c.setFont("Courier", 10)
        
        # Format: no) words - location (direction (@column, row))
        location_found = False
        direction = ""
        column = ""
        row = ""
        
        # Check for exact match first
        if word_key in answer_data:
            location_info = answer_data[word_key]
            direction = location_info['direction']
            column = location_info['column']
            row = location_info['row']
            location_found = True
        else:
            # For multi-word terms, check if individual words are found
            words_in_phrase = original_word.split()
            if len(words_in_phrase) > 1:
                # Check if all individual words are found and have the same location
                first_word_data = None
                all_words_same_location = True
                
                for single_word in words_in_phrase:
                    if single_word in answer_data:
                        if first_word_data is None:
                            first_word_data = answer_data[single_word]
                        elif (answer_data[single_word]['column'] != first_word_data['column'] or 
                              answer_data[single_word]['row'] != first_word_data['row'] or
                              answer_data[single_word]['direction'] != first_word_data['direction']):
                            all_words_same_location = False
                            break
                    else:
                        all_words_same_location = False
                        break
                
                if all_words_same_location and first_word_data:
                    direction = first_word_data['direction']
                    column = first_word_data['column']
                    row = first_word_data['row']
                    location_found = True
        
        if location_found:
            # Calculate end coordinates
            word_length = len(original_word.replace(' ', ''))  # Remove spaces for actual word length
            end_col, end_row = calculate_end_coordinates(column, row, direction, word_length)
            answer_line = f"{i:2d}) {original_word} - location ({direction} (@{row}, {column}) to (@{end_row}, {end_col}))"
        else:
            answer_line = f"{i:2d}) {original_word} - location (not found)"
        
        c.drawString(50, y, answer_line)
        y -= 15
    
    c.save()

def main():
    df = pd.read_csv("words1.csv")
    words = df["words"].tolist()
    clues = df["clue"].tolist()
    
    # Create a dictionary mapping words to clues
    word_to_clue = dict(zip(words, clues))
    
    total_puzzles_created = 0  # Initialize the total counter
    
    for mask_image, limit in MASK_IMAGES_FILE_NAMES.items():
        puzzle_count = 0  # Initialize the counter for each mask image
        
        while puzzle_count < limit:
            print(f"Creating puzzle {total_puzzles_created + 1} with mask {mask_image}")
            # get current working directory
            current_dir = os.getcwd()
            mask_image_file_name = mask_image.split(".")[0]
            # get the full path of the mask image
            mask_image = os.path.join(current_dir, MASK_IMAGES_DIR, mask_image)


            # Step 2: Select 10 random words
            selected_words = random.sample(words, 10)
            
            # Get clues for selected words
            selected_clues = [word_to_clue[word] for word in selected_words]
            
            print("Selected words with clues:")
            for word, clue in zip(selected_words, selected_clues):
                print(f"- {word}: {clue}")
            
            # create string of words separated by comma
            string_of_words = ", ".join(selected_words)
            
            # Create puzzle with mask applied properly
            try:
                # Create the puzzle first
                puzzle = WordSearch(string_of_words, level=DIFFICULTY_LEVEL, size=35)
                
                # Load and apply the mask
                mask = BitmapImage(mask_image)
                puzzle.apply_mask(mask)  # Apply the mask
                
                print(f"Puzzle created with mask {mask_image}")
                
            except Exception as e:
                print(f"Error applying mask {mask_image}: {e}")
                print("Creating puzzle without mask...")
                # Fallback to puzzle without mask
                puzzle = WordSearch(string_of_words, level=DIFFICULTY_LEVEL, size=35)
            

            # Generate the puzzle PDF filename as {mask_image}_question_{number}.pdf
            while True:
                puzzle_filename = f"{mask_image_file_name}_question_{total_puzzles_created + 1}.pdf"
                if not os.path.exists(puzzle_filename):
                    break
                total_puzzles_created += 1  # Avoid overwriting, increment if file exists

            # Create custom puzzle PDF with clues instead of words
            create_custom_puzzle_pdf(puzzle, selected_words, selected_clues, puzzle_filename)
            
            puzzle_count += 1  # Increment the counter for the current mask image
            total_puzzles_created += 1  # Increment the total counter

    print("Total puzzles created:", total_puzzles_created)

if __name__ == "__main__":
    main()