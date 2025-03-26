# This project relates to UN SDG 14: Life Below Water.
# The project is a fishing simulation game that allows players to experience the challenges of fishing sustainably in a polluted environment.
# The game encourages players to think about the impact of their actions on the environment and the importance of sustainable fishing practices.

# The game is a simple fishing game where the player must catch fish to feed the community.
# The player can catch and deposit fish into the bucket, and they can catch a maximum of 5 fish per day.
# The player needs to catch enough fish to feed the community, while refraining from catching too many fish and depleting the fish population.
# Trash and pollution occasionally float by in the water, which reduce the fish population and reproduction rate.
# The player can click on trash items to remove them, which will decrease the pollution level and restore the fish population growth rate.
# The player will lose the game if the community runs out of food, the fish have all gone extinct, or if the water becomes too polluted.
# The player tries to meet the community's daily food needs while sustaining a healthy fish population for 20 days.

from cmu_graphics import *
import random
import math

def create_game():
    game = Group()

    # Initial game parameters
    game.fish_population = 30
    game.food_decrease_base = 50
    game.food_level = 100
    game.day = 1
    game.target_days = 20
    game.game_over = False
    game.time = 0
    game.caught_fish_today = 0
    game.caught_fish_sizes = []

    # Mouse position tracking
    game.mouse_x = 200
    game.mouse_y = 200
    game.dragged_fish = None

    # Bucket dimensions and position
    game.bucket_height = 40
    game.bucket_top_width = 40
    game.bucket_bottom_width = 25
    game.bucket_x = 350
    game.bucket_y = 120

    # Trash and fish visualization
    game.trash = Group()
    game.trash_timer = 0
    game.pollution_level = 0
    game.visible_fish = []
    game.max_visible_fish = 3

    # Create UI elements
    game.background = Group()

    # Sky and water
    sky = Rect(0, 0, 400, 400, fill='skyBlue')
    water = Rect(0, 180, 400, 220, fill=rgb(0, 105, 148))

    # Land/Dock
    land = Rect(0, 130, 400, 50, fill=rgb(139, 69, 19))
    land_detail = Rect(0, 130, 400, 10, fill=rgb(101, 67, 33))

    # Dock posts
    for x in [50, 150, 250]:
        post = Rect(x, 130, 10, 70, fill=rgb(101, 67, 33))
        game.background.add(post)

    # Add background elements
    game.background.add(sky)
    game.background.add(water)
    game.background.add(land)
    game.background.add(land_detail)
    game.background.add(game.trash)

    # Create bucket
    game.bucket = Group()

    # Trapezoid body
    bucket_body = Polygon(
        game.bucket_x - game.bucket_top_width/2, game.bucket_y,
        game.bucket_x + game.bucket_top_width/2, game.bucket_y,
        game.bucket_x + game.bucket_bottom_width/2, game.bucket_y + game.bucket_height,
        game.bucket_x - game.bucket_bottom_width/2, game.bucket_y + game.bucket_height,
        fill='silver'
    )

    # Handle and rim
    handle_radius = 20
    bucket_handle = Arc(game.bucket_x, game.bucket_y, handle_radius * 2, handle_radius * 2, 
                       -90, 180, fill=None, border='silver', borderWidth=2)
    bucket_rim = Oval(game.bucket_x, game.bucket_y, game.bucket_top_width, 10, fill=rgb(130, 130, 130))
    bucket_counter = Label('0/5', game.bucket_x, game.bucket_y + 20, size=14, bold=True)

    game.bucket.add(bucket_body)
    game.bucket.add(bucket_handle)
    game.bucket.add(bucket_rim)
    game.bucket.add(bucket_counter)

    # Create hunger bar
    game.hunger_bar = Group()
    bar_width = 100
    bar_height = 15
    bar_x = 120
    bar_y = 53

    # Background
    bar_bg = Rect(bar_x, bar_y, bar_width, bar_height, fill='darkGray')
    bar_border = Rect(bar_x, bar_y, bar_width, bar_height, 
                     fill=None, border='black', borderWidth=2)

    # Inner bar
    bar_fill = Rect(bar_x + 1, bar_y + 1, bar_width - 2, bar_height - 2, 
                    fill=rgb(50, 205, 50))

    # Add shine effect
    shine = Polygon(
        bar_x + 1, bar_y + 1,
        bar_x + bar_width - 1, bar_y + 1,
        bar_x + bar_width - 1, bar_y + 4,
        bar_x + 1, bar_y + 4,
        fill=rgb(255, 255, 255), opacity=20
    )

    game.hunger_bar.add(bar_bg)
    game.hunger_bar.add(bar_fill)
    game.hunger_bar.add(shine)
    game.hunger_bar.add(bar_border)

    # Create fishing rod
    game.rod = Group()

    # Rod handle and grip
    handle = Line(0, 100, 80, 100, fill=rgb(139, 69, 19), lineWidth=8)
    handle_grip = Line(-70, 100, 30, 100, fill=rgb(101, 67, 33), lineWidth=10)

    # Rod body
    rod_color = rgb(160, 82, 45)
    rod_sections = []
    curve_points = [(80, 100), (120, 110), (160, 130), (180, 140)]
    for i in range(len(curve_points)-1):
        section = Line(curve_points[i][0], curve_points[i][1],
                      curve_points[i+1][0], curve_points[i+1][1],
                      fill=rod_color, lineWidth=4-i*0.8)
        rod_sections.append(section)

    # Rod guides
    for x, y in [(100, 105), (130, 120), (160, 135)]:
        guide = Circle(x, y, 3, fill=None, border='silver', borderWidth=1)
        game.rod.add(guide)

    # Add all rod parts
    game.rod.add(handle)
    game.rod.add(handle_grip)
    for section in rod_sections:
        game.rod.add(section)
    game.rod.rotateAngle = -35
    game.rod.centerY = 150

    # Create fishing line with hook
    game.line = Group()
    rod_tip = rod_sections[-1]
    main_line = Line(rod_tip.x2, rod_tip.y2, rod_tip.x2, rod_tip.y2, fill='white', opacity=50, lineWidth=1)

    # Create hook
    hook_size = 6
    hook_group = Group()

    # Vertical line
    hook_line = Line(0, 0, 0, hook_size * 2, fill='black', lineWidth=2)

    # Curved hook
    curve_points = []
    segments = 12
    for i in range(segments + 1):
        angle = math.pi * i / segments
        x = hook_size * math.cos(angle)
        y = hook_size * 2 + hook_size * math.sin(angle)
        if i == 0:
            x = 0
            y = hook_size * 2
        curve_points.append((x, y))

    # Create smooth curve
    for i in range(len(curve_points) - 1):
        segment = Line(curve_points[i][0], curve_points[i][1],
                      curve_points[i+1][0], curve_points[i+1][1],
                      fill='black', lineWidth=2)
        hook_group.add(segment)

    hook_group.add(hook_line)
    hook_group.rotateAngle = 180

    game.line.add(main_line)
    game.line.add(hook_group)

    # Instructions
    game.instructions = Group(
        Label('Sustainable Fishing Simulator', 200, 16, size=16, bold=True),
        Label('Use the fishing rod to catch fish', 200, 350, size=14),
        Label('Press D to end the day', 200, 370, size=14),
        Label('Catch enough fish to feed the community, but don\'t overfish!', 200, 390, size=14)
    )

    # Stats display
    game.stats = Group()
    game.stats.left_position = 15

    game.stats.add(
        Label('Day: 1', game.stats.left_position, 20),
        Label('Fish Population: 30', game.stats.left_position, 40),
        Label('Food Level: 100%', game.stats.left_position, 60),
        Label('Caught Today: 0/5', game.stats.left_position, 80)
    )

    # Game over screen
    game_over_overlay = Rect(0, 0, 400, 400, fill=rgb(0, 0, 0), opacity=60)
    game.game_over_screen = Group(
        game_over_overlay,
        Label('GAME OVER', 200, 180, size=30, fill='white'),
        Label('', 200, 220, fill='white'),
        Label('', 200, 240, fill='white'),
        Label('Press R to restart', 200, 280, fill='white')
    )
    game.game_over_screen.visible = False
    game.game_over_screen.toFront()

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
    # Adjust max visible fish based on population
    # At 30 fish: 3 fish on screen
    # At 20 fish: 2 fish on screen
    # At 10 fish: 1 fish on screen
    app.game.max_visible_fish = max(1, min(3, int(1 + app.game.fish_population / 10)))

    # Adjust spawn rate based on population
    # Lower population = lower spawn rate
    spawn_chance = max(0.2, min(1.0, app.game.fish_population / 30))

    while len(app.game.visible_fish) < app.game.max_visible_fish:
        # Only spawn if random check passes
        if random.random() > spawn_chance:
            continue

        # Spawn fish on either side of the screen
        side = random.choice(['left', 'right'])
        x = -50 if side == 'left' else 450  # Start off-screen
        y = random.randint(200, 350)  # Only spawn in water area
        # Generate size on 1-10 scale, then convert to visual size (30-50)
        size_scale = random.randint(1, 10)
        size = 30 + (size_scale - 1) * 2.2  # Convert 1-10 to 30-50 range
        
        # Create fish shape
        fish_group = Group()
        fish_group.dragged = False  # Add dragged property

        # Random fish colors
        main_color, belly_color = create_fish_colors()

        # Set direction based on spawn side (reversed from before)
        # If spawning on left, move right (direction = 1)
        # If spawning on right, move left (direction = -1)
        fish_group.direction = -1 if side == 'right' else 1

        # Create fish components with x-coordinates flipped if swimming left
        # Fish spawning on left (moving right) have normal orientation (x_multiplier = 1)
        # Fish spawning on right (moving left) have flipped orientation (x_multiplier = -1)
        x_multiplier = -1 if side == 'right' else 1

        # Main body (more elongated oval)
        fish_body = Oval(0, 0, size * 2, size, fill=main_color)

        # Belly (lighter colored underside)
        fish_belly = Oval(0, size/4, size * 1.6, size/2, fill=belly_color)

        # Tail (larger triangle shape)
        tail = Polygon(
            -size * x_multiplier, 0,                  # Center point where tail meets body
            -size * 1.6 * x_multiplier, -size * 0.5,  # Top point
            -size * 1.6 * x_multiplier, size * 0.5,   # Bottom point
            fill=main_color
        )

        # Bottom fin (positioned underneath)
        bottom_fin_points = [
            size/4 * x_multiplier, size/3,    # Bottom tip
            size/2 * x_multiplier, 0,         # Back
            0, 0,                             # Front
        ]
        fish_bottom_fin = Polygon(*bottom_fin_points, fill=main_color)

        # Eye (slightly repositioned)
        fish_eye = Circle(size/2 * x_multiplier, -size/6, size/10, fill='white')
        fish_pupil = Circle(size/2 * x_multiplier, -size/6, size/20, fill='black')

        # Add gill detail - using a partial circle border for the curved line
        fish_gill = Circle(size/3 * x_multiplier, 0, size/2, fill=None, border=main_color, borderWidth=2)
        fish_gill.opacity = 30  # Only show a portion of the circle

        # Add all parts to the group in the correct order
        fish_group.add(tail)           # Tail first (behind body)
        fish_group.add(fish_body)      # Body
        fish_group.add(fish_belly)     # Belly detail
        fish_group.add(fish_bottom_fin) # Bottom fin
        fish_group.add(fish_gill)      # Gill detail
        fish_group.add(fish_eye)       # Eye
        fish_group.add(fish_pupil)     # Pupil

        # Store both visual size and scale size for different purposes
        fish_body.fish_size = size  # For collision detection
        fish_body.size_scale = size_scale  # For display and calculations

        # Set speed and position
        fish_group.speed = random.uniform(1, 2)  # Random speed for variety
        fish_group.centerX = x
        fish_group.centerY = y

        # Add some vertical movement
        fish_group.vertical_offset = random.uniform(0, 2*math.pi)  # Random starting phase
        fish_group.vertical_speed = random.uniform(0.02, 0.04)  # Random speed for vertical motion

        app.game.visible_fish.append(fish_group)

def calculate_reproduction():
    """Calculate daily fish population changes"""
    base_growth_rate = 0.15  # Keep 15% base growth rate
    carrying_capacity = 100  # Reduced from 2000 to 100 to be more realistic

    # Pollution reduces growth rate (max 60% reduction at 100 pollution)
    pollution_factor = 1 - (app.game.pollution_level / 500) * 0.6  # Pollution maxes at 500
    base_growth_rate *= max(0.4, pollution_factor)  # Minimum 40% of growth rate

    # Calculate average size of caught fish
    if app.game.caught_fish_sizes:
        avg_size = sum(app.game.caught_fish_sizes) / len(app.game.caught_fish_sizes)
        # Convert visual size back to 1-10 scale for calculations
        avg_size_scale = (avg_size - 30) / 2.2 + 1
        # Larger fish reduce reproduction rate more significantly
        # Each size unit above 5 reduces growth rate by 0.04
        size_penalty = max(0, (avg_size_scale - 5) * 0.04)

        # Calculate population-dependent minimum growth rate
        # At 10 fish: 15% minimum
        # At 20 fish: 12% minimum
        # At 30 fish (starting): 10% minimum
        # At 40 fish: 8% minimum
        # At 50+ fish: 5% minimum
        min_growth_rate = max(0.05, 0.15 - (app.game.fish_population / 50) * 0.10)
        growth_rate = max(min_growth_rate, base_growth_rate - size_penalty)
    else:
        growth_rate = base_growth_rate

    # Calculate reproduction with size-adjusted growth rate
    reproduction = app.game.fish_population * growth_rate * (1 - app.game.fish_population / carrying_capacity)

    # Add pollution-based mortality (increases with pollution level)
    # At 0% pollution: 0% mortality
    # At 50% pollution: 7.5% mortality
    # At 100% pollution: 20% mortality
    mortality_rate = (app.game.pollution_level / 500) * 0.20  # Linear increase up to 20% at max pollution
    mortality = int(app.game.fish_population * mortality_rate)

    # Apply both reproduction and mortality
    app.game.fish_population = max(0, int(app.game.fish_population + reproduction - mortality))

    # Clear the caught fish sizes for the next day
    app.game.caught_fish_sizes = []

def update_hunger():
    """Update community food level based on caught fish"""
    fish_deficit = max(0, app.game.food_decrease_base - app.game.caught_fish_today)
    app.game.food_level = max(0, app.game.food_level - fish_deficit * 0.5)  # Each fish deficit decreases food by 0.5%
    if app.game.food_level <= 0:  # Changed condition to check for 0 food
        app.game.game_over = True

def check_game_over():
    """Check if any failure conditions are met or if player has won"""
    if app.game.food_level <= 0:  # Changed condition to check for 0 food
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()  # Ensure game over screen is on top
        app.game.game_over_screen.children[1].value = 'GAME OVER'  # Set title for lose condition
        app.game.game_over_screen.children[2].value = f'You failed to keep the community fed! Final fish population: {app.game.fish_population}'
        app.game.game_over_screen.children[3].value = ''  # Clear second line
        update_hunger_bar()  # Update hunger bar immediately when game is over
        return True  # Return True to indicate game is over
    elif app.game.pollution_level >= 500:  # New pollution-based game over condition
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()  # Ensure game over screen is on top
        app.game.game_over_screen.children[1].value = 'GAME OVER'  # Set title for lose condition
        app.game.game_over_screen.children[2].value = 'The water has become too polluted!'
        app.game.game_over_screen.children[3].value = f'Final fish population: {app.game.fish_population}'
        return True  # Return True to indicate game is over
    elif app.game.day >= app.game.target_days:
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()  # Ensure game over screen is on top
        app.game.game_over_screen.children[1].value = 'YOU WIN!'  # Set title for win condition
        app.game.game_over_screen.children[2].value = 'Congratulations! You kept the community fed for 20 days!'
        app.game.game_over_screen.children[3].value = f'Final fish population: {app.game.fish_population}'
        update_hunger_bar()  # Update hunger bar immediately when game is over
        return True  # Return True to indicate game is over
    return False  # Return False if game should continue

def update_trash():
    """Update trash positions and create new trash"""
    app.game.trash_timer += 1

    # Create new trash
    if app.game.trash_timer >= 300:  # Every ~10 seconds
        app.game.trash_timer = 0
        if len(app.game.trash.children) < 2:  # Max 2 pieces of trash
            trash = create_trash()
            # Randomly choose which side to spawn from
            side = random.choice(['left', 'right'])
            trash.centerX = -50 if side == 'left' else 450  # Start off-screen
            trash.centerY = random.randint(200, 350)  # Only spawn in water area
            trash.spawn_side = side  # Store which side it spawned from
            app.game.trash.add(trash)
            # Increase pollution when new trash appears (100 pollution per piece = 20%)
            app.game.pollution_level = min(500, app.game.pollution_level + 100)

    # Move existing trash
    for trash in app.game.trash.children:
        # Move horizontally based on spawn side
        if trash.spawn_side == 'left':
            trash.centerX += 1
        else:
            trash.centerX -= 1

        # Add gentle wave motion
        trash.centerY += math.sin(trash.vertical_offset + app.game.time * 0.1) * 0.5

        # Add slight rotation for floating effect
        trash.rotateAngle += math.sin(app.game.time * 0.05) * 0.5

        # Remove if off screen
        if trash.centerX < -100 or trash.centerX > 500:
            trash.visible = False
            app.game.trash.remove(trash)
            # Increase pollution when trash leaves screen without being collected (50 pollution = 10%)
            app.game.pollution_level = min(500, app.game.pollution_level + 50)

def update_hunger_bar():
    """Update food bar color and size"""
    if not app.game.game_over:
        bar = app.game.hunger_bar.children[1]  # The fill bar
        food = app.game.food_level

        # Update size (now directly proportional to food level)
        bar.width = max(0, 98 * (food/100))

        # Update color with smooth transitions
        if food > 70:
            bar.fill = rgb(0, 255, 0)
            bar.opacity = 100  # Full opacity for good food level
        elif food > 30:
            # Reset opacity to full when transitioning to warning colors
            bar.opacity = 100
            # Gradient from green to yellow to red
            if food > 50:
                # Green to yellow
                ratio = (food - 50) / 20
                bar.fill = rgb(255 * (1-ratio),  # Red component
                             255,                 # Green component
                             0)                   # Blue component
            else:
                # Yellow to red
                ratio = (food - 30) / 20
                bar.fill = rgb(255,                          # Red component
                             255 * ratio,                    # Green component
                             0)                              # Blue component
        else:
            bar.fill = 'red'
            # Add pulsing effect when food is low
            bar.opacity = 50 + math.sin(app.game.time * 0.2) * 50
    else:
        # Only make bar red if game ended due to no food
        if app.game.food_level <= 0:
            bar = app.game.hunger_bar.children[1]  # The fill bar
            bar.width = 98  # Keep bar full width
            bar.fill = 'red'
            bar.opacity = 100  # Full opacity

def update_fishing_rod():
    """Update fishing line position based on mouse"""
    if not app.game.game_over:
        # Update line position
        line = app.game.line.children[0]
        hook = app.game.line.children[1]

        # Get the rod tip position from the last rod section
        # The rod has 3 guides, handle, grip, and 3 sections
        # The last section (tip) is at index 7
        rod_tip = app.game.rod.children[7]  # The last rod section
        rod_tip_x = rod_tip.x2
        rod_tip_y = rod_tip.y2

        # Update line start position to rod tip
        line.x1 = rod_tip_x
        line.y1 = rod_tip_y

        # Calculate line angle and length
        dx = app.game.mouse_x - rod_tip_x
        dy = app.game.mouse_y - rod_tip_y
        length = min(math.sqrt(dx*dx + dy*dy), 300)

        # Update line end point with slight lag
        angle = math.atan2(dy, dx)
        line.x2 = rod_tip_x + length * math.cos(angle)
        line.y2 = rod_tip_y + length * math.sin(angle)

        # Update hook position and rotation
        hook.centerX = line.x2
        hook.centerY = line.y2
        hook.rotateAngle = math.degrees(angle) + 270  # Adjusted to keep hook oriented correctly

def try_catch_fish(mouse_x, mouse_y):
    """Attempt to catch a fish at the clicked location"""
    if app.game.game_over:
        return

    # Get line end position
    line = app.game.line.children[0]
    hook_x, hook_y = line.x2, line.y2

    # Check if clicking near bucket with dragged fish
    if app.game.dragged_fish:
        bucket = app.game.bucket
        # Check if bucket is full
        if app.game.caught_fish_today >= 5:
            return False  # Can't add more fish if bucket is full

        # Use bucket dimensions from game state for hit detection
        if (mouse_x > bucket.centerX - app.game.bucket_top_width/2 and 
            mouse_x < bucket.centerX + app.game.bucket_top_width/2 and
            mouse_y > bucket.centerY - app.game.bucket_height/2 and 
            mouse_y < bucket.centerY + app.game.bucket_height/2):
            app.game.caught_fish_today += 1
            if app.game.dragged_fish in app.game.visible_fish:
                app.game.visible_fish.remove(app.game.dragged_fish)  # Remove from list if present
            app.game.dragged_fish.visible = False
            app.game.dragged_fish.dragged = False  # Reset dragged state

            # Store fish size before removing the fish
            fish_size = app.game.dragged_fish.children[1].fish_size
            app.game.caught_fish_sizes.append(fish_size)

            # Reduce fish population by 1
            app.game.fish_population = max(0, app.game.fish_population - 1)

            # Check if population reached 0
            if app.game.fish_population <= 0:
                app.game.game_over = True
                app.game.game_over_screen.visible = True
                app.game.game_over_screen.toFront()  # Ensure game over screen is on top
                app.game.game_over_screen.children[2].value = f'Game Over! The fish population has been depleted!'
                app.game.game_over_screen.children[3].value = ''  # Clear second line
                return True

            app.game.dragged_fish = None
            # Update bucket counter
            bucket.children[3].value = f'{app.game.caught_fish_today}/5'

            # Convert visual size to 1-10 scale for food calculation
            size_scale = (fish_size - 30) / 2.2 + 1
            # Base food increase of 2% per size unit, with moderate scaling
            food_increase = 2 + (size_scale - 1) * 1.5  # Base 2% + 1.5% per size above 1
            # Cap the maximum food increase at 15%
            food_increase = min(15, food_increase)
            app.game.food_level = min(100, app.game.food_level + food_increase)  # Cap at 100%

            # If bucket is now full, automatically end the day
            if app.game.caught_fish_today >= 5:
                end_day()
            return True
        return False  # If clicking outside bucket while dragging fish, do nothing

    # Check if clicking on trash (only if not dragging a fish)
    for trash in app.game.trash.children:
        if trash.hits(mouse_x, mouse_y):
            app.game.trash.remove(trash)
            trash.visible = False

            # Calculate minimum pollution based on remaining trash (100 pollution per piece = 20%)
            remaining_trash = len(app.game.trash.children)
            min_pollution = remaining_trash * 100

            # Reduce pollution by 30% (150 units), but never below the minimum
            new_pollution = max(min_pollution, app.game.pollution_level - 150)
            app.game.pollution_level = new_pollution

            return True

    # Try to catch new fish (check in reverse order to catch frontmost fish first)
    for fish in reversed(app.game.visible_fish[:]):  # Use slice copy to avoid modification while iterating
        fish_body = fish.children[1]
        distance = math.sqrt((fish.centerX - hook_x)**2 + (fish.centerY - hook_y)**2)
        if distance < fish_body.fish_size:
            # Only allow catching if bucket isn't full
            if app.game.caught_fish_today < 5:
                app.game.dragged_fish = fish
                fish.dragged = True  # Set dragged state
                return True

    return False

def end_day():
    """Process end of day events"""
    # Check for game over conditions first
    if check_game_over():
        return  # End the function if game is over

    # Only process day events if game is not over
    calculate_reproduction()
    update_hunger()

    # Check for game over again after updating hunger
    if check_game_over():
        return  # End the function if game is over

    # Only increment day if we haven't won yet
    app.game.day += 1
    app.game.caught_fish_today = 0

    # Update stats display
    update_stats_display()

def update_stats_display():
    """Update the display of game statistics"""
    # Update values while maintaining left alignment
    app.game.stats.children[0].value = f'Day: {app.game.day}/{app.game.target_days}'
    app.game.stats.children[0].left = app.game.stats.left_position  # Reset left position

    app.game.stats.children[1].value = f'Fish Population: {app.game.fish_population}'
    app.game.stats.children[1].left = app.game.stats.left_position  # Reset left position

    app.game.stats.children[2].value = f'Food Level: {int(app.game.food_level)}%'  # Changed from Hunger Level
    app.game.stats.children[2].left = app.game.stats.left_position  # Reset left position

    # Calculate average size of caught fish from stored sizes
    if app.game.caught_fish_sizes:
        # Convert visual sizes to 1-10 scale for display
        avg_size = sum(app.game.caught_fish_sizes) / len(app.game.caught_fish_sizes)
        # Convert to 1-10 scale and round to 1 decimal place
        avg_size_scale = int(((avg_size - 30) / 2.2 + 1) * 10 + 0.5) / 10
        app.game.stats.children[3].value = f'Caught Today: {app.game.caught_fish_today}/5 (Avg Size: {avg_size_scale})'
    else:
        app.game.stats.children[3].value = f'Caught Today: {app.game.caught_fish_today}/5'
    app.game.stats.children[3].left = app.game.stats.left_position  # Reset left position

    # Add pollution level display if it doesn't exist
    if len(app.game.stats.children) < 5:
        app.game.stats.add(Label('Pollution: 0%', app.game.stats.left_position, 100))

    # Update pollution level display
    pollution_percent = min(100, int(app.game.pollution_level / 5))  # Convert to percentage (max 500 = 100%)
    app.game.stats.children[4].value = f'Pollution: {pollution_percent}%'
    app.game.stats.children[4].left = app.game.stats.left_position  # Reset left position

def create_trash():
    """Create a piece of floating trash"""
    # Randomly choose which side to spawn from
    side = random.choice(['left', 'right'])
    x = -50 if side == 'left' else 450  # Start off-screen
    y = random.randint(200, 350)  # Only spawn in water area

    trash_group = Group()
    trash_type = random.choice(['bottle', 'bag', 'can'])

    if trash_type == 'bottle':
        shape = Circle(x, y, 8, fill='lightGray')
    elif trash_type == 'bag':
        shape = Rect(x-8, y-8, 16, 16, fill='white', opacity=50)
    else:  # can
        shape = Rect(x-6, y-8, 12, 16, fill='silver')

    trash_group.add(shape)
    trash_group.trash_type = trash_type

    # Add some random rotation for variety
    trash_group.rotateAngle = random.randint(-45, 45)

    # Add some random vertical offset for wave motion
    trash_group.vertical_offset = random.uniform(0, 2*math.pi)

    return trash_group

def onAppStart():
    app.game = create_game()
    app.stepsPerSecond = 30

def onStep():
    if not app.game.game_over:
        app.game.time += 1
        spawn_fish()
        update_fishing_rod()
        update_trash()
        update_hunger_bar()

        # Check for game over conditions immediately
        if app.game.food_level <= 0 or app.game.pollution_level >= 500:
            check_game_over()

        # Update fish positions
        for fish in app.game.visible_fish[:]:  # Use slice copy to avoid modification while iterating
            if not fish.dragged:  # Only move fish that aren't being dragged
                # Horizontal movement
                fish.centerX += fish.direction * fish.speed

                # Vertical wavy movement
                fish.centerY += math.sin(fish.vertical_offset + app.game.time * fish.vertical_speed) * 0.5

                # Remove fish if they swim off screen
                if (fish.centerX < -100 or fish.centerX > 500):
                    if fish in app.game.visible_fish:
                        app.game.visible_fish.remove(fish)
                    fish.visible = False

        # Update dragged fish position
        if app.game.dragged_fish:
            app.game.dragged_fish.centerX = app.game.mouse_x
            app.game.dragged_fish.centerY = app.game.mouse_y
    update_stats_display()

def onMousePress(mouseX, mouseY):
    try_catch_fish(mouseX, mouseY)

def onKeyPress(key):
    if key == 'd':
        end_day()
    elif key == 'r' and app.game.game_over:
        # Remove old game
        app.game.visible = False
        # Create new game
        app.game = create_game()

def onMouseMove(mouseX, mouseY):
    app.game.mouse_x = mouseX
    app.game.mouse_y = mouseY

onAppStart()
cmu_graphics.run()
