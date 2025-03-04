import pygame
from Models import Agent
from Matrix_calculations import adjust_prob_matrix, choose_sequence

#The matrix of probabilites to choose the action
#Agent will use the probabilities below to choose an actions genes
#probabilites are adjusted per agent based on sensory nodes from genetics
PROB_MATRIX_TEMPLATE = [
    #(PROBABILITY, ACTION CLASS GENETICS) 
    [0.25, 'AAAA'], #move forward
    [0.25, 'AAAG'],
    [0.25, 'AAGA'],
    [0.25, 'AAGG']
]

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
            # strength = sense_strength +*/= connect_strength
            # Adjust_matrix(matrix, action_code, connection_type, strength)

    #2. check if genes have that action, if that action has an ouput to another action:
            # save last actions nucletide makeup
            # agent.check_genes_for_action_connection('<action nucleotides>')
            # strength = connect_strength
            # Adjust_matrix(matrix, action_code, connection_type, strength)

    #3. Matrix is run to get a random action, action is executed

    #4. Repeat      
                
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    organisms = [Agent() for _ in range(1)]
    for o in organisms:
        o.anywhere_but_here()
        o.scramble_genes(30)

    # running loop
    running = True
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((50, 44, 40))
        count += 1

        #Create the probability matrix for each agent and run it to get an action
            #This matrix is adjusted by all the nodes in the agent that are made up from its genetics
        #Run this action for each agent to get a movement
        for org in organisms:
            #Check for sensory node to adjust matrix
            Agent_action_matrix = PROB_MATRIX_TEMPLATE.copy()

            list_of_sense_nodes = org.check_for_sensory_nodes_in_genes()
            for sense_node_in_agent in list_of_sense_nodes:
                #return a list of tuples of (action_code, connection_type, connection_strength) for each action node that is an output of this sensory node
                connections_going_to_actions = org.check_genes_for_action_connection(sense_node_in_agent)

                sense_strength = org.run_sensory_node(sense_node_in_agent)

                #For each sensory connection to an action, adjust the matrix based on that sense strength and action
                for connection in connections_going_to_actions:
                    strength = sense_strength + connection[2]
                    adjust_prob_matrix(Agent_action_matrix, connection[0], connection[1], strength)

            #Check for action nodes
            #Checking for action nodes, because if the agent has a gene for the last action it did, it will adjust any actions that its connected to, kinda like sensory
            list_of_action_nodes = org.check_for_action_nodes_in_genes()
            for action_node_in_agent in list_of_action_nodes:
                #return a list of tuples of (action_code, connection_type, connection_strength) for each action node that is an output of this action node
                connections_going_to_actions = org.check_genes_for_action_connection(action_node_in_agent)

                #For each action connection to an action, adjust the matrix based on that action and connection strength
                for connection in connections_going_to_actions:
                    strength = connection[2] * 10/4   #Scaling so it will be 0-1
                    adjust_prob_matrix(Agent_action_matrix, connection[0], connection[1], strength)

            #Run the matrix to get an action and run it
            action_sequence = choose_sequence(Agent_action_matrix)
            org.run_action_node(action_sequence)

        # Draw on organisms
        for org in organisms:
            pygame.draw.circle(screen, (45, 199, 106), (org.x, org.y), 5)

        if count % 100 == 0:
            for org in organisms:
                #org.print_genes()
                org.scramble_genes(2)
                

        #Implement the fitness aspect for survival of the fittest, food source


        pygame.display.flip()
        clock.tick(20)

    pygame.quit()

if __name__ == '__main__':
    main()