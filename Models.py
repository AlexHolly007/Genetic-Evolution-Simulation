import random
from nodes_abilities import Move_forward, Turn_left, Turn_right, U_Turn, Sense_food_left, Sense_food_right, Sense_food_straight, Sense_proximity_to_agents, Sense_wall_straight

ACTION_NUCLEOTIDES_NUM = 4  #length of the action/sensory node genes - 2^4 = 16 possibilities
CONNECTION_NUCLEOTIDES_NUM = 3  #Length of connection genes - 2^3 = 8 possibilities
NUM_ACTIONS = 4 #go straight - AAAA,   turn left - AAAG,   turn right - AAGA,   flip 180 - AAGG.
NUM_SENSORS = 5 #senses food right - GGGG,   senses food left - GGGA,   sensed food straight - GGAA,   wall straight ahead - GAGA,   closeness to group - GAGG
NUM_CONNECTIONS = 3 #makes likley to - AAA & AAG,   makes unlikley to - GGG & GGA,   stops - AGA

#Maps the genetic code to the action class and its functions
ACTION_DICT = {
    'AAAA': Move_forward('action'),
    'AAAG': Turn_right('action'),
    'AAGA': Turn_left('action'),
    'AAGG': U_Turn('action'),
}

#Maps genetic code to sensory node classes and their functions
SENSORY_DICT = { 
    'GGGG': Sense_food_right('sensor'),
    'GGGA': Sense_food_left('sensor'), 
    'GGAA': Sense_food_straight('sensor'),
    'GAGA': Sense_wall_straight('sensor'),
    'GAGG': Sense_proximity_to_agents('sensor'),
}

#Maps genetic code to connection type
CONNECTION_DICT = {
    'AAA': 1,
    'AAG': 1,
    'GGG': -1,
    'GGA': -1,
    'AGA': 0, 
}

#The matrix of probabilites to choose the action
#Agent makes a move based on the prob_matrix, then runs the action of that probability
PROB_MATRIX_TEMPLATE = [
    #(PROBABILITY, ACTION CLASS GENETICS) 
    (0.25, 'AAAA'),
    (0.25, 'AAAG'),
    (0.25, 'AAGA'),
    (0.25, 'AAGG')
]





#Genes for an agent. Each agent will have a few genes that will corespond to an action/sensor that helps the agent interact with environment.
#Each gene will have a connection to each other gene to determine how they affect each other
class Gene:
    def __init__(self, id, num_genes):
        #Nucleotides can be either A or G, but are initialized as E
        self.id = id
        self.nucleotides = 'E' * ACTION_NUCLEOTIDES_NUM #The combination of letters here determines this genes functionality / existence
        self.connections = {} #Will be filled with all gene id's other than its own

        #Create connection to every other node
        for i in range(num_genes):
            if id == i: #Skip itself
                continue
            self.connections[i] = ('E' * CONNECTION_NUCLEOTIDES_NUM, random.randint(1,10))



#Each agent will have genes that determine how they interact with the environment
class Agent:
    #The start
    def __init__(self, num_nodes = 3):
        self.x = 0 #0-500
        self.y = 0 #0-500
        self.orientation = random.choice(['L','R','U','D']) #L,R,U,D for left,right,up,down facing
        self.num_nodes = num_nodes

        #initialize the genes of the agent. will start empty
        self.genes = [Gene(id=idx, num_genes=num_nodes) for idx in enumerate(range(3))]

    
    #Will alter the amount of letters that the mutations is equal to. picked at random from this agents genes.
    def scramble_genes(self, mutations):

        #i is the gene # from this agent
        #j is the connection # for the gene to other genes (if this is the same as the gene selected, we will be changing the gene instead of a connection)
        #k if a connection is choosen - k is the nucleotide choice for within the connection choosen
        #z if a connection is not choosen - z is the nucletide choice for the action of the gene
        nucleotides_to_change = random.choices(
            [[i, j, k, z] for i in range(self.num_nodes) 
            for j in [x for x in range(self.num_nodes)] 
            for k in range(CONNECTION_NUCLEOTIDES_NUM)
            for z in range(ACTION_NUCLEOTIDES_NUM)],
            k=mutations #Amount of choices to make
        )

        print(nucleotides_to_change)

        for nucleotide_indexs in nucleotides_to_change:
            # When the connection index is the same as the gene index picked, it will change the genes
            #       action/sensor nucleotides instead of the connections nucleotides
            if nucleotide_indexs[0] == nucleotide_indexs[1]: 
                #same string with 1 scrambled letter
                self.genes[nucleotide_indexs[0]].nucleotides = \
                    self.genes[nucleotide_indexs[0]].nucleotides[:nucleotide_indexs[3]] + random.choice(['A','G']) + self.genes[nucleotide_indexs[0]].nucleotides[nucleotide_indexs[3]:]
            
            # this one is for scramebling a connection
            else:
                #same string with 1 scrambled letter 
                self.genes[nucleotide_indexs[0]].connections[nucleotide_indexs[1]][0] = \
                    self.genes[nucleotide_indexs[0]].connections[nucleotide_indexs[1]][0][:nucleotide_indexs[2]] + random.choice(['A', 'G']) + self.genes[nucleotide_indexs[0]].connections[nucleotide_indexs[1]][0][nucleotide_indexs[2]:] 

            print(nucleotide_indexs)


    # Gives the agent a random location on the environment
    def anywhere_but_here(self):
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)


    #INPUT: nucleotides for an action or sensory node
    #OUTPUT: output_action, connection_type to that output action, strength of connection to output action node
    #This function checks the agents genes to see if there is a connection from the nucleotides inputted to any action node
    #Its used to see if an actions probability needs to be affected by a sensor, or other action node connection
    def check_genes_for_action_connection(self, nucleotides_of_node):
        #Return a tuple of (action_code, connection_type, connection_strength) for each action node that is an output
        return_connections = []
        for gene in self.genes:
            if gene.nucleotides == nucleotides_of_node:
                for gene_id in gene.connections.keys():

                    #If a connection from the node being checked points to an action node
                    if self.genes[gene_id].nucleotides in ACTION_DICT.keys():
                        #return action_code, connection type(1, -1, or 0), and connection strength
                        return_connections.append((self.genes[gene_id].nucleotides, CONNECTION_DICT[gene.connections[gene_id][0]], gene.connections[gene_id][1]))
        
        return return_connections