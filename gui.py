import pygame

# initialize pygame
pygame.init()

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# define screen size
screen_width = 1820
screen_height = 980

# set up the display window
screen = pygame.display.set_mode((screen_width, screen_height))

# set the title of the window
pygame.display.set_caption("Blinking Circles")

# set the font for the text boxes
font = pygame.font.Font(None, 36)

# set the circle parameters
circle_radius = 50
circle_center_y = screen_height // 2
circle_spacing = 700

# set the circle frequencies
frequency_1 = 7
frequency_2 = 10
frequency_3 = 13

# set the initial circle colors
circle_color_1 = BLACK
circle_color_2 = BLACK
circle_color_3 = BLACK

# set the initial times for the circles
last_time_1 = pygame.time.get_ticks()
last_time_2 = pygame.time.get_ticks()
last_time_3 = pygame.time.get_ticks()

# run the game loop
running = True
while running:

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get the current time
    current_time = pygame.time.get_ticks()

    # calculate the time differences
    time_diff_1 = current_time - last_time_1
    time_diff_2 = current_time - last_time_2
    time_diff_3 = current_time - last_time_3

    # check if the circles should change color
    if time_diff_1 >= 1000 / frequency_1:
        circle_color_1 = WHITE if circle_color_1 == BLACK else BLACK
        last_time_1 = current_time

    if time_diff_2 >= 1000 / frequency_2:
        circle_color_2 = WHITE if circle_color_2 == BLACK else BLACK
        last_time_2 = current_time

    if time_diff_3 >= 1000 / frequency_3:
        circle_color_3 = WHITE if circle_color_3 == BLACK else BLACK
        last_time_3 = current_time

    # fill the background
    screen.fill(GREY)

    # draw the circles
    circle_1_center_x = screen_width // 2 - circle_spacing
    pygame.draw.circle(screen, circle_color_1, (circle_1_center_x, circle_center_y), circle_radius)

    circle_2_center_x = screen_width // 2
    pygame.draw.circle(screen, circle_color_2, (circle_2_center_x, circle_center_y), circle_radius)

    circle_3_center_x = screen_width // 2 + circle_spacing
    pygame.draw.circle(screen, circle_color_3, (circle_3_center_x, circle_center_y), circle_radius)

    # add text to the circles
    text_surface_1 = font.render(f"{frequency_1} Hz", True, WHITE)
    text_rect_1 = text_surface_1.get_rect(center=(circle_1_center_x, circle_center_y + circle_radius + 20))
    screen.blit(text_surface_1, text_rect_1)

    text_surface_2 = font.render(f"{frequency_2} Hz", True, WHITE)
    text_rect_2 = text_surface_2.get_rect(center=(circle_2_center_x, circle_center_y + circle_radius + 20))
    screen.blit(text_surface_2, text_rect_2)

    text_surface_3 = font.render(f"{frequency_3} Hz", True, (255, 255, 255))
    text_rect_3 = text_surface_3.get_rect(center=(circle_3_center_x, circle_center_y + circle_radius + 20))
    screen.blit(text_surface_3, text_rect_3)

    # Update the screen
    pygame.display.update()

    # Wait for 1 millisecond to ensure the screen updates properly
    pygame.time.wait(1)

# Quit the program
pygame.quit()

