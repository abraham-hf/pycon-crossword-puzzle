# Word Search Puzzle Generator

A Python-based word search puzzle generator that creates custom puzzles with clues, mask shapes, and answer keys in PDF format.

## Features

- **Custom Shapes**: Use image masks to create puzzles in different shapes (HuggingFace logo, Git, Python, GitHub, VS Code, etc.)
- **Clue-based Puzzles**: Instead of just listing words, provides descriptive clues for players to solve
- **Professional PDF Output**: Generates clean, printable PDFs with:
  - Puzzle grid in custom shapes
  - Clues split into two columns on the first page ("CLUES" and "WORDS")
  - Complete answer key on the second page
- **Multiple Difficulty Levels**: Automatically generates puzzles with different difficulty levels (3-9)
- **Customizable Word Lists**: Uses CSV files for words and clues

## Prerequisites

- Python 3.8 or higher
- Poetry (Python package manager)

## Environment Setup

### 1. Install Poetry (if not already installed)

```bash
# On macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# On Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 2. Navigate to Project Directory

```bash
# Change to your project directory
cd "/Users/happyfox/Documents/pycon/cross-word/word-search 3"

# Or wherever you have the project files
cd "/path/to/your/word-search-project"
```

### 3. Install Dependencies

```bash
# Install all required packages using Poetry
poetry install
```

This will create a virtual environment and install:
- `word-search-generator`: Core puzzle generation library
- `pandas`: For CSV data handling
- `reportlab`: For PDF generation
- `PyPDF2`: For PDF manipulation

### 4. Activate the Virtual Environment

```bash
# Method 1: Activate the Poetry shell
poetry shell

# Method 2: Run commands with Poetry prefix (no need to activate)
poetry run python main.py
```

## Project Structure

```
word-search/
├── main.py                 # Main puzzle generator script
├── words1.csv             # Word and clue database
├── pyproject.toml         # Poetry configuration
├── poetry.lock           # Locked dependencies
├── mask_images/          # Shape mask images
│   ├── hf.png           # HuggingFace logo
│   ├── git.png          # Git logo
│   ├── python.png       # Python logo
│   ├── github.png       # GitHub logo
│   └── VS-CODE.png      # VS Code logo
└── README.md            # This documentation
```

## Usage

### Quick Start

```bash
# Navigate to project directory
cd "/Users/happyfox/Documents/pycon/cross-word/word-search 3"

# Method 1: Using Poetry shell
poetry shell
python main.py

# Method 2: Direct execution with Poetry
poetry run python main.py
```

### What the Script Does

1. **Reads Word Database**: Loads words and clues from `words1.csv`
2. **Generates 5 Puzzles**: Creates puzzles using different mask shapes:
   - HuggingFace logo (hf.png)
   - Git logo (git.png)  
   - Python logo (python.png)
   - GitHub logo (github.png)
   - VS Code logo (VS-CODE.png)
3. **Creates Multiple Difficulty Levels**: Generates levels 3-9 for each puzzle
4. **Produces PDF Files**: Each puzzle gets its own PDF with clues and answer key

## Output Files

The script generates PDF files with this naming convention:
- `{mask_name}_{puzzle_number}_lvl_{difficulty}.pdf`

Example outputs:
- `hf_1_lvl_3.pdf` (HuggingFace puzzle, difficulty 3)
- `git_2_lvl_5.pdf` (Git puzzle, difficulty 5)
- `python_3_lvl_7.pdf` (Python puzzle, difficulty 7)

Each PDF contains:
- **Page 1**: Puzzle grid + clues in two columns (CLUES | WORDS)
- **Page 2**: Complete answer key with coordinates and directions

## Customization

### Adding New Words and Clues

Edit the `words1.csv` file:

```csv
word_no,words,clue
1,PYTHON,Programming language named after a British comedy troupe
2,JUPYTER,Interactive computing environment for data science
3,PANDAS,Data manipulation and analysis library
4,NUMPY,Fundamental package for scientific computing arrays
...
```

### Adding New Mask Shapes

1. Add PNG images to the `mask_images/` folder
2. Update the `mask_files` list in `main.py`:

```python
mask_files = [
    'hf.png',
    'git.png', 
    'python.png',
    'github.png',
    'VS-CODE.png',
    'your-new-mask.png'  # Add your new mask here
]
```

### Adjusting Difficulty Levels

Modify the difficulty range in `main.py`:

```python
# Current: generates levels 3-9
for difficulty in range(3, 10):
    
# For easier puzzles: generate levels 1-5
for difficulty in range(1, 6):
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**:
   ```bash
   poetry install
   poetry shell
   ```

2. **File Not Found Errors**:
   ```bash
   # Make sure you're in the right directory
   pwd
   ls -la  # Should see main.py, words1.csv, etc.
   ```

3. **Permission Errors**:
   ```bash
   # Check write permissions
   ls -la
   chmod 755 main.py
   ```

4. **Mask Images Not Loading**:
   ```bash
   # Check mask images exist
   ls -la mask_images/
   ```

### Environment Issues

```bash
# Reset Poetry environment
poetry env remove python
poetry install

# Check Python version
poetry run python --version

# List installed packages
poetry show
```

### Debug Commands

```bash
# Activate environment manually
source ".venv/bin/activate"

# Check if packages are installed
python -c "import pandas; print('pandas OK')"
python -c "import word_search_generator; print('word_search_generator OK')"
python -c "import reportlab; print('reportlab OK')"
```

## Understanding the Answer Key

The answer file includes:

1. **Direction Guide**:
   - N = North (↑ Move Up)
   - NE = Northeast (↗ Move Up & Right)
   - E = East (→ Move Right)
   - SE = Southeast (↘ Move Down & Right)
   - S = South (↓ Move Down)
   - SW = Southwest (↙ Move Down & Left)
   - W = West (← Move Left)
   - NW = Northwest (↖ Move Up & Left)

2. **Coordinates Format**:
   - Row numbers start from top (1) and increase downward
   - Column numbers start from left (1) and increase rightward
   - Format: "WORD - direction (@row, column)"

3. **Two-Column Layout**:
   - **CLUES**: Descriptive hints for finding words
   - **WORDS**: The actual words to find in the puzzle

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section above
- Review console output for error messages
- Ensure all dependencies are properly installed with `poetry install`
- Verify you're in the correct directory with the project files