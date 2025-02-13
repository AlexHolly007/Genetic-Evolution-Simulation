import random

#INPUT: probability matrix to choose action,   action that is having its probability affected,   connection type(1= increase, 2= decrease, 0 = stops  prob of action),  strength - how much it affects. on a scale of 0 to 1
def adjust_prob_matrix(matrix, action_code, connection_type, strength):
    for action_tuple in matrix:
        if action_code == action_tuple[1]:

            #can raise of lower by orders of itself, so it can be reduced to 0, or all the way up to 4x probability
            #action_tyuple[0] is the probability for that action to occur
            match connection_type:
                case 1:
                    action_tuple[0] = action_tuple[0] + (action_tuple[0] * strength * 3)
                
                case -1:
                    action_tuple[0] = action_tuple[0] - (action_tuple[0] * strength * 0.8)
                
                case 0:
                    action_tuple[0] = 0.0

    return matrix


#Choooses a action sequence based on the probability matrix
def choose_sequence(prob_matrix):
    total_weight = sum(weight for weight, _ in prob_matrix)
    r = random.uniform(0, total_weight)
    cumulative = 0.0
    for weight, sequence in prob_matrix:
        cumulative += weight
        if r < cumulative:
            return sequence