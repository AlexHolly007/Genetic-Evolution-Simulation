import random

class Node:
    def __init__(self, function):
        self.function = function # can either be 'action' or 'sensor'

    def execute(self, agent):
        raise NotImplementedError("Each action node must define its own execute method.")
    

# Different action nodes with unique behavior
class Move_forward(Node):
    def execute(self, agent):
        match agent.orientation:
            case 'L':
                if agent.x != 0:
                    agent.x -= 1

            case 'R':
                if agent.x != 500:
                    agent.x += 1

            case 'U':
                if agent.y != 500:
                    agent.y += 1

            case 'D':
                if agent.y != 0:
                    agent.y -= 1
class Turn_left(Node):
    def execute(self, agent):
        match agent.orientation:
            case 'L':
                agent.orientation = 'D'

            case 'R':
                agent.orientation = 'U'

            case 'U':
                agent.orientation = 'L'

            case 'D':
                agent.orientation = 'R'

class Turn_right(Node):
    def execute(self, agent):
        match agent.orientation:
            case 'L':
                agent.orientation = 'U'

            case 'R':
                agent.orientation = 'D'

            case 'U':
                agent.orientation = 'R'

            case 'D':
                agent.orientation = 'L'
    
class U_Turn(Node):
    def execute(self, agent):
        match agent.orientation:
            case 'L':
                agent.orientation = 'R'

            case 'R':
                agent.orientation = 'L'

            case 'U':
                agent.orientation = 'D'

            case 'D':
                agent.orientation = 'U'


#Different sensoring nodes
class Sense_food_right(Node):
    def execute(self, agent):
        return random.randint(1,6)/10
    
class Sense_food_left(Node):
    def execute(self, agent):
        return random.randint(1,6)/10
    
class Sense_food_straight(Node):
    def execute(self, agent):
        return random.randint(1,6)/10
    
class Sense_wall_straight(Node):
    def execute(self, agent):
        return random.randint(1,6)/10
    
class Sense_proximity_to_agents(Node):
    def execute(self, agent):
        return random.randint(1,6)/10