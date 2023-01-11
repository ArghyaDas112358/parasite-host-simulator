from ursina import *
from Brain import *
model = "assets/Bat"
texture = 'Bat_Texture.png'
class Predator(Entity):
    def __init__(self,view_radius = 10, degree_scan = 10,speed=1,Gender = "M",position=(0,0,0),adult = False,**kwargs):
        super().__init__(model=model, origin_y=-.5, collider='box', 
                    texture = texture,position=position, scale = (1,1,1))
        self.view_radius = view_radius
        self.degree_scan = degree_scan
        self.speed = speed

        self.counter = 1
        self.rotation_direction = 1

        self.adult = adult  #False by default
        self.age = 0


        random_generator = random.Random()
        red = random_generator.random() * 255
        green = random_generator.random() * 255
        blue = random_generator.random() * 255
        self.color = color.rgb(red,green,blue)
        
        self.weights1 = np.random.rand(1,8) #Weights for the Neural network
        self.weights2 = np.random.rand(8,1)

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def update(self):
        self.age += 1
        if self.age == 500:
            self.adult = True #Became adult and ready to reproduce after one day 

        dist = 0 
            
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, self.view_radius, ignore=(self,))
        entity = hit_info.entity
        str_entity = str(entity)

        very_close_hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 2, ignore=(self,))
        close_entity = very_close_hit_info.entity
        str_close_entity = str(close_entity)

        if self.age >= 1000:
            destroy(self)
            return
        if str_close_entity == "wall":
            destroy(self)
            return
        elif str_close_entity == "animal"and self.adult:
            destroy(close_entity)
            self.mass_reproduction(3)
            self.adult = False
            close_entity.adult = False
            #destroy(self)
            return

        elif str_entity != "None":
            self.rotation_y += time.dt*rotation_brain(str_entity,self.weights1, self.weights2)
            dist = distance_xz(entity.position, self.position)
            if dist > 2:
                self.position += self.forward * time.dt * self.speed
                return
        
        else:
            self.random_move()    

    def random_move(self):
        self.counter += 1
        if self.counter%50==0:
            rotation_direction_list = [-1,1]
            self.rotation_direction = random.choice(rotation_direction_list)
            self.counter = 1
        self.rotation_y += time.dt*self.degree_scan*self.rotation_direction
        self.position += self.forward * time.dt * self.speed

    def mass_reproduction(self,num):
        for i in range(num):
            Predator(view_radius = 10,degree_scan = 90,speed = 10,
                        position = self.position+(random.randint(-5,5),0,random.randint(-5,5)),
                        color = self.color,
                        weights1 = self.weights1,
                        weights2 = self.weights2
                        )
