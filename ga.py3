# another small change

import numpy
import random
import sound_generation
import os
import math
from datetime import datetime

# List of global constants

# Number of chromosomes in each generation
mems_per_pop = 8

# Number of chromosomes used for matingpool
num_parents = mems_per_pop // 2

# Number of genes each chromosome should have, should not be adjusted
num_genes = 6

# Number of ints in each gene
gene_length = 10

# Number of generations created each time program is run
loops = 10

# Used to determine chance of mutation occurence in each generation
chance = 1

# Used to determine how many fitness helper we have in total
num_funcs = 12

# Used to scale how aggresively the mutation function changes the genes
mutate_scalar = 0.05

# Number of crossover function
num_crossover = 3

# Determines which crossover function is used, 0 for midpoint, 1 for uniform, 2 for deep uniform
selected_crossover = 2

# Number of mutation functions
num_mutation = 2

# Determines which mutation function is used, 0 for gene mutation, 1 for chromosome mutation
selected_mutation = 1

# For testing purposes, makes it so wav files aren't generated if you don't want them
dont_generate_files = True

# Number of islands in representation
num_isles = 10


# Making an ideal set, used for dummy fitness function
    
harms = [0] * gene_length

amps = [1.0, 0.65, 0.61, 0.15, 0.09, 0.02, 0.02, 0.01, 0.01, 0.01]

a = [0.01] * gene_length
d = [0.1] * gene_length
s = [0.5] * gene_length
r = [1.5] * gene_length  

freq = 247
for i in range(gene_length):
    harms[i] = (i+1) * freq

ideal_set1 = [harms, amps, a, d, s, r]


harms = [0] * gene_length

amps = [1.0, 0.35, 0.61, 0.09, 0.04, 0.02, 0.02, 0.01, 0.01, 0.01]

a = [0.02] * gene_length
d = [0.4] * gene_length
s = [0.3] * gene_length
r = [1.0] * gene_length  

freq = 220
for i in range(gene_length):
    harms[i] = (i+1) * freq

ideal_set2 = [harms, amps, a, d, s, r]

# End of ideal set


# Class used to store info about fitness helper functions
class fitness_helpers:
    weights = [0] * num_funcs
    funcs = [0] * num_funcs
    on_off_switch = [0] * num_funcs

helper = fitness_helpers()

# Setting data for helper functions
# When adding new functions, be sure to adjust num_funcs accordingly
# helper functions will need at least population, scores and helper.weights[i] as parameters

helper.weights[0] = 1
helper.funcs[0] = "dummy_fitness_helper(population, ideal_set1, scores, helper.weights[0], island_weights)"
helper.on_off_switch[0] = True

helper.weights[1] = 5
helper.funcs[1] = "dummy_fitness_helper(population, ideal_set2, scores, helper.weights[1], island_weights)"
helper.on_off_switch[1] = True

helper.weights[2] = 0.1
helper.funcs[2] = "check_bad_amps(population, scores, helper.weights[2], island_weights)"
helper.on_off_switch[2] = True

helper.weights[3] = 0.1
helper.funcs[3] = "check_increasing_harmonics(population, scores, helper.weights[3], island_weights)"
helper.on_off_switch[3] = True

helper.weights[4] = 5
helper.funcs[4] = "check_true_harmonics(population, scores, helper.weights[4], island_weights)"
helper.on_off_switch[4] = True

helper.weights[5] = 5
helper.funcs[5] = "check_wobbling(population, scores, helper.weights[5], island_weights)"
helper.on_off_switch[5] = True

helper.weights[6] = 5
helper.funcs[6] = "check_octaves(population, scores, helper.weights[6], island_weights)"
helper.on_off_switch[6] = True

helper.weights[7] = 5
helper.funcs[7] = "check_fifths(population, scores, helper.weights[7], island_weights)"
helper.on_off_switch[7] = True

helper.weights[8] = 0.5
helper.funcs[8] = "amps_sum(population, scores, helper.weights[8], island_weights)"
helper.on_off_switch[8] = True

helper.weights[9] = 0.0025
helper.funcs[9] = "error_off_partial(population, scores, helper.weights[9], island_weights)"
helper.on_off_switch[9] = True

helper.weights[10] = 1
helper.funcs[10] = "error_off_amps(population, scores, helper.weights[10], island_weights)"
helper.on_off_switch[10] = True

helper.weights[11] = 0.16
helper.funcs[11] = "check_decreasing_attacks(population, scores, helper.weights[11], island_weights)"
helper.on_off_switch[11] = True


# Set up for choosing crossover
# In main function, will use eval to run one of these functions stored in the list

crossover_list = [0] * num_crossover

crossover_list[0] = "crossover(parents)"
crossover_list[1] = "uniform_crossover(parents)"
crossover_list[2] = "deep_uniform_crossover(parents)"


# Set up for choosing mutation
# In main function, will use eval to run one of these functions stored in the list

mutation_list = [0] * num_mutation

mutation_list[0] = "mutate_gene(new_population)"
mutation_list[1] = "mutate_chromosome(new_population)"


def dummy_fitness_helper(population, ideal_set, scores, weight, island_weights):

    # Used to store score
    temp_score = 0

    # Goes through each element in array to see the difference between it and the ideal set version
    for i in range(mems_per_pop):
        for j in range(num_genes):
            for k in range(gene_length):
                # Calculates score of each element in gene array
                temp_score += abs(ideal_set[j][k] - population[i][j][k])
        # At this point, score should be the sum of scores of all elements in all the genes of the current parent
        # Then we average it by dividing by the total number of elements in each parent
        temp_score = temp_score / (num_genes * gene_length)
    

        # Make the score the inverse so the larger scores are picked for the mating pool
        scores[i] += (1 / temp_score) * weight * island_weights[i] 
        temp_score = 0;

    return scores


def check_bad_amps(population, scores, weight, island_weights):

    # Gives bad fitness scores to parents with extreme amplitudes 
    # Made to get rid of parents that are too loud

    temp_score = 0

    for i in range(mems_per_pop):
        # Takes array of amplitudes from population array
        amplitude = population[i][1]

        for j in range(gene_length):
            if(amplitude[j] < 0.3):
                # Increase score if amplitude is not "too loud"
                temp_score = temp_score + 1

        scores[i] += temp_score * weight * island_weights[i]
        temp_score = 0

    return scores


def check_increasing_harmonics(population, scores, weight, island_weights):

    # Gives good fitness scores to parents that have increasing partials
    # That pattern of partials is generally more desirable than random changes in partials

    temp_score = 0

    for i in range(mems_per_pop):
        # Takes array of harmonics from population array
        frequency = population[i][0] 

        # Current method only checks adjacent harmonics
        for j in range(gene_length - 1):
            if(frequency[j] < frequency[j + 1]):
                temp_score = temp_score + 1

        scores[i] += temp_score * weight * island_weights[i]
        temp_score = 0

    return scores

# Have a fitness functions that rewards true harmonics (other frequencies are multiples of the base frequency)
def check_true_harmonics(population, scores, weight, island_weights):

    # Rewards true harmonics by comparing the base frequency and checking for multiples

    temp_score = 0

    for i in range(mems_per_pop):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0] 

        for j in range(gene_length - 1):

            # Uses int division to round
            if(population[i][0][j + 1] // base_freq == 0 and population[i][0][j + 1] > base_freq):
                temp_score = temp_score + 1
                #print(int(population[i][0][j + 1]))
                #print(int(base_freq))

        scores[i] += temp_score * weight * island_weights[i]
        temp_score = 0

    return scores


# Have a function that punishes "wobbling" or when frequencies are too close, creating a wobbling sound
def check_wobbling(population, scores, weight, island_weights):

    # Punishes frequencies that are too close to the base frequency
    # An alternate version that checks each frequency against each other may be useful

    temp_score = 0

    for i in range(mems_per_pop):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0]

        for j in range(gene_length - 1):

            # Instead of 10, may want to change it to a smaller range like 5
            if(abs(base_freq - population[i][0][j + 1]) < 10):
                temp_score = temp_score + 1 

        scores[i] -= temp_score * weight * island_weights[i]
        temp_score = 0

    return scores

# Have a function that looks for octaves (ratio 2 to 1) and a function that looks for perfect fifth (ratio 3 to 2)
def check_octaves(population, scores, weight, island_weights):

    # Rewards members that have octaves in them

    temp_score = 0

    for i in range(mems_per_pop):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0] 

        for j in range(gene_length - 1):

            # Checks if there is a direct octave to base frequency
            if(int(population[i][0][j + 1]) == int(base_freq) * 2 ):
                temp_score = temp_score + 1

        scores[i] += temp_score * weight * island_weights[i]
        temp_score = 0

    return scores


def check_fifths(population, scores, weight, island_weights):

    # Rewards members that have perfect fifths in them

    temp_score = 0

    for i in range(mems_per_pop):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0] 

        for j in range(gene_length - 1):

            # Checks if there is a perfect fifth to base frequency
            if(int(population[i][0][j + 1]) * 2 == int(base_freq) * 3 ):
                temp_score = temp_score + 1

        scores[i] += temp_score * weight * island_weights[i]
        temp_score = 0

    return scores

def amps_sum(population, scores, weight, island_weights):

    # Punishes members if their sum of amplitudes is to large aka too loud

    for i in range(mems_per_pop):

        amp_sum = 0

        for j in range(gene_length):
            amp_sum += population[i][1][j]

        while(amp_sum > 1):
            scores[i] -= 1 * weight * island_weights[i]
            amp_sum -= 1

    # actually shouldn't need to return scores in helper fitness functions
    return scores


def closestMultiple(n, x):
    if x > n:
        return x;
    z = (int)(x / 2);
    n = n + z;
    n = n - (n % x);
    return n; 


def error_off_partial(population, scores, weight, island_weights):

    # Rewards members that have frequencies that are closer to partials

    for i in range(mems_per_pop):

        # Used to help calculate partials
        base_freq = population[i][0][0]

        temp_sum = 0

        for j in range(gene_length - 1):

            # Finds the the multiple of base freq that is closest to current freq
            if base_freq > population[i][0][j + 1]:
                temp_sum += pow(base_freq - population[i][0][j + 1], 2)
            
            else:    
                # Runs if base freq is smaller than the current freq
                n = closestMultiple(population[i][0][j + 1], base_freq)

                if(population[i][0][j + 1] - n > 0.5):
                    n = n + 1

                temp_sum += pow(population[i][0][j + 1] - n, 2)

        # Use inverse of score because a bigger sum means a larger off error which is bad
        scores[i] -= math.sqrt(temp_sum) * weight * island_weights[i]

    return scores

 
def error_off_amps(population, scores, weight, island_weights):

    # Rewards members that have frequencies that are closer to partials

    for i in range(mems_per_pop):

        temp_sum = 0

        for j in range(gene_length - 1):
            temp_sum += pow(population[i][1][j] / 2 - population[i][1][j + 1], 2)

        # Use inverse of score because a bigger sum means a larger off error which is bad
        # The difference is smaller, so this will skew the results so make sure weight is low
        scores[i] -= math.sqrt(temp_sum) * weight * island_weights[i] 

    return scores       


def check_decreasing_attacks(population, scores, weight, island_weights):

    # Rewards members that have decreasing attack values

    temp_score = 0

    for i in range(mems_per_pop):
        # Takes array of attacks from population array
        attack = population[i][2] 

        # Current method only checks adjacent harmonics
        for j in range(gene_length - 1):
            if(attack[j] > attack[j + 1]):
                temp_score = temp_score + 1

        scores[i] += temp_score * weight * island_weights[i]
        temp_score = 0

    return scores


# Due to the random nature, maybe have it so it's within a range instead of an exact ratio 

def fitness_calc(population, helpers, count, island_weights):
    
    # Stores average scores of all chromosomes
    # Make sure to use += in helper functions when calculating scores to avoid overwriting scores 

    # Each member of the population has their own score
    scores = [0] * mems_per_pop
    for i in range(num_funcs):

        if(helper.on_off_switch[i]):
            eval(helper.funcs[i])

        if(count == (loops - 1)):
            #print(scores)
            # instead of writing scores of each member at the end, it may be good
            # to show scores of each member after each fitness helper??
            write_helper_score(scores, i)


    if(count == (loops - 1)):
        f = open("GA_fitness_scores.txt", "a")
        f.write("---------------------------------------------------\n")
        f.close()

    return scores


def pick_matingpool(population, scores):

    # Picks best parents sort of like tournament style

    # Stores the parents that will be used to make new generation
    matingpool = [0] * num_parents
    j = 0

    # Checks two adjacent chromosomes, picks the one with the higher fitness score
    # For loop advances by 2, not 1 like most loops
    for i in range(0, mems_per_pop, 2):
        if(scores[i] > scores[i + 1]):
            matingpool[j] = population[i]
        else:
            matingpool[j] = population[i + 1]

        # Advance to next index in parent array
        j = j + 1

    return matingpool


def crossover(parents):

    # Halfway point in gene for child, first half goes to one parent, second half goes to the other
    cross_point = num_genes // 2

    count = 0

    # Create empty 3d array to represent new generation
    new_generation = [[0 for x in range(num_genes)] for y in range(mems_per_pop)]

    # Create empty 2d arrays for new members of population
    offspring1 = [0 for y in range(num_genes)]
    offspring2 = [0 for y in range(num_genes)]

    # Used to reset both offspring
    blank_slate = [0 for y in range(num_genes)]


    # For loop that run the same number of times as there are parents
    # Parents will be i and i + 1 except last iteration in loop, which will use the first and last index
    for i in range(num_parents):
        if(i == num_parents - 1):
            # Exception with last element to avoid array out of bounds

            # Takes one half from one parent and one half from the other parent
            offspring1[0:cross_point] = parents[i][0:cross_point]
            offspring1[cross_point:] = parents[0][cross_point:]

            # Takes one half from one parent and one half from the other parent except flipped for this offspring
            offspring2[0:cross_point] = parents[0][0:cross_point]
            offspring2[cross_point:] = parents[i][cross_point:]

            # Add offspring to new generation
            new_generation[count] = offspring1
            new_generation[count + 1] = offspring2

            break


        # Takes one half from one parent and one half from the other parent
        offspring1[0:cross_point] = parents[i][0:cross_point]
        offspring1[cross_point:] = parents[i + 1][cross_point:]

        # Takes one half from one parent and one half from the other parent except flipped for this offspring
        offspring2[0:cross_point] = parents[i + 1][0:cross_point]
        offspring2[cross_point:] = parents[i][cross_point:]

        # Add offspring to new generation
        new_generation[count] = offspring1
        new_generation[count + 1] = offspring2

        # Empty out previous data offspring stored
        offspring1 = blank_slate.copy()
        offspring2 = blank_slate.copy()
        
        # Advance index by 2 since two members were added
        count = count + 2

    return new_generation


def uniform_crossover(parents):

    # Flips a coin between the two parents to decide which genes are passed to the children

    # Create empty 3d array to represent new generation
    new_generation = [[0 for x in range(num_genes)] for y in range(mems_per_pop)]
    z = 0

    for c in range(num_parents):

        # Create new members of population
        child1 = [0] * num_genes
        child2 = [0] * num_genes

        # Special case to avoid array out of bounds
        if(c == num_parents - 1):

            # Picks the first and last parents in the array of parents
            parent1 = parents[0]
            parent2 = parents[num_parents - 1]

            for i in range(num_genes):

                # Flip a coin to determine which parent is picked
                coin = random.randint(0, 1)

                if(coin):
                    # pick parent 1
                    child1[i] = parent1[i]

                else:
                    # pick parent 2
                    child1[i] = parent2[i]

                # Flip a coin to determine which parent is picked
                coin = random.randint(0, 1)

                if(coin):
                    # pick parent 1
                    child2[i] = parent1[i]
                    
                else:
                    # pick parent 2
                    child2[i] = parent2[i]

            
            # Add two new members to new population
            new_generation[z] = child1
            z = z + 1
            new_generation[z] = child2
            z = z + 1
            break

        # Set each parent using parents array
        parent1 = parents[c]
        parent2 = parents[c + 1]

        for i in range(num_genes):

            # Flip a coin to determine which parent is picked
            coin = random.randint(0, 1)

            if(coin):
                # pick parent 1
                child1[i] = parent1[i]
            
            else:
                # pick parent 2
                child1[i] = parent2[i]

            
            # Flip a coin to determine which parent is picked
            coin = random.randint(0, 1)

            if(coin):
                # pick parent 1
                child2[i] = parent1[i]
            
            else:
                # pick parent 2
                child2[i] = parent2[i]

            
        # Add two new members to new population 
        new_generation[z] = child1
        z = z + 1
        new_generation[z] = child2
        z = z + 1

    return new_generation


def deep_uniform_crossover (parents):
    # Similar to uniform crossover, except the coin flip swaps the individual
    # int values in each gene array instead of the whole array
    
    # Create a 3d array to represent new population
    new_generation = [[0 for x in range(num_genes)] for y in range(mems_per_pop)]
    z = 0

    for c in range(num_parents):

        # New children created this way to keep it a numpy type list
        # This allows the main function to be more modular later on

        harms = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        amps = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        a = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        d = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        s = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        r = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)

        child1 = [harms, amps, a, d, s, r]

        # New variables are created because otherwise child1 and child2 hold the same data

        harms2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        amps2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        a2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        d2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        s2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        r2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)

        child2 = [harms2, amps2, a2, d2, s2, r2]

        if(c == num_parents - 1):

            # Special case that helps avoid array out of bounds error
            parent1 = parents[0]
            parent2 = parents[num_parents - 1]

            for i in range(num_genes):
                for j in range(gene_length):

                    # Flip a coin to determine which parent is picked
                    coin = random.randint(0, 1)

                    if(coin):
                        # pick parent 1
                        child1[i][j] = parent1[i][j]

                    else:
                        # pick parent 2
                        child1[i][j] = parent2[i][j]

                    # Flip a coin to determine which parent is picked
                    coin = random.randint(0, 1)

                    if(coin):
                        # pick parent 1
                        child2[i][j] = parent1[i][j]

                    else:
                        # pick parent 2
                        child2[i][j] = parent2[i][j]

            # Add two new members to new population
            new_generation[z] = child1
            # z = z + 1
            new_generation[z + 1] = child2
            z = z + 2
            break

        # Set each parent using parents array
        parent1 = parents[c]
        parent2 = parents[c + 1]

        for i in range(num_genes):
                for j in range(gene_length):

                    # Flip a coin to determine which parent is picked
                    coin = random.randint(0, 1)

                    if(coin):
                        # pick parent 1
                        child1[i][j] = parent1[i][j]

                    else:
                        # pick parent 2
                        child1[i][j] = parent2[i][j]

                    # Flip a coin to determine which parent is picked
                    coin = random.randint(0, 1)

                    if(coin):
                        # pick parent 1
                        child2[i][j] = parent1[i][j]

                    else:
                        # pick parent 2
                        child2[i][j] = parent2[i][j]

        # Add two new members to new population
        new_generation[z] = child1
        # z = z + 1
        new_generation[z + 1] = child2
        z = z + 2



    return new_generation


def mutate_gene(population):

    # Random number generator from 0-7, will decide which chromosome is picked
    # Random number generator from 0-5, will decide which gene is picked
    p = random.randint(0,mems_per_pop - 1)
    c = random.randint(0,num_genes - 1)

    # Coin flip to determine if scalar increases or decreases values
    a = random.randint(0,1)

    # Determines how aggresive mutation is
    if(a):
        scalar = 1 - mutate_scalar
    else:
        scalar = 1 + mutate_scalar

    if(c == 0):
        # print("Mutated h!")
        for i in range(gene_length):
            population[p][c][i] = population[p][c][i] * scalar

    elif(c == 1):
        # print("Mutated m!")
        for i in range(gene_length):
            population[p][c][i] = population[p][c][i] * scalar

    elif(c == 2):
        # print("Mutated a!")
        for i in range(gene_length):
            population[p][c][i] = population[p][c][i] * scalar

    elif(c == 3):
        # print("Mutated d!")
        for i in range(gene_length):
            population[p][c][i] = population[p][c][i] * scalar

    elif(c == 4):
        # print("Mutated s!")
        for i in range(gene_length):
            population[p][c][i] = population[p][c][i] * scalar

    elif(c == 5):
        # print("Mutated r!")
        for i in range(gene_length):
            population[p][c][i] = population[p][c][i] * scalar

    return population


def mutate_chromosome(population):

    # Random number generator from 0-7, will decide which chromosome is picked
    p = random.randint(0,num_parents - 1)

    # Coin flip to determine if scalar increases or decreases values
    a = random.randint(0,1)

    # Determines how aggresive mutation is
    if(a):
        scalar = 1 - mutate_scalar
    else:
        scalar = 1 + mutate_scalar

    for i in range(num_genes):
        for j in range(gene_length):
            population[p][i][j] = population[p][i][j] * scalar


    return population

def intial_gen():

    # Creates a new population using randomly generated values
    new_population = [0] * mems_per_pop
    for i in range(mems_per_pop):
        new_population[i] = [0] * num_genes

    # May want to change high range of m if wav files are too loud
    # Was originally 1.0 instead of 0.5

    for i in range(mems_per_pop):
        h = numpy.random.uniform(low=0.0, high=2500.0, size=gene_length)
        m = numpy.random.uniform(low=0.0, high=0.5, size=gene_length)
        a = numpy.random.uniform(low=0.0, high=0.02, size=gene_length)
        d = numpy.random.uniform(low=0.0, high=0.2, size=gene_length)
        s = numpy.random.uniform(low=0.0, high=1.0, size=gene_length)
        r = numpy.random.uniform(low=0.0, high=3.0, size=gene_length)
        new_population[i] = [h, m, a, d, s, r]

    return new_population


def print_generation(gen):

    # Prints all genes in each chromosome
    for i in range(mems_per_pop):
        print("chromosome {0}".format(i + 1))
        for j in range(num_genes):
            print("Gene {0}".format(j + 1))
            print(gen[i][j])


def write_generation(gen):

    # Writes all genes in a file, useful to verify everything is working as intended
    # Use a for append or w for overwrite
    f = open("GA_output.txt", "a")
    for i in range(mems_per_pop):
        f.write("chromosome {0}\n".format(i + 1))
        for j in range(num_genes):
            f.write("Gene {0}\n".format(j + 1))
            
            f.write("{0}\n".format(gen[i][j]))
    f.write("-------------------------------------------------------------------------------------------------\n")
    f.close()


def write_generation_csv(gen):

    # Writes all genes in a file, useful to verify everything is working as intended
    # Use a for append or w for overwrite
    f = open("GA_output.txt", "a")
    for i in range(mems_per_pop):
        f.write("chromosome {0}\n".format(i + 1))
        for j in range(num_genes):
            f.write("Gene {0}\n".format(j + 1))
            
            for k in range(gene_length):
                f.write("{0}".format(gen[i][j][k]))
                if(k == gene_length - 1):
                    f.write("\n")
                    break
                else:
                    f.write(", ")


    f.close()

def write_fitness_scores(scores):

    # Writes all genes in a file, useful to verify everything is working as intended
    # Use a for append or w for overwrite
    f = open("GA_fitness_scores.txt", "a")
    for i in range(mems_per_pop):
        f.write("Member {0}'s score: {1}\n".format(i + 1, scores[i]))
            
    f.write("---------------------------------------------------------------\n")
    f.close()


def write_helper_score(scores, num):

    f = open("GA_fitness_scores.txt", "a")
    #for i in range(mems_per_pop):
    f.write("Helper {0}'s score: {1}\n".format(num + 1, scores))
            
    #f.write("---------------------------------------------------------------\n")
    f.close()


# Rename this to something like single island??
# Change it so it can accept input??
# Last part should be that it returns the latest population
def single_island(param_pop, island_weights):

    # Checking if passed in population is empty
    if(param_pop[0] == "empty"):
        # Creating the initial population.
        new_population = intial_gen()
        print("THIS IS THE VERY FIRST, empty island!!!")
    else:
        new_population = param_pop

    # Wipes file clean of previous input
    f = open("GA_output.txt", "w")
    f.write("New series of generations:\n")
    f.close()

    # Write intial population into file
    # FOR TESTING PURPOSE, THIS WILL BE COMMENTED OUT FOR NOW

    write_generation(new_population)



    # Creating new generations
    for c in range(loops):

        # Calculates fitness scores using helper functions
        fit_scores = fitness_calc(new_population, helper, c, island_weights)

        # Determintes which chromosomes will be used as parents
        parents = pick_matingpool(new_population, fit_scores)

        # Creates new generation using parents
        # Chooses between list of crossover methods, toggleable at top of file
        new_population = eval(crossover_list[selected_crossover])

        # Uses chance variable at top of file to determine if mutation occurs or not
        p = random.randint(0,chance)
        if(p == 1):
            # Chooses between list of mutation methods, toggleable at top of file
            new_population = eval(mutation_list[selected_mutation])

        # Writes data about current generation in a txt file
        write_generation(new_population)


    
    # Generating wav file section, seperate from actual GA loop

    if(dont_generate_files):
        return new_population


    if(c != (loops - 1)):
        return new_population


    # Creating directory for latest population
    # Folder name includes the Month, day, year, hour and minute

    now = datetime.now()
    # Can add %S at the end to include seconds as well
    date_string = now.strftime("%B %d %Y %H %M %S")

    directory_name = "Generation "
    directory_name = directory_name + date_string

    # May want to make this more modular, have a var pathname at the top
    path = os.path.join("/Users/johnk/OneDrive/Computer Science/Lab stuff/sounds", directory_name)
    os.mkdir(path)

    # Generating file names

    names = [0] * mems_per_pop

    for i in range(mems_per_pop):
        filename = "Sound " + str(i + 1) +".wav"
        names[i] = filename


    # Generates wav files
    for c in range(mems_per_pop):

        for z in range(num_genes):
            # Converts list from numpy floats to normal floats
            # Done this way to give variable types that pyo can use
            new_population[c][z] = new_population[c][z].tolist()

        # Uses sound_generation.py to generate wav files using pyo
        newSound = sound_generation.instrument(new_population[c][0], new_population[c][1], new_population[c][2], new_population[c][3], new_population[c][4], new_population[c][5], gene_length, names[c], directory_name)
        newSound.play_note()


    return new_population



def main():

    # Will keep track of several islands
    # Will run generations using the single_island method repeatedly
    f = open("GA_output.txt", "w")
    f.write("New series of generations:\n")
    f.close()

    f = open("GA_fitness_scores.txt", "w")
    f.write("New series of generations:\n")
    f.close()

    empty_pop = ["empty"]

    islands = [0] * num_isles
    #island_weights = [0] * num_isles


    # each item in islands has the island in 0 and the island_weight in 1
    # this way I can use shuffle for island transfering to get random pairs while
    # not losing track on each island's weight
    for i in range(num_isles):
        # will eventually make it so each island has an array of weights for each helper function, not just one value
        #island_weights[i] = random.uniform(0.1, 5.0)
        weight = numpy.random.uniform(low=0.1, high=5.0, size=gene_length)
        islands[i] = [single_island(empty_pop, weight), weight]


        # numpy.random.uniform(low=0.0, high=2500.0, size=gene_length)


    # create intial islands
    # the random.uniform is the random fitness weight that each island will have on top of each fitness helper's individual weight
    # island_1_weight = random.uniform(0.1, 5.0)
    # print(island_1_weight)
    # island_1 = single_island(empty_pop, island_1_weight)

    # island_2_weight = random.uniform(0.1, 5.0)
    # print(island_2_weight)
    # island_2 = single_island(empty_pop, island_2_weight)



    # run single_island

    # rand_mem1 = random.randint(0, 7)
    # rand_mem2 = random.randint(0, 7)


    #print(island_1[rand_mem1])
    #print(island_2[rand_mem2])

    # retrieve data created from multiple uses of single_island


    # chance to intermingle ?
    # USE RANDOM.SHUFFLE to mix up array, so we can still just trade with adjacent pairs
    # since they will be different everytime

    random.shuffle(islands)

    for x in range(0, num_isles - 1, 2):

        rand_mem1 = random.randint(0, 7)
        rand_mem2 = random.randint(0, 7)

        transfer_member = islands[x][0][rand_mem1]
        islands[x + 1][0][rand_mem1] = islands[x][0][rand_mem2]
        islands[x + 1][0][rand_mem2] = transfer_member


    for i in range(num_isles):
        write_generation(islands[i][0])
    
    #write_generation(island_2)


    # run single_island once again or FOR NOW just check that intermingling worked
    # then just loop this part until satisfied

    # eventually make this range a variable at the top, more modular
    for i in range(4):

        # island_1 = single_island(island_1, island_1_weight)
        # island_2 = single_island(island_2, island_2_weight)

        for i in range(num_isles):
            weight = islands[i][1]
            islands[i][0] = single_island(islands[i][0], weight)

        # rand_mem1 = random.randint(0, 7)
        # rand_mem2 = random.randint(0, 7)

        random.shuffle(islands)

        # might be num_isles - 1
        for x in range(0, num_isles, 2):

            rand_mem1 = random.randint(0, 7)
            rand_mem2 = random.randint(0, 7)

            transfer_member = islands[x][0][rand_mem1]
            islands[x + 1][0][rand_mem1] = islands[x][0][rand_mem2]
            islands[x + 1][0][rand_mem2] = transfer_member

        # transfer_member = island_1[rand_mem1]
        # island_1[rand_mem1] = island_2[rand_mem2]
        # island_2[rand_mem2] = transfer_member

        # write_generation(island_1)
        # write_generation(island_2)

        for i in range(num_isles):
            write_generation(islands[i][0])






main()



