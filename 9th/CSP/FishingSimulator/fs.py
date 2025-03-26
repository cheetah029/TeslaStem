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
    game.time = 0  # For animations
    
    # Mouse position tracking
    game.mouse_x = 200
    game.mouse_y = 200
    
    # Fish being dragged
    game.dragged_fish = None
    
    # Bucket dimensions and position (stored in game state)
    game.bucket_height = 40
    game.bucket_top_width = 40
    game.bucket_bottom_width = 25
    game.bucket_x = 350
    game.bucket_y = 120  # Moved bucket down
    
    # Clouds
    game.clouds = Group()
    game.cloud_timer = 0
    
    # Trash
    game.trash = Group()
    game.trash_timer = 0
    game.pollution_level = 0
    
    # Upgrade states
    game.upgrades = {
        'net': 1,  # Fishing efficiency multiplier
        'patrol': 1,  # Illegal fishing prevention
        'bait': 1,  # Catch rate multiplier
    }
    
    # Fish visualization
    game.visible_fish = []
    game.max_visible_fish = 3  # Reduced from 5 to 3
    
    # Create UI elements
    game.background = Group()
    
    # Sky (ensure full coverage)
    sky = Rect(0, 0, 400, 400, fill='skyBlue')  # Extended to full height
    
    # Land/Dock
    land = Rect(0, 130, 400, 50, fill=rgb(139, 69, 19))  # Brown dock, moved down
    land_detail = Rect(0, 130, 400, 10, fill=rgb(101, 67, 33))  # Darker wood detail
    
    # Add dock posts
    post1 = Rect(50, 130, 10, 70, fill=rgb(101, 67, 33))
    post2 = Rect(150, 130, 10, 70, fill=rgb(101, 67, 33))
    post3 = Rect(250, 130, 10, 70, fill=rgb(101, 67, 33))
    
    # Water
    water = Rect(0, 180, 400, 220, fill=rgb(0, 105, 148))  # Adjusted water position
    
    # Create bucket
    game.bucket = Group()
    
    # Trapezoid body
    bucket_body = Polygon(
        game.bucket_x - game.bucket_top_width/2, game.bucket_y,  # Top left
        game.bucket_x + game.bucket_top_width/2, game.bucket_y,  # Top right
        game.bucket_x + game.bucket_bottom_width/2, game.bucket_y + game.bucket_height,  # Bottom right
        game.bucket_x - game.bucket_bottom_width/2, game.bucket_y + game.bucket_height,  # Bottom left
        fill='silver'
    )
    
    # Semicircle handle (rotated 180 degrees to be right side up)
    handle_radius = 20
    bucket_handle = Arc(game.bucket_x, game.bucket_y, handle_radius * 2, handle_radius * 2, 
                       -90, 180, fill=None, border='silver', borderWidth=2)
    
    # Oval rim at top
    bucket_rim = Oval(game.bucket_x, game.bucket_y, game.bucket_top_width, 10, fill=rgb(130, 130, 130))
    
    bucket_counter = Label('0/5', game.bucket_x, game.bucket_y + 20, size=14, bold=True)
    
    game.bucket.add(bucket_body)
    game.bucket.add(bucket_handle)
    game.bucket.add(bucket_rim)
    game.bucket.add(bucket_counter)
    
    # Create hunger bar with better design (moved up and right)
    game.hunger_bar = Group()
    bar_width = 100
    bar_height = 15
    bar_x = 150  # Moved right
    bar_y = 40   # Moved up
    corner_radius = 5  # For rounded corners
    
    # Background with rounded corners
    bar_bg = Rect(bar_x, bar_y, bar_width, bar_height, fill='darkGray')
    bar_bg.radius = corner_radius
    
    bar_border = Rect(bar_x, bar_y, bar_width, bar_height, 
                     fill=None, border='black', borderWidth=2)
    bar_border.radius = corner_radius
    
    # Inner bar with rounded corners and brighter green
    bar_fill = Rect(bar_x + 1, bar_y + 1, bar_width - 2, bar_height - 2, 
                    fill=rgb(50, 205, 50))  # Brighter green
    bar_fill.radius = corner_radius - 1
    
    # Add shine effect
    shine = Polygon(
        bar_x + 1, bar_y + 1,  # Top left
        bar_x + bar_width - 1, bar_y + 1,  # Top right
        bar_x + bar_width - 1, bar_y + 4,  # Bottom right
        bar_x + 1, bar_y + 4,  # Bottom left
        fill=rgb(255, 255, 255), opacity=20
    )
    
    game.hunger_bar.add(bar_bg)
    game.hunger_bar.add(bar_fill)
    game.hunger_bar.add(shine)
    game.hunger_bar.add(bar_border)
    
    # Add background elements in correct order
    game.background.add(sky)
    game.background.add(water)
    game.background.add(post1)
    game.background.add(post2)
    game.background.add(post3)
    game.background.add(land)
    game.background.add(land_detail)
    
    # Create a separate group for fish to ensure they're behind the rod and line
    game.fish_layer = Group()
    game.background.add(game.fish_layer)
    
    # Create fishing rod with hook
    game.rod = Group()
    
    # Rod handle (brown wood texture) - extended handle
    handle = Line(0, 100, 80, 100, fill=rgb(139, 69, 19), lineWidth=8)  # Extended handle length
    handle_grip = Line(-70, 100, 30, 100, fill=rgb(101, 67, 33), lineWidth=10)  # Longer grip
    
    # Rod body (elegant curve using multiple lines)
    rod_color = rgb(160, 82, 45)  # Lighter brown for rod
    rod_sections = []
    curve_points = [(80, 100), (120, 110), (160, 130), (180, 140)]  # Adjusted curve points to match new handle
    for i in range(len(curve_points)-1):
        section = Line(curve_points[i][0], curve_points[i][1],
                      curve_points[i+1][0], curve_points[i+1][1],
                      fill=rod_color, lineWidth=4-i*0.8)  # Gradually thinner
        rod_sections.append(section)
    
    # Rod guides (line holders)
    guides = []
    guide_positions = [(100, 105), (130, 120), (160, 135)]  # Adjusted guide positions
    for x, y in guide_positions:
        guide = Circle(x, y, 3, fill=None, border='silver', borderWidth=1)
        guides.append(guide)
    
    # Add all rod parts
    game.rod.add(handle)
    game.rod.add(handle_grip)
    for section in rod_sections:
        game.rod.add(section)
    for guide in guides:
        game.rod.add(guide)
    game.rod.rotateAngle = -35
    game.rod.centerY = 145
    
    # Create fishing line with hook after rod is positioned
    game.line = Group()
    rod_tip = rod_sections[-1]  # Get the last rod section (the tip)
    main_line = Line(rod_tip.x2, rod_tip.y2, rod_tip.x2, rod_tip.y2, fill='white', opacity=50, lineWidth=1)
    
    # Create hook using smooth line segments
    hook_size = 6
    hook_group = Group()
    
    # Vertical line
    hook_line = Line(0, 0, 0, hook_size * 2, fill='black', lineWidth=2)
    
    # Curved hook using multiple small line segments
    curve_points = []
    segments = 12  # Increased segments for smoother curve
    for i in range(segments + 1):
        angle = math.pi * i / segments
        x = hook_size * math.cos(angle)
        y = hook_size * 2 + hook_size * math.sin(angle)
        # Adjust points to connect smoothly to vertical line
        if i == 0:
            x = 0  # Start at the bottom of vertical line
            y = hook_size * 2
        curve_points.append((x, y))
    
    # Create smooth curve using line segments
    for i in range(len(curve_points) - 1):
        segment = Line(curve_points[i][0], curve_points[i][1],
                      curve_points[i+1][0], curve_points[i+1][1],
                      fill='black', lineWidth=2)
        hook_group.add(segment)
    
    hook_group.add(hook_line)
    hook_group.rotateAngle = 180  # Rotate hook 180 degrees
    
    game.line.add(main_line)
    game.line.add(hook_group)
    
    # Instructions
    game.instructions = Group(
        Label('Sustainable Fishing Simulator', 200, 20, size=16, bold=True),
        Label('Use the fishing rod to catch fish', 200, 350, size=14),
        Label('Press D to end the day', 200, 370, size=14),
        Label('Catch enough fish to feed the community!', 200, 390, size=14)
    )
    
    # Stats display
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
        x = random.randint(150, 350)  # Adjusted to spawn only on right side
        y = random.randint(180, 350)  # Adjusted to spawn only in water below dock
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
        app.game.fish_layer.add(fish_group)  # Add to the fish layer group

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

def update_clouds():
    """Update cloud positions and create new clouds"""
    app.game.cloud_timer += 1
    
    # Create new cloud
    if app.game.cloud_timer >= 200:  # Every ~6 seconds
        app.game.cloud_timer = 0
        if len(app.game.clouds.children) < 3:  # Max 3 clouds
            cloud = create_cloud()
            app.game.clouds.add(cloud)
    
    # Move existing clouds
    for cloud in app.game.clouds.children:
        cloud.centerX += 0.5
        if cloud.centerX > 450:  # Remove when off screen
            cloud.visible = False
            app.game.clouds.remove(cloud)

def update_trash():
    """Update trash positions and create new trash"""
    app.game.trash_timer += 1
    
    # Create new trash
    if app.game.trash_timer >= 300:  # Every ~10 seconds
        app.game.trash_timer = 0
        if len(app.game.trash.children) < 2:  # Max 2 pieces of trash
            trash = create_trash()
            trash.centerX = random.choice([-20, 420])  # Start off either edge
            trash.centerY = random.randint(200, 350)
            app.game.trash.add(trash)
    
    # Move existing trash
    for trash in app.game.trash.children:
        if trash.centerX < 200:
            trash.centerX += 1
        else:
            trash.centerX -= 1
        
        # Add some vertical movement
        trash.centerY += math.sin(app.game.time * 0.1) * 0.5
        
        # Remove if off screen
        if trash.centerX < -50 or trash.centerX > 450:
            trash.visible = False
            app.game.trash.remove(trash)

def update_hunger_bar():
    """Update hunger bar color and size"""
    if not app.game.game_over:
        bar = app.game.hunger_bar.children[1]  # The fill bar
        hunger = app.game.hunger_level
        
        # Update size
        bar.width = max(0, 98 * (1 - hunger/100))
        
        # Update color with smooth transitions
        if hunger < 30:
            bar.fill = 'green'
        elif hunger < 70:
            # Gradient from green to yellow to red
            if hunger < 50:
                # Green to yellow
                ratio = (hunger - 30) / 20
                bar.fill = rgb(255 * ratio + 0 * (1-ratio),  # Red component
                             255,                             # Green component
                             0)                              # Blue component
            else:
                # Yellow to red
                ratio = (hunger - 50) / 20
                bar.fill = rgb(255,                          # Red component
                             255 * (1-ratio),                # Green component
                             0)                              # Blue component
        else:
            bar.fill = 'red'
            # Add pulsing effect when critical
            bar.opacity = 50 + math.sin(app.game.time * 0.2) * 50

def update_fishing_rod():
    """Update fishing line position based on mouse"""
    if not app.game.game_over:
        # Update line position
        line = app.game.line.children[0]
        hook = app.game.line.children[1]
        
        # Get the rod tip position from the last rod section (index 4 since we have handle, grip, and 3 sections)
        rod_tip = app.game.rod.children[4]  # The last rod section
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
    
    # Check if clicking on trash
    for trash in app.game.trash.children:
        if trash.hits(mouse_x, mouse_y):
            app.game.trash.remove(trash)
            trash.visible = False
            app.game.pollution_level = max(0, app.game.pollution_level - 10)
            return True
    
    # Get line end position
    line = app.game.line.children[0]
    hook_x, hook_y = line.x2, line.y2
    
    # Check if clicking near bucket with dragged fish
    if app.game.dragged_fish:
        bucket = app.game.bucket
        # Use bucket dimensions from game state for hit detection
        if (mouse_x > bucket.centerX - app.game.bucket_top_width/2 and 
            mouse_x < bucket.centerX + app.game.bucket_top_width/2 and
            mouse_y > bucket.centerY - app.game.bucket_height/2 and 
            mouse_y < bucket.centerY + app.game.bucket_height/2):
            app.game.caught_fish_today += 1
            if app.game.dragged_fish in app.game.visible_fish:
                app.game.visible_fish.remove(app.game.dragged_fish)  # Remove from list if present
            app.game.dragged_fish.visible = False
            app.game.dragged_fish = None
            # Update bucket counter
            bucket.children[3].value = f'{app.game.caught_fish_today}/5'
            return True
    
    # Try to catch new fish
    for fish in app.game.visible_fish[:]:
        fish_body = fish.children[1]
        distance = math.sqrt((fish.centerX - hook_x)**2 + (fish.centerY - hook_y)**2)
        if distance < fish_body.fish_size:
            app.game.dragged_fish = fish
            return True
    
    return False

def end_day():
    """Process end of day events"""
    calculate_reproduction()
    update_hunger()
    check_game_over()

    if app.game.game_over:
        return

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

def create_cloud():
    """Create a cloud shape"""
    cloud = Group()
    # Random cloud size and position
    size = random.randint(30, 50)
    y = random.randint(20, 80)
    
    # Create cloud using overlapping circles
    main = Circle(-size, y, size/2, fill='white', opacity=80)
    part1 = Circle(-size+size/3, y-size/4, size/3, fill='white', opacity=80)
    part2 = Circle(-size+size/2, y, size/3, fill='white', opacity=80)
    part3 = Circle(-size+size/3, y+size/4, size/3, fill='white', opacity=80)
    
    cloud.add(main)
    cloud.add(part1)
    cloud.add(part2)
    cloud.add(part3)
    return cloud

def create_trash():
    """Create a piece of floating trash"""
    trash_types = [
        ('bottle', Circle(0, 0, 8, fill='lightGray')),
        ('bag', Rect(-8, -8, 16, 16, fill='white', opacity=50)),
        ('can', Rect(-6, -8, 12, 16, fill='silver'))
    ]
    
    trash_group = Group()
    trash_type, shape = random.choice(trash_types)
    trash_group.add(shape)
    trash_group.trash_type = trash_type
    return trash_group

def onAppStart():
    app.game = create_game()
    app.stepsPerSecond = 30

def onStep():
    if not app.game.game_over:
        app.game.time += 1
        spawn_fish()
        update_fishing_rod()
        update_clouds()
        update_trash()
        update_hunger_bar()
        
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
