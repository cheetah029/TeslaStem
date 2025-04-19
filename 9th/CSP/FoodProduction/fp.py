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
    game.selected_food = None
    
    # Production facility dimensions and position
    game.facility_x = 350
    game.facility_y = 120
    
    # Conveyor belt parameters
    game.conveyor_x = 200
    game.conveyor_y = 200
    game.conveyor_width = 350  # Increased width
    game.conveyor_height = 30  # Increased height
    game.conveyor_items = []
    game.conveyor_timer = 0
    game.conveyor_spacing = 70  # Fixed spacing between food items
    game.conveyor_speed = 1.5   # Fixed speed for all food items
    
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
    
    # Background landscape (rural area)
    hills = Group()
    for i in range(3):
        hill = Oval(100 + i*150, 300, 200, 100, fill=rgb(34, 139, 34))
        hills.add(hill)
    
    # Farm fields in background
    fields = Group()
    for i in range(4):
        field = Rect(50 + i*80, 250, 60, 40, fill=rgb(139, 69, 19))
        fields.add(field)
    
    # Ground (factory floor)
    ground = Rect(0, 180, 400, 220, fill=rgb(169, 169, 169))
    
    # Factory elements
    factory = Group()
    
    # Factory walls
    wall_left = Rect(0, 130, 50, 50, fill=rgb(192, 192, 192))
    wall_right = Rect(350, 130, 50, 50, fill=rgb(192, 192, 192))
    
    # Factory windows
    for x in [20, 370]:
        window = Rect(x, 140, 20, 30, fill=rgb(135, 206, 235))
        factory.add(window)
    
    # Production facility
    facility = Group()
    
    # Main facility body
    facility_body = Rect(game.facility_x - 30, game.facility_y - 20, 60, 40, fill=rgb(70, 130, 180))
    
    # Conveyor belt
    conveyor = Rect(game.facility_x - 40, game.facility_y + 20, 80, 10, fill=rgb(100, 100, 100))  # Darker color
    conveyor_details = Group()
    for i in range(8):
        detail = Rect(game.facility_x - 40 + i*10, game.facility_y + 20, 5, 10, fill=rgb(80, 80, 80))  # Darker color
        conveyor_details.add(detail)
    
    # Control panel
    panel = Rect(game.facility_x - 25, game.facility_y - 15, 50, 30, fill=rgb(47, 79, 79))
    panel_details = Group()
    for i in range(3):
        button = Circle(game.facility_x - 15 + i*15, game.facility_y, 3, fill=rgb(255, 0, 0))
        panel_details.add(button)
    
    # Add all facility parts
    facility.add(facility_body)
    facility.add(conveyor)
    facility.add(conveyor_details)
    facility.add(panel)
    facility.add(panel_details)
    
    # Add all factory elements
    factory.add(wall_left)
    factory.add(wall_right)
    factory.add(facility)
    
    # Add background elements
    game.background.add(sky)
    game.background.add(hills)
    game.background.add(fields)
    game.background.add(ground)
    game.background.add(factory)
    game.background.add(game.waste)
    
    # Create main conveyor belt
    game.conveyor_belt = Group()
    
    # Conveyor belt base
    belt_base = Rect(game.conveyor_x - game.conveyor_width/2, 
                    game.conveyor_y - game.conveyor_height/2, 
                    game.conveyor_width, 
                    game.conveyor_height, 
                    fill=rgb(100, 100, 100))  # Darker color
    
    # Conveyor belt details (segments)
    belt_details = Group()
    segment_width = 30
    num_segments = int(game.conveyor_width / segment_width)
    
    for i in range(num_segments):
        x = game.conveyor_x - game.conveyor_width/2 + i * segment_width
        segment = Rect(x, game.conveyor_y - game.conveyor_height/2, 
                      segment_width, game.conveyor_height, 
                      fill=rgb(80, 80, 80))  # Darker color
        belt_details.add(segment)
    
    # Conveyor belt rollers
    rollers = Group()
    roller_spacing = 40
    num_rollers = int(game.conveyor_width / roller_spacing) + 1
    
    for i in range(num_rollers):
        x = game.conveyor_x - game.conveyor_width/2 + i * roller_spacing
        roller = Circle(x, game.conveyor_y + game.conveyor_height/2 + 5, 5, fill=rgb(192, 192, 192))
        rollers.add(roller)
    
    # Add all conveyor belt parts
    game.conveyor_belt.add(belt_base)
    game.conveyor_belt.add(belt_details)
    game.conveyor_belt.add(rollers)
    
    # Create mouse cursor indicator
    game.cursor_indicator = Group()
    
    # Create a circular cursor indicator
    cursor_outer = Circle(0, 0, 15, fill=None, border='white', borderWidth=2)
    cursor_inner = Circle(0, 0, 5, fill='white')
    
    # Add cursor parts
    game.cursor_indicator.add(cursor_outer)
    game.cursor_indicator.add(cursor_inner)
    
    # Create production indicator
    game.production_indicator = Group()
    indicator = Circle(game.facility_x, game.facility_y + 40, 10, fill='white', opacity=50)
    game.production_indicator.add(indicator)
    
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
    
    # Instructions
    game.instructions = Group(
        Label('Sustainable Food Production', 200, 16, size=16, bold=True),
        Label('Click on food items on the conveyor belt', 200, 350, size=14),
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

def create_food_item():
    """Create a food item for the conveyor belt"""
    food_group = Group()
    food_type = random.choice(['bread', 'apple', 'carrot', 'tomato', 'potato', 'corn', 'wheat'])
    food_group.food_type = food_type
    
    # Set position at the start of the conveyor belt
    x = app.game.conveyor_x - app.game.conveyor_width/2 + 20
    y = app.game.conveyor_y - 10
    
    if food_type == 'bread':
        # Bread loaf
        bread = Oval(x, y, 20, 10, fill=rgb(210, 180, 140))
        food_group.add(bread)
        
        # Bread details
        for i in range(3):
            detail = Line(x - 8 + i*8, y - 3, x - 8 + i*8, y + 3, 
                         fill=rgb(180, 150, 110), lineWidth=1)
            food_group.add(detail)
            
    elif food_type == 'apple':
        # Apple body
        apple = Circle(x, y, 8, fill='red')
        food_group.add(apple)
        
        # Apple stem
        stem = Line(x, y - 8, x, y - 12, fill=rgb(101, 67, 33), lineWidth=2)
        food_group.add(stem)
        
        # Apple leaf
        leaf = Oval(x + 2, y - 12, 6, 3, fill='green')
        food_group.add(leaf)
        
    elif food_type == 'carrot':
        # Carrot body
        carrot = Polygon(
            x - 5, y,
            x + 5, y,
            x + 3, y + 15,
            x - 3, y + 15,
            fill=rgb(255, 140, 0)
        )
        food_group.add(carrot)
        
        # Carrot top
        top = Polygon(
            x - 5, y,
            x + 5, y,
            x + 3, y - 8,
            x - 3, y - 8,
            fill='green'
        )
        food_group.add(top)
        
    elif food_type == 'tomato':
        # Tomato body
        tomato = Circle(x, y, 8, fill='red')
        food_group.add(tomato)
        
        # Tomato stem
        stem = Line(x, y - 8, x, y - 12, fill=rgb(101, 67, 33), lineWidth=2)
        food_group.add(stem)
        
    elif food_type == 'potato':
        # Potato body
        potato = Oval(x, y, 15, 10, fill=rgb(210, 180, 140))
        food_group.add(potato)
        
        # Potato eyes
        for i in range(2):
            eye = Circle(x - 5 + i*10, y - 3, 2, fill='black')
            food_group.add(eye)
            
    elif food_type == 'corn':
        # Corn cob
        cob = Oval(x, y, 15, 8, fill=rgb(255, 215, 0))
        food_group.add(cob)
        
        # Corn kernels
        for i in range(3):
            kernel = Circle(x - 5 + i*5, y, 2, fill=rgb(255, 200, 0))
            food_group.add(kernel)
            
    else:  # wheat
        # Wheat bundle
        bundle = Group()
        
        # Wheat stalks
        for i in range(5):
            stalk = Line(x - 10 + i*4, y + 5, x - 10 + i*4, y - 5, 
                        fill=rgb(139, 69, 19), lineWidth=1)
            bundle.add(stalk)
            
        food_group.add(bundle)
    
    # Set fixed movement properties
    food_group.speed = app.game.conveyor_speed
    food_group.centerX = x
    food_group.centerY = y
    food_group.selected = False
    
    return food_group

def spawn_crops():
    """Spawn new visible crops for harvesting"""
    # Adjust max visible crops based on production
    app.game.max_available_crops = max(1, min(3, int(1 + app.game.food_production / 10)))
    
    # Adjust spawn rate based on production
    spawn_chance = max(0.2, min(1.0, app.game.food_production / 30))
    
    while len(app.game.available_crops) < app.game.max_available_crops:
        if random.random() > spawn_chance:
            continue
        
        # Spawn crops in fixed positions on the factory floor
        # Use predefined positions instead of random ones
        positions = [(100, 200), (200, 200), (300, 200)]
        position_index = len(app.game.available_crops) % len(positions)
        x, y = positions[position_index]
        
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

def update_conveyor_belt():
    """Update conveyor belt and food items"""
    app.game.conveyor_timer += 1
    
    # Create new food items with fixed spacing
    if app.game.conveyor_timer >= 60:  # Every ~2 seconds
        app.game.conveyor_timer = 0
        
        # Check if we need a new food item
        if len(app.game.conveyor_items) < 5:  # Max 5 items on conveyor
            # Check if the last item has moved far enough to make space
            if not app.game.conveyor_items or app.game.conveyor_items[-1].centerX > app.game.conveyor_x - app.game.conveyor_width/2 + app.game.conveyor_spacing:
                food_item = create_food_item()
                app.game.conveyor_items.append(food_item)
    
    # Move existing food items at the same speed
    for food in app.game.conveyor_items[:]:  # Use slice copy to avoid modification while iterating
        food.centerX += app.game.conveyor_speed
        
        # Remove food if it reaches the end of the conveyor
        if food.centerX > app.game.conveyor_x + app.game.conveyor_width/2:
            food.visible = False
            app.game.conveyor_items.remove(food)
            
            # Increase food production when food reaches the end
            app.game.food_production = min(100, app.game.food_production + 1)

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

def create_waste():
    """Create a piece of waste"""
    # Create waste in fixed positions on the factory floor
    x = random.randint(50, 350)
    y = random.randint(200, 350)  # Only spawn in ground area
    
    waste_group = Group()
    waste_type = random.choice(['plastic', 'chemical', 'organic'])
    
    if waste_type == 'plastic':
        # Plastic container
        container = Rect(x-8, y-8, 16, 16, fill='lightBlue', opacity=80)
        waste_group.add(container)
        
        # Plastic lid
        lid = Circle(x, y-12, 5, fill='lightBlue', opacity=80)
        waste_group.add(lid)
        
    elif waste_type == 'chemical':
        # Chemical container
        container = Rect(x-6, y-10, 12, 20, fill='purple', opacity=70)
        waste_group.add(container)
        
        # Chemical label
        label = Rect(x-4, y-8, 8, 12, fill='white', opacity=50)
        waste_group.add(label)
        
    else:  # organic
        # Food waste
        waste = Oval(x-8, y-8, 16, 12, fill='brown')
        waste_group.add(waste)
        
        # Mold spots
        for i in range(3):
            spot = Circle(x-6 + i*6, y-6 + i*2, 2, fill='green')
            waste_group.add(spot)
    
    waste_group.waste_type = waste_type
    
    return waste_group

def update_waste():
    """Update waste positions and create new waste"""
    app.game.waste_timer += 1
    
    # Create new waste
    if app.game.waste_timer >= 300:  # Every ~10 seconds
        app.game.waste_timer = 0
        if len(app.game.waste.children) < 2:  # Max 2 pieces of waste
            waste = create_waste()
            waste.centerX = random.randint(50, 350)
            waste.centerY = random.randint(200, 350)
            app.game.waste.add(waste)
            app.game.pollution_level = min(500, app.game.pollution_level + 100)
    
    # Waste no longer moves - it stays in place
    # This removes the floating behavior from the fishing simulator

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

def update_cursor_indicator():
    """Update cursor indicator position based on mouse"""
    if not app.game.game_over:
        # Update cursor indicator position
        app.game.cursor_indicator.centerX = app.game.mouse_x
        app.game.cursor_indicator.centerY = app.game.mouse_y
        
        # Update production indicator position
        indicator = app.game.production_indicator.children[0]
        indicator.centerX = app.game.mouse_x
        indicator.centerY = app.game.mouse_y

def try_harvest_crop(mouse_x, mouse_y):
    """Attempt to interact with food items on the conveyor belt"""
    if app.game.game_over:
        return
    
    # Check if a food item is being clicked
    for food in app.game.conveyor_items[:]:
        # Simple distance check for food items
        distance = math.sqrt((food.centerX - mouse_x)**2 + (food.centerY - mouse_y)**2)
        if distance < 15:  # Click radius
            # Food item clicked
            if app.game.produced_food_today >= 5:
                return False
            
            # Mark food as selected
            food.selected = True
            app.game.selected_food = food
            
            # Update production counter
            app.game.produced_food_today += 1
            app.game.produced_food_types.append(food.food_type)
            app.game.stats.children[3].value = f'Produced Today: {app.game.produced_food_today}/5'
            
            # Increase food level
            food_increase = min(15, 5 + random.randint(0, 5))
            app.game.food_level = min(100, app.game.food_level + food_increase)
            
            # Remove food from conveyor
            food.visible = False
            app.game.conveyor_items.remove(food)
            app.game.selected_food = None
            
            if app.game.produced_food_today >= 5:
                end_day()
            return True
    
    # Check if waste is being clicked
    for waste in app.game.waste.children:
        if waste.hits(mouse_x, mouse_y):
            app.game.waste.remove(waste)
            waste.visible = False
            
            remaining_waste = len(app.game.waste.children)
            min_pollution = remaining_waste * 100
            new_pollution = max(min_pollution, app.game.pollution_level - 150)
            app.game.pollution_level = new_pollution
            
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

def onAppStart():
    app.game = create_game()
    app.stepsPerSecond = 30

def onStep():
    if not app.game.game_over:
        app.game.time += 1
        spawn_crops()
        update_cursor_indicator()
        update_waste()
        update_conveyor_belt()
        update_hunger_bar()
        
        # Check for game over conditions immediately
        if app.game.food_level <= 0 or app.game.pollution_level >= 500:
            check_game_over()
        
        # Crops no longer move or follow the mouse
        # They stay in their fixed positions
        
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