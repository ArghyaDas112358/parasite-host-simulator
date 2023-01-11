from re import X
import numpy as np

entity_dict = {"wall":1,"animal":2}

#output = [[output_rotation]]


def sigmoid(x):
    return 1/(1 + np.exp(-x))
def rotation_brain(entity,weights1,weights2, amplification = 0.1):
    input_value = np.array(entity_dict.get("wall"))

    
    weights1   = weights1 + np.random.rand(1,8) * amplification
    weights2   = weights2 + np.random.rand(8,1) * amplification

    layer1 = sigmoid(np.dot(input_value, weights1))
    output_rotation = sigmoid(np.dot(layer1, weights2))                 
    return output_rotation*360.0

if __name__ == '__main__':
    print(entity_dict.get("wall"))
    print(rotation_brain("wall",np.random.rand(1,8),np.random.rand(1,8)))