from cmu_graphics import *

# ---------------------------------------
# SETUP APP VARIABLES
# ---------------------------------------
def onAppStart():
    # Basic grid config
    app.background = 'limeGreen'
    app.cellSize = 80
    app.rows = 4
    app.cols = 5
    app.maxDays = 20
    app.maxStages = 4

    # Each cell is [plantType, growthStage, hasPests, waterNeeded, fertilized].
    # We'll have a parallel 2D list of shape references for each cell's "plant shapes."
    app.grid = []
    app.cellPlants = []
    app.cellBackgrounds = []

    # Game state
    app.dayCounter = 0
    app.actionMode = 'plant'
    app.gameOver = False

    # Display for day and action
    app.display = Label(f"Day: {app.dayCounter}   Action: {app.actionMode.upper()}", 10,
            app.rows * app.cellSize + 10, align='left', size=14, fill='black')

    # We'll animate fully grown plants with a simple "pulse" in onStep.
    app.tick = 0

    # Create the grid data and shapes.
    setupGame()

# ---------------------------------------
# SETUP GAME
# ---------------------------------------
def setupGame():
    # Initialize the 2D lists for the grid, shape references, etc.
    for r in range(app.rows):
        rowData = []
        rowPlantShapes = []
        rowBG = []

        for c in range(app.cols):
            # Empty cell: [None, 0, False, 0, False]
            rowData.append([None, 0, False, 0, False])

            # Background shape
            xPos = c * app.cellSize
            yPos = r * app.cellSize
            bg = Rect(xPos, yPos, app.cellSize, app.cellSize, fill='saddlebrown', border='black', borderWidth=1)
            rowBG.append(bg)

            # No plant shapes yet
            rowPlantShapes.append([])

        app.grid.append(rowData)
        app.cellPlants.append(rowPlantShapes)
        app.cellBackgrounds.append(rowBG)

    # Simple instructions
    Label("Press p/w/f/x to set action, click cells, press d to end day", 10,
          app.rows * app.cellSize + 40, size=14, fill='black', align='left')
    Label("Goal: After 20 days, grow as many flowers as possible!", 10,
          app.rows * app.cellSize + 60, size=14, fill='black', align='left')

# ---------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------
def clearPlantShapes(r, c):
    """
    Remove old shape objects for this cell's plant.
    """
    for shape in app.cellPlants[r][c]:
        shape.visible = False
    app.cellPlants[r][c].clear()

def drawPlant(r, c, stage, hasPests):
    """
    Draw shapes for a plant at a given growth stage, plus a pest indicator if needed.
    """
    xPos = c * app.cellSize
    yPos = r * app.cellSize
    centerX = xPos + app.cellSize/2
    centerY = yPos + app.cellSize/2

    # Stage 0: seed
    if stage == 0:
        seed = Circle(centerX, centerY, 6, fill='sienna')
        if app.grid[r][c][4]:
            seed.fill = 'black'
        app.cellPlants[r][c].append(seed)

    # Stage 1: small sprout
    elif stage == 1:
        root = Circle(centerX, centerY + 10, 6, fill='sienna')
        stem = Rect(centerX - 2, centerY - 10, 4, 20, fill='lime')
        leafLeft = Oval(centerX - 8, centerY - 10, 16, 8, fill='lime')
        leafRight = Oval(centerX + 8, centerY - 10, 16, 8, fill='lime')
        app.cellPlants[r][c].extend([root, stem, leafLeft, leafRight])

    # Stage 2: developing plant
    elif stage == 2:
        root = Circle(centerX, centerY + 10, 6, fill='sienna')
        stem = Rect(centerX - 2, centerY - 20, 4, 30, fill='lime')
        leafLeft = Oval(centerX - 8, centerY - 10, 16, 8, fill='lime')
        leafRight = Oval(centerX + 8, centerY - 10, 16, 8, fill='lime')
        leafTop = Oval(centerX, centerY - 20, 8, 16, fill='lime')
        app.cellPlants[r][c].extend([root, stem, leafLeft, leafRight, leafTop])

    # Stage 3: mature plant
    elif stage == 3:
        stem = Rect(centerX - 2, centerY - 20, 4, 35, fill='lime')
        leafLeft = Oval(centerX - 8, centerY, 16, 8, fill='lime')
        leafRight = Oval(centerX + 8, centerY, 16, 8, fill='lime')
        leafLeft2 = Oval(centerX - 8, centerY - 10, 16, 8, fill='lime')
        leafRight2 = Oval(centerX + 8, centerY - 10, 16, 8, fill='lime')
        leafTop = Oval(centerX, centerY - 20, 8, 16, fill='lime')
        app.cellPlants[r][c].extend([stem, leafLeft, leafRight, leafLeft2, leafRight2, leafTop])

    # Stage 4: fully grown flower
    else:
        stem = Rect(centerX - 2, centerY - 15, 4, 30, fill='darkGoldenrod')
        leafLeft = Oval(centerX - 8, centerY, 16, 8, fill='darkGoldenrod')
        leafRight = Oval(centerX + 8, centerY, 16, 8, fill='darkGoldenrod')
        petal1 = Circle(centerX - 5, centerY - 15, 5, fill='pink')
        petal2 = Circle(centerX + 5, centerY - 15, 5, fill='pink')
        petal3 = Circle(centerX, centerY - 20, 5, fill='pink')
        petal4 = Circle(centerX, centerY - 11, 5, fill='pink')
        center = Circle(centerX, centerY - 15, 5, fill='yellow')
        app.cellPlants[r][c].extend([stem, leafLeft, leafRight, petal1, petal2, petal3, petal4, center])

    # If pests are present, place a small red "bug" indicator
    if hasPests:
        bug = Circle(xPos + app.cellSize - 10, yPos + 10, 5, fill='red')
        app.cellPlants[r][c].append(bug)

def updateCellVisual(r, c):
    """
    Remove old shapes, then draw new ones based on cell data.
    """
    clearPlantShapes(r, c)
    cell = app.grid[r][c]
    plantType, stage, pests, wNeed, fert = cell
    if plantType is not None:
        drawPlant(r, c, stage, pests)

def updateDayDisplay():
    """
    Update the day/action display at the bottom.
    """
    # Overwrite with a small rectangle
    # Rect(0, app.rows * app.cellSize, 400, 40, fill='white')
    app.display.value = f"Day: {app.dayCounter}   Action: {app.actionMode.upper()}"
    app.display.left = 10

def calculateScore():
    """
    Count how many plants have reached maximum growth stage.
    """
    score = 0
    for r in range(app.rows):
        for c in range(app.cols):
            cell = app.grid[r][c]
            if cell[0] is not None and cell[1] >= app.maxStages:
                score += 1
    return score

def endGame():
    """
    Display final score and freeze the game.
    """
    app.gameOver = True
    finalScore = calculateScore()
    Rect(0, 0, app.cols*app.cellSize, app.rows*app.cellSize, fill='lightgray', opacity=70)
    Label(f"Good Job! Score: {finalScore}", 120, 150, size=20, fill='blue', bold=True)
    Label("(No more actions possible)", 120, 180, size=16, fill='black')

# ---------------------------------------
# GAME LOGIC
# ---------------------------------------
def handleAction(row, col):
    if app.gameOver:
        return
    if not (0 <= row < app.rows and 0 <= col < app.cols):
        return
    
    cell = app.grid[row][col]
    plantType, stage, hasPests, waterNeeded, fert = cell
    
    if app.actionMode == 'plant':
        if plantType is None:
            # Plant a new seed
            cell[0] = "flower"
            cell[1] = 0
            cell[2] = False
            cell[3] = 2  # water needed
            cell[4] = False
    elif app.actionMode == 'water':
        if plantType is not None:
            cell[3] = max(0, waterNeeded - 1)
    elif app.actionMode == 'fertilize':
        if plantType is not None:
            cell[4] = True
    elif app.actionMode == 'preventPests':
        if plantType is not None:
            cell[2] = False

    updateCellVisual(row, col)

def endOfDayUpdate():
    if app.gameOver:
        return

    app.dayCounter += 1

    # Apply daily logic to each cell
    for r in range(app.rows):
        for c in range(app.cols):
            cell = app.grid[r][c]
            plantType, stage, pests, waterNeeded, fert = cell
            if plantType is not None:
                # If not fully watered, hamper growth
                if waterNeeded > 0:
                    cell[1] = max(0, stage - 1)
                
                # If pests present, hamper growth
                if pests:
                    cell[1] = max(0, cell[1] - 1)
                
                # If fertilized, boost growth
                if fert:
                    cell[1] = min(app.maxStages, cell[1] + 1)
                
                # If no water needed or pests, normal growth
                if waterNeeded == 0 and not pests and not fert:
                    cell[1] = min(app.maxStages, cell[1] + 1)
                
                # Reset daily
                cell[3] = 0  # waterNeeded
                cell[4] = False  # fertilized
            
            updateCellVisual(r, c)

    # Check game end
    if app.dayCounter >= app.maxDays:
        endGame()
    else:
        updateDayDisplay()

# ---------------------------------------
# EVENT HANDLERS
# ---------------------------------------
def onMousePress(x, y):
    if app.gameOver:
        return
    row = y // app.cellSize
    col = x // app.cellSize
    handleAction(row, col)

def onKeyPress(key):
    if app.gameOver:
        return

    if key == 'p':
        app.actionMode = 'plant'
    elif key == 'w':
        app.actionMode = 'water'
    elif key == 'f':
        app.actionMode = 'fertilize'
    elif key == 'x':
        app.actionMode = 'preventPests'
    elif key == 'd':
        endOfDayUpdate()

    updateDayDisplay()

app.tick = 0

# def onStep():
#     # We do a small animation for fully grown plants (stage >= maxStages).
#     # Toggle their opacity every ~10 steps to "pulse."
#     app.tick += 1
#     modVal = app.tick % 20

#     for r in range(app.rows):
#         for c in range(app.cols):
#             cell = app.grid[r][c]
#             if cell[0] is not None and cell[1] >= app.maxStages:
#                 # stage >= maxStages => fade between 70 and 100
#                 targetOpacity = 100 if modVal < 10 else 70
#                 for shapeObj in app.cellPlants[r][c]:
#                     shapeObj.opacity = targetOpacity

onAppStart()
cmu_graphics.run()
