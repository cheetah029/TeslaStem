from cmu_graphics import *
import random
import math

def create_game():
    game = Group()
    
    # Initial game parameters
    game.fish_population = 1000
    game.daily_fish_needed = 50
    game.hunger_level = 0
    game.day = 1
    game.score = 0
    game.caught_fish_today = 0
    game.game_over = False
    
    # Upgrade states
    game.upgrades = {
        'net': 1,  # Fishing efficiency multiplier
        'patrol': 1,  # Illegal fishing prevention
        'bait': 1,  # Catch rate multiplier
    }
    
    # Fish visualization
    game.visible_fish = []
    game.max_visible_fish = 5
    
    # Create UI elements
    game.background = Rect(0, 0, 400, 400, fill='lightBlue')
    game.stats = Group(
        Label('Day: 1', 20, 20, align='left'),
        Label('Fish Population: 1000', 20, 40, align='left'),
        Label('Hunger Level: 0%', 20, 60, align='left'),
        Label('Caught Today: 0/50', 20, 80, align='left')
    )
    
    # Game over screen (initially hidden)
    game_over_overlay = Rect(0, 0, 400, 400, fill=rgb(0, 0, 0), opacity=60)
    game.game_over_screen = Group(
        game_over_overlay,
        Label('GAME OVER', 200, 180, size=30, fill='white'),
        Label('Final Score: 0', 200, 220, fill='white'),
        Label('Press R to restart', 200, 260, fill='white')
    )
    game.game_over_screen.visible = False
    
    return game

def create_fish_colors():
    """Create a random fish color scheme"""
    # Base colors for fish
    base_colors = [
        rgb(255, 128, 0),  # Orange
        rgb(255, 160, 0),  # Light orange
        rgb(255, 215, 0),  # Golden
        rgb(255, 99, 71),  # Tomato red
        rgb(255, 140, 0),  # Dark orange
    ]
    main_color = random.choice(base_colors)
    # Make belly color lighter
    belly_color = rgb(min(255, main_color.red + 40),
                     min(255, main_color.green + 40),
                     min(255, main_color.blue + 40))
    return main_color, belly_color

def spawn_fish():
    """Spawn new visible fish for catching"""
    while len(app.game.visible_fish) < app.game.max_visible_fish:
        x = random.randint(50, 350)
        y = random.randint(50, 350)
        size = random.randint(30, 50)  # Base size
        
        # Create fish shape
        fish_group = Group()
        
        # Random fish colors
        main_color, belly_color = create_fish_colors()
        
        # Main body (more elongated oval)
        fish_body = Oval(0, 0, size * 2, size, fill=main_color)
        
        # Belly (lighter colored underside)
        fish_belly = Oval(0, size/4, size * 1.6, size/2, fill=belly_color)
        
        # Tail (larger triangle shape)
        tail = Polygon(
            -size, 0,          # Center point where tail meets body
            -size * 1.6, -size * 0.5,  # Top point
            -size * 1.6, size * 0.5,   # Bottom point
            fill=main_color
        )
        
        # Bottom fin (positioned underneath)
        bottom_fin_points = [
            size/4, size/3,    # Bottom tip
            size/2, 0,         # Back
            0, 0,              # Front
        ]
        fish_bottom_fin = Polygon(*bottom_fin_points, fill=main_color)
        
        # Eye (slightly repositioned)
        fish_eye = Circle(size/2, -size/6, size/10, fill='white')
        fish_pupil = Circle(size/2, -size/6, size/20, fill='black')
        
        # Add gill detail - using a partial circle border for the curved line
        fish_gill = Circle(size/3, 0, size/2, fill=None, border=main_color, borderWidth=2)
        fish_gill.opacity = 30  # Only show a portion of the circle
        
        # Add all parts to the group in the correct order
        fish_group.add(tail)           # Tail first (behind body)
        fish_group.add(fish_body)      # Body
        fish_group.add(fish_belly)     # Belly detail
        fish_group.add(fish_bottom_fin) # Bottom fin
        fish_group.add(fish_gill)      # Gill detail
        fish_group.add(fish_eye)       # Eye
        fish_group.add(fish_pupil)     # Pupil
        
        # Store size in the body shape for collision detection
        fish_body.fish_size = size
        
        # Only flip horizontally (0 or 360 degrees)
        if random.choice([True, False]):
            fish_group.rotateAngle = 0
        else:
            fish_group.rotateAngle = 360
        
        # Move the fish after setting rotation
        fish_group.centerX = x
        fish_group.centerY = y
        
        app.game.visible_fish.append(fish_group)

def calculate_reproduction():
    """Calculate daily fish population changes"""
    growth_rate = 0.1
    carrying_capacity = 2000
    reproduction = app.game.fish_population * growth_rate * (1 - app.game.fish_population / carrying_capacity)
    app.game.fish_population = max(0, int(app.game.fish_population + reproduction - app.game.caught_fish_today))

def update_hunger():
    """Update community hunger based on caught fish"""
    fish_deficit = max(0, app.game.daily_fish_needed - app.game.caught_fish_today)
    app.game.hunger_level += fish_deficit * 0.1
    if app.game.hunger_level >= 100:
        app.game.game_over = True

def check_game_over():
    """Check if any failure conditions are met"""
    if app.game.fish_population <= 0 or app.game.hunger_level >= 100:
        app.game.game_over = True
        app.game.game_over_screen.visible = True

def try_catch_fish(mouse_x, mouse_y):
    """Attempt to catch a fish at the clicked location"""
    if app.game.game_over:
        return
    
    for fish in app.game.visible_fish[:]:
        # Get the fish body (first child of the group)
        fish_body = fish.children[1]  # Body is now second element after tail
        distance = math.sqrt((fish.centerX - mouse_x)**2 + (fish.centerY - mouse_y)**2)
        if distance < fish_body.fish_size:  # Made hitbox slightly larger
            app.game.caught_fish_today += 1 * app.game.upgrades['net'] * app.game.upgrades['bait']
            app.game.visible_fish.remove(fish)
            fish.visible = False
            return True
    return False

def end_day():
    """Process end of day events"""
    calculate_reproduction()
    update_hunger()
    check_game_over()
    app.game.caught_fish_today = 0
    app.game.day += 1
    app.game.score = app.game.day * (100 - app.game.hunger_level) * (app.game.fish_population / 1000)
    
    # Clean up old fish
    for fish in app.game.visible_fish:
        fish.visible = False
    app.game.visible_fish.clear()
    
    # Update stats display
    update_stats_display()

def update_stats_display():
    """Update the display of game statistics"""
    app.game.stats.children[0].value = f'Day: {app.game.day}'
    app.game.stats.children[1].value = f'Fish Population: {app.game.fish_population}'
    app.game.stats.children[2].value = f'Hunger Level: {int(app.game.hunger_level)}%'
    app.game.stats.children[3].value = f'Caught Today: {app.game.caught_fish_today}/{app.game.daily_fish_needed}'
    
    if app.game.game_over:
        app.game.game_over_screen.children[2].value = f'Final Score: {int(app.game.score)}'

def onAppStart():
    app.game = create_game()
    app.stepsPerSecond = 30

def onStep():
    if not app.game.game_over:
        spawn_fish()
    update_stats_display()

def onMousePress(mouseX, mouseY):
    try_catch_fish(mouseX, mouseY)

def onKeyPress(key):
    if key == 'space':
        end_day()
    elif key == 'r' and app.game.game_over:
        # Remove old game
        app.game.visible = False
        # Create new game
        app.game = create_game()

onAppStart()
cmu_graphics.run()
