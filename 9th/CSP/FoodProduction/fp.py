# Sustainable Food Production Game

# Goal is to sustainably grow food for the population to survive for 20 days.
# The player must balance food production with waste and pollution management.

from cmu_graphics import *
import random
import math
import time

def create_game():
    game = Group()

    # Initial game parameters
    game.food_production = 0
    game.food_decrease_base = 15  # Reduced from 50 to make hunger more manageable
    game.food_level = 75
    game.food_waste = 0
    game.day = 1
    game.target_days = 20
    game.game_over = False
    game.time = 0
    game.produced_food_today = 0
    game.produced_food_types = []
    
    # New balance parameters
    game.food_production_pollution = 20  # Pollution per food item produced
    game.food_production_waste = 15      # Waste increase per food item
    game.waste_pollution_factor = 2      # How much waste contributes to pollution
    game.correct_sort_reduction = 25     # How much correct sorting reduces waste
    game.correct_sort_pollution_reduction = 15  # How much correct sorting reduces pollution
    game.incorrect_sort_waste_increase = 20     # How much incorrect sorting increases waste
    game.incorrect_sort_pollution_increase = 10 # How much incorrect sorting increases pollution
    game.daily_food_decrease = 25        # Increased from 10 to 25 to make hunger more challenging
    
    # Mouse position tracking
    game.mouse_x = 200
    game.mouse_y = 200
    game.selected_food = None
    game.selected_waste = None
    
    # Production facility dimensions and position
    game.facility_x = 350
    game.facility_y = 120
    
    # Conveyor belt parameters
    game.conveyor_x = 200
    game.conveyor_y = 200
    game.conveyor_width = 450  # Even wider conveyor belt
    game.conveyor_height = 40  # Thicker conveyor belt
    game.conveyor_items = []
    game.conveyor_timer = 0
    game.conveyor_spacing = 70
    game.conveyor_speed = 1.5
    
    # Waste and pollution visualization
    game.waste = Group()
    game.waste_timer = 0
    game.pollution_level = 0
    
    # Feedback system
    game.feedback_timer = None
    game.feedback_label = None
    game.feedback_group = Group()  # New dedicated feedback group
    
    # Create feedback box and label
    game.feedback_box = Rect(50, 220, 300, 30, fill='white', border='red', opacity=80)
    game.feedback_text = Label('', 200, 235, size=12, fill='red', bold=True)
    game.feedback_group.add(game.feedback_box)
    game.feedback_group.add(game.feedback_text)
    game.feedback_group.visible = False
    
    # game.add(game.feedback_group)  # Add feedback group to game
    game.feedback_group.toFront()  # Ensure feedback is always on top
    
    # Designated areas
    game.trash_area_x = 350  # Right side trash area
    game.trash_area_y = 250  # Original position
    game.compost_area_x = 50  # Left side compost area
    game.compost_area_y = 250  # Same height as trash area
    
    # Waste sorting parameters
    game.waste_to_sort = []  # List of waste items waiting to be sorted
    game.max_waste_to_sort = 3  # Maximum number of waste items that can be waiting to be sorted
    game.sorting_correct = 0  # Counter for correctly sorted waste
    game.sorting_incorrect = 0  # Counter for incorrectly sorted waste
    
    # Food selection parameters
    game.food_selection_mode = False
    game.selected_food_type = None
    game.food_options = ['bread', 'apple', 'carrot', 'tomato', 'potato', 'corn', 'wheat']
    game.food_option_buttons = []
    
    # Food collection parameters
    game.selected_food = None
    game.food_collection_area_x = 200
    game.food_collection_area_y = 150
    game.food_collection_area_width = 100
    game.food_collection_area_height = 60
    game.food_collection_area = None
    game.food_collection_count = 0
    game.food_collection_target = 5
    
    # Create UI elements
    game.background = Group()
    
    # Sky and ground
    sky = Rect(0, 0, 400, 400, fill='skyBlue')
    
    # # Background landscape (rural area)
    # hills = Group()
    # for i in range(3):
    #     hill = Oval(100 + i*150, 300, 200, 100, fill=rgb(34, 139, 34))
    #     hills.add(hill)
    
    # # Farm fields in background
    # fields = Group()
    # for i in range(4):
    #     field = Rect(50 + i*80, 250, 60, 40, fill=rgb(139, 69, 19))
    #     fields.add(field)
    
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
    conveyor = Rect(game.facility_x - 40, game.facility_y + 20, 80, 10, fill=rgb(100, 100, 100))
    conveyor_details = Group()
    for i in range(8):
        detail = Rect(game.facility_x - 40 + i*10, game.facility_y + 20, 5, 10, fill=rgb(80, 80, 80))
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
    # game.background.add(hills)
    # game.background.add(fields)
    game.background.add(ground)
    game.background.add(factory)
    # game.background.add(game.waste)
    
    # Create main conveyor belt
    game.conveyor_belt = Group()
    
    # Conveyor belt base
    belt_base = Rect(game.conveyor_x - game.conveyor_width/2, 
                    game.conveyor_y - game.conveyor_height/2, 
                    game.conveyor_width, 
                    game.conveyor_height, 
                    fill=rgb(80, 80, 80))  # Darker gray for better visibility
    
    # Conveyor belt details (segments)
    belt_details = Group()
    segment_width = 30
    num_segments = int(game.conveyor_width / segment_width)
    
    for i in range(num_segments):
        x = game.conveyor_x - game.conveyor_width/2 + i * segment_width
        segment = Rect(x, game.conveyor_y - game.conveyor_height/2, 
                      segment_width, game.conveyor_height, 
                      fill=rgb(60, 60, 60))  # Even darker for segments
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
    cursor_middle = Circle(0, 0, 10, fill='white', opacity=50)
    
    # Add cursor parts
    game.cursor_indicator.add(cursor_outer)
    game.cursor_indicator.add(cursor_inner)
    game.cursor_indicator.add(cursor_middle)
    
    # Create stats panel
    game.stats_panel = Group()
    
    # Stats panel background
    stats_panel_bg = Rect(10, 10, 150, 140, fill=rgb(50, 50, 50), opacity=80)
    game.stats_panel.add(stats_panel_bg)
    
    # Stats labels - all left-aligned with the same left value
    # Create individual label variables to ensure consistent left alignment
    game.day_label = Label('Day: 1/20', 20, 25, size=12, fill='white', align='left')
    game.produced_label = Label('Produced: 0/5', 20, 45, size=12, fill='white', align='left')
    game.food_label = Label(f'Food: {game.food_level}%', 20, 65, size=12, fill='white', align='left')
    game.waste_label = Label('Waste: 0%', 20, 85, size=12, fill='white', align='left')
    game.pollution_label = Label('Pollution: 0%', 20, 105, size=12, fill='white', align='left')
    game.sorting_label = Label('Sorting: 0/0', 20, 125, size=12, fill='white', align='left')
    
    # Add labels to panel
    game.stats_panel.add(game.day_label)
    game.stats_panel.add(game.produced_label)
    game.stats_panel.add(game.food_label)
    game.stats_panel.add(game.waste_label)
    game.stats_panel.add(game.pollution_label)
    game.stats_panel.add(game.sorting_label)
    
    # Create hunger bar - moved closer to the text
    game.hunger_bar = Group()
    bar_width = 80
    bar_height = 10
    bar_x = 100  # Moved left to be closer to text
    bar_y = 65  # Aligned with food text
    
    # Background and border
    bar_bg = Rect(bar_x, bar_y, bar_width, bar_height, fill='darkGray')
    bar_border = Rect(bar_x, bar_y, bar_width, bar_height, 
                     fill=None, border='black', borderWidth=1)
    
    # Fill bar and shine effect - shortened to fit within border
    bar_fill = Rect(bar_x + 1, bar_y + 1, bar_width - 2, bar_height - 2, 
                    fill=rgb(50, 205, 50))
    shine = Polygon(
        bar_x + 1, bar_y + 1,
        bar_x + bar_width - 1, bar_y + 1,
        bar_x + bar_width - 1, bar_y + 3,
        bar_x + 1, bar_y + 3,
        fill=rgb(255, 255, 255), opacity=20
    )
    
    game.hunger_bar.add(bar_bg)
    game.hunger_bar.add(bar_fill)
    game.hunger_bar.add(shine)
    game.hunger_bar.add(bar_border)
    
    # Create food waste meter - moved closer to the text
    game.waste_meter = Group()
    waste_bar_width = 80
    waste_bar_height = 10
    waste_bar_x = 100  # Moved left to be closer to text
    waste_bar_y = 85  # Aligned with waste text
    
    # Background and border
    waste_bar_bg = Rect(waste_bar_x, waste_bar_y, waste_bar_width, waste_bar_height, fill='darkGray')
    waste_bar_border = Rect(waste_bar_x, waste_bar_y, waste_bar_width, waste_bar_height, 
                     fill=None, border='black', borderWidth=1)
    
    # Fill bar and shine effect - shortened to fit within border
    waste_bar_fill = Rect(waste_bar_x + 1, waste_bar_y + 1, waste_bar_width - 2, waste_bar_height - 2, 
                    fill=rgb(139, 69, 19))  # Brown color for waste
    waste_shine = Polygon(
        waste_bar_x + 1, waste_bar_y + 1,
        waste_bar_x + waste_bar_width - 1, waste_bar_y + 1,
        waste_bar_x + waste_bar_width - 1, waste_bar_y + 3,
        waste_bar_x + 1, waste_bar_y + 3,
        fill=rgb(255, 255, 255), opacity=20
    )
    
    game.waste_meter.add(waste_bar_bg)
    game.waste_meter.add(waste_bar_fill)
    game.waste_meter.add(waste_shine)
    game.waste_meter.add(waste_bar_border)
    
    # Create pollution meter - moved closer to the text
    game.pollution_meter = Group()
    pollution_bar_width = 80
    pollution_bar_height = 10
    pollution_bar_x = 100  # Moved left to be closer to text
    pollution_bar_y = 105  # Aligned with pollution text
    
    # Background and border
    pollution_bar_bg = Rect(pollution_bar_x, pollution_bar_y, pollution_bar_width, pollution_bar_height, fill='darkGray')
    pollution_bar_border = Rect(pollution_bar_x, pollution_bar_y, pollution_bar_width, pollution_bar_height, 
                     fill=None, border='black', borderWidth=1)
    
    # Fill bar and shine effect - shortened to fit within border
    pollution_bar_fill = Rect(pollution_bar_x + 1, pollution_bar_y + 1, pollution_bar_width - 2, pollution_bar_height - 2, 
                    fill=rgb(128, 128, 128))  # Gray color for pollution
    pollution_shine = Polygon(
        pollution_bar_x + 1, pollution_bar_y + 1,
        pollution_bar_x + pollution_bar_width - 1, pollution_bar_y + 1,
        pollution_bar_x + pollution_bar_width - 1, pollution_bar_y + 3,
        pollution_bar_x + 1, pollution_bar_y + 3,
        fill=rgb(255, 255, 255), opacity=20
    )
    
    game.pollution_meter.add(pollution_bar_bg)
    game.pollution_meter.add(pollution_bar_fill)
    game.pollution_meter.add(pollution_shine)
    game.pollution_meter.add(pollution_bar_border)
    
    # Create compost area indicator
    game.compost_area = Group()
    compost_area_rect = Rect(game.compost_area_x - 30, game.compost_area_y - 22, 60, 60, 
                         fill=None, border='green', borderWidth=2, opacity=50)
    game.compost_area.add(compost_area_rect)
    
    # Create trash area indicator
    game.trash_area = Group()
    trash_area_rect = Rect(game.trash_area_x - 30, game.trash_area_y - 22, 60, 60, 
                          fill=None, border='red', borderWidth=2, opacity=50)
    game.trash_area.add(trash_area_rect)
    
    # Create left side computer monitor (compost monitor)
    game.left_monitor = Group()
    
    # Monitor base
    monitor_base = Rect(30, 300, 40, 10, fill=rgb(50, 50, 50))
    
    # Monitor stand
    monitor_stand = Rect(40, 310, 20, 10, fill=rgb(50, 50, 50))
    
    # Monitor screen
    monitor_screen = Rect(20, 250, 60, 50, fill=rgb(0, 0, 0))
    
    # Monitor frame
    monitor_frame = Rect(15, 245, 70, 60, fill=rgb(100, 100, 100))
    
    # Monitor details
    monitor_details = Group()
    for i in range(3):
        button = Circle(25 + i*15, 270, 2, fill=rgb(255, 0, 0))
        monitor_details.add(button)
    
    # Add label
    monitor_label = Label('COMPOST', 50, 240, size=10, fill='white', bold=True)
    monitor_details.add(monitor_label)
    
    # Add all monitor parts
    game.left_monitor.add(monitor_base)
    game.left_monitor.add(monitor_stand)
    game.left_monitor.add(monitor_screen)
    game.left_monitor.add(monitor_frame)
    game.left_monitor.add(monitor_details)
    
    # Create right side computer monitor (waste monitor)
    game.right_monitor = Group()
    
    # Monitor base
    right_monitor_base = Rect(330, 300, 40, 10, fill=rgb(50, 50, 50))
    
    # Monitor stand
    right_monitor_stand = Rect(340, 310, 20, 10, fill=rgb(50, 50, 50))
    
    # Monitor screen
    right_monitor_screen = Rect(320, 250, 60, 50, fill=rgb(0, 0, 0))
    
    # Monitor frame
    right_monitor_frame = Rect(315, 245, 70, 60, fill=rgb(100, 100, 100))
    
    # Monitor details
    right_monitor_details = Group()
    for i in range(3):
        button = Circle(325 + i*15, 270, 2, fill=rgb(255, 0, 0))
        right_monitor_details.add(button)
    
    # Add label
    right_monitor_label = Label('TRASH', 350, 240, size=10, fill='white', bold=True)
    right_monitor_details.add(right_monitor_label)
    
    # Add all monitor parts
    game.right_monitor.add(right_monitor_base)
    game.right_monitor.add(right_monitor_stand)
    game.right_monitor.add(right_monitor_screen)
    game.right_monitor.add(right_monitor_frame)
    game.right_monitor.add(right_monitor_details)
    
    # Create waste sorting area
    game.sorting_area = Group()
    sorting_area_rect = Rect(150, 250, 100, 80, 
                           fill=None, border='yellow', borderWidth=2, opacity=50)
    game.sorting_area.add(sorting_area_rect)
    
    # Create waste sorting instructions
    game.sorting_instructions = Group(
        Label('Sort waste here', 200, 230, size=12, fill='black'),
        Label('Organic → Compost', 200, 245, size=10, fill='green'),
        Label('Plastic/Chemical → Trash', 200, 260, size=10, fill='red')
    )
    
    # # Create food selection panel
    # game.food_selection_panel = Group()
    # food_panel_bg = Rect(150, 100, 100, 120, fill=rgb(50, 50, 50), opacity=80)
    # food_panel_title = Label('Select Food Type', 200, 110, size=14, fill='white', bold=True)
    # game.food_selection_panel.add(food_panel_bg)
    # game.food_selection_panel.add(food_panel_title)
    # game.food_selection_panel.visible = False
    
    # Create food collection area
    game.food_collection_area = Group()
    
    # Collection area background
    collection_area_bg = Rect(game.food_collection_area_x - game.food_collection_area_width/2,
                            game.food_collection_area_y - game.food_collection_area_height/2,
                            game.food_collection_area_width,
                            game.food_collection_area_height,
                            fill=rgb(70, 130, 180), opacity=80)
    
    # Collection area border
    collection_area_border = Rect(game.food_collection_area_x - game.food_collection_area_width/2,
                                game.food_collection_area_y - game.food_collection_area_height/2,
                                game.food_collection_area_width,
                                game.food_collection_area_height,
                                fill=None, border='white', borderWidth=2)
    
    # Collection area label 1
    collection_area_label1 = Label('PROCESS', 
                                game.food_collection_area_x, 
                                game.food_collection_area_y - 20, 
                                size=12, fill='white', bold=True)

    # Collection area label 2
    collection_area_label2 = Label('FOOD HERE', 
                                game.food_collection_area_x, 
                                game.food_collection_area_y - 5, 
                                size=12, fill='white', bold=True)
    
    # Collection area counter
    collection_area_counter = Label('0/5', 
                                  game.food_collection_area_x, 
                                  game.food_collection_area_y + 10, 
                                  size=14, fill='white', bold=True)
    
    # Add all collection area parts
    game.food_collection_area.add(collection_area_bg)
    game.food_collection_area.add(collection_area_border)
    game.food_collection_area.add(collection_area_label1)
    game.food_collection_area.add(collection_area_label2)
    game.food_collection_area.add(collection_area_counter)
    
    # Instructions
    game.instructions = Group(
        Label('Sustainable Food Production', 200, 16, size=16, bold=True),
        Label('Click food on conveyor to collect it', 200, 350, size=14),
        Label('Drop food in processing area to produce', 200, 370, size=14),
        Label('Click waste, then click a bin to sort. Press D to end the day', 200, 390, size=14),
        # Label('Press D to end the day', 200, 410, size=14)
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

# def create_crop_colors():
#     """Create a random crop color scheme"""
#     # Base colors for crops
#     base_colors = [
#         rgb(0, 128, 0),  # Green
#         rgb(255, 215, 0),  # Golden
#         rgb(255, 140, 0),  # Dark orange
#         rgb(139, 69, 19),  # Brown
#         rgb(128, 128, 0),  # Olive
#     ]
#     main_color = random.choice(base_colors)
#     # Make detail color slightly different
#     detail_color = rgb(min(255, main_color.red + 20),
#                      min(255, main_color.green + 20),
#                      min(255, main_color.blue + 20))
#     return main_color, detail_color

def create_food_item():
    """Create a food item for the conveyor belt"""
    food_group = Group()
    food_type = random.choice(['bread', 'apple', 'carrot', 'tomato', 'potato', 'corn', 'mushroom', 'wheat'])
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
        
        # # Tomato stem
        # stem = Line(x, y - 8, x, y - 12, fill=rgb(101, 67, 33), lineWidth=2)
        # food_group.add(stem)

        # # Tomato top
        # top = Oval(x, y - 5, 4, 3, fill='orange')
        # food_group.add(top)

        # Tomato leaves
        leaf1 = Line(x, y - 5, x - 5, y - 9, fill='green')
        leaf2 = Line(x, y - 5, x, y - 11, fill='green')
        leaf3 = Line(x, y - 5, x + 5, y - 9, fill='green')
        food_group.add(leaf1)
        food_group.add(leaf2)
        food_group.add(leaf3)
        
    elif food_type == 'potato':
        # Potato body - improved design without prominent eyes
        potato = Oval(x, y, 15, 10, fill=rgb(210, 180, 140))
        food_group.add(potato)
        
        # Potato texture - subtle bumps instead of eyes
        for i in range(3):
            bump = Circle(x - 5 + i*5, y, 1, fill=rgb(180, 150, 110))
            food_group.add(bump)
            
    elif food_type == 'corn':
        # Corn cob
        cob = Oval(x, y, 15, 8, fill=rgb(255, 215, 0))
        food_group.add(cob)
        
        # Corn kernels
        for i in range(3):
            kernel = Circle(x - 5 + i*5, y, 2, fill=rgb(255, 200, 0))
            food_group.add(kernel)
            
    elif food_type == 'mushroom':
        # Mushroom cap and stem body
        potato = Oval(x, y, 15, 10, fill=rgb(210, 180, 140))
        food_group.add(potato)

        # Covering for stem
        for i in range(2):
            eye = Circle(x - 5 + i*10, y + 3, 2, fill='black')
            food_group.add(eye)

    else:  # wheat
        # Wheat bundle
        bundle = Group()
        
        # Wheat stem
        stem = Line(x, y - 9, x, y + 20, fill='beige')
        bundle.add(stem)
        
        # Wheat stalks
        for i in range(5):
            stalk = Line(x - 5, y - 5 + i*4, x + 5, y - 5 + i*4, 
                        fill=rgb(210, 180, 140))
            bundle.add(stalk)
            
        food_group.add(bundle)
    
    # Set fixed movement properties
    food_group.speed = app.game.conveyor_speed
    food_group.centerX = x
    food_group.centerY = y
    food_group.selected = False
    
    return food_group

# def spawn_crops():
#     """Spawn new visible crops for harvesting"""
#     # Adjust max visible crops based on production
#     app.game.max_available_crops = max(1, min(3, int(1 + app.game.food_production / 10)))
    
#     # Adjust spawn rate based on production
#     spawn_chance = max(0.2, min(1.0, app.game.food_production / 30))
    
#     while len(app.game.available_crops) < app.game.max_available_crops:
#         if random.random() > spawn_chance:
#             continue
        
#         # Spawn crops in the designated crop area
#         # Use positions within the crop area
#         positions = [
#             (app.game.crop_area_x, app.game.crop_area_y),
#             (app.game.crop_area_x - 15, app.game.crop_area_y + 15),
#             (app.game.crop_area_x + 15, app.game.crop_area_y + 15)
#         ]
#         position_index = len(app.game.available_crops) % len(positions)
#         x, y = positions[position_index]
        
#         size_scale = random.randint(1, 10)
#         size = 20 + (size_scale - 1) * 2
        
#         # Create crop shape
#         crop_group = Group()
#         crop_group.harvested = False
        
#         # Random crop colors
#         main_color, detail_color = create_crop_colors()
        
#         # Create crop components
#         crop_type = random.choice(['wheat', 'corn', 'potato', 'tomato', 'carrot'])
#         crop_group.crop_type = crop_type
        
#         # Add crop health indicator
#         crop_group.health = 100
#         crop_group.health_indicator = Circle(0, -size/2 - 10, 5, fill='green')
#         crop_group.add(crop_group.health_indicator)
        
#         # Add crop type indicator
#         crop_group.type_indicator = Label(crop_type[0].upper(), 0, -size/2 - 10, size=8, fill='white', bold=True)
#         crop_group.add(crop_group.type_indicator)
        
#         if crop_type == 'wheat':
#             # Wheat stalk
#             stalk = Line(0, 0, 0, size * 1.5, fill=rgb(139, 69, 19), lineWidth=2)
#             crop_group.add(stalk)
            
#             # Wheat head
#             head = Oval(0, -size/2, size, size/2, fill=main_color)
#             crop_group.add(head)
            
#             # Wheat details
#             for i in range(5):
#                 detail = Line(-size/2, -size/2 + i*size/4, size/2, -size/2 + i*size/4, 
#                              fill=detail_color, lineWidth=1)
#                 crop_group.add(detail)
                
#         elif crop_type == 'corn':
#             # Corn stalk
#             stalk = Line(0, 0, 0, size * 1.5, fill=rgb(139, 69, 19), lineWidth=2)
#             crop_group.add(stalk)
            
#             # Corn cob
#             cob = Oval(0, -size/2, size/2, size, fill=main_color)
#             crop_group.add(cob)
            
#             # Corn kernels
#             for i in range(3):
#                 kernel = Circle(0, -size/2 + i*size/2, size/6, fill=detail_color)
#                 crop_group.add(kernel)
                
#         elif crop_type == 'potato':
#             # Potato plant
#             plant = Polygon(
#                 -size/2, 0,
#                 size/2, 0,
#                 size/3, -size,
#                 -size/3, -size,
#                 fill=rgb(0, 100, 0)
#             )
#             crop_group.add(plant)
            
#             # Potato
#             potato = Oval(0, size/4, size, size/2, fill=main_color)
#             crop_group.add(potato)
            
#             # Potato texture - subtle bumps instead of eyes
#             for i in range(3):
#                 bump = Circle(-size/4 + i*size/2, size/4, 1, fill=rgb(180, 150, 110))
#                 crop_group.add(bump)
                
#         elif crop_type == 'tomato':
#             # Tomato plant
#             plant = Polygon(
#                 -size/2, 0,
#                 size/2, 0,
#                 size/3, -size,
#                 -size/3, -size,
#                 fill=rgb(0, 100, 0)
#             )
#             crop_group.add(plant)
            
#             # Tomato
#             tomato = Circle(0, size/4, size/2, fill=main_color)
#             crop_group.add(tomato)
            
#             # Tomato stem
#             stem = Line(0, size/4 - size/2, 0, size/4, fill=rgb(0, 100, 0), lineWidth=2)
#             crop_group.add(stem)
            
#         else:  # carrot
#             # Carrot top
#             top = Polygon(
#                 -size/2, 0,
#                 size/2, 0,
#                 size/3, -size,
#                 -size/3, -size,
#                 fill=rgb(0, 100, 0)
#             )
#             crop_group.add(top)
            
#             # Carrot
#             carrot = Polygon(
#                 -size/4, 0,
#                 size/4, 0,
#                 size/6, size,
#                 -size/6, size,
#                 fill=main_color
#             )
#             crop_group.add(carrot)
        
#         # Store size information
#         crop_group.crop_size = size
#         crop_group.size_scale = size_scale
        
#         # Set position
#         crop_group.centerX = x
#         crop_group.centerY = y
        
#         # Add crop to available crops
#         app.game.available_crops.append(crop_group)
        
#         # Add crop to game
#         app.game.background.add(crop_group)

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
        # Clear any selected items
        if app.game.selected_food:
            app.game.selected_food.visible = False
            app.game.selected_food = None
        if app.game.selected_waste:
            app.game.selected_waste.visible = False
            app.game.selected_waste = None
        return True
    elif app.game.pollution_level >= 500:
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()
        app.game.game_over_screen.children[1].value = 'GAME OVER'
        app.game.game_over_screen.children[2].value = 'The environment has become too polluted!'
        app.game.game_over_screen.children[3].value = f'Final food production: {app.game.food_production}'
        # Clear any selected items
        if app.game.selected_food:
            app.game.selected_food.visible = False
            app.game.selected_food = None
        if app.game.selected_waste:
            app.game.selected_waste.visible = False
            app.game.selected_waste = None
        return True
    elif app.game.food_waste >= 100:  # New waste-based game over condition
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()
        app.game.game_over_screen.children[1].value = 'GAME OVER'
        app.game.game_over_screen.children[2].value = 'Waste management has failed! The facility is overwhelmed with waste!'
        app.game.game_over_screen.children[3].value = f'Final food production: {app.game.food_production}'
        # # Clear any selected items
        # if app.game.selected_food:
        #     app.game.selected_food.visible = False
        #     app.game.selected_food = None
        # if app.game.selected_waste:
        #     app.game.selected_waste.visible = False
        #     app.game.selected_waste = None
        return True
    elif app.game.day >= app.game.target_days:
        app.game.game_over = True
        app.game.game_over_screen.visible = True
        app.game.game_over_screen.toFront()
        app.game.game_over_screen.children[1].value = 'YOU WIN!'
        app.game.game_over_screen.children[2].value = 'Congratulations! You kept the community fed for 20 days!'
        app.game.game_over_screen.children[3].value = f'Final food production: {app.game.food_production}'
        update_hunger_bar()
        # Clear any selected items
        if app.game.selected_food:
            app.game.selected_food.visible = False
            app.game.selected_food = None
        if app.game.selected_waste:
            app.game.selected_waste.visible = False
            app.game.selected_waste = None
        return True
    return False

def create_waste(size_scale=1):
    # Define waste types with their correct destinations and descriptions
    waste_types = [
        # Compostable waste (organic materials that can decompose)
        {
            'type': 'apple_peels',
            'destination': 'compost',
            'description': 'Apple peels',
            'color': 'red',
            'shape': 'apple'
        },
        {
            'type': 'corn_husks',
            'destination': 'compost',
            'description': 'Corn husks',
            'color': 'yellow',
            'shape': 'corn'
        },
        {
            'type': 'potato_skins',
            'destination': 'compost',
            'description': 'Potato skins',
            'color': 'brown',
            'shape': 'potato'
        },
        {
            'type': 'carrot_tops',
            'destination': 'compost',
            'description': 'Carrot tops',
            'color': 'green',
            'shape': 'carrot'
        },
        {
            'type': 'rice_hulls',
            'destination': 'compost',
            'description': 'Rice hulls',
            'color': 'tan',
            'shape': 'rice'
        },
        
        # Non-compostable waste (materials that shouldn't decompose)
        {
            'type': 'plastic_wrappers',
            'destination': 'trash',
            'description': 'Plastic wrappers',
            'color': 'blue',
            'shape': 'wrapper'
        },
        {
            'type': 'tin_cans',
            'destination': 'trash',
            'description': 'Tin cans',
            'color': 'gray',
            'shape': 'can'
        },
        {
            'type': 'rubber_bands',
            'destination': 'trash',
            'description': 'Rubber bands',
            'color': 'black',
            'shape': 'band'
        },
        {
            'type': 'twine',
            'destination': 'trash',
            'description': 'Twine',
            'color': 'white',
            'shape': 'twine'
        },
        {
            'type': 'labels',
            'destination': 'trash',
            'description': 'Labels',
            'color': 'red',
            'shape': 'label'
        }
    ]
    
    # Create waste group
    waste = Group()
    
    # Randomly select a waste type
    waste_type = random.choice(waste_types)
    
    # Create waste item based on type
    if waste_type['shape'] == 'apple':
        # Apple core with peels
        core = Circle(0, 0, 10 * size_scale, fill='white')
        peel1 = Arc(0, 0, 20 * size_scale, 20 * size_scale, 0, 180, fill='red')
        peel2 = Arc(0, 0, 20 * size_scale, 20 * size_scale, 180, 180, fill='red')
        stem = Line(0, -10 * size_scale, 0, -15 * size_scale, fill='brown', lineWidth=2)
        leaf = Oval(2 * size_scale, -15 * size_scale, 6 * size_scale, 3 * size_scale, fill='green')
        waste.add(core)
        waste.add(peel1)
        waste.add(peel2)
        waste.add(stem)
        waste.add(leaf)
        
    elif waste_type['shape'] == 'corn':
        # Corn cob with partially peeled husks
        cob = Oval(0, 0, 8 * size_scale, 15 * size_scale, fill='yellow')
        waste.add(cob)
        # Add some kernel texture
        for i in range(3):
            kernel = Circle(0, -5 * size_scale + i*5 * size_scale, 0.5 * size_scale, fill=rgb(255, 200, 0))
            waste.add(kernel)
        
        # Add two husks that are partially peeled back
        husk1 = Arc(0, 10 * size_scale, 20 * size_scale, 15 * size_scale, 180, 135, fill='lightGreen')
        husk2 = Arc(0, 10 * size_scale, 20 * size_scale, 15 * size_scale, 45, 135, fill='lightGreen')
        waste.add(husk1)
        waste.add(husk2)
        
    elif waste_type['shape'] == 'potato':
        # Potato with skin
        potato = Oval(0, 0, 15 * size_scale, 10 * size_scale, fill='brown')
        skin = Arc(0, 0, 20 * size_scale, 15 * size_scale, 0, 180, fill='tan')
        eye1 = Circle(-5 * size_scale, -2 * size_scale, 1 * size_scale, fill='black')
        eye2 = Circle(5 * size_scale, 2 * size_scale, 1 * size_scale, fill='black')
        waste.add(potato)
        waste.add(skin)
        waste.add(eye1)
        waste.add(eye2)
        
    elif waste_type['shape'] == 'carrot':
        # Carrot top with greens
        carrot = Polygon(-5 * size_scale, 0, 5 * size_scale, 0, 3 * size_scale, 15 * size_scale, -3 * size_scale, 15 * size_scale, fill='orange')
        greens = Group()
        for i in range(5):
            leaf = Line(-5 * size_scale + i*2.5 * size_scale, 0, -3 * size_scale + i*2.5 * size_scale, -8 * size_scale, fill='green', lineWidth=2)
            greens.add(leaf)
        waste.add(carrot)
        waste.add(greens)
        
    elif waste_type['shape'] == 'rice':
        # Rice hulls
        hulls = Group()
        for i in range(3):
            hull = Oval(-10 * size_scale + i*10 * size_scale, 0, 8 * size_scale, 4 * size_scale, fill='tan')
            hulls.add(hull)
        waste.add(hulls)
        
    elif waste_type['shape'] == 'wrapper':
        # Plastic wrapper
        wrapper = Rect(-10 * size_scale, -5 * size_scale, 20 * size_scale, 10 * size_scale, fill='lightBlue')
        fold1 = Line(-10 * size_scale, 0, 10 * size_scale, 0, fill='white', lineWidth=1)
        fold2 = Line(0, -5 * size_scale, 0, 5 * size_scale, fill='white', lineWidth=1)
        waste.add(wrapper)
        waste.add(fold1)
        waste.add(fold2)
        
    elif waste_type['shape'] == 'can':
        # Tin can
        can = Rect(-6 * size_scale, -12 * size_scale, 12 * size_scale, 24 * size_scale, fill='silver')
        top = Circle(0, -12 * size_scale, 6 * size_scale, fill='silver')
        bottom = Circle(0, 12 * size_scale, 6 * size_scale, fill='silver')
        rim = Circle(0, -12 * size_scale, 6 * size_scale, fill=None, border='gray', borderWidth=1)
        waste.add(can)
        waste.add(top)
        waste.add(bottom)
        waste.add(rim)
        
    elif waste_type['shape'] == 'band':
        # Rubber band
        band = Circle(0, 0, 12 * size_scale, fill=None, border='black', borderWidth=3)
        waste.add(band)
        
    elif waste_type['shape'] == 'twine':
        # Twine
        twine = Group()
        for i in range(3):
            strand = Line(-15 * size_scale + i*15 * size_scale, -2 * size_scale, -15 * size_scale + i*15 * size_scale, 2 * size_scale, fill='white', lineWidth=2)
            twine.add(strand)
        waste.add(twine)
        
    elif waste_type['shape'] == 'label':
        # Produce label
        label = Rect(-8 * size_scale, -4 * size_scale, 16 * size_scale, 8 * size_scale, fill='red')
        text = Label('PLU', 0, 0, size=6 * size_scale, fill='white', bold=True)
        waste.add(label)
        waste.add(text)
    
    # Add description label
    label = Label(waste_type['description'], 0, 25 * size_scale, size=10 * size_scale, fill='black')
    waste.add(label)
    
    # Store waste type and destination
    waste.waste_type = waste_type['type']
    waste.destination = waste_type['destination']
    
    return waste

def update_waste():
    """Update waste positions and create new waste"""
    app.game.waste_timer += 1
    
    # Create new waste - now only happens when food is produced (in try_harvest_crop)
    # This function is kept for future use if needed
    pass

def update_hunger_bar():
    """Update food bar color and size"""
    if not app.game.game_over:
        bar = app.game.hunger_bar.children[1]  # The fill bar
        food = app.game.food_level
        
        # Ensure width is always at least 1 pixel but doesn't exceed the bar width
        bar.width = max(1, min(78, 78 * (food/100)))
        
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
            bar.width = 78
            bar.fill = 'red'
            bar.opacity = 100

def update_waste_meter():
    """Update food waste meter color and size"""
    if not app.game.game_over:
        bar = app.game.waste_meter.children[1]  # The fill bar
        waste = app.game.food_waste
        
        # Ensure width is always at least 1 pixel but doesn't exceed the bar width
        bar.width = max(1, min(78, 78 * (waste/100)))
        
        if waste > 70:
            bar.fill = rgb(139, 0, 0)  # Dark red for high waste
            bar.opacity = 100
        elif waste > 30:
            bar.opacity = 100
            if waste > 50:
                ratio = (waste - 50) / 20
                bar.fill = rgb(139, 69 * (1-ratio), 19)
            else:
                ratio = (waste - 30) / 20
                bar.fill = rgb(139, 69 + 186 * ratio, 19)
        else:
            bar.fill = rgb(139, 69, 19)  # Brown for low waste
            bar.opacity = 50 + math.sin(app.game.time * 0.2) * 50
    else:
        bar = app.game.waste_meter.children[1]
        # Ensure width is always at least 1 pixel but doesn't exceed the bar width
        bar.width = max(1, min(78, 78 * (app.game.food_waste/100)))
        bar.fill = rgb(139, 0, 0)
        bar.opacity = 100

def update_pollution_meter():
    """Update pollution meter color and size"""
    if not app.game.game_over:
        bar = app.game.pollution_meter.children[1]  # The fill bar
        pollution = app.game.pollution_level / 5  # Convert to percentage
        
        # Calculate exact width based on pollution percentage
        bar_width = 78 * (pollution / 100)
        bar.width = max(1, min(78, bar_width))
        
        if pollution > 70:
            bar.fill = rgb(50, 0, 0)  # Very dark red for high pollution
            bar.opacity = 100
        elif pollution > 30:
            bar.opacity = 100
            if pollution > 50:
                ratio = (pollution - 50) / 20
                bar.fill = rgb(128, 128 * (1-ratio), 128)
            else:
                ratio = (pollution - 30) / 20
                bar.fill = rgb(128, 128, 128 + 127 * ratio)
        else:
            bar.fill = rgb(128, 128, 128)  # Gray for low pollution
            bar.opacity = 50 + math.sin(app.game.time * 0.2) * 50
    else:
        bar = app.game.pollution_meter.children[1]
        pollution = app.game.pollution_level / 5  # Convert to percentage
        bar_width = 78 * (pollution / 100)
        bar.width = max(1, min(78, bar_width))
        bar.fill = rgb(50, 0, 0)
        bar.opacity = 100

def update_cursor_indicator():
    """Update cursor indicator position based on mouse"""
    if not app.game.game_over:
        # Update cursor indicator position
        app.game.cursor_indicator.centerX = app.game.mouse_x
        app.game.cursor_indicator.centerY = app.game.mouse_y

def try_process_food(mouse_x, mouse_y):
    """Attempt to interact with food items on the conveyor belt"""
    if app.game.game_over:
        return
    
    # Check if a food item is being clicked
    for food in app.game.conveyor_items[:]:
        # Simple distance check for food items
        distance = math.sqrt((food.centerX - mouse_x)**2 + (food.centerY - mouse_y)**2)
        if distance < 15:  # Click radius
            # Only select if nothing else is currently selected
            if app.game.selected_food is None and app.game.selected_waste is None:
                # Food item clicked - select it
                app.game.selected_food = food
                app.game.conveyor_items.remove(food)
                return True
            return False  # Ignore click if something else is selected
    
    # Check if selected food is being dropped in the collection area
    if app.game.selected_food:
        # Check if dropped in food collection area
        if (mouse_x > app.game.food_collection_area_x - app.game.food_collection_area_width/2 and
            mouse_x < app.game.food_collection_area_x + app.game.food_collection_area_width/2 and
            mouse_y > app.game.food_collection_area_y - app.game.food_collection_area_height/2 and
            mouse_y < app.game.food_collection_area_y + app.game.food_collection_area_height/2):
            
            # Process the food
            app.game.food_collection_count += 1
            app.game.food_collection_area.children[4].value = f'{app.game.food_collection_count}/{app.game.food_collection_target}'
            
            # Update production counter
            app.game.produced_food_today += 1
            app.game.food_production += 1  # Increment total food production
            app.game.produced_food_types.append(app.game.selected_food.food_type)
            app.game.produced_label.value = f'Produced: {app.game.produced_food_today}/5'
            app.game.produced_label.left = 20
            
            # Increase food level
            food_increase = min(15, 5 + random.randint(0, 5))
            app.game.food_level = min(100, app.game.food_level + food_increase)
            app.game.food_label.value = f'Food: {int(app.game.food_level)}%'
            app.game.food_label.left = 20
            
            # Increase waste and pollution from food production
            app.game.food_waste = min(100, app.game.food_waste + app.game.food_production_waste)
            app.game.waste_label.value = f'Waste: {int(app.game.food_waste)}%'
            app.game.waste_label.left = 20
            
            # Check for waste-based game over immediately
            if app.game.food_waste >= 100:
                app.game.game_over = True
                app.game.game_over_screen.visible = True
                app.game.game_over_screen.toFront()
                app.game.game_over_screen.children[1].value = 'GAME OVER'
                app.game.game_over_screen.children[2].value = 'Waste management has failed! The facility is overwhelmed with waste!'
                app.game.game_over_screen.children[3].value = f'Final food production: {app.game.food_production}'
                return True
            
            # Increase pollution from food production and current waste level
            pollution_increase = app.game.food_production_pollution + (app.game.food_waste * app.game.waste_pollution_factor / 100)
            app.game.pollution_level = min(500, app.game.pollution_level + pollution_increase)
            app.game.pollution_label.value = f'Pollution: {min(100, int(app.game.pollution_level / 5))}%'
            app.game.pollution_label.left = 20
            
            # Create waste when food is produced
            if len(app.game.waste.children) < app.game.max_waste_to_sort:
                # Create smaller waste for regular food items
                waste = create_waste(0.8)  # 80% of normal size
                app.game.waste.add(waste)
                
                # Add waste to sorting queue if not already at max
                if len(app.game.waste_to_sort) < app.game.max_waste_to_sort:
                    app.game.waste_to_sort.append(waste)
                    waste.centerX = 200
                    waste.centerY = 280
            
            # Remove the food item
            app.game.selected_food.visible = False
            app.game.selected_food = None
            
            # Check if we've collected enough food
            if app.game.food_collection_count >= app.game.food_collection_target:
                end_day()
            
            return True
    
    # Check if waste is being clicked for sorting
    for waste in app.game.waste_to_sort[:]:
        if (abs(waste.centerX - mouse_x) < 20 and 
            abs(waste.centerY - mouse_y) < 20):
            if app.game.selected_food is None and app.game.selected_waste is None:
                app.game.selected_waste = waste
                app.game.waste_to_sort.remove(waste)
                app.game.selected_waste.centerX = mouse_x
                app.game.selected_waste.centerY = mouse_y
                return True
            return False
    
    # Check if a monitor is being clicked for waste sorting
    if app.game.selected_waste:
        # Check if left monitor (compost) is clicked
        if (mouse_x > 20 and mouse_x < 80 and 
            mouse_y > 250 and mouse_y < 300):
            # Check if waste should go to compost
            if app.game.selected_waste.destination == 'compost':
                app.game.sorting_correct += 1
                # Reduce waste and pollution for correct sorting
                app.game.food_waste = max(0, app.game.food_waste - app.game.correct_sort_reduction)
                app.game.waste_label.value = f'Waste: {int(app.game.food_waste)}%'
                app.game.waste_label.left = 20
                
                app.game.pollution_level = max(0, app.game.pollution_level - app.game.correct_sort_pollution_reduction)
                app.game.pollution_label.value = f'Pollution: {min(100, int(app.game.pollution_level / 5))}%'
                app.game.pollution_label.left = 20
            else:
                app.game.sorting_incorrect += 1
                # Increase waste and pollution for incorrect sorting
                app.game.food_waste = min(100, app.game.food_waste + app.game.incorrect_sort_waste_increase)
                app.game.waste_label.value = f'Waste: {int(app.game.food_waste)}%'
                app.game.waste_label.left = 20
                
                app.game.pollution_level = min(500, app.game.pollution_level + app.game.incorrect_sort_pollution_increase)
                app.game.pollution_label.value = f'Pollution: {min(100, int(app.game.pollution_level / 5))}%'
                app.game.pollution_label.left = 20
                
                # Show error feedback
                app.game.feedback_text.value = f'Incorrect! {app.game.selected_waste.waste_type.replace("_", " ").title()} should go in TRASH'
                app.game.feedback_text.fill = 'red'
                app.game.feedback_group.visible = True
                app.game.feedback_group.toFront()
            
            # Remove feedback after 2 seconds
            app.game.feedback_timer = time.time() + 2
            app.game.feedback_label = app.game.feedback_text
            
            # Remove waste from game
            app.game.waste.remove(app.game.selected_waste)
            app.game.selected_waste.visible = False
            app.game.selected_waste = None
            
            # Update sorting stats
            app.game.sorting_label.value = f'Sorting: {app.game.sorting_correct}/{app.game.sorting_correct + app.game.sorting_incorrect}'
            app.game.sorting_label.left = 20
            
            return True
        
        # Check if right monitor (trash) is clicked
        elif (mouse_x > 320 and mouse_x < 380 and 
              mouse_y > 250 and mouse_y < 300):
            # Check if waste should go to trash
            if app.game.selected_waste.destination == 'trash':
                app.game.sorting_correct += 1
                # Reduce waste and pollution for correct sorting
                app.game.food_waste = max(0, app.game.food_waste - app.game.correct_sort_reduction)
                app.game.waste_label.value = f'Waste: {int(app.game.food_waste)}%'
                app.game.waste_label.left = 20
                
                app.game.pollution_level = max(0, app.game.pollution_level - app.game.correct_sort_pollution_reduction)
                app.game.pollution_label.value = f'Pollution: {min(100, int(app.game.pollution_level / 5))}%'
                app.game.pollution_label.left = 20
            else:
                app.game.sorting_incorrect += 1
                # Increase waste and pollution for incorrect sorting
                app.game.food_waste = min(100, app.game.food_waste + app.game.incorrect_sort_waste_increase)
                app.game.waste_label.value = f'Waste: {int(app.game.food_waste)}%'
                app.game.waste_label.left = 20
                
                app.game.pollution_level = min(500, app.game.pollution_level + app.game.incorrect_sort_pollution_increase)
                app.game.pollution_label.value = f'Pollution: {min(100, int(app.game.pollution_level / 5))}%'
                app.game.pollution_label.left = 20
                
                # Show error feedback
                app.game.feedback_text.value = f'Incorrect! {app.game.selected_waste.waste_type.replace("_", " ").title()} should go in COMPOST'
                app.game.feedback_text.fill = 'red'
                app.game.feedback_group.visible = True
                app.game.feedback_group.toFront()
            
            # Remove feedback after 2 seconds
            app.game.feedback_timer = time.time() + 2
            app.game.feedback_label = app.game.feedback_text
            
            # Remove waste from game
            app.game.waste.remove(app.game.selected_waste)
            app.game.selected_waste.visible = False
            app.game.selected_waste = None
            
            # Update sorting stats
            app.game.sorting_label.value = f'Sorting: {app.game.sorting_correct}/{app.game.sorting_correct + app.game.sorting_incorrect}'
            app.game.sorting_label.left = 20
            
            return True
    
    return False

def end_day():
    """Process end of day events"""
    # Check for game over conditions first
    if check_game_over():
        return
    
    # Decrease food level each day
    app.game.food_level = max(0, app.game.food_level - app.game.daily_food_decrease)
    app.game.food_label.value = f'Food: {int(app.game.food_level)}%'
    app.game.food_label.left = 20
    
    # Only increment day if we haven't won yet
    app.game.day += 1
    app.game.produced_food_today = 0
    app.game.food_collection_count = 0
    app.game.food_collection_area.children[4].value = f'{app.game.food_collection_count}/{app.game.food_collection_target}'
    
    # Update stats display
    app.game.day_label.value = f'Day: {app.game.day}/{app.game.target_days}'
    app.game.day_label.left = 20
    app.game.produced_label.value = f'Produced: {app.game.produced_food_today}/5'
    app.game.produced_label.left = 20
    app.game.waste_label.value = f'Waste: {int(app.game.food_waste)}%'
    app.game.waste_label.left = 20
    app.game.pollution_label.value = f'Pollution: {min(100, int(app.game.pollution_level / 5))}%'
    app.game.pollution_label.left = 20
    
    if app.game.sorting_correct + app.game.sorting_incorrect > 0:
        app.game.sorting_label.value = f'Sorting: {app.game.sorting_correct}/{app.game.sorting_correct + app.game.sorting_incorrect}'
    else:
        app.game.sorting_label.value = f'Sorting: 0/0'
    app.game.sorting_label.left = 20
    
    # Update meters
    update_hunger_bar()
    update_waste_meter()
    update_pollution_meter()

def onAppStart():
    app.game = create_game()
    app.stepsPerSecond = 30
    
    # # Create a dedicated layer for waste items that will be drawn on top
    # app.game.waste_layer = Group()
    # app.game.add(app.game.waste_layer)
    
    # Ensure area indicators are drawn on top
    app.game.compost_area.toFront()
    app.game.trash_area.toFront()
    
    # # Move waste items to the top layer
    # for waste in app.game.waste.children:
    #     waste.visible = False
    #     app.game.waste_layer.add(waste)
    #     waste.visible = True
    
    # # Ensure waste layer is always on top
    # app.game.waste_layer.toFront()

    app.game.waste.toFront()
    
    # Initialize feedback timer
    app.game.feedback_timer = None
    app.game.feedback_label = None
    
    # Ensure cursor indicator is always on top
    app.game.cursor_indicator.toFront()
    
    # Make sure monitors are visible and properly positioned
    app.game.left_monitor.centerX = 50
    app.game.left_monitor.centerY = 275
    app.game.right_monitor.centerX = 350
    app.game.right_monitor.centerY = 275
    
    # Ensure monitors are visible
    app.game.left_monitor.visible = True
    app.game.right_monitor.visible = True

def onStep():
    if not app.game.game_over:
        app.game.time += 1
        update_cursor_indicator()
        update_waste()
        update_conveyor_belt()
        
        # Check for game over conditions immediately
        if app.game.food_level <= 0 or app.game.pollution_level >= 500:
            check_game_over()
            return
        
        # Check if feedback timer has expired
        if app.game.feedback_timer is not None and app.game.feedback_label is not None:
            if time.time() > app.game.feedback_timer:
                app.game.feedback_group.visible = False
                app.game.feedback_timer = None
                app.game.feedback_label = None
        
        # Ensure monitors are visible
        app.game.left_monitor.visible = True
        app.game.right_monitor.visible = True
        
        # Ensure waste layer is always on top
        app.game.waste.toFront()
        
        # Ensure cursor indicator is always on top
        app.game.cursor_indicator.toFront()
    
    # Update meters
    update_hunger_bar()
    update_waste_meter()
    update_pollution_meter()

def onMousePress(mouseX, mouseY):
    try_process_food(mouseX, mouseY)

def onKeyPress(key):
    if key == 'd':
        end_day()
    elif key == 'r' and app.game.game_over:
        # Remove old game
        app.game.visible = False
        # Create new game
        app.game = create_game()
    # elif key == 'f':
    #     # Toggle food selection mode
    #     app.game.food_selection_mode = not app.game.food_selection_mode
    #     app.game.food_selection_panel.visible = app.game.food_selection_mode

def onMouseMove(mouseX, mouseY):
    app.game.mouse_x = mouseX
    app.game.mouse_y = mouseY
    
    # Only move selected items if the game is not over
    if not app.game.game_over:
        # Move selected food with mouse
        if app.game.selected_food:
            app.game.selected_food.centerX = mouseX
            app.game.selected_food.centerY = mouseY
        
        # Move selected waste with mouse
        if app.game.selected_waste:
            app.game.selected_waste.centerX = mouseX
            app.game.selected_waste.centerY = mouseY
        
        # Ensure waste layer is always on top
        app.game.waste.toFront()
        
        # Ensure cursor indicator is always on top
        app.game.cursor_indicator.toFront()

# def onMouseRelease(mouseX, mouseY):
#     # No need for special handling here anymore
#     # All waste sorting is handled in try_harvest_crop
#     pass

onAppStart()
cmu_graphics.run()
