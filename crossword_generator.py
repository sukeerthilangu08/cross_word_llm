import random
import sys

def read_words(filepath):
    """Reads words from a file, one word per line."""
    with open(filepath, 'r') as f:
        words = [word.strip().upper() for word in f if word.strip()]
    return words

def initialize_grid(size):
    """Initializes an empty grid of a given size."""
    return [['_' for _ in range(size)] for _ in range(size)]

def display_grid(grid, title="Grid"):
    """Displays the crossword grid with a title."""
    print(f"\n--- {title} ---")
    for row in grid:
        print(' '.join(row))
    print("------------------")

def add_symmetric_black_squares(grid, density=0.2):
    """Adds rotationally symmetric black squares to the grid."""
    size = len(grid)
    for r in range(size):
        for c in range(size // 2 + 1):
            if random.random() < density:
                grid[r][c] = '#'
                grid[size - 1 - r][size - 1 - c] = '#'

def get_user_confirmation():
    """Prompts the user for a yes/no confirmation."""
    while True:
        response = input("Do you want to generate a crossword puzzle? (yes/no): ").lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def get_grid_size():
    """Prompts the user to select the grid size."""
    while True:
        try:
            size = int(input("Enter the desired grid size (e.g., 15 for 15x15): "))
            if size > 0:
                return size
            else:
                print("Grid size must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def can_place_word_at(grid, word, row, col, direction, require_intersection=False):
    """Checks if a word can be placed at a specific location, considering intersections and rules."""
    grid_size = len(grid)
    word_len = len(word)
    intersection_found = False

    if col < 0 or row < 0 or col >= grid_size or row >= grid_size:
        return False

    if direction == 0:  # Horizontal
        if col + word_len > grid_size: return False
        if col > 0 and grid[row][col - 1] not in ['_', '#']: return False
        if col + word_len < grid_size and grid[row][col + word_len] not in ['_', '#']: return False

        for i in range(word_len):
            char_on_grid = grid[row][col + i]
            char_in_word = word[i]

            if char_on_grid == '#': return False

            if char_on_grid == char_in_word:
                intersection_found = True
                continue
            
            if char_on_grid != '_': return False

            if row > 0 and grid[row - 1][col + i] not in ['_', '#']: return False
            if row < grid_size - 1 and grid[row + 1][col + i] not in ['_', '#']: return False
    
    else:  # Vertical
        if row + word_len > grid_size: return False
        if row > 0 and grid[row - 1][col] not in ['_', '#']: return False
        if row + word_len < grid_size and grid[row + word_len][col] not in ['_', '#']: return False

        for i in range(word_len):
            char_on_grid = grid[row + i][col]
            char_in_word = word[i]

            if char_on_grid == '#': return False

            if char_on_grid == char_in_word:
                intersection_found = True
                continue

            if char_on_grid != '_': return False

            if col > 0 and grid[row + i][col - 1] not in ['_', '#']: return False
            if col < grid_size - 1 and grid[row + i][col + 1] not in ['_', '#']: return False
            
    return intersection_found if require_intersection else True

def place_word_on_grid(grid, word, row, col, direction):
    """Places a word on the grid."""
    if direction == 0:  # Horizontal
        for i in range(len(word)):
            grid[row][col + i] = word[i]
    else:  # Vertical
        for i in range(len(word)):
            grid[row + i][col] = word[i]

def find_all_placements(grid, word, require_intersection=False):
    """Finds all valid placements for a word on the grid."""
    placements = []
    grid_size = len(grid)
    for r in range(grid_size):
        for c in range(grid_size):
            # Horizontal
            if can_place_word_at(grid, word, r, c, 0, require_intersection):
                placements.append((r, c, 0))
            # Vertical
            if can_place_word_at(grid, word, r, c, 1, require_intersection):
                placements.append((r, c, 1))
    return placements

def solve_backtracking(grid, words):
    """Recursively tries to place words on the grid using backtracking."""
    if not words:
        return grid  # Success

    word_to_place = words[0]
    remaining_words = words[1:]

    # If grid has no letters yet, first word doesn't need an intersection.
    has_letters = any(cell not in ['_', '#'] for row in grid for cell in row)
    
    placements = find_all_placements(grid, word_to_place, require_intersection=has_letters)
    random.shuffle(placements)

    for r, c, d in placements:
        new_grid = [row[:] for row in grid]
        place_word_on_grid(new_grid, word_to_place, r, c, d)
        
        result = solve_backtracking(new_grid, remaining_words)
        if result is not None:
            return result

    return None

# Main execution
if __name__ == "__main__":
    if not get_user_confirmation():
        print("Crossword generation cancelled.")
        sys.exit()

    GRID_SIZE = get_grid_size()
    words = read_words('words.txt')

    # Filter out words that are too long for the grid and notify the user
    original_word_count = len(words)
    words = [word for word in words if len(word) <= GRID_SIZE]
    filtered_count = original_word_count - len(words)
    if filtered_count > 0:
        print(f"Filtered out {filtered_count} words that were too long for the {GRID_SIZE}x{GRID_SIZE} grid.")

    if not words:
        print("No words from the list fit within the specified grid size. Cannot generate crossword.")
        sys.exit()

    words.sort(key=len, reverse=True)

    grid = initialize_grid(GRID_SIZE)
    add_symmetric_black_squares(grid)
    display_grid(grid, "Initial Grid")

    print("Starting backtracking solver...")
    final_grid = solve_backtracking(grid, words)

    if final_grid:
        display_grid(final_grid, "Final Grid")
    else:
        print("\nCould not generate a valid crossword with the given words and grid size.")
        print("This can happen if the word list is incompatible with the black square layout.")
        print("Try running the generator again for a different random layout.")
