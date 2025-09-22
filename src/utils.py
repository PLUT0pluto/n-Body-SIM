# utils.py
import math
import random
import pygame
import pygame.gfxdraw

def random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) #from 50 so that no black

def points_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def draw_arrow_by_angle(surface, start_pos, angle_degrees, length=60, width=1, arrowhead_length=10, color=(255, 255, 255)):
    arrowhead_angle = math.pi / 6  # 30 degrees
    angle_rad = math.radians(angle_degrees)

    end_pos_tip = (
        start_pos[0] + length * math.cos(angle_rad),
        start_pos[1] + length * math.sin(angle_rad)
    )

    shorten_by = arrowhead_length * math.cos(arrowhead_angle)
    shaft_end_pos = (
        start_pos[0] + (length - shorten_by) * math.cos(angle_rad),
        start_pos[1] + (length - shorten_by) * math.sin(angle_rad)
    )

    #draw line
    direction = (end_pos_tip[0] - start_pos[0], end_pos_tip[1] - start_pos[1])
    if all(v == 0 for v in direction): return #avoid division by zero if length is 0
    
    perpendicular = pygame.math.Vector2(direction).normalize().rotate(90)
    half_width = width / 2
    
    p1 = pygame.math.Vector2(start_pos) - perpendicular * half_width
    p2 = pygame.math.Vector2(start_pos) + perpendicular * half_width
    p3 = pygame.math.Vector2(shaft_end_pos) + perpendicular * half_width
    p4 = pygame.math.Vector2(shaft_end_pos) - perpendicular * half_width
    
    shaft_points = [p1, p2, p3, p4]
    pygame.gfxdraw.filled_polygon(surface, shaft_points, color)
    pygame.gfxdraw.aapolygon(surface, shaft_points, color)

    #draw arrowhead
    head_angle_rad = math.atan2(start_pos[1] - end_pos_tip[1], start_pos[0] - end_pos_tip[0])
    ah_p1 = (
        end_pos_tip[0] + arrowhead_length * math.cos(head_angle_rad + arrowhead_angle),
        end_pos_tip[1] + arrowhead_length * math.sin(head_angle_rad + arrowhead_angle)
    )
    ah_p2 = (
        end_pos_tip[0] + arrowhead_length * math.cos(head_angle_rad - arrowhead_angle),
        end_pos_tip[1] + arrowhead_length * math.sin(head_angle_rad - arrowhead_angle)
    )
    arrowhead_points = [end_pos_tip, ah_p1, ah_p2]
    pygame.gfxdraw.filled_polygon(surface, arrowhead_points, color)
    pygame.gfxdraw.aapolygon(surface, arrowhead_points, color)