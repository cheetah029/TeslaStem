from cmu_graphics import *
# (Uncomment in your CMU CS Academy code.)

# ==========================================
# GRID AND SHAPES
# ==========================================

# Set the number of rows/cols in your "land".
rows = 5
cols = 5

# Decide how large each cell will be on-screen (in pixels).
cellSize = 400 / rows

# This 2D list holds the state for each cell. Each cell is:
# [plantType, growthStage, hasPests, waterNeeded, fertilized]
# e.g., ["flower", 2, False, 0, True]
grid = []

# This 2D list holds the actual Rect (or Circle, etc.) for each cell in Shape Mode.
# We'll update these shapes' .fill or other properties to show changes.
gridShapes = Group()

# ==========================================
# SIMPLE GLOBAL VARIABLES
# ==========================================
dayCounter = 0        # How many "days" have passed
maxDays = 20          # Optional limit
actionMode = "plant"  # 'plant', 'water', 'fertilize', or 'preventPests'

# ==========================================
# SETUP FUNCTION
# ==========================================
def setupGame():
    """
    Initialize the grid and shapes. Called once at the start.

    TODO:
    1. Build 'grid' with rows x cols, each cell as [None, 0, False, 0, False].
       (Meaning: no plant yet, growth=0, no pests, needs 0 water, not fertilized.)
    2. For each cell, create a shape (Rect) in the same row/col position,
       e.g.: shape = Rect(c*cellSize, r*cellSize, cellSize, cellSize, fill='brown')
    3. Store these shapes in the 'shapes' 2D list in parallel to 'grid'.
    """
    for row in range(rows):
        for col in range(cols):
            grid.append([0, 0, 0, 0, 0])
            gridShapes.add(Rect(col*cellSize, row*cellSize, cellSize, cellSize, fill='saddleBrown', border='black'))

# ==========================================
# MAIN ACTIONS
# ==========================================
def handleAction(row, col):
    """
    Based on 'actionMode', modify the cell at grid[row][col].

    'plant': If cell is empty (plantType=None), set plantType to something (e.g. "flower"),
             also set growthStage=0, waterNeeded=2, etc.
    'water': Reduce waterNeeded by 1 (don't go below 0).
    'fertilize': cell[4] = True.
    'preventPests': cell[2] = False.

    After updating the cell, you may also want to change shapes[row][col].fill
    to visually represent the update.

    TODO:
    1. Access the cell list: cell = grid[row][col].
    2. Use if/elif to check actionMode and modify the cell accordingly.
    3. Update shapes[row][col].fill to reflect the new state if desired.
    """
    pass

def endOfDayUpdate():
    """
    Runs once after the user finishes a day (e.g., pressing 'd').

    TODO:
    1. Increase dayCounter by 1.
    2. Loop over every cell in grid:
       - If waterNeeded > 0, the plant might not grow or might wither.
       - If hasPests=True, hamper or reset growth unless it was prevented.
       - If fertilized=True, you might add +1 to growthStage or similar boost.
       - Then reset waterNeeded/fertilized as needed for the next day.
    3. Optionally check if dayCounter >= maxDays or if you've met a "biodiversity" goal.
    """
    pass

# Optional function if you want a "score" or something similar.
def calculateBiodiversityScore():
    """
    Example helper that returns how many cells have different types or certain growth levels.
    
    TODO:
    1. Loop over grid, count plant types that are grown.
    2. Return a number representing the "score".
    """
    pass

# ==========================================
# EVENT HANDLERS
# ==========================================
def onMousePress(x, y):
    """
    When the user clicks, figure out which cell was clicked and call handleAction(row, col).

    TODO:
    1. Convert x, y to row, col by dividing by cellSize:
        row = y // cellSize
        col = x // cellSize
    2. Check boundaries (0 <= row < rows, etc.).
    3. Call handleAction(row, col) if valid.
    """
    pass

def onKeyPress(key):
    """
    Handles user input from the keyboard to set actionMode or end the day.

    - 'p' => 'plant'
    - 'w' => 'water'
    - 'f' => 'fertilize'
    - 'x' => 'preventPests'
    - 'd' => calls endOfDayUpdate()

    TODO:
    1. if key == 'p': actionMode = 'plant'
       if key == 'w': actionMode = 'water'
       if key == 'f': actionMode = 'fertilize'
       if key == 'x': actionMode = 'preventPests'
       if key == 'd': endOfDayUpdate()
    """
    pass

def onStep():
    """
    Called many times per second in Shape Mode. If you want a purely "turn-based" game,
    you might not need anything here except optional animations.

    TODO (optional):
    1. Animate shapes if a plant grows from stage 0 to stage 1, or color changes, etc.
    2. Or simply leave it empty if you don't need real-time animations.
    """
    pass

# ==========================================
# MAIN START (SIMPLE)
# ==========================================
setupGame()
cmu_graphics.run()
#
# In some CMU CS Academy environments, you might put setupGame() in onAppStart. 
# The key is to ensure the grid/shapes are created before user interaction begins.
