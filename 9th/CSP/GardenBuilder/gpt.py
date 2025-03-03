from cmu_graphics import *
import random

def createPlant(row, col):
    """Create a new plant using Group with attributes"""
    plant = Group()
    # Plant attributes
    plant.row = row
    plant.col = col
    plant.type = "flower"
    plant.growth_stage = 0
    plant.has_pests = False
    plant.water_needed = 0  # This will now represent water icons (0-3)
    plant.is_fertilized = False
    plant.days_without_water = 0  # Track consecutive days without water
    plant.germination_days = 0  # Track days as a seed
    return plant

# Plant functions
def waterPlant(plant):
    plant.water_needed = 0  # Remove all water icons
    plant.days_without_water = 0  # Reset days without water

def fertilizePlant(plant):
    plant.is_fertilized = True

def removePests(plant):
    plant.has_pests = False

def addGrowth(plant):
    plant.growth_stage = min(app.maxStages, plant.growth_stage + 1)

def reduceGrowth(plant):
    plant.growth_stage = max(0, plant.growth_stage - 1)

def isFullyGrown(plant):
    return plant.growth_stage >= app.maxStages

def resetDaily(plant):
    """Reset daily attributes and update water status"""
    plant.is_fertilized = False
    plant.days_without_water += 1

    # Update water needs based on days without water
    if plant.days_without_water >= 1:
        plant.water_needed = min(3, plant.days_without_water)

    # Only add pests to plants that have sprouted (growth_stage > 0)
    if plant.growth_stage > 0 and random.randrange(0, 5) == 0:  # 20% chance to get pests each day
        plant.has_pests = True

def plantDies(plant):
    """Remove a plant and clean up its Group object"""
    plant.visible = False  # Hide the Group object
    app.grid[plant.row][plant.col] = None
    clearPlantShapes(plant.row, plant.col)

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

    # Each cell will contain a Plant group or None
    app.grid = []
    app.cellPlants = []
    app.cellBackgrounds = []

    # Game state
    app.dayCounter = 0
    app.actionMode = 'seed'
    app.gameOver = False

    # Display for day and action
    app.display = Label(f"Day: {app.dayCounter}   Action: {app.actionMode.upper()}", 10,
            app.rows * app.cellSize + 10, align='left', size=14, fill='black')

    app.tick = 0
    setupGame()

# ---------------------------------------
# SETUP GAME
# ---------------------------------------
def setupGame():
    for r in range(app.rows):
        rowData = []
        rowPlantShapes = []
        rowBG = []

        for c in range(app.cols):
            rowData.append(None)  # Start with no plant
            
            xPos = c * app.cellSize
            yPos = r * app.cellSize
            bg = Rect(xPos, yPos, app.cellSize, app.cellSize, fill='saddlebrown', border='black', borderWidth=1)
            rowBG.append(bg)
            rowPlantShapes.append([])

        app.grid.append(rowData)
        app.cellPlants.append(rowPlantShapes)
        app.cellBackgrounds.append(rowBG)

    Label("Press s/w/f/x to set action, click cells, press d to end day", 10,
          app.rows * app.cellSize + 40, size=14, fill='black', align='left')
    Label("Goal: After 20 days, grow as many flowers as possible!", 10,
          app.rows * app.cellSize + 60, size=14, fill='black', align='left')

def drawPlant(r, c, stage):
    """
    Draw shapes for a plant at a given growth stage.
    """
    xPos = c * app.cellSize
    yPos = r * app.cellSize
    centerX = xPos + app.cellSize/2
    centerY = yPos + app.cellSize/2

    plant = app.grid[r][c]
    seedColor = 'sienna'
    stemColor = 'lime'
    leafColor = 'lime'
    petalColor = 'pink'
    centerColor = 'yellow'
    witheredColor = 'darkGoldenrod'
    witheredColor2 = 'grey'
    pestColor = 'red'
    waterColor = 'skyBlue'

    # Update colors based on days without water
    if plant.days_without_water >= 2:
        stemColor = witheredColor
        leafColor = witheredColor
    if plant.days_without_water >= 3:
        stemColor = witheredColor2
        leafColor = witheredColor2
    if plant.is_fertilized:
        seedColor = 'black'

    # Stage 0: seed
    if stage == 0:
        seed = Circle(centerX, centerY, 6, fill=seedColor)
        app.cellPlants[r][c].append(seed)

    # Stage 1: small sprout
    elif stage == 1:
        root = Circle(centerX, centerY + 10, 6, fill=seedColor)
        stem = Rect(centerX - 2, centerY - 10, 4, 20, fill=stemColor)
        leafLeft = Oval(centerX - 8, centerY - 10, 16, 8, fill=leafColor)
        leafRight = Oval(centerX + 8, centerY - 10, 16, 8, fill=leafColor)
        app.cellPlants[r][c].extend([root, stem, leafLeft, leafRight])

    # Stage 2: developing plant
    elif stage == 2:
        root = Circle(centerX, centerY + 10, 6, fill=seedColor)
        stem = Rect(centerX - 2, centerY - 20, 4, 30, fill=stemColor)
        leafLeft = Oval(centerX - 8, centerY - 10, 16, 8, fill=leafColor)
        leafRight = Oval(centerX + 8, centerY - 10, 16, 8, fill=leafColor)
        leafTop = Oval(centerX, centerY - 20, 8, 16, fill=leafColor)
        app.cellPlants[r][c].extend([root, stem, leafLeft, leafRight, leafTop])

    # Stage 3: mature plant
    elif stage == 3:
        stem = Rect(centerX - 2, centerY - 20, 4, 35, fill=stemColor)
        leafLeft = Oval(centerX - 8, centerY, 16, 8, fill=leafColor)
        leafRight = Oval(centerX + 8, centerY, 16, 8, fill=leafColor)
        leafLeft2 = Oval(centerX - 8, centerY - 10, 16, 8, fill=leafColor)
        leafRight2 = Oval(centerX + 8, centerY - 10, 16, 8, fill=leafColor)
        leafTop = Oval(centerX, centerY - 20, 8, 16, fill=leafColor)
        app.cellPlants[r][c].extend([stem, leafLeft, leafRight, leafLeft2, leafRight2, leafTop])

    # Stage 4: fully grown flower
    else:
        stem = Rect(centerX - 2, centerY - 15, 4, 30, fill=stemColor)
        leafLeft = Oval(centerX - 8, centerY, 16, 8, fill=leafColor)
        leafRight = Oval(centerX + 8, centerY, 16, 8, fill=leafColor)
        petal1 = Circle(centerX - 5, centerY - 15, 5, fill=petalColor)
        petal2 = Circle(centerX + 5, centerY - 15, 5, fill=petalColor)
        petal3 = Circle(centerX, centerY - 20, 5, fill=petalColor)
        petal4 = Circle(centerX, centerY - 11, 5, fill=petalColor)
        center = Circle(centerX, centerY - 15, 5, fill=centerColor)
        app.cellPlants[r][c].extend([stem, leafLeft, leafRight, petal1, petal2, petal3, petal4, center])

    # Draw indicators
    # Pest indicator in top-right
    if plant.has_pests:
        bug = Circle(xPos + app.cellSize - 10, yPos + 10, 5, fill=pestColor)
        app.cellPlants[r][c].append(bug)
    
    # Water droplets in bottom-right
    if plant.water_needed > 0:
        for i in range(plant.water_needed):
            dropY = yPos + app.cellSize - 10 - (i * 15)  # Start from bottom, go up
            drop = Circle(xPos + app.cellSize - 10, dropY, 5, fill=waterColor)
            dropTop = Circle(xPos + app.cellSize - 10, dropY - 3, 3, fill=waterColor)
            app.cellPlants[r][c].extend([drop, dropTop])

def handleAction(row, col):
    if app.gameOver:
        return
    if not (0 <= row < app.rows and 0 <= col < app.cols):
        return

    plant = app.grid[row][col]

    if app.actionMode == 'seed':
        if plant is None:
            newPlant = createPlant(row, col)
            app.grid[row][col] = newPlant
            updateCellVisual(row, col)
    elif plant is not None:
        if app.actionMode == 'water':
            waterPlant(plant)
        elif app.actionMode == 'fertilize':
            fertilizePlant(plant)
        elif app.actionMode == 'preventPests':
            removePests(plant)
        updateCellVisual(row, col)

def updateCellVisual(r, c):
    clearPlantShapes(r, c)
    plant = app.grid[r][c]
    if plant is not None:
        drawPlant(r, c, plant.growth_stage)

def endOfDayUpdate():
    if app.gameOver:
        return

    app.dayCounter += 1

    for r in range(app.rows):
        for c in range(app.cols):
            plant = app.grid[r][c]
            if plant is not None:
                # Check if plant dies from lack of water
                if plant.days_without_water >= 3:
                    plantDies(plant)
                    continue

                # Handle negative effects (only for sprouted plants)
                if plant.growth_stage > 0 and plant.has_pests:
                    if plant.growth_stage == 1:
                        plantDies(plant)
                        continue
                    else:
                        reduceGrowth(plant)

                # Handle seed germination
                if plant.growth_stage == 0:
                    plant.germination_days += 1
                    if plant.germination_days >= 2:  # Sprout after 2 days
                        if plant.days_without_water == 0:
                            plant.growth_stage = 1
                            plant.germination_days = 0

                # Handle normal growth conditions
                elif plant.days_without_water <= 1 and not plant.has_pests:
                    # Plant grows if not withered and no pests
                    addGrowth(plant)

                # Handle fertilizer bonus (can still grow even if withered)
                if plant.is_fertilized:
                    addGrowth(plant)

                resetDaily(plant)
                updateCellVisual(r, c)

    if app.dayCounter >= app.maxDays:
        endGame()
    else:
        updateDayDisplay()

def calculateScore():
    score = 0
    for r in range(app.rows):
        for c in range(app.cols):
            plant = app.grid[r][c]
            if plant is not None and isFullyGrown(plant):
                score += 1
    return score

# Keep existing helper functions and event handlers
def clearPlantShapes(r, c):
    for shape in app.cellPlants[r][c]:
        shape.visible = False
    app.cellPlants[r][c].clear()

def updateDayDisplay():
    app.display.value = f"Day: {app.dayCounter}   Action: {app.actionMode.upper()}"
    app.display.left = 10

def endGame():
    app.gameOver = True
    finalScore = calculateScore()
    Rect(0, 0, app.cols*app.cellSize, app.rows*app.cellSize, fill='lightgray', opacity=70)
    Label(f"Good Job! Score: {finalScore}", 120, 150, size=20, fill='blue', bold=True)
    Label("(No more actions possible)", 120, 180, size=16, fill='black')

def onMousePress(x, y):
    if app.gameOver:
        return
    row = y // app.cellSize
    col = x // app.cellSize
    handleAction(row, col)

def onKeyPress(key):
    if app.gameOver:
        return

    if key == 's':
        app.actionMode = 'seed'
    elif key == 'w':
        app.actionMode = 'water'
    elif key == 'f':
        app.actionMode = 'fertilize'
    elif key == 'x':
        app.actionMode = 'preventPests'
    elif key == 'd':
        endOfDayUpdate()

    updateDayDisplay()

onAppStart()
cmu_graphics.run()
