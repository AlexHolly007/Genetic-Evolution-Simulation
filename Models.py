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
            self.connections[i] = ['E' * CONNECTION_NUCLEOTIDES_NUM, random.randint(1,4)/10]



#Each agent will have genes that determine how they interact with the environment
class Agent:
    #The start
    def __init__(self, num_nodes = 3):
        self.x = 0 #0-500
        self.y = 0 #0-500
        self.orientation = random.choice(['L','R','U','D']) #L,R,U,D for left,right,up,down facing
        self.num_nodes = num_nodes
        self.last_run_action = None

        #initialize the genes of the agent. will start empty
        self.genes = [Gene(id=idx, num_genes=num_nodes) for idx in range(3)]

    #Prints the genes of the agent
    def print_genes(self):
        for gene in self.genes:
            print(f'Gene: {gene.id} - {gene.nucleotides} - {gene.connections}')
            if gene.nucleotides in ACTION_DICT.keys():
                print(f'    Gene function: {ACTION_DICT[gene.nucleotides]} - ', end='')
            elif gene.nucleotides in SENSORY_DICT.keys():
                print(f'    Gene function: {SENSORY_DICT[gene.nucleotides]} - ', end='')
            else:
                print('    Gene function: None - ', end='')

            print('Connections: ', end='')
            for connection in gene.connections.keys():
                if gene.connections[connection][0] in CONNECTION_DICT.keys():
                    print(f'({connection}: {CONNECTION_DICT[gene.connections[connection][0]]}) - ', end='')
                else:
                    print(f'({connection}: None) - ', end='')
            print()

    
    #Will alter the amount of letters that the mutations is equal to. picked at random from this agents genes.
    # max mutations = ACTION_NUCLEOTIDES_NUM * num_nodes + CONNECTION_NUCLEOTIDES_NUM * num_nodes * num_nodes-1 
    # = 4 * 3   +   3 * 3 * 2   = 12 + 18 =   30
    def scramble_genes(self, mutations):

        #Make population that has a total of <max_mutations>(30) items, 1 for each possible mutation
        #make a population for all possible connections
        connection_population = [(gene.id, connection_id, connection_nucleotide_id) for gene in self.genes for connection_id in gene.connections.keys() for connection_nucleotide_id in range(CONNECTION_NUCLEOTIDES_NUM)]
        #make a population for all possible genes
        gene_population = [(gene.id, nucleotide_id) for gene in self.genes for nucleotide_id in range(ACTION_NUCLEOTIDES_NUM)] 

        #join the two populations, should be of length <max_mutations>
        population = connection_population + gene_population     

        # This will choose `mutations` unique items from the population.
        nucleotides_to_change = random.sample(population, mutations)

        for nucleotide_indexs in nucleotides_to_change:
            # check the length of the nucleotide_indexs to see if its a gene or a connection thats being mutated
            if len(nucleotide_indexs) == 2: #It is a gene 
                #same string with 1 scrambled letter
                self.genes[nucleotide_indexs[0]].nucleotides = \
                    self.genes[nucleotide_indexs[0]].nucleotides[:nucleotide_indexs[1]] + random.choice(['A','G']) + self.genes[nucleotide_indexs[0]].nucleotides[nucleotide_indexs[1] + 1:]
            
            # changing a connection nucleotide
            else:
                #same string with 1 scrambled letter
                self.genes[nucleotide_indexs[0]].connections[nucleotide_indexs[1]][0] = \
                    self.genes[nucleotide_indexs[0]].connections[nucleotide_indexs[1]][0][:nucleotide_indexs[2]] + random.choice(['A', 'G']) + self.genes[nucleotide_indexs[0]].connections[nucleotide_indexs[1]][0][nucleotide_indexs[2] + 1:] 


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
                    if self.genes[gene_id].nucleotides in ACTION_DICT.keys() and gene.connections[gene_id][0] in CONNECTION_DICT.keys():
                        #return action_code, connection type(1, -1, or 0), and connection strength
                        return_connections.append((self.genes[gene_id].nucleotides, CONNECTION_DICT[gene.connections[gene_id][0]], gene.connections[gene_id][1]))
        
        return return_connections


    #INPUT the genetic gone for a sensory node, agent its being run with
    #Description - will run the sensory node ability to get a sense strength
    def run_sensory_node(self, sense_nucleotides):
        return SENSORY_DICT[sense_nucleotides].execute(self)

   #INPUT the genetic code for an action node, agent being run on
   #Description - will run the action
    def run_action_node(self, action_nucleotides):
        return ACTION_DICT[action_nucleotides].execute(self)
    
    #Return a list of sensory nodes that are within the genes of agent
    def check_for_sensory_nodes_in_genes(self):
        return [gene.nucleotides for gene in self.genes if gene.nucleotides in SENSORY_DICT.keys()]
    
    #Return a list of action nodes that are within genes
    def check_for_action_nodes_in_genes(self):
        return [gene.nucleotides for gene in self.genes if gene.nucleotides in ACTION_DICT.keys()]