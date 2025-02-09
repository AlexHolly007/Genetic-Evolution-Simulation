import pygame
import random
from Models import Agent, Gene

#Make a action_nodes.py, this has classes for each action node, and their functions needed.
#Make sensory_nodes.py for each sensory node type

#Play Matrix - Percent chance of every action happeneing
    #starts with percentages all at a fixed rate for each agent

#Actions Nodes 
    #If this action was choosen as last move for the agent, then activate signal out 
        #Signal out strength is determined 1-8 in agent when created - constant
    #If signal is coming in, then alter the play matrix for this action based on signal strength.

#Sesory Nodes
    #These will sense every turn, and give a strength connection based on that sense to send to any putput
        #This strength is also effected by the strength that is randomly choosen once it is created (-10,10)


#Workflow of agent
    #1. For each sensory Node that has output to action node, check if it is sensing anything
            # agent.check_for_sensory_nodes(), or run all sesnory node possibilities in next step
            # agent.check_genes_for_action_connection('<any sensory node genes>')
            # sense_strength = SENSORY_DICT[<sense node>].execute
            # coonect_strength = sense_strength +*/= connect_strength
            # Adjust_matrix(matrix, action_code, connection_type, strength)

    #2. check if genes have that action, if that action has an ouput to another action:
            # save last actions nucletide makeup
            # agent.check_genes_for_action_connection('<action nucleotides>')
            # strength = connect_strength
            # Adjust_matrix(matrix, action_code, connection_type, strength)

    #3. Matrix is run to get a random action, action is executed

    #4. Repeat      
                

##TODO
#Set up simple gene scramble and action function
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    organisms = [Agent() for _ in range(10)]
    for o in organisms:
        o.anywhere_but_here()
        #o.scramble_genes(3)

    # running loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((50, 44, 40))

        # Draw on organisms
        for org in organisms:
            org.x += random.randint(-2,2) 
            org.x = max(0, min(500, org.x))

            org.y += random.randint(-2, 2)
            org.y = max(0, min(500, org.y))

            pygame.draw.circle(screen, (45, 199, 106), (org.x, org.y), 5)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()