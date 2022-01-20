import numpy
import random
import sound_generation
import os
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
loops = 1

# Used to determine chance of mutation occurence in each generation
chance = 1

# Used to determine how many fitness helper we have in total
num_funcs = 4

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
helper.funcs[0] = "dummy_fitness_helper(population, ideal_set1, scores, helper.weights[0])"
helper.on_off_switch[0] = True

helper.weights[1] = 5
helper.funcs[1] = "dummy_fitness_helper(population, ideal_set2, scores, helper.weights[1])"
helper.on_off_switch[1] = True

helper.weights[2] = 0.0025
helper.funcs[2] = "check_bad_amps(population, scores, helper.weights[2])"
helper.on_off_switch[2] = True

helper.weights[3] = 0.005
helper.funcs[3] = "check_increasing_harmonics(population, scores, helper.weights[3])"
helper.on_off_switch[3] = True


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


def dummy_fitness_helper(population, ideal_set, scores, weight):

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
        scores[i] += (1 / temp_score) * weight
        temp_score = 0;

    return scores


def check_bad_amps(population, scores, weight):

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

        scores[i] += temp_score * weight
        temp_score = 0

    return scores


def check_increasing_harmonics(population, scores, weight):

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

        scores[i] += temp_score * weight
        temp_score = 0

    return scores


def fitness_calc(population, helpers):
    
    # Stores average scores of all chromosomes
    # Make sure to use += in helper functions when calculating scores to avoid overwriting scores 

    # Each member of the population has their own score
    scores = [0] * mems_per_pop
    for i in range(num_funcs):

        if(helper.on_off_switch[i]):
            eval(helper.funcs[i])

        # print(scores)

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
            # f.write(gen[i][j])
            f.write("{0}\n".format(gen[i][j]))
    f.write("-------------------------------------------------------------------------------------------------\n")
    f.close()


def main():

    # Creating the initial population.
    new_population = intial_gen()

    # Wipes file clean of previous input
    f = open("GA_output.txt", "w")
    f.write("New series of generations:\n")
    f.close()

    # Write intial population into file
    write_generation(new_population)

    # Creating new generations
    for c in range(loops):

        # Calculates fitness scores using helper functions
        fit_scores = fitness_calc(new_population, helper)

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

    # Creating directory for latest population
    # Folder name includes the Month, day, year, hour and minute

    now = datetime.now()
    # Can add %S at the end to include seconds as well
    date_string = now.strftime("%B %d %Y %H %M")

    directory_name = "Generation "
    directory_name = directory_name + date_string

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

main()



