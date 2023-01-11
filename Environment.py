from ursina import *

size = 100
wall_height = 5
ground = Entity(model='plane', collider='mesh', scale=(size,1,size), texture='grass', texture_scale=(4,4))
wall1 = Entity(model = 'cube',collider = 'cube', scale = (size,wall_height,2),position = (0,0,size/2), texture = 'brick', texture_scale=(4,4), color = color.red)
wall2 = duplicate(wall1,position = (0,0,-size/2))
wall3 = duplicate(wall1,scale = (2,wall_height,size),position = (-size/2,0,0))
wall4 = duplicate(wall3,position = (size/2,0,0))
