# I have read the Create Task sections of the AP Exam Student Handout.
# This project relates to UN SDG #12: Responsible Consumption and Production

# Waste Sorting Game

# This game is a simple waste-sorting game where the player must sort waste into the correct bins.
# The player can drag waste items into the correct bins, and they will receive points for each correct item.
# They will lose points for every item placed incorrectly.
# The player tries to achieve the highest score by sorting as many items correctly as possible within 60 seconds.

import random
from cmu_graphics import *

app.background = 'lightSkyBlue'
app.stepsPerSecond = 30

# Game states: 'countdown', 'running', 'gameOver'
app.mode = 'countdown'

# Countdown and main timer
app.countdownSteps = 5 * app.stepsPerSecond   # Total countdown time including text: Get Ready, 3, 2, 1, Go
app.gameTimeSteps = 60 * app.stepsPerSecond   # 60 seconds main timer, total steps

# Score
app.score = 0

# Title text
title = Label('Drag waste items into the correct bins!', 200, 35, size=20)
countdown = Label('Get Ready!', 200, 75, size=30, fill='red')
score = Label('Score: 0', 340, 75, size=20)

# For showing quick error explanation on incorrect sort
errorBox = Rect(50, 220, 300, 30, fill='white', border='red', opacity=80)
errorLabel = Label('', 200, 235, size=12, fill='red')
app.errorMessageTimer = 0 # Countdown to remove error message

errorMessage = Group(errorBox, errorLabel)
errorMessage.visible = False

gameOverBox = Rect(80, 125, 240, 150, fill='aliceBlue', border='blue', borderWidth=4)
gameOverLabel = Label('Time\'s Up! Good job!', 200, 150, size=20, fill='blue')
gameOverScoreLabel = Label('Your Final Score Is: 0', 200, 200, size=20, fill='blue')
gameOverMessage = Group(gameOverBox, gameOverLabel, gameOverScoreLabel)
gameOverMessage.visible = False

# Lists of item names
compostNames = [
    'Banana Peel', 'Eggshell', 'Apple Core', 'Stale Bread',
    'Orange Peel', 'Corn Husk', 'Tomato'
]
recyclingNames = [
    'Aluminum Can', 'Plastic Bottle', 'Cardboard Box',
    'Newspaper', 'Magazine', 'Milk Carton', 'Egg Carton'
]
trashNames = [
    'Chip Bag', 'Aluminum Foil', 'Styrofoam Cup',
    'Plastic Utensils', 'Plastic Wrap', 'Batteries', 'Candy Wrapper'
]

# Draw waste bins
compostBin = Rect(50, 300, 80, 80, fill='green')
compostBinLabel = Label("Compost", 90, 340, size=15, fill='white')

recyclingBin = Rect(160, 300, 80, 80, fill='blue')
recyclingBinLabel = Label("Recycle", 200, 340, size=15, fill='white')

trashBin = Rect(270, 300, 80, 80, fill='grey')
trashBinLabel = Label("Trash", 310, 340, size=15, fill='white')

wasteBins = [compostBin, recyclingBin, trashBin]

# Draw placeholders for waste items
placeholders = [
    Circle(90, 150, 22, fill='deepSkyBlue'),
    Circle(200, 150, 22, fill='deepSkyBlue'),
    Circle(310, 150, 22, fill='deepSkyBlue')
]

# Initialize attribute 'selected' for placeholders
for placeholder in placeholders:
    placeholder.selected = False
    placeholder.currentItem = None

currentItems = [None for placeholder in placeholders]
app.lastItem = None

def updateScore(change, errorText=None):
    if app.score + change < 0: # The score should never go below 0
        change = -app.score    # If the score would go below 0, edit the change variable to make it 0

    app.score += change

    # Update the score label
    score.value = f"Score: {app.score}"

    if errorText:
        if change == 0: # Display change before errorText if it is not 0
            errorLabel.value = errorText
        else:
            errorLabel.value = f'{change} {errorText}'

        errorMessage.visible = True
        app.errorMessageTimer = 4 * app.stepsPerSecond # Display error message for 4 seconds

def onStep():
    if app.mode == 'countdown':
        app.countdownSteps -= 1

        if app.countdownSteps >= 4 * app.stepsPerSecond: # Get Ready phase
            countdown.value = 'Get Ready!'
        elif app.countdownSteps > app.stepsPerSecond: # Countdown 3 2 1 phase
            countdown.value = app.countdownSteps // app.stepsPerSecond
        elif app.countdownSteps > 0: # 'GO!' phase
            countdown.value = 'GO!'
        else:
            app.mode = 'running' # Finished countdown mode
    else:
        if app.gameTimeSteps > 0:
            app.gameTimeSteps -= 1
            countdown.value = f'{app.gameTimeSteps // app.stepsPerSecond}s'
        else:
            gameOverScoreLabel.value = f'Your Final Score Is: {app.score}'
            gameOverMessage.visible = True
            gameOverMessage.toFront()
            app.mode = 'gameOver'

        if app.errorMessageTimer > 0:
            app.errorMessageTimer -= 1
        else:
            errorMessage.visible = False

        for i in range(len(currentItems)):
            if currentItems[i] == None:
                currentItem = random.choice(allItems)

                while currentItem in currentItems or currentItem == app.lastItem:
                    currentItem = random.choice(allItems)

                currentItems[i] = currentItem
                placeholder = placeholders[i]
                currentItem.placeholder = placeholder
                placeholder.currentItem = currentItem
                currentItem.centerX = placeholder.centerX
                currentItem.visible = True

def onMousePress(mouseX, mouseY):
    if app.mode == 'running' and None not in currentItems:
        for placeholder in placeholders:
            if placeholder.hits(mouseX, mouseY):
                placeholder.selected = True
                placeholder.currentItem.selected = True
                placeholder.fill = 'yellow'
            else:
                binIsClicked = False

                for wasteBin in wasteBins:
                    if wasteBin.hits(mouseX, mouseY):
                        binIsClicked = True

                if not binIsClicked:
                    placeholder.selected = False
                    placeholder.currentItem.selected = False
                    placeholder.fill = 'deepSkyBlue'

def onMouseRelease(mouseX, mouseY):
    if app.mode == 'running' and None not in currentItems:
        for i in range(len(wasteBins)):
            if wasteBins[i].hits(mouseX, mouseY):
                for j in range(len(placeholders)):
                    if placeholders[j].selected:
                        # Check if the selected item's category matches the correct bin
                        if currentItems[j].category == wasteBins[i].name:
                            updateScore(1)
                        else:
                            updateScore(-1, f'Incorrect! {currentItems[j].name} goes in the {currentItems[j].category}.')

                        # Reset the placeholder selection
                        placeholders[j].selected = False
                        placeholders[j].currentItem.selected = False
                        placeholders[j].fill = 'deepSkyBlue'

                        # Remove the deposited item from the placeholder and store it as the last item
                        app.lastItem = currentItems[j]
                        placeholders[j].currentItem.visible = False
                        placeholders[j].currentItem = None
                        currentItems[j] = None

                        break
                break

# Define icon shapes of waste items
cx = placeholders[0].centerX
cy = placeholders[0].centerY

bananaPeel = Group(
    Arc(cx - 8, cy, 20, 20, 0, 180, fill='gold', border='darkGoldenrod'),
    Arc(cx + 8, cy, 20, 20, 0, 180, fill='gold', border='darkGoldenrod'),
    Polygon(cx - 5, cy, cx, cy - 8, cx + 5, cy, fill='gold', border='darkGoldenrod'),
    Label('Banana Peel', cx, cy + 22, size=10)
    )

eggshell = Group(
    Oval(cx, cy + 5, 24, 16, fill='beige', border='dimgrey'),
    Line(cx - 12, cy, cx - 6, cy - 4, fill='dimGrey', lineWidth=1),
    Line(cx - 6, cy - 4, cx, cy, fill='dimGrey', lineWidth=1),
    Line(cx, cy, cx + 6, cy - 4, fill='dimGrey', lineWidth=1),
    Line(cx + 6, cy - 4, cx + 12, cy, fill='dimGrey', lineWidth=1),
    Oval(cx, cy - 8, 14, 8, fill='beige', border='dimGrey'),
    Label('Eggshell', cx, cy + 25, size=10)
    )

appleCore = Group(
    Arc(cx, cy - 8, 16, 16, -90, 180, fill='red'),
    Arc(cx, cy + 8, 16, 16, 90, 180, fill='red'),
    Rect(cx - 4, cy - 8, 8, 16, fill='ivory', border='red'),
    Circle(cx, cy, 1, fill='black'),
    Circle(cx - 2, cy + 2, 1, fill='black'),
    Label('Apple Core', cx, cy + 26, size=10)
    )

staleBread = Group(
    Polygon(cx - 15, cy, cx - 12, cy - 12, cx + 12, cy - 12, 
                         cx + 15, cy, cx + 12, cy + 12, cx - 12, cy + 12,
                         fill='burlyWood', border='peru'),
    Circle(cx - 12, cy - 12, 3, fill='peru'),
    Circle(cx + 12, cy - 12, 3, fill='peru'),
    Circle(cx - 12, cy + 12, 3, fill='peru'),
    Circle(cx + 12, cy + 12, 3, fill='peru'),
    Label('Stale Bread', cx, cy + 26, size=10)
    )

orangePeel = Group(
    Circle(cx, cy, 10, fill='orange'),
    Arc(cx - 5, cy, 10, 20, 90, 270, fill='darkOrange', border='chocolate'),
    Arc(cx + 5, cy, 10, 20, -90, 90, fill='darkOrange', border='chocolate'),
    Label('Orange Peel', cx, cy + 22, size=10),
    )

cornHusk = Group(
    Rect(cx - 3, cy - 13, 10, 20, fill='gold', border='black', rotateAngle=45),
    Circle(cx + 4, cy - 6, 1, fill='saddleBrown'),
    Circle(cx, cy - 3, 1, fill='saddleBrown'),
    Circle(cx + 4, cy - 3, 1, fill='saddleBrown'),
    Circle(cx - 4, cy, 1, fill='saddleBrown'),
    Circle(cx, cy, 1, fill='saddleBrown'),
    Circle(cx, cy + 3, 1, fill='saddleBrown'),
    Arc(cx - 4, cy + 3, 20, 20, 90, 270, fill='limeGreen', border='green'),
    Label('Corn Husk', cx, cy + 22, size=10)
    )

tomato = Group(
    Circle(cx, cy, 12, fill='red'),
    Line(cx, cy - 5, cx - 7, cy - 12, fill='green'),
    Line(cx, cy - 5, cx, cy - 15, fill='green'),
    Line(cx, cy - 5, cx + 7, cy - 12, fill='green'),
    Label('Tomato', cx, cy + 20, size=10)
    )

### --- RECYCLING ITEMS --- ###

aluminumCan = Group(
    Rect(cx - 5, cy - 12, 10, 24, fill='silver'),
    Oval(cx, cy - 12, 10, 4, fill='gainsboro', border='grey'),
    Oval(cx, cy + 12, 10, 4, fill='silver', border='grey'),
    Label('Aluminum Can', cx, cy + 26, size=10)
    )

plasticBottle = Group(
    Rect(cx - 5, cy - 10, 10, 20, fill='skyBlue', border='blue'),
    Rect(cx - 2, cy - 12, 4, 2, fill='skyBlue'),
    Rect(cx - 2, cy - 16, 4, 4, fill='blue'),
    Line(cx - 2, cy - 10, cx - 2, cy + 10, fill='white', opacity=40),
    Label('Plastic Bottle', cx, cy + 30, size=10)
    )

cardboardBox = Group(
    Rect(cx - 10, cy, 20, 10, fill='tan', border='saddleBrown'),
    Polygon(cx - 10, cy, cx - 14, cy - 6, cx + 6, cy - 6, cx + 10, cy,
                      fill='burlywood', border='saddleBrown'),
    Polygon(cx - 10, cy, cx - 14, cy - 6, cx - 14, cy + 4, cx - 10, cy + 10,
                       fill='wheat', border='saddleBrown'),
    Polygon(cx + 10, cy, cx + 14, cy - 6, cx + 14, cy + 4, cx + 10, cy + 10,
                        fill='wheat', border='saddleBrown'),
    Label('Cardboard Box', cx, cy + 25, size=10)
    )

newspaper = Group(
    Rect(cx - 15, cy - 8, 30, 16, fill='white', border='black'),
    Line(cx - 13, cy - 4, cx + 13, cy - 4, fill='darkGrey'),
    Line(cx - 13, cy, cx + 13, cy, fill='darkGrey'),
    Line(cx - 13, cy + 4, cx + 13, cy + 4, fill='darkGrey'),
    Polygon(cx + 15, cy - 8, cx + 10, cy - 8, cx + 10, cy - 2, fill='lightGrey'),
    Label('Newspaper', cx, cy + 25, size=10)
    )

magazine = Group(
    Rect(cx - 15, cy - 8, 30, 16, fill='lightPink', border='black'),
    Rect(cx - 15, cy - 8, 30, 4, fill='hotPink'),
    Line(cx - 13, cy - 2, cx + 13, cy - 2, fill='darkGrey'),
    Line(cx - 13, cy + 2, cx + 13, cy + 2, fill='darkGrey'),
    Line(cx - 13, cy + 6, cx + 13, cy + 6, fill='darkGrey'),
    Label('Magazine', cx, cy + 25, size=10)
    )

milkCarton = Group(
    Rect(cx - 8, cy - 10, 16, 20, fill='white', border='black'),
    Polygon(cx - 8, cy - 10, cx, cy - 18, cx + 8, cy - 10,
                  fill='lightskyBlue', border='blue'),
    Line(cx, cy - 18, cx, cy - 10, fill='blue'),
    Label('Milk Carton', cx, cy + 25, size=10)
    )

eggCarton = Group()
eggCarton.add(Rect(cx - 15, cy - 5, 30, 10, fill='lightGrey', border='dimGrey'))
for i in range(-10, 11, 5):
    eggCarton.add(Circle(cx + i, cy - 5, 4, fill='silver'))
eggCarton.add(Label('Egg Carton', cx, cy + 20, size=10))

### --- TRASH ITEMS --- ###

chipBag = Group(
    Polygon(cx - 10, cy - 12, cx - 12, cy - 8, cx - 8, cy,
                  cx - 10, cy + 8, cx - 8, cy + 12, cx + 8, cy + 12,
                  cx + 10, cy + 8, cx + 8, cy, cx + 12, cy - 8,
                  cx + 10, cy - 12,
                  fill='orangeRed', border='darkRed'),
    Label('Chip Bag', cx, cy + 20, size=10)
    )

aluminumFoil = Group(
    Polygon(cx - 15, cy - 5, cx, cy - 10, cx + 15, cy - 5,
           cx + 10, cy + 5, cx - 10, cy + 5,
           fill='silver', border='grey'),
    Line(cx - 5, cy - 5, cx - 2, cy, fill='darkGrey'),
    Line(cx + 5, cy - 5, cx + 2, cy, fill='darkGrey'),
    Label('Aluminum Foil', cx, cy + 20, size=10)
    )

styrofoamCup = Group(
    Polygon(cx - 7, cy - 10, cx + 7, cy - 10, cx + 5, cy + 10, cx - 5, cy + 10,
                      fill='white', border='lightGrey'),
    Oval(cx, cy - 10, 14, 4, fill='lightGrey'),
    Label('Styrofoam Cup', cx, cy + 24, size=10)
    )

plasticUtensils = Group(
    Rect(cx - 1.5, cy - 12, 3, 24, fill='lightGrey'),
    Circle(cx, cy - 10, 4.5, fill='lightGrey'),
    Rect(cx - 12, cy - 1.5, 24, 3, fill='lightGrey'),
    Rect(cx + 7, cy - 4, 8, 2, fill='lightGrey'),
    Rect(cx + 6, cy - 2, 8, 2, fill='lightGrey'),
    Rect(cx + 6, cy, 8, 2, fill='lightGrey'),
    Rect(cx + 7, cy + 2, 8, 2, fill='lightGrey')
    )
plasticUtensils.rotateAngle = -45
plasticUtensils.centerX = cx
plasticUtensils.add(Label('Plastic Utensils', cx, cy + 20, size=10))

plasticWrap = Group(
    Polygon(cx - 12, cy - 6, cx + 12, cy - 6, cx + 10, cy + 6, cx - 14, cy + 6,
                        fill='lightBlue', opacity=30, border='lightCyan'),
    Line(cx - 8, cy, cx + 8, cy, fill='white', dashes=True, opacity=50),
    Label('Plastic Wrap', cx, cy + 20, size=10)
    )

batteries = Group(
    Rect(cx - 10, cy - 15, 20, 10, fill='chocolate'),
    Circle(cx - 10, cy - 10, 5, fill='orange'),
    Circle(cx + 10, cy - 10, 5, fill='fireBrick'),
    Line(cx - 13, cy - 10, cx - 7, cy - 10, lineWidth=1),
    Line(cx - 10, cy - 13, cx - 10, cy - 7, lineWidth=1),
    Rect(cx - 10, cy, 20, 10, fill='chocolate'),
    Circle(cx - 10, cy + 5, 5, fill='orange'),
    Circle(cx + 10, cy + 5, 5, fill='fireBrick'),
    Line(cx - 13, cy + 5, cx - 7, cy + 5, lineWidth=1),
    Label('Batteries', cx, cy + 18, size=10)
    )

candyWrapper = Group(
    Rect(cx - 8, cy - 5, 16, 10, fill='hotPink'),
    Polygon(cx - 8, cy - 5, cx - 12, cy - 8, cx - 12, cy + 8, cx - 8, cy + 5, fill='pink'),
    Polygon(cx + 8, cy - 5, cx + 12, cy - 8, cx + 12, cy + 8, cx + 8, cy + 5, fill='pink'),
    Label('Candy Wrapper', cx, cy + 20, size=10)
    )

compostItems = [
    bananaPeel,
    eggshell,
    appleCore,
    staleBread,
    orangePeel,
    cornHusk,
    tomato
]

recyclingItems = [
    aluminumCan,
    plasticBottle,
    cardboardBox,
    newspaper,
    magazine,
    milkCarton,
    eggCarton
]

trashItems = [
    chipBag,
    aluminumFoil,
    styrofoamCup,
    plasticUtensils,
    plasticWrap,
    batteries,
    candyWrapper
]

compostBin.name = 'Compost'
recyclingBin.name = 'Recycling'
trashBin.name = 'Trash'
compostBin.items = compostItems
recyclingBin.items = recyclingItems
trashBin.items = trashItems

allItems = []

for i in range(len(compostItems)):
    item = compostItems[i]
    item.visible = False
    allItems.append(item)
    item.name = compostNames[i]
    item.category = 'Compost'
for i in range(len(recyclingItems)):
    item = recyclingItems[i]
    item.visible = False
    allItems.append(item)
    item.name = recyclingNames[i]
    item.category = 'Recycling'
for i in range(len(trashItems)):
    item = trashItems[i]
    item.visible = False
    allItems.append(item)
    item.name = trashNames[i]
    item.category = 'Trash'

cmu_graphics.run()
