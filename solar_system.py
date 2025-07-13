#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pygame

"""
Define colors and constants.
"""

# constants
G = 6.67430e-11
mass_sun = 1.99e30
mass_mars = 6.39e26
mass_jupiter = 10.89e27
mass_earth = 5.97e24

luminosity_sun = 3.85e26

radius_sun = 6.96e8
radius_mars = 3.4e6
radius_jupiter = 7.15e7
radius_earth = 6.37e6

# colors
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
cadmiumorange = (255,97,3)
azure4 = (131,139,139)

hotpink1 = (255, 110, 180)  
hotpink2 = (238, 106, 167)  
hotpink3 = (205, 96, 144)   

# for more colors:
# https://www.webucator.com/article/python-color-constants-module/ 



# In[4]:


"""
This is the Body class, which includes the information for each Body as well as all of the physics
created by the program (and a function to detect where the mouse is in correlation to the bodies.
"""
class Body:
    def __init__(self, name, mass, position, velocity, color, radius, luminosity):
        self.name = name
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.acceleration = np.zeros(2)
        self.color = color
        self.radius = radius
        self.luminosity = luminosity

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def calculate_acceleration(self, bodies):
        total_force = np.zeros(2)
        for body in bodies:
            if body is not self:
                r_vector = body.position - self.position
                r = np.linalg.norm(r_vector)
                force_magnitude = G * self.mass * body.mass / r**2
                force_direction = r_vector / r
                total_force += force_magnitude * force_direction
        self.acceleration = total_force / self.mass

    def is_mouse_over(self, mouse_pos, scale, sun_center):
        body_pos_screen = sun_center + (self.position / scale)
        distance = np.linalg.norm(mouse_pos - body_pos_screen)
        return distance < 10  

# intensity (luminosity) as a function of time of star
# take FT and show frequencies, show whch planet is which


# In[ ]:


# intensity function

def intensity(distance):
    I = luminosity/(4*math.pi*distance**2)
    


# In[5]:


# design celestial bodies

sun = Body("Sun", mass_sun, [0, 0], [0, 0], yellow, radius_sun, luminosity_sun)
mars = Body("Mars", mass_mars, [227e9, 300], [0, 24e3], red, radius_mars, 0)  
jupiter = Body("Jupiter", mass_jupiter, [100e9, 0], [0, 13e3], orange, radius_jupiter, 0) 
earth = Body("Earth", mass_earth, [-149e9,0],[0,-30e3], blue, radius_earth, 0)
#sun2 = Body("Second Sun", mass_sun, [100e3, 100e3], [0,0], white)
alpha_centauri = Body("Alpha Centauri", 2*mass_sun, [100e10,0],[0,0],cadmiumorange, 2*radius_sun, 2*luminosity_sun)
dark_matter = Body("Dark Matter", 100000*mass_sun, [100e40,0],[0,0], azure4, 10e30,0)

# declare celestial bodies
bodies = [sun,mars,jupiter,earth,alpha_centauri,dark_matter]


# In[6]:


# pygame setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
paused = False
scale = 1e9  
sun_center = np.array([width // 2, height // 2])

def draw_body(body):
    position = sun_center + (body.position / scale)
    pygame.draw.circle(screen, body.color, position.astype(int), 5)


# In[7]:


# draw info box and speed box

def draw_info_box(body):
    font = pygame.font.Font(None, 24)
    info_text = [
        f"Name: {body.name}",
        f"X: {body.position[0]:.2e}",
        f"Y: {body.position[1]:.2e}",
        f"v: {np.linalg.norm(body.velocity):.2e}",
        f"a: {np.linalg.norm(body.acceleration):.2e}"
    ]
    box_width = max(font.size(line)[0] for line in info_text) + 20
    box_height = len(info_text) * font.get_linesize()

    # Draw a rectangle as the background of the info box
    box_rect = pygame.Rect(10, 10, box_width, box_height)
    screen.fill((0, 0, 0), box_rect)
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 1)

    for i, line in enumerate(info_text):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (15, 15 + i * font.get_linesize()))

#### dt = 10000  # Time step in seconds

speed_settings = [5000, 10000, 15000, 20000, 25000]  # Different time steps for simulation speed
current_speed_index = 1

def draw_speed_box():
    font = pygame.font.Font(None, 24)
    speed_text = f"Time Speed: {current_speed_index + 1}"
    text_surface = font.render(speed_text, True, (255, 255, 255))

    box_width = text_surface.get_width() + 20
    box_height = text_surface.get_height() + 10

    # Position the box at the bottom left corner
    box_rect = pygame.Rect(10, height - box_height - 10, box_width, box_height)
    screen.fill((0, 0, 0), box_rect)
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 1)
    screen.blit(text_surface, (15, height - box_height))


# In[8]:


# MAIN LOOP and CONTROLS

zoom_speed = 0.1
scroll_speed = 10

dragging = False
last_mouse_pos = None
selected_body = None

frame_rate = 60
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP: 
                current_speed_index = min(current_speed_index + 1, len(speed_settings) - 1)
            elif event.key == pygame.K_DOWN:
                current_speed_index = max(current_speed_index - 1, 0)
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                mouse_pos = np.array(pygame.mouse.get_pos())
                body_clicked = False
                for body in bodies:
                    if body.is_mouse_over(mouse_pos, scale, sun_center):
                        selected_body = body  
                        body_clicked = True
                        break
                if not body_clicked:
                    selected_body = None
            
            if event.button == 1:  
                dragging = True
                last_mouse_pos = np.array(pygame.mouse.get_pos())
            elif event.button == 4:  
                scale *= (1 + zoom_speed)
            elif event.button == 5: 
                scale /= (1 + zoom_speed)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                current_mouse_pos = np.array(pygame.mouse.get_pos())
                mouse_delta = current_mouse_pos - last_mouse_pos
                sun_center += mouse_delta
                last_mouse_pos = current_mouse_pos

    if not running:
        break

    dt = speed_settings[current_speed_index]  

    if not paused:
        for body in bodies:
            body.calculate_acceleration(bodies)
            body.update(dt)

    mouse_pos = np.array(pygame.mouse.get_pos())

    # Check if mouse is over any body
    hovered_body = None
    for body in bodies:
        if body.is_mouse_over(mouse_pos, scale, sun_center):
            hovered_body = body
            break
    
    screen.fill((0, 0, 0))
    for body in bodies:
        draw_body(body)

    if selected_body:
        draw_info_box(selected_body)
    elif hovered_body:
        draw_info_box(hovered_body)

    draw_speed_box()

    pygame.display.flip()
    clock.tick(frame_rate)

pygame.quit()

