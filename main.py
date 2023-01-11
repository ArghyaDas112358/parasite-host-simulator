from ctypes import alignment
from ursina import *   
from ursina import camera 
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
import random
from Animal import Animal
from Predator import Predator

app = Ursina()

class Wall(Entity):
    def __init__(self, size,scale, position):
        super().__init__(model = 'cube',collider='box', 
                texture = 'brick', texture_scale=(4,4), color = color.red)
        self.scale = scale
        self.position = position
size = 100
wall_height = 5
ground = Entity(model='plane', collider='mesh', scale=(size,1,size), texture='grass', texture_scale=(4,4))

wall1 = Wall(size = size,scale = (size,wall_height,2),position = (0,0,size/2))
wall2 = Wall(size = size,scale = (size,wall_height,2),position = (0,0,-size/2))
wall3 = Wall(size = size,scale = (2,wall_height,size),position = (-size/2,0,0))
wall4 = Wall(size = size,scale = (2,wall_height,size),position = (size/2,0,0))

def mass_animal_generator(num):
    for i in range(num):
        Animal(view_radius=10,degree_scan = 90,speed=10,
                position=(random.randint(-size//3,size//3),0,random.randint(-size//3,size//3)),
                scale=(1,1,1),
                seed = random.randint(0,999)*i,
                adult=True)

def mass_predator_generator(num):
    for i in range(num):
        Predator(view_radius=10,degree_scan = 90,speed=10,
                position=(random.randint(-size//3,size//3),0,random.randint(-size//3,size//3)),
                seed = random.randint(0,999)*i,
                adult=True)

def num_animals(scene):
    try:
        return str(len(scene.entities)- 25) 
    except:
        return "0"
day_counter = 0
def update():
    global day_counter,day_text
    day_counter += 1
    if day_counter%500 == 0:
        pass
        #mass_animal_generator(15)
    destroy(day_text)
    day_text = Text("Day = "+str((day_counter//5)/100)+"\nEntities = "+num_animals(scene))
    if held_keys['t']:
        if len(scene.entities)<=1:
            pass
        else:
            chosesn_entity = random.choice(scene.entities)
            print(str(chosesn_entity.name)== 'animanl')
            if str(chosesn_entity.name) == 'animanl':
                print(str(chosesn_entity.name))
                destroy(chosesn_entity)
        
    

mass_animal_generator(20)
mass_predator_generator(10)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5)
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))
#EditorCamera()
day_text = Text("Day = "+str(day_counter//500)+"\nEntities = "+num_animals(scene))
app.run()   