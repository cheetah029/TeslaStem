# Community Water Consumption Tracker
# Using cmu_graphics for animation

from cmu_graphics import *

# Global variables for demonstration:
usageList = [50, 65, 85, 120, 40]  # A sample list of daily usage
bars = []                          # Will hold shape references for each bar
finalHeights = []                 # Target bar heights
animationSpeed = 2                # Speed at which bars grow

def analyzeConsumption(usageData, threshold):
    """
    Analyzes daily water usage.
    Returns (averageUsage, countExceedThreshold).
    
    usageData: list of numeric usage values
    threshold: numeric threshold
    """
    total = 0
    countExceed = 0
    
    # ITERATION + SELECTION
    for usage in usageData:
        total += usage
        if usage > threshold:
            countExceed += 1
    
    averageUsage = total / len(usageData) if len(usageData) > 0 else 0
    return (averageUsage, countExceed)

# We do two function calls with different thresholds:
avg1, exceed1 = analyzeConsumption(usageList, 80)
avg2, exceed2 = analyzeConsumption(usageList, 100)

print(f"Threshold=80 -> Average={avg1}, Days Exceeding={exceed1}")
print(f"Threshold=100 -> Average={avg2}, Days Exceeding={exceed2}")

# --- Setup the bar shapes for animation ---
def setupBars():
    """
    Creates Rect shapes for each day's usage
    and saves their target heights in finalHeights.
    """
    barWidth = 30
    gap = 10
    startX = 50
    groundY = 300  # y-position from which bars will grow downward
    
    for i, usage in enumerate(usageList):
        # For example, usage is scaled so that usage=1 -> 1 pixel
        barHeight = usage
        x = startX + i*(barWidth + gap)
        
        # Create the bar at height=0 initially
        bar = Rect(x, groundY, barWidth, 0, fill='blue')
        bars.append(bar)
        
        # Store the final height we want to reach
        finalHeights.append(barHeight)

# --- Animate the bars in onStep ---
def onStep():
    """
    Gradually increase each bar's height until it reaches the target finalHeights.
    If a bar's usage is above a certain threshold (like 80), color it differently.
    """
    # We'll pick one threshold for the color difference
    thresholdForColor = 80
    
    for i in range(len(bars)):
        bar = bars[i]
        target = finalHeights[i]
        
        # If current height is less than target, grow the bar
        if bar.height < target:
            bar.height += animationSpeed
            
            # Keep the bar anchored at the bottom by adjusting its y
            bar.y -= animationSpeed
        
        # SELECTION to color bars
        usageValue = target  # same as finalHeights[i]
        if usageValue > thresholdForColor:
            bar.fill = 'tomato'
        else:
            bar.fill = 'dodgerBlue'

# Optionally, let the user add new usage data via key presses
# Just a minimal example of "user input" in CMU Graphics:
newUsage = 0

def onKeyPress(key):
    global newUsage
    
    # If user types a digit, build a number
    if key.isdigit():
        newUsage = newUsage*10 + int(key)  # build the number
    elif key == 'enter':
        # When Enter is pressed, add the new usage to the usageList
        usageList.append(newUsage)
        # Also create a new bar for it
        addNewBar(newUsage)
        print(f"User added usage: {newUsage}")
        newUsage = 0  # reset

def addNewBar(usage):
    """
    Adds a new bar shape at the right side of the chart for an added usage value.
    """
    previousBarCount = len(bars)
    barWidth = 30
    gap = 10
    groundY = 300
    x = 50 + previousBarCount*(barWidth+gap)
    
    bar = Rect(x, groundY, barWidth, 0, fill='blue')
    bars.append(bar)
    finalHeights.append(usage)

# Run the setup once at the start
setupBars()

cmu_graphics.run()
