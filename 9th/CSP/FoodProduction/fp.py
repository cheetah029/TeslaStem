# Sustainable Food Production Game

# Goal is to sustainably grow food for the population to survive for 20 days.
# The player must balance food production with waste and pollution management.

from cmu_graphics import *
import random
import math

def create_game():
    game = Group()

    # Initial game parameters
    game.food_production = 0
    game.food_decrease_base = 50
    game.food_level = 100
    game.day = 1
    game.target_days = 20
    game.game_over = False
    game.time = 0
    game.produced_food_today = 0
    game.produced_food_types = []
    
    # Mouse position tracking
    game.mouse_x = 200
    game.mouse_y = 200
    game.selected_crop = None
    
    # Storage dimensions and position
    game.storage_height = 40
    game.storage_top_width = 40
    game.storage_bottom_width = 25
    game.storage_x = 350
    game.storage_y = 120
    
    # Waste and pollution visualization
    game.waste = Group()
    game.waste_timer = 0
    game.pollution_level = 0
    game.available_crops = []
    game.max_available_crops = 3
    
    # Create UI elements
    game.background = Group()
    
    # Sky and ground
    sky = Rect(0, 0, 400, 400, fill='skyBlue')
    ground = Rect(0, 180, 400, 220, fill=rgb(139, 69, 19))
    
    # Farmland
    farmland = Rect(0, 130, 400, 50, fill=rgb(101, 67, 33))
    farmland_detail = Rect(0, 130, 400, 10, fill=rgb(101, 67, 33))
    
    # Farm structures
    for x in [50, 150, 250]:
        barn = Rect(x, 130, 10, 70, fill=rgb(139, 69, 19))
        game.background.add(barn)
    
    # Add background elements
    game.background.add(sky)
    game.background.add(ground)
    game.background.add(farmland)
    game.background.add(farmland_detail)
    game.background.add(game.waste)
    
    # Create storage
    game.storage = Group()
    
    # Trapezoid body
    storage_body = Polygon(
        game.storage_x - game.storage_top_width/2, game.storage_y,
        game.storage_x + game.storage_top_width/2, game.storage_y,
        game.storage_x + game.storage_bottom_width/2, game.storage_y + game.storage_height,
        game.storage_x - game.storage_bottom_width/2, game.storage_y + game.storage_height,
        fill='brown'
    )
    
    # Handle and rim
    handle_radius = 20
    storage_handle = Arc(game.storage_x, game.storage_y, handle_radius * 2, handle_radius * 2, 
                       -90, 180, fill=None, border='brown', borderWidth=2)
    storage_rim = Oval(game.storage_x, game.storage_y, game.storage_top_width, 10, fill=rgb(101, 67, 33))
    storage_counter = Label('0/5', game.storage_x, game.storage_y + 20, size=14, bold=True)
    
    game.storage.add(storage_body)
    game.storage.add(storage_handle)
    game.storage.add(storage_rim)
    game.storage.add(storage_counter)
    
    # Create hunger bar
    game.hunger_bar = Group()
    bar_width = 100
    bar_height = 15
    bar_x = 120
    bar_y = 53
    
    # Background and border
    bar_bg = Rect(bar_x, bar_y, bar_width, bar_height, fill='darkGray')
    bar_border = Rect(bar_x, bar_y, bar_width, bar_height, 
                     fill=None, border='black', borderWidth=2)
    
    # Fill bar and shine effect
    bar_fill = Rect(bar_x + 1, bar_y + 1, bar_width - 2, bar_height - 2, 
                    fill=rgb(50, 205, 50))
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
    
    # Create farming tool
    game.tool = Group()
    
    # Tool handle and grip
    handle = Line(0, 100, 80, 100, fill=rgb(139, 69, 19), lineWidth=8)
    handle_grip = Line(-70, 100, 30, 100, fill=rgb(101, 67, 33), lineWidth=10)
    
    # Tool body
    tool_color = rgb(160, 82, 45)
    tool_sections = []
    curve_points = [(80, 100), (120, 110), (160, 130), (180, 140)]
    for i in range(len(curve_points)-1):
        section = Line(curve_points[i][0], curve_points[i][1],
                      curve_points[i+1][0], curve_points[i+1][1],
                      fill=tool_color, lineWidth=4-i*0.8)
        tool_sections.append(section)
    
    # Tool head
    for x, y in [(100, 105), (130, 120), (160, 135)]:
        head = Circle(x, y, 3, fill=None, border='silver', borderWidth=1)
        game.tool.add(head)
    
    # Add all tool parts
    game.tool.add(handle)
    game.tool.add(handle_grip)
    for section in tool_sections:
        game.tool.add(section)
    game.tool.rotateAngle = -35
    game.tool.centerY = 150
    
    # Create tool action indicator
    game.action_indicator = Group()
    tool_tip = tool_sections[-1]
    action_circle = Circle(tool_tip.x2, tool_tip.y2, 10, fill='white', opacity=50)
    game.action_indicator.add(action_circle)
    
    # Instructions
    game.instructions = Group(
        Label('Sustainable Food Production', 200, 16, size=16, bold=True),
        Label('Use the farming tool to harvest crops', 200, 350, size=14),
        Label('Press D to end the day', 200, 370, size=14),
        Label('Produce enough food to feed the community, but manage waste!', 200, 390, size=14)
    )
    
    # Stats display
    game.stats = Group()
    game.stats.left_position = 15
    
    game.stats.add(
        Label('Day: 1', game.stats.left_position, 20),
        Label('Food Production: 0', game.stats.left_position, 40),
        Label('Food Level: 100%', game.stats.left_position, 60),
        Label('Produced Today: 0/5', game.stats.left_position, 80)
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

def create_crop_colors():
    """Create a random crop color scheme"""
    # Base colors for crops
    base_colors = [
        rgb(0, 128, 0),  # Green
        rgb(255, 215, 0),  # Golden
        rgb(255, 140, 0),  # Dark orange
        rgb(139, 69, 19),  # Brown
        rgb(128, 128, 0),  # Olive
    ]
    main_color = random.choice(base_colors)
    # Make detail color slightly different
    detail_color = rgb(min(255, main_color.red + 20),
                     min(255, main_color.green + 20),
                     min(255, main_color.blue + 20))
    return main_color, detail_color

def spawn_crops():
    """Spawn new visible crops for harvesting"""
    # Adjust max visible crops based on production
    app.game.max_available_crops = max(1, min(3, int(1 + app.game.food_production / 10)))
    
    # Adjust spawn rate based on production
    spawn_chance = max(0.2, min(1.0, app.game.food_production / 30))
    
    while len(app.game.available_crops) < app.game.max_available_crops:
        if random.random() > spawn_chance:
            continue
        
        # Spawn crops in different areas of the farmland
        x = random.randint(50, 350)
        y = random.randint(140, 170)
        size_scale = random.randint(1, 10)
        size = 20 + (size_scale - 1) * 2
        
        # Create crop shape
        crop_group = Group()
        crop_group.harvested = False
        
        # Random crop colors
        main_color, detail_color = create_crop_colors()
        
        # Create crop components
        crop_type = random.choice(['wheat', 'corn', 'potato', 'tomato', 'carrot'])
        crop_group.crop_type = crop_type
        
        if crop_type == 'wheat':
            # Wheat stalk
            stalk = Line(0, 0, 0, size * 1.5, fill=rgb(139, 69, 19), lineWidth=2)
            crop_group.add(stalk)
            
            # Wheat head
            head = Oval(0, -size/2, size, size/2, fill=main_color)
            crop_group.add(head)
            
            # Wheat details
            for i in range(5):
                detail = Line(-size/2, -size/2 + i*size/4, size/2, -size/2 + i*size/4, 
                             fill=detail_color, lineWidth=1)
                crop_group.add(detail)
                
        elif crop_type == 'corn':
            # Corn stalk
            stalk = Line(0, 0, 0, size * 1.5, fill=rgb(139, 69, 19), lineWidth=2)
            crop_group.add(stalk)
            
            # Corn cob
            cob = Oval(0, -size/2, size/2, size, fill=main_color)
            crop_group.add(cob)
            
            # Corn kernels
            for i in range(3):
                kernel = Circle(0, -size/2 + i*size/2, size/6, fill=detail_color)
                crop_group.add(kernel)
                
        elif crop_type == 'potato':
            # Potato plant
            plant = Polygon(
                -size/2, 0,
                size/2, 0,
                size/3, -size,
                -size/3, -size,
                fill=rgb(0, 100, 0)
            )
            crop_group.add(plant)
            
            # Potato
            potato = Oval(0, size/4, size, size/2, fill=main_color)
            crop_group.add(potato)
            
        elif crop_type == 'tomato':
            # Tomato plant
            plant = Polygon(
                -size/2, 0,
                size/2, 0,
                size/3, -size,
                -size/3, -size,
                fill=rgb(0, 100, 0)
            )
            crop_group.add(plant)
            
            # Tomato
            tomato = Circle(0, size/4, size/2, fill=main_color)
            crop_group.add(tomato)
            
            # Tomato stem
            stem = Line(0, size/4 - size/2, 0, size/4, fill=rgb(0, 100, 0), lineWidth=2)
            crop_group.add(stem)
            
        else:  # carrot
            # Carrot top
            top = Polygon(
                -size/2, 0,
                size/2, 0,
                size/3, -size,
                -size/3, -size,
                fill=rgb(0, 100, 0)
            )
            crop_group.add(top)
            
            # Carrot
            carrot = Polygon(
                -size/4, 0,
                size/4, 0,
                size/6, size,
                -size/6, size,
                fill=main_color
            )
            crop_group.add(carrot)
        
        # Store size information
        crop_group.crop_size = size
        crop_group.size_scale = size_scale
        
        # Set position
        crop_group.centerX = x
        crop_group.centerY = y
        
        app.game.available_crops.append(crop_group)

def calculate_production():
    """Calculate daily food production changes"""
    base_production_rate = 0.15
    max_production = 100
    
    # Pollution reduces production rate
    pollution_factor = 1 - (app.game.pollution_level / 500) * 0.6
    base_production_rate *= max(0.4, pollution_factor)
    
    # Calculate average size of harvested crops
    if app.game.produced_food_types:
        crop_types = set(app.game.produced_food_types)
        diversity_bonus = min(0.2, len(crop_types) * 0.05)
        production_rate = base_production_rate * (1 + diversity_bonus)
    else:
        production_rate = base_production_rate
    
    # Calculate production and waste
    production = app.game.food_production * production_rate * (1 - app.game.food_production / max_production)
    waste_rate = (app.game.pollution_level / 500) * 0.20
    waste = int(app.game.food_production * waste_rate)
    
    # Apply changes
    app.game.food_production = max(0, int(app.game.food_production + production - waste))
    app.game.produced_food_types = []

def update_hunger():
    """Update community food level based on produced food"""
    food_deficit = max(0, app.game.food_decrease_base - app.game.produced_food_today)
    app.game.food_level = max(0, app.game.food_level - food_deficit * 0.5)
    if app.game.food_level <= 0:
        app.game.game_over = True

def check_game_over():
    """Check if any failure conditions are met or if player has won"""
    if app.game.food_level <= 0:
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()
        app.game.game_over_screen.children[1].value = 'GAME OVER'
        app.game.game_over_screen.children[2].value = f'You failed to keep the community fed! Final food production: {app.game.food_production}'
        update_hunger_bar()
        return True
    elif app.game.pollution_level >= 500:
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()
        app.game.game_over_screen.children[1].value = 'GAME OVER'
        app.game.game_over_screen.children[2].value = 'The environment has become too polluted!'
        app.game.game_over_screen.children[3].value = f'Final food production: {app.game.food_production}'
        return True
    elif app.game.day >= app.game.target_days:
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()
        app.game.game_over_screen.children[1].value = 'YOU WIN!'
        app.game.game_over_screen.children[2].value = 'Congratulations! You kept the community fed for 20 days!'
        app.game.game_over_screen.children[3].value = f'Final food production: {app.game.food_production}'
        update_hunger_bar()
        return True
    return False

def update_waste():
    """Update waste positions and create new waste"""
    app.game.waste_timer += 1
    
    # Create new waste
    if app.game.waste_timer >= 300:  # Every ~10 seconds
        app.game.waste_timer = 0
        if len(app.game.waste.children) < 2:  # Max 2 pieces of waste
            waste = create_waste()
            side = random.choice(['left', 'right'])
            waste.centerX = -50 if side == 'left' else 450
            waste.centerY = random.randint(200, 350)
            waste.spawn_side = side
            app.game.waste.add(waste)
            app.game.pollution_level = min(500, app.game.pollution_level + 100)
    
    # Move existing waste
    for waste in app.game.waste.children:
        if waste.spawn_side == 'left':
            waste.centerX += 1
        else:
            waste.centerX -= 1
        
        waste.centerY += math.sin(waste.vertical_offset + app.game.time * 0.1) * 0.5
        waste.rotateAngle += math.sin(app.game.time * 0.05) * 0.5
        
        if waste.centerX < -100 or waste.centerX > 500:
            waste.visible = False
            app.game.waste.remove(waste)
            app.game.pollution_level = min(500, app.game.pollution_level + 50)

def update_hunger_bar():
    """Update food bar color and size"""
    if not app.game.game_over:
        bar = app.game.hunger_bar.children[1]  # The fill bar
        food = app.game.food_level
        
        bar.width = max(0, 98 * (food/100))
        
        if food > 70:
            bar.fill = rgb(0, 255, 0)
            bar.opacity = 100
        elif food > 30:
            bar.opacity = 100
            if food > 50:
                ratio = (food - 50) / 20
                bar.fill = rgb(255 * (1-ratio), 255, 0)
            else:
                ratio = (food - 30) / 20
                bar.fill = rgb(255, 255 * ratio, 0)
        else:
            bar.fill = 'red'
            bar.opacity = 50 + math.sin(app.game.time * 0.2) * 50
    else:
        if app.game.food_level <= 0:
            bar = app.game.hunger_bar.children[1]
            bar.width = 98
            bar.fill = 'red'
            bar.opacity = 100

def update_farming_tool():
    """Update farming tool position based on mouse"""
    if not app.game.game_over:
        indicator = app.game.action_indicator.children[0]
        
        # Get tool tip position (last section at index 7)
        tool_tip = app.game.tool.children[7]
        tool_tip_x, tool_tip_y = tool_tip.x2, tool_tip.y2
        
        # Update indicator position
        indicator.centerX = tool_tip_x
        indicator.centerY = tool_tip_y

def try_harvest_crop(mouse_x, mouse_y):
    """Attempt to harvest a crop at the clicked location"""
    if app.game.game_over:
        return
    
    indicator = app.game.action_indicator.children[0]
    indicator_x, indicator_y = indicator.centerX, indicator.centerY
    
    if app.game.selected_crop:
        storage = app.game.storage
        if app.game.produced_food_today >= 5:
            return False
        
        if (mouse_x > storage.centerX - app.game.storage_top_width/2 and 
            mouse_x < storage.centerX + app.game.storage_top_width/2 and
            mouse_y > storage.centerY - app.game.storage_height/2 and 
            mouse_y < storage.centerY + app.game.storage_height/2):
            app.game.produced_food_today += 1
            if app.game.selected_crop in app.game.available_crops:
                app.game.available_crops.remove(app.game.selected_crop)
            app.game.selected_crop.visible = False
            app.game.selected_crop.harvested = False
            
            crop_size = app.game.selected_crop.crop_size
            app.game.produced_food_types.append(app.game.selected_crop.crop_type)
            
            app.game.selected_crop = None
            storage.children[3].value = f'{app.game.produced_food_today}/5'
            
            size_scale = (crop_size - 20) / 2 + 1
            food_increase = min(15, 2 + (size_scale - 1) * 1.5)
            app.game.food_level = min(100, app.game.food_level + food_increase)
            
            if app.game.produced_food_today >= 5:
                end_day()
            return True
        return False
    
    for waste in app.game.waste.children:
        if waste.hits(mouse_x, mouse_y):
            app.game.waste.remove(waste)
            waste.visible = False
            
            remaining_waste = len(app.game.waste.children)
            min_pollution = remaining_waste * 100
            new_pollution = max(min_pollution, app.game.pollution_level - 150)
            app.game.pollution_level = new_pollution
            
            return True
    
    for crop in reversed(app.game.available_crops[:]):
        distance = math.sqrt((crop.centerX - indicator_x)**2 + (crop.centerY - indicator_y)**2)
        if distance < crop.crop_size and app.game.produced_food_today < 5:
            app.game.selected_crop = crop
            crop.harvested = True
            return True
    
    return False

def end_day():
    """Process end of day events"""
    # Check for game over conditions first
    if check_game_over():
        return  # End the function if game is over
    
    # Only process day events if game is not over
    calculate_production()
    update_hunger()
    
    # Check for game over again after updating hunger
    if check_game_over():
        return  # End the function if game is over
    
    # Only increment day if we haven't won yet
    app.game.day += 1
    app.game.produced_food_today = 0
    
    # Update stats display
    update_stats_display()

def update_stats_display():
    """Update the display of game statistics"""
    app.game.stats.children[0].value = f'Day: {app.game.day}/{app.game.target_days}'
    app.game.stats.children[0].left = app.game.stats.left_position
    
    app.game.stats.children[1].value = f'Food Production: {app.game.food_production}'
    app.game.stats.children[1].left = app.game.stats.left_position
    
    app.game.stats.children[2].value = f'Food Level: {int(app.game.food_level)}%'
    app.game.stats.children[2].left = app.game.stats.left_position
    
    if app.game.produced_food_types:
        unique_types = len(set(app.game.produced_food_types))
        app.game.stats.children[3].value = f'Produced Today: {app.game.produced_food_today}/5 (Types: {unique_types})'
    else:
        app.game.stats.children[3].value = f'Produced Today: {app.game.produced_food_today}/5'
    app.game.stats.children[3].left = app.game.stats.left_position
    
    if len(app.game.stats.children) < 5:
        app.game.stats.add(Label('Pollution: 0%', app.game.stats.left_position, 100))
    
    pollution_percent = min(100, int(app.game.pollution_level / 5))
    app.game.stats.children[4].value = f'Pollution: {pollution_percent}%'
    app.game.stats.children[4].left = app.game.stats.left_position

def create_waste():
    """Create a piece of waste"""
    # Randomly choose which side to spawn from
    side = random.choice(['left', 'right'])
    x = -50 if side == 'left' else 450  # Start off-screen
    y = random.randint(200, 350)  # Only spawn in ground area
    
    waste_group = Group()
    waste_type = random.choice(['plastic', 'chemical', 'organic'])
    
    if waste_type == 'plastic':
        shape = Circle(x, y, 8, fill='lightBlue')
    elif waste_type == 'chemical':
        shape = Rect(x-8, y-8, 16, 16, fill='purple', opacity=70)
    else:  # organic
        shape = Rect(x-6, y-8, 12, 16, fill='brown')
    
    waste_group.add(shape)
    waste_group.waste_type = waste_type
    
    # Add some random rotation for variety
    waste_group.rotateAngle = random.randint(-45, 45)
    
    # Add some random vertical offset for wave motion
    waste_group.vertical_offset = random.uniform(0, 2*math.pi)
    
    return waste_group

def onAppStart():
    app.game = create_game()
    app.stepsPerSecond = 30

def onStep():
    if not app.game.game_over:
        app.game.time += 1
        spawn_crops()
        update_farming_tool()
        update_waste()
        update_hunger_bar()
        
        # Check for game over conditions immediately
        if app.game.food_level <= 0 or app.game.pollution_level >= 500:
            check_game_over()
        
        # Update crop positions
        for crop in app.game.available_crops[:]:  # Use slice copy to avoid modification while iterating
            if not crop.harvested:  # Only animate crops that aren't being harvested
                # Gentle swaying animation
                crop.centerY += math.sin(crop.centerY * 0.01 + app.game.time * 0.05) * 0.2
        
        # Update selected crop position
        if app.game.selected_crop:
            app.game.selected_crop.centerX = app.game.mouse_x
            app.game.selected_crop.centerY = app.game.mouse_y
    update_stats_display()

def onMousePress(mouseX, mouseY):
    try_harvest_crop(mouseX, mouseY)

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