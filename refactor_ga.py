# Main goal of refactoring is to make GA representation more readiable and writeable to help make it better for setup with DB and website

import numpy
import random
# import sound_generation        
import ga_query_functions as query
import os
import math
from datetime import datetime
import json
import sys

# Used to pull constant values from config file
with open('config.json') as config_file:
    data = json.load(config_file)

# List of global constants

# Number of chromosomes in each generation
mems_per_pop = data["mems_per_pop"]

# Number of chromosomes used for matingpool, should be half of mems_per_pop SO when changing memes_per_pop in the JSON, remember to change num_parents as well
num_parents = data["num_parents"]

# Number of genes each chromosome should have, should not be adjusted
num_genes = data["num_genes"]

# Number of values in each gene
gene_length = data["gene_length"]

# Maximum score of functions used to normalize values into range, should be equal to gene_length
max_score = data["max_score"]

# Used to determine how many fitness helper we have in total
num_funcs = data["num_funcs"]

# Number of selection functions
num_selection = data["num_selection"]

# Determines which selection function is used, 0 for tournament, 1 for elitism, 2 for variety, 3 for roulette, 4 for rank
selected_selection = data["selected_selection"]

# Number of crossover functions
num_crossover = data["num_crossover"]

# Determines which crossover function is used, 0 for midpoint, 1 for uniform, 2 for deep uniform
selected_crossover = data["selected_crossover"]

# Number of mutation functions
num_mutation = data["num_mutation"]

# Used to determine chance of mutation occurence in each generation
chance = data["chance"]

# Boolean that switches between sound version (floats) and instrument version (ratios)
sound_mode = data["sound_mode"]

# Number of generations made on a single island before cross mingling occurs
gen_loops = data["gen_loops"]

# Number of times islands swap members and run generations
island_loops = data["island_loops"]

# Used to scale how aggresively the mutation function changes the genes
mutate_scalar = data["mutate_scalar"]

# Used for generating wav files so we can better understand the meaningful differences between the sounds
universal_base_freq = data["universal_base_freq"]

# For testing purposes, makes it so wav files aren't generated if you don't want them
generate_files = data["generate_files"]

# Number of islands each generation in representation, with current representation should always be an even number
num_isles = data["num_isles"]

# A constant used as a weight for the voting ratio of a particular chromosome/member
voting_weight = data["voting_weight"]


# A couple of safety nets to make sure certain variables are changed correctly

if(mems_per_pop % 2 != 0):
    sys.exit("ERROR mems_per_pop must be an even number")
if(num_parents % 2 != 0):
    sys.exit("ERROR num_parents must be an even number")
if(mems_per_pop / 2 != num_parents):
    sys.exit("ERROR num_parents should be half the value of mems_per_pop")

        



# Class used to store info about fitness helper functions
class fitness_helpers:
    weights = [0] * num_funcs
    funcs = [0] * num_funcs
    on_off_switch = [0] * num_funcs

helpers = fitness_helpers()

# Setting data for helper functions
# When adding new functions, be sure to adjust num_funcs accordingly
# helper functions will need at least population, scores and helper.weights[i] and an int to indicate the helper function being used as parameters
# helper weights are used to normalize each helper function
# the on off switch determines which helper functions are used in the first place
# mems_per_pop = data["mems_per_pop"] 
helpers.weights[0] = data["helper_weight_0"]
helpers.funcs[0] = data["helper_func_0"]
helpers.on_off_switch[0] = data["helper_on_off_0"]

helpers.weights[1] = data["helper_weight_1"]
helpers.funcs[1] = data["helper_func_1"]
helpers.on_off_switch[1] = data["helper_on_off_1"]

helpers.weights[2] = data["helper_weight_2"]
helpers.funcs[2] = data["helper_func_2"]
helpers.on_off_switch[2] = data["helper_on_off_2"]

helpers.weights[3] = data["helper_weight_3"]
helpers.funcs[3] = data["helper_func_3"]
helpers.on_off_switch[3] = data["helper_on_off_3"]

helpers.weights[4] = data["helper_weight_4"]
helpers.funcs[4] = data["helper_func_4"]
helpers.on_off_switch[4] = data["helper_on_off_4"]

helpers.weights[5] = data["helper_weight_5"]
helpers.funcs[5] = data["helper_func_5"]
helpers.on_off_switch[5] = data["helper_on_off_5"]

helpers.weights[6] = data["helper_weight_6"]
helpers.funcs[6] = data["helper_func_6"]
helpers.on_off_switch[6] = data["helper_on_off_6"]

helpers.weights[7] = data["helper_weight_7"]
helpers.funcs[7] = data["helper_func_7"]
helpers.on_off_switch[7] = data["helper_on_off_7"]

helpers.weights[8] = data["helper_weight_8"]
helpers.funcs[8] = data["helper_func_8"]
helpers.on_off_switch[8] = data["helper_on_off_8"]

helpers.weights[9] = data["helper_weight_9"]
helpers.funcs[9] = data["helper_func_9"]
helpers.on_off_switch[9] = data["helper_on_off_9"]

helpers.weights[10] = data["helper_weight_10"]
helpers.funcs[10] = data["helper_func_10"]
helpers.on_off_switch[10] = data["helper_on_off_10"]

helpers.weights[11] = data["helper_weight_11"]
helpers.funcs[11] = data["helper_func_11"]
helpers.on_off_switch[11] = data["helper_on_off_11"]

helpers.weights[12] = data["helper_weight_12"]
helpers.funcs[12] = data["helper_func_12"]
helpers.on_off_switch[12] = data["helper_on_off_12"]

helpers.weights[13] = data["helper_weight_13"]
helpers.funcs[13] = data["helper_func_13"]
helpers.on_off_switch[13] = data["helper_on_off_13"]

helpers.weights[14] = data["helper_weight_14"]
helpers.funcs[14] = data["helper_func_14"]
helpers.on_off_switch[14] = data["helper_on_off_14"]

helpers.weights[15] = data["helper_weight_15"]
helpers.funcs[15] = data["helper_func_15"]
helpers.on_off_switch[15] = data["helper_on_off_15"]

helpers.weights[16] = data["helper_weight_16"]
helpers.funcs[16] = data["helper_func_16"]
helpers.on_off_switch[16] = data["helper_on_off_16"]

helpers.weights[17] = data["helper_weight_17"]
helpers.funcs[17] = data["helper_func_17"]
helpers.on_off_switch[17] = data["helper_on_off_17"]

helpers.weights[18] = data["helper_weight_18"]
helpers.funcs[18] = data["helper_func_18"]
helpers.on_off_switch[18] = data["helper_on_off_18"]

helpers.weights[19] = data["helper_weight_19"]
helpers.funcs[19] = data["helper_func_19"]
helpers.on_off_switch[19] = data["helper_on_off_19"]

helpers.weights[20] = data["helper_weight_20"]
helpers.funcs[20] = data["helper_func_20"]
helpers.on_off_switch[20] = data["helper_on_off_20"]

helpers.weights[21] = data["helper_weight_21"]
helpers.funcs[21] = data["helper_func_21"]
helpers.on_off_switch[21] = data["helper_on_off_21"]

helpers.weights[22] = data["helper_weight_22"]
helpers.funcs[22] = data["helper_func_22"]
helpers.on_off_switch[22] = data["helper_on_off_22"]

helpers.weights[23] = data["helper_weight_23"]
helpers.funcs[23] = data["helper_func_23"]
helpers.on_off_switch[23] = data["helper_on_off_23"]


# Set up for choosing selection
# In main function, will use eval to run one of these functions stored in the list

selection_list = [0] * num_selection

selection_list[0] = data["selection_0"]
selection_list[1] = data["selection_1"]
selection_list[2] = data["selection_2"]
selection_list[3] = data["selection_3"]
selection_list[4] = data["selection_4"]


# Set up for choosing crossover
# In main function, will use eval to run one of these functions stored in the list

crossover_list = [0] * num_crossover

crossover_list[0] = data["crossover_0"]
crossover_list[1] = data["crossover_1"]
crossover_list[2] = data["crossover_2"]


# Set up for choosing mutation
# In main function, will use eval to run one of these functions stored in the list

mutation_list = [0] * num_mutation

mutation_list[0] = data["mutation_0"]
mutation_list[1] = data["mutation_1"]
mutation_list[2] = data["mutation_2"]


# Making an ideal set, used for dummy fitness function
    
harms = [0] * gene_length

amps = gene_length * [0]

for i in range(gene_length):
    amps[i] = random.random();

amps.sort(reverse=True)

a = [0.01] * gene_length
d = [0.1] * gene_length
s = [0.5] * gene_length
r = [1.5] * gene_length  

freq = 247
for i in range(gene_length):
    harms[i] = (i+1) * freq

# FOR REFACTOR VERSION will need to use setters to make this happen
ideal_set1 = query.GA()
temp_set1 = [harms, amps, a, d, s, r]
ideal_set1.set_genes(temp_set1)


harms = [0] * gene_length

for i in range(gene_length):
    amps[i] = random.random();

amps.sort(reverse=True)

a = [0.02] * gene_length
d = [0.4] * gene_length
s = [0.3] * gene_length
r = [1.0] * gene_length  

freq = 220
for i in range(gene_length):
    harms[i] = (i+1) * freq

ideal_set2 = query.GA()
temp_set2 = [harms, amps, a, d, s, r]
ideal_set2.set_genes(temp_set2)

# End of ideal set




def dummy_fitness_helper(population, ideal_set, scores, weight, weight_index):


    # Used to store score
    temp_score = 0

    compare_genes = ideal_set.get_genes()

    # Goes through each element in array to see the difference between it and the ideal set version
    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue


        #print(population[i])

        mem_genes = population[i].get_genes()
        # Corresponds to the first element in the freq array
        base_freq = mem_genes[0][0]
        for j in range(num_genes):
            for k in range(gene_length):
                # Calculates score of each element in gene array
                if(sound_mode == False and i == 0):
                    temp_score += abs(compare_genes[j][k] - (mem_genes[j][k] * base_freq) )      
                else:
                    temp_score += abs(compare_genes[j][k] - mem_genes[j][k])
                    
        # At this point, score should be the sum of scores of all elements in all the genes of the current parent
        # Then we average it by dividing by the total number of elements in each parent
        temp_score = temp_score / (num_genes * gene_length)
    
        # Make the score the inverse so the larger scores are picked for the mating pool
        if(sound_mode):
            scores[i] += (1 / temp_score) * weight
        else:
        # population[i][num_genes + 1][weight_index] is the individual member weight for this helper function in the weight array
            scores[i] += (1 / temp_score) * weight * population[i].get_weight(weight_index) 
        temp_score = 0;

    return scores





# Helper fitness functions

def check_bad_amps(population, scores, weight, weight_index):

    # Rewards parents that do not have any extreme amplitudes
    # Goal is too avoid one or a few partials being over centralizing
    # Made to get rid of parents that are too loud

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        # Takes array of amps from population array using get methods
        amps = population[i].get_amps()

        for j in range(gene_length):
            if amps[j] < 0.18:
                # Increse score if amplitude is not "too loud"
                temp_score = temp_score + 1

        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i].get_weight(weight_index)

    return scores


def check_increasing_harmonics(population, scores, weight, weight_index):

    # Gives good fitness scores to members that have increasing partials
    # That pattern of partials is generally more desirable than random changes in partials
    # Don't need to change for insturment mode since the ratios ideally will increase anyway

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        # Takes array of harmonics from population array
        frequency = population[i].get_harms()

        # Current method only check adjacent harmonics
        for j in range(gene_length - 1):
            if(frequency[j] < frequency[j + 1]):
                temp_score += 1

        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i].get_weight(weight_index)

        temp_score = 0

    return scores


def check_true_harmonics(population, scores, weight, weight_index):

    # Rewards (almost) true harmonics by comparing the base frequency and checking for multiples

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        # Take the frequency array from a member of the population
        freq = population[i].get_harms()

        # Take the first frequency in the harmonics array of one member
        if(sound_mode):
            base_freq = freq[0]
        else:
            base_freq = 1.0


        for j in range(gene_length - 1):

            if(sound_mode):
                # Use int division to round since true harmonics will basically never happen 
                # instead we rewards frequencies that are almost true harmonics
                if(freq[j + 1] // base_freq == 0 and freq[j + 1] > base_freq):
                    temp_score += 1

            else:
                # Uses < to effectively round since true harmonics will basically never happen
                # instead we rewards frequencies that are almost true harmonics
                if(freq[j + 1] % 1 < 0.1):
                    temp_score = temp_score + 1

            temp_score /= max_score

            if(sound_mode):
                scores[i] += temp_score * weight
            else:
                scores[i] += temp_score * weight * population[i].get_weight(weight_index)
            temp_score = 0

        return scores


def check_wobbling(population, scores, weight, weight_index):

    # Punishes frequencies that are too close to the base frequency

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        # Take the first frequency in the harmonics array of one member
        freq = population[i].get_harms()
        base_freq = freq[0]

        for j in range(gene_length - 1):

            if(sound_mode):
                # Instead of 10, may want to change it to a smaller range like 5
                if(abs(base_freq - freq[j + 1] < 10)):
                    temp_score += 1

            else:
                if(abs(freq[j + 1] < 0.1)):
                    temp_score += 1

        temp_score /= max_score

        if(sound_mode):
            scores -= temp_score * weight
        else:
            scores[i] -= temp_score * weight * population[i].get_weight(weight_index)
        temp_score = 0

    return scores


def check_octaves(population, scores, weight, weight_index):

    # Rewards members that basically have octaves

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        freq = population[i].get_harms()
        # Take the first frequency in the harmonics array of one member
        base_freq = freq[0]

        for j in range(gene_length - 1):

            if(sound_mode):
                # Check if there is an almost direct octave to base frequency
                if(int(freq[j + 1] == int(base_freq) * 2)):
                    temp_score += 1

            else:
                if(freq[j + 1] == 2.0):
                    temp_score += 1

        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i].get_weight(weight_index)
        temp_score = 0

    return scores


def check_fifths(population, scores, weight, weight_index):

    # Rewards members that have perfect fifths in them

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        freq = population[i].get_harms()
        # Take the first frequency in the harmonics array of one member
        base_freq = freq[0]

        for j in range(gene_length - 1):

            if(sound_mode):
                # Checks if there is a perfect fifth to base frequency
                if(int(freq[j + 1]) * 2 ==  int(base_freq) * 3):
                    temp_score += 1

            else:
                if(freq[j + 1] == 1.5):
                    temp_score += 1

        temp_score /= max_score

        if(sound_mode):
            socres[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i].get_weight(weight_index)
        temp_score = 0

    return scores


def amps_sum(population, scores, weight, weight_index):

    # Punishes members if their sum of amplitudes is too large to avoid clipping

    amp_sum = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        amps = population[i].get_amps()


        for j in range(gene_length):
            amp_sum += amps[j]

        if(amp_sum < 1):
            if(sound_mode):
                scores[i] += (weight / max_score)
            else:
                scores[i] += weight * population[i].get_weight(weight_index)

        amp_sum = 0

    return scores



def closestMultiple(n, x):
    if x > n:
        return x
    z = (int)(x / 2)
    n = n + z
    n = n - (n % x)
    return n


def error_off_partials(population, scores, weight, weight_index):

    # Rewards members that have frequencies that are closer to partials

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        freq = population[i].get_harms()

        # Used to help calculate partials
        if(sound_mode):
            base_freq = freq[0]
        else:
            base_freq = universal_base_freq

        temp_sum = 0

        for j in range(gene_length - 1):

            if(sound_mode):
                # Finds the multiple of base freq that is closest to current freq
                if base_freq > freq[j + 1]:
                    temp_sum += pow(base_freq - freq[j + 1], 2)

                else:
                    # Runs if base freq is smaller than the current freq
                    n = closestMultiple(freq[j + 1], base_freq)

                    if(freq[j + 1] - n > 0.5):
                        n = n + 1
                    temp_sum += pow(freq[j + 1] - n, 2)
            else:
                nearest_partial = round(freq[j + 1])
                temp_sum += pow(freq[j + 1] - nearest_partial, 2)

            if(sound_mode):
                scores[i] -= (math.sqrt(temp_sum) * weight)
            else:
                scores[i] -= math.sqrt(temp_sum) * weight * population[i].get_weight(weight_index)

    return scores


def error_off_amps(population, scores, weight, weight_index):

    # Rewards members that have amplitudes that are closer to integer values

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        amps = population[i].get_amps()

        temp_sum = 0

        for j in range(gene_length - 1):
            temp_sum += pow(amps[j] / 2 - amps[j + 1], 2)

        temp_sum = math.tanh(temp_sum)

        if(sound_mode):
            scores[i] -= math.sqrt(temp_sum) * weight
        else:
            scores[i] -= math.sqrt(temp_sum) * weight * population[i].get_weight(weight_index)

    return scores


def check_decreasing_attacks(population, scores, weight, weight_index):

    # Rewards members that have decreasing attack values

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        # Takes array of attacks from population array
        attack = population[i].get_a()

        # Current method only checks adjacent harmonics
        for j in range(gene_length - 1):
            if(attack[j] > attack[j + 1]):
                temp_score += 1

        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i].get_weight(weight_index)

        temp_score = 0

    return scores


def check_amp_sum(population, scores, weight, weight_index):

    # Checks and rewards sounds that overall have an amplitude less than 1

    amp_sum = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        amps = population[i].get_amps()

        for j in range(gene_length):
            amp_sum += amps[j]

        if amp_sum < 1:
            if(sound_mode):
                scores[i] += weight
            else:
                scores[i] += weight * population[i].get_weight(weight_index)
        amp_sum = 0

    return scores



def check_pads(population, scores, weight, weight_index):

    # Checks and rewards ADSR envelopes that have long attacks and long releases

    # sum of attack and release values
    A_sum = 0
    R_sum = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        attacks = population[i].get_a()
        releases = population[i].get_r()

        for j in range(gene_length):
            if attacks[j] > 0.15:
                A_sum += 1
            if releases[j] > 2.25:
                R_sum += 1

        if(sound_mode):
            scores[i] += R_sum * weight
            scores[i] += A_sum * weight
        else:
            scores[i] += R_sum * weight * population[i].get_weight(weight_index)
            scores[i] += A_sum * weight * population[i].get_weight(weight_index)
        A_sum = 0
        R_sum = 0

    return scores


def check_stacatos(population, scores, weight, weight_index):

    # Checks and rewards ADSR envelopes with short attacks and short releases

    # sum of attack and release values
    A_sum = 0
    R_sum = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        attacks = population[i].get_a()
        releases = population[i].get_r()

        for j in range(gene_length):
            if releases[j] < 0.75:
                R_sum += 1
            if attacks[j] < 0.05:
                A_sum += 1

        A_sum /= max_score
        R_sum /= max_score

        if(sound_mode):
            scores[i] += R_sum * weight
            scores[i] += A_sum * weight
        else:
            scores[i] += R_sum * weight * population[i].get_weight(weight_index)
            scores[i] += A_sum * weight * population[i].get_weight(weight_index)
        A_sum = 0
        R_sum = 0

    return scores


def check_percussive_sounds(population, scores, weight, weight_index):

    # Checks and rewards ADSR envelopes with short attacks and long releases

    # sum of attack and release values
    A_sum = 0
    R_sum = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        attacks = population[i].get_a()
        releases = population[i].get_r()

        for j in range(gene_length):
            if releases[j] > 2.25:
                R_sum +=1

            if attacks[j] < 0.05:
                A_sum += 1

        A_sum /= max_score
        R_sum /= max_score

        if(sound_mode):
            scores[i] += (R_sum + A_sum) * weight
        else: scores[i] += (R_sum + A_sum) * weight * population[i].get_weight(weight_index)

        A_sum = 0
        R_sum = 0

    return scores



def check_transients(population, scores, weight, weight_index):

    # Checks and rewards ADSR envelopes with short sustains and longer decays

    # sum of decay and sustain values
    D_sum = 0
    S_sum = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        decays = population[i].get_d()
        sustains = population[i].get_s()

        for j in range(gene_length):
            if sustains[j] > 2.25:
                S_sum += 1

            if decays[j] < 0.05:
                D_sum += 1

        S_sum /= max_score
        D_sum /= max_score

        if(sound_mode):
            scores[i] += (D_sum + S_sum) * weight
        else:
            scores[i] += (D_sum + S_sum) * weight * population[i].get_weight(weight_index)

        D_sum = 0
        S_sum = 0

    return scores



def check_amp_sparseness(population, scores, weight, weight_index):

    # Checks and rewards a more consisten set of amplitude instead of one central amplitude
    # Uses standard deviation to calculate consistency

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        amp_mean = 0
        temp = 0
        amps = population[i].get_amps()

        for j in amps:
            amp_mean += j

        amp_mean /= gene_length

        for j in amps:
            temp += math.pow(j - amp_mean, 2)

        temp /= gene_length
        temp = math.sqrt(temp)
        temp = math.tanh(temp)

        if(sound_mode):
            scores[i] += temp * weight
        else:
            scores[i] += temp * weight * population[i].get_weight(weight_index)

    return scores



def avoid_too_quiet(population, scores, weight, weight_index):

    # Checks and rewards any amp above a certain threshold

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        amps = population[i].get_amps()

        for j in amps:
            if(j > 0.05):
                temp_score +=1

        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i].get_weight(weight_index)

        temp_score = 0

    return scores


def check_decreasing_amps(population, scores, weight, weight_index):

    temp_score = 0

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        # Takes array of harmonics and amplitudes from population array
        freq = population[i].get_harms()
        amps = population[i].get_amps()

        # Current method only checks adjacent harmonics
        for j in range(gene_length - 1):
            if(freq[j] < freq[j + 1] and amps[j] > amps[j + 1]):
                temp_score += 1

        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i].get_weight(weight_index)
        temp_score = 0

    return scores



def fundamental_freq_amp(population, scores, weight, weight_index):

    # Punishes any partial that is louder than the base freq/fundamental freq

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        # Will need to search through each amplitude of each member
        amplitudes = population[i].get_amps()

        for j in range(gene_length - 1):
            if amplitudes[j + 1] > amplitudes[0]:
                if(sound_mode):
                    scores[i] -= (0.5 * weight) / (max_score / 2)
                else:
                    scores[i] -= (0.5 * weight * population[i].get_weight(weight_index) / (max_score / 2))

    return scores



def inverse_squared_amp(population, scores, weight, weight_index):

    # Rewards functions that amps are closer to equaling 1/(index^2)
    # Takes the difference between the actual value and 1/(index^2)

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        amplitude = population[i].get_amps()

        for j in range(gene_length):

            ideal_amp = 1 / pow(j + 1, 2)
            temp_score = abs(ideal_amp - amplitude[j])

        temp_score = math.tanh(temp_score)

        if(sound_mode):
            scores[i] -= temp_score * weight
        else:
            scores[i] -= temp_score * weight * population[i].get_weight(weight_index)

    return scores



def check_freq_sparseness(population, scores, weight, weight_index):

    # Punishes partials that are too close to each other

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        freq = population[i].get_harms()
        freq.sort()

        temp_score = 0

        for j in range(gene_length - 1):

            if(freq[j + 1] - freq[j] < 0.5):
                if(sound_mode):
                    temp_score += 0.5 * weight
                else:
                    temp_score += 0.5 * weight * population[i].get_weight(weight_index)


        temp_score /= (max_score / 2)
        scores[i] -= temp_score

    return scores



def check_multiples_band(population, scores, weight, weight_index):

    # Favors partials that are within given band range of mulitples of fundamental

    bandwidth = 0.05
    

    for i in range(mems_per_pop):

        # Checks if this particular member has this helper function flipped on
        # if it's flipped off, that member will be skipped for this helper function
        if(not(population[i].get_weight_on_off(weight_index))):
            continue

        freq = population[i].get_harms()
        temp_score = 0
        base_freq = freq[0]
        for j in range(gene_length - 1):
            if(freq[j + 1] > round(freq[j + 1] - bandwidth) and freq[j + 1] < round(freq[j + 1]) + bandwidth):
                temp_score += 1

        temp_score /= max_score

        scores[i] += temp_score * weight * population[i].get_weight(weight_index)

    return scores



def fitness_calc(population, helpers, count):
    
    # Stores average scores of all chromosomes
    # Make sure to use += in helper functions when calculating scores to avoid overwriting scores 

    # Each member of the population has their own score
    scores = [0] * mems_per_pop

    # Based on fitness functions
    for i in range(num_funcs):

        # WHEN UPDATING THIS will probably need a way to adjust scores to account for members that have more fitness functions activated
        # maybe multiply each member's score by the inverse of its num funcs switched on?
        # WILL ALSO need to update fitness functions, currently they are global and can only be turned on or off for all members, include index in parameters in config?
        # OR within each fitness function, check if the on_off switch is on (this would probably be easier)

        # Allows specific helper functions to be turned off globally instead of at the being randomly on or off at the individual level
        if(helpers.on_off_switch[i]):
            eval(helpers.funcs[i])

        #if(count == (gen_loops - 1)):
            # for the future, it may be useful to show scores of each member after each fitness helper as an alternative
            # will need to change or update this to occasionally write the scores down
            # write_helper_score(scores, i)

    # Adjust scores to account for the fact that each member may have different number of helper functions used to calculate their score
    for i in range(mems_per_pop):
        count = 0

        # checks how many helper functions this particular member used to calculate its fitness score
        for j in range(num_funcs):
            count += population[i].get_weight_on_off(j)
        # print(count)

        # avoids divide by zero error
        if count == 0:
            continue

        # multiply by the inverse of helper functions used in order to normalize scores
        scores[i] *= 1 / count


    # Based on votes from website
    for i in range(mems_per_pop):
        scores[i] += query.count_votes(population[i].chromosomeID) * voting_weight

    if(count == (gen_loops - 1)):
        f = open("GA_fitness_scores.txt", "a")
        f.write("---------------------------------------------------\n")
        f.close()

    #print(scores)
    return scores


def tournament_selection(population, scores):

    # Picks the parents sort of like tournament style with a bracket

    # Stores the parents that will be used to make a new generation
    matingpool = [0] * num_parents
    j = 0

    # Checks two adjacent chromosomes, picks the one with the higher fitness score
    # For loop advances by 2, not 1 like most loops
    for i in range(0, mems_per_pop, 2):
        if(scores[i] > scores[i + 1]):
            matingpool[j] = population[i]
        else:
            matingpool[j] = population[i + 1]

        # Advance to the next index in parent array
        j += 1

    return matingpool



def elitism_selection(population, scores):

    # Picks the best parents purely based on the top scores

    matingpool = [0] * num_parents

    for i in range(num_parents):
        # Stores index of the max score each loop
        index_of_max = 0
        latest_max = 0

        for j in range(len(scores)):

            if(scores[j] > latest_max):
                # Index of maximum
                index_of_max = j
                latest_max = scores[j]


        # Zeroes out the maximum scores so the loop can find the other highest scores
        scores[index_of_max] = 0
        # Adds the member with the latest maximum score to become parents

        matingpool[i] = population[index_of_max]

    return matingpool


def variety_selection(population, scores):

    # Picks the most different members in the list (should hopefully be those with
    # the most differences) to try and create more diverse populations

    matingpool = [0] * num_parents

    temp_scores = scores

    temp_scores.sort()

    #Used to determine number of loops and indexing
    t = num_parents // 2

    maxs = [0] * t
    mins = [0] * t

    for i in range(t):

        # Finds the maximum and minimum scores
        maxs[i] = temp_scores[i]
        mins[i] = temp_scores[mems_per_pop - 1 - i]


    # Used to index through matingpool array
    j = 0
    for k in range(t):
        # Finds the index of the maximum and minimum scores in the scores array
        # and adds them to the matingpool so they become parents
        matingpool[j] = population[scores.index(maxs[k])]
        matingpool[j + 1] = population[scores.index(mins[k])]
        j += 2

    return matingpool


def roulette_selection(population, scores):

    # Sum up all the scores to get the upper bound of the roulette wheel
    maximum = 0
    for i in scores:
        maximum += i

    matingpool = []

    # Keeps track of selected parents indices
    mate_index = []

    for k in range(num_parents):

        wheel = random.uniform(0, maximum)
        curr = 0

        for j in range(len(scores)):
            curr += scores[j]
            if curr > wheel and j not in mate_index:
                mate_index.append(j)
                break

    c = 0
    # This accounts for edge cases when not enough elements are added to mate_index
    while(len(mate_index) < num_parents):
        if c not in mate_index:
            mate_index.append(c)
        c += 1

    # Using the indices in mate_index, matingpool is filled with the selected parents
    for p in range(num_parents):
        matingpool.append(population[mate_index[p]])

    return matingpool



def rank_selection(population, scores):

    # Assigns rank and then performs roulette selection

    matingpool = []

    temp_scores = scores

    # orts in descending order instead of ascending order
    temp_scores.sort(reverse=True)

    # Sums up all of the scores to get the upper bound of the roulette wheel
    maximum = 0
    for i in scores:
        maximum += 1

    # Keeps track of selected parents indices
    mate_index = []

    for k in range(num_parents):

        wheel =  random.uniform(0, maximum)
        curr = 0

        for j in range(len(temp_scores)):
            curr += temp_scores[j]
            if curr > wheel and j not in mate_index:
                # returns the index of scores that correspond to the element in the sorted scores
                mate_index.append(scores.index(temp_scores[j]))
                break

    c = 0
    # This accounts for edge cases when not enough elements are added to mate_index
    while(len(mate_index) < num_parents):
        if c not in mate_index:
            mate_index.append(c)
        c += 1

    # Using the indices in mate_index, matingpool is filled with the selected parents
    for p in range(num_parents):
        matingpool.append(population[mate_index[p]])


    return matingpool



def crossover(parents):

    # Halfway point in gene for child, first half goes to one parent, second half goes to the other
    cross_point = num_genes // 2

    count = 0

    # Create am empty array of class GA's to represent the new generation
    new_generation = [0] * mems_per_pop

    # Create empty arrays for new members of population
    offspring1 = [0 for y in range(num_genes)]
    offspring2 = [0 for y in range(num_genes)]

    # Used to reset for both offspring
    blank_slate = [0 for y in range(num_genes)]


    # For loop that runs the same number of times as there are parents
    # Parents will be i and i + 1 except last iteration in the loop which will use the first and last index
    for i in range(num_parents):
        if i == num_parents - 1:
            # Exception with last element to avoid array out of bounds

            # Retrieve all genes from two parents to perform crossover
            parent1 = parents[0].get_genes()
            pid1 = parents[0].get_chromosomeID()
            parent2 = parents[i].get_genes()
            pid2 = parents[i].get_chromosomeID()
            par_gen_num = parents[0].get_gen_number()

            # Takes one half from parent1 and other half from parent2
            #offspring1[0:cross_point] = parent1[0:cross_point]
            offspring1[:cross_point] = parent1[:cross_point]
            offspring1[cross_point:] = parent2[cross_point:]

            # Takes one half from parent1 and other half from parent2 except flipped for this offspring
            offspring2[:cross_point] = parent2[:cross_point]
            offspring2[cross_point:] = parent1[cross_point:]

            # Create new GA's to store new offspring's genes
            mem1 = query.GA()
            mem2 = query.GA()

            # Set genes using the 2 offspring arrays
            mem1.set_genes(offspring1)
            mem2.set_genes(offspring2)

            # Also need to add member specific weights since that is not included in genes array
            mem1.set_weights(parents[0].get_weights())
            mem2.set_weights(parents[i].get_weights())

            # Also need to add which helper functions are used for each member since that is not included in the genes array
            mem1.set_weight_on_off(parents[0].get_weight_on_offs())
            mem2.set_weight_on_off(parents[i].get_weight_on_offs())

            # Also need to store the parents by storing their chromosomeIDs
            mem1.set_parent1(pid1)
            mem1.set_parent2(pid2)

            mem2.set_parent1(pid1)
            mem2.set_parent2(pid2)

            # Also need to set generation number
            #mem1.set_gen_number(par_gen_num + 1)
            #mem2.set_gen_number(par_gen_num + 1)
            new_gen_num = par_gen_num + 1
            mem1.set_gen_number(new_gen_num)
            mem2.set_gen_number(new_gen_num)

            # Add offspring to new generation
            new_generation[count] = mem1
            new_generation[count + 1] = mem2

            break

        # Retrieve all genes from two parents to perfrom crossover
        parent1 = parents[i].get_genes()
        pid1 = parents[i].get_chromosomeID()
        parent2 = parents[i + 1].get_genes()
        pid2 = parents[i + 1].get_chromosomeID()
        par_gen_num = parents[i].get_gen_number()

        # Takes one half from parent1 and other half from parent2
        offspring1[:cross_point] = parent1[:cross_point]
        offspring1[cross_point:] = parent2[cross_point:]

        # Takes one half from parent1 and other half from parent2 except flipped for this offspring
        offspring2[:cross_point] = parent2[:cross_point]
        offspring2[cross_point:] = parent1[cross_point:]

        # Create new GA's to store new offspring's genes
        # may need to use reset method to wipe mem1 and mem2 clean each loop iteration
        mem1 = query.GA()
        mem2 = query.GA()

        # Set genes using the 2 offspring arrays
        mem1.set_genes(offspring1)
        mem2.set_genes(offspring2)

        # Also need to add member specific weights since that is not included in genes array
        mem1.set_weights(parents[i].get_weights())
        mem2.set_weights(parents[i + 1].get_weights())

        # Also need to add which helper functions are used for each member since that is not included in the genes array
        mem1.set_weight_on_off(parents[i].get_weight_on_offs())
        mem2.set_weight_on_off(parents[i + 1].get_weight_on_offs())

        # Also need to store the parents by storing their chromosomeIDs
        mem1.set_parent1(pid1)
        mem1.set_parent2(pid2)

        mem2.set_parent1(pid1)
        mem2.set_parent2(pid2)

        # Also need to set generation number
        new_gen_num = par_gen_num + 1
        #print(new_gen_num)
        mem1.set_gen_number(new_gen_num)
        mem2.set_gen_number(new_gen_num)


        # Add addspring to new generation
        new_generation[count] = mem1
        new_generation[count + 1] = mem2

        # Advance index by 2 since two members were added
        count += 2

    return new_generation


def uniform_crossover(parents):

    # Flips a coin between the two parents to decide which genes are passed to the children

    # Create empty array to represent new generation
    new_generation = [0] * mems_per_pop
    count = 0

    for c in range(num_parents):

        # Create new members of population
        child1 = [0] * num_genes
        child2 = [0] * num_genes

        # Special case to avoid array out of bounds 
        if(c == num_parents - 1):

            # Picks the first and last parents in parent array
            parent1 = parents[0].get_genes()
            pid1 = parents[0].get_chromosomeID()
            parent2 = parents[num_parents - 1].get_genes()
            pid2 = parents[num_parents - 1].get_chromosomeID()
            par_gen_num = parents[0].get_gen_number()

            for i in range(num_genes):

                # Flip a coin to determine which parent is picked for child1
                coin = random.randint(0,1)

                if(coin):
                    # Picks parent 1
                    child1[i] = parent1[i]

                else:
                    # Picks parent 2
                    child1[i] = parent2[i]


                # Flip a coin to determine which parent is picked for child2
                coin = random.randint(0,1)

                if(coin):
                    # Picks parent 1
                    child2[i] = parent1[i]

                else:
                    # Picks parent 2
                    child2[i] = parent2[i]


            #  Create new GA's to store new offspring's genes
            mem1 = query.GA()
            mem2 = query.GA()

            mem1.set_genes(child1)
            mem2.set_genes(child2)

            # Also need to store each member's parents
            mem1.set_parent1(pid1)
            mem1.set_parent2(pid2)

            mem2.set_parent1(pid1)
            mem2.set_parent2(pid2)

            # Also need to set generation number
            mem1.set_gen_number(par_gen_num + 1)
            mem2.set_gen_number(par_gen_num + 1)

            # Also need to do a coin flip to decide which parent's weights will be passed down and which helper functions will be used
            coin = random.randint(0,1)
            coin2 = random.randint(0,1)

            if(coin):
                # Picks parent 1 for weights
                mem1.set_weights(parents[0].get_weights())
            else:
                # Picks parent 2 for weights
                mem1.set_weights(parents[num_parents - 1].get_weights())

            if(coin2):
                # Picks parent 1 for on off switches
                mem1.set_weight_on_off(parents[0].get_weight_on_offs())
            else:
                # Picks parent 2 for on off switches
                mem1.set_weight_on_off(parents[num_parents - 1].get_weight_on_offs)


            coin = random.randint(0,1)
            coin2 = random.randint(0,1)

            if(coin):
                # Picks parent 1 for weights
                mem2.set_weights(parents[0].get_weights())
            else:
                # Picks parent 2 for weights
                mem2.set_weights(parents[num_parents - 1].get_weights())

            if(coin2):
                # Picks parent 1 for on off switches
                mem2.set_weight_on_off(parents[0].get_weight_on_offs())
            else:
                # Picks parent 2 for on off switches
                mem2.set_weight_on_off(parents[num_parents - 1].get_weight_on_offs)

            


            # Add two new members to new population
            new_generation[count] = mem1
            new_generation[count + 1] = mem2

            break


        # Pick the parents from the parent array
        parent1 = parents[c].get_genes()
        pid1 = parents[c].get_chromosomeID()
        parent2 = parents[c + 1].get_genes()
        pid2 = parents[c + 1].get_chromosomeID()
        par_gen_num = parents[c].get_gen_number()

        for i in range(num_genes):

            # Flip a coin to determine which parent is picked for child1
            coin = random.randint(0,1)

            if(coin):
                # Picks parent 1
                child1[i] = parent1[i]
            else:
                # Picks parent 2
                child1[i] = parent2[i]


            # Flip a coin to determine which parent is picked for child2
            coin = random.randint(0,1)

            if(coin):
                # Picks parent 1
                child2[i] = parent1[i]
            else:
                # Picks parent 2
                child2[i] = parent2[i]


        #  Create new GA's to store new offspring's genes
        mem1 = query.GA()
        mem2 = query.GA()

        mem1.set_genes(child1)
        mem2.set_genes(child2)

        # Also need to store each member's parents
        mem1.set_parent1(pid1)
        mem1.set_parent2(pid2)

        mem2.set_parent1(pid1)
        mem2.set_parent2(pid2) 

        # Also need to set generation number
        mem1.set_gen_number(par_gen_num + 1)
        mem2.set_gen_number(par_gen_num + 1)

        # Also need to do a coin flip to decide which parent's weights will be passed down and which helper functions will be used
        coin = random.randint(0,1)
        coin2 = random.randint(0,1)

        if(coin):
            # Picks parent 1 for weight
            mem1.set_weights(parents[0].get_weights())
        else:
            # Picks parent 2 for weight
            mem1.set_weights(parents[num_parents - 1].get_weights())

        if(coin2):
            # Picks parent 1 for on off switch
            mem1.set_weight_on_off(parents[0].get_weight_on_offs())
        else:
            # Picks parent 2 for on off switch
            mem1.set_weight_on_off(parents[num_parents - 1].get_weight_on_offs())


        coin = random.randint(0,1)
        coin2 = random.randint(0,1)

        if(coin):
            # Picks parent 1 for weight
            mem2.set_weights(parents[0].get_weights())
        else:
            # Picks parent 2 for weight
            mem2.set_weights(parents[num_parents - 1].get_weights())

        if(coin2):
            # Picks parent 1 for on off switch
            mem1.set_weight_on_off(parents[0].get_weight_on_offs())
        else:
            # Picks parent 2 for on off switch
            mem1.set_weight_on_off(parents[num_parents - 1].get_weight_on_offs())


        # Add two new members to new population
        new_generation[count] = mem1
        new_generation[count + 1] = mem2

        count += 2


    return new_generation

        

def deep_uniform_crossover(parents):
    # Similar to uniform crossover except the coin flip swaps individual
    # int values in each gene array instead of the whole array

    # Create an array to represent the new population
    new_generation = [0] * mems_per_pop
    count = 0

    for c in range(num_parents):

        # Create arrays for each gene array for child1
        harmonics1 = [0] * gene_length
        amplitudes1 = [0] * gene_length
        attack1 = [0] * gene_length
        decay1 = [0] * gene_length
        sustain1 = [0] * gene_length
        release1 = [0] * gene_length
        weight1 = [0] * num_funcs
        on_off1 = [0] * num_funcs

        child1 = [harmonics1, amplitudes1, attack1, decay1, sustain1, release1]

        # Create arrays for each gene array for child2
        harmonics2 = [0] * gene_length
        amplitudes2 = [0] * gene_length
        attack2 = [0] * gene_length
        decay2 = [0] * gene_length
        sustain2 = [0] * gene_length
        release2 = [0] * gene_length
        weight2 = [0] * num_funcs
        on_off2 = [0] * num_funcs

        child2 = [harmonics2, amplitudes2, attack2, decay2, sustain2, release2]


        if(c == num_parents - 1):
            # Special case that helps avoid array out of bounds error
            parent1 = parents[0].get_genes()
            pid1 = parents[0].get_chromosomeID()
            parent2 = parents[num_parents - 1].get_genes()
            pid2 = parents[num_parents - 1].get_chromosomeID()
            par_gen_num = parents[0].get_gen_number()

            p_weights1 = parents[0].get_weights()
            p_weights2 = parents[num_parents - 1].get_weights()
            p_on_off_1 = parents[0].get_weight_on_offs()
            p_on_off_2 = parents[num_parents - 1].get_weight_on_offs()

            for i in range(num_genes):
                for j in range(gene_length):

                    # Flip a coin to determine which parent is picked
                    coin = random.randint(0,1)

                    if(coin):
                        # Pick parent 1
                        child1[i][j] = parent1[i][j]

                    else:
                        # Pick parent 2
                        child1[i][j] = parent2[i][j]

                    # Flip a coin to determine which parent is picked
                    coin = random.randint(0,1)

                    if(coin):
                        # Pick parent 1
                        child2[i][j] = parent1[i][j]

                    else:
                        # Pick parent 2
                        child2[i][j] = parent2[i][j]

            for z in range(num_funcs):

                # Extra handling for the weight and on off arrays since they are different than the other genes

                # Flip two coins to determine which parent is picked
                coin = random.randint(0,1)
                coin2 = random.randint(0,1)

                if(coin):
                    # Pick parent 1 for weight
                    weight1[z] = p_weights1[z]
                else:
                    # Pick parent 2 for weight
                    weight1[z] = p_weights2[z]

                if(coin2):
                    # Pick parent 1 for on off switch
                    on_off1[z] = p_on_off_1[z]
                else:
                    # Pick parent 2 for on off switch
                    on_off1[z] = p_on_off_2[z]

                # Flip two coins to determine which parent is picked
                coin = random.randint(0,1)
                coin2 = random.randint(0,1)

                if(coin):
                    # Pick parent 1 for weight
                    weight2[z] = p_weights1[z]
                else:
                    # Pick parent 2 for weight
                    weight2[z] = p_weights2[z]

                if(coin2):
                    # Pick parent 1 for on off switch
                    on_off2[z] = p_on_off_1[z]
                else:
                    # Pick parent 2 for on off switch
                    on_off2[z] = p_on_off_2[z]

            # Create new GA's for children
            mem1 = query.GA()
            mem2 = query.GA()

            # Set genes and weights of mem1 and mem2
            mem1.set_genes(child1)
            mem1.set_weights(weight1)
            mem1.set_weight_on_off(on_off1)

            mem2.set_genes(child2)
            mem2.set_weights(weight2)
            mem2.set_weight_on_off(on_off2)

            # Also need to store each member's parents
            mem1.set_parent1(pid1)
            mem1.set_parent2(pid2)

            mem2.set_parent1(pid1)
            mem2.set_parent2(pid2)

            # Also need to set generation number
            #mem1.set_gen_number(par_gen_num + 1)
            #mem2.set_gen_number(par_gen_num + 1)
            new_gen_num = par_gen_num + 1
            #print(new_gen_num)
            mem1.set_gen_number(new_gen_num)
            mem2.set_gen_number(new_gen_num)

            # Add new mems to new population
            new_generation[count] = mem1
            new_generation[count + 1] = mem2

            # Used to have a break statement but it did not break out of all loops
            # Instead a return statement is used to exit out of the function properly

            return new_generation


        # Everything below is similar to the special case above, the main
        # difference is that the indexing of the parents is slightly different
        parent1 = parents[c].get_genes()
        pid1 = parents[c].get_chromosomeID()
        parent2 = parents[c + 1].get_genes()
        pid2 = parents[c + 1].get_chromosomeID()
        par_gen_num = parents[c].get_gen_number()

        p_weights1 = parents[0].get_weights()
        p_weights2 = parents[num_parents - 1].get_weights()
        p_on_off_1 = parents[0].get_weight_on_offs()
        p_on_off_2 = parents[num_parents - 1].get_weight_on_offs()

        for i in range(num_genes):
            for j in range(gene_length):

                # Flip a coin to determine which parent is picked
                coin = random.randint(0,1)

                if(coin):
                    # Pick parent 1
                    child1[i][j] = parent1[i][j]

                else:
                    # Pick parent 2
                    child1[i][j] = parent2[i][j]

                # Flip a coin to determine which parent is picked
                coin = random.randint(0,1)

                if(coin):
                    # Pick parent 1
                    child2[i][j] = parent1[i][j]

                else:
                    # Pick parent 2
                    child2[i][j] = parent2[i][j]

        for z in range(num_funcs):
            
            # Extra handling for the weight array since it is different than the other genes

            # Flip two coins to determine which parent is picked
            coin = random.randint(0,1)
            coin2 = random.randint(0,1)

            if(coin):
                # Pick parent 1 for weight
                weight1[z] = p_weights1[z]
            else:
                # Pick parent 2 for weight
                weight1[z] = p_weights2[z]

            if(coin2):
                # Pick parent 1 for on off switch
                on_off1[z] = p_on_off_1[z]
            else:
                # Pick parent 2 for on off switch
                 on_off1[z] = p_on_off_2[z]

            # Flip two coins to determine which parent is picked
            coin = random.randint(0,1)
            coin2 = random.randint(0,1)

            if(coin):
                # Pick parent 1 for weight
                weight2[z] = p_weights1[z]
            else:
                # Pick parent 2 for weight
                weight2[z] = p_weights2[z]

            if(coin2):
                # Pick parent 1 for on off switch
                on_off2[z] = p_on_off_1[z]
            else:
                # Pick parent 2 for on off switch
                on_off2[z] = p_on_off_2[z]

        # Create new GA's for children
        mem1 = query.GA()
        mem2 = query.GA()

        # Set genes and weights of mem1 and mem2
        mem1.set_genes(child1)
        mem1.set_weights(weight1)

        mem2.set_genes(child2)
        mem2.set_weights(weight2)

        # Also need to store each member's parents
        mem1.set_parent1(pid1)
        mem1.set_parent2(pid2)

        mem2.set_parent1(pid1)
        mem2.set_parent2(pid2)

        # Also need to set generation number
        #mem1.set_gen_number(par_gen_num + 1)
        #mem2.set_gen_number(par_gen_num + 1)
        new_gen_num = par_gen_num + 1
        #print(new_gen_num)
        mem1.set_gen_number(new_gen_num)
        mem2.set_gen_number(new_gen_num)

        # Add new mems to new population
        new_generation[count] = mem1
        new_generation[count + 1] = mem2

        count += 2

        # No return at the bottom because there is an earlier return statement
        # that will always execute as the last step


def mutate_gene(population):

    # Random number generator from 0-7 that decides which chromosome is picked
    # Random number generator from 0-5 that decides which gene is picked
    p = random.randint(0, mems_per_pop - 1)
    c = random.randint(0, num_genes - 1)

    # Coin flip to determine if scalar increases or decreases values
    a = random.randint(0,1)

    # Determines how aggresive mutation is:
    if a:
        scalar = 1 - mutate_scalar
    else:
        scalar = 1 + mutate_scalar

    if c == 0:
        harms = population[p].get_harms()
        for i in range(gene_length):
            # Additional handling required for instrument/ratio mode to ignore base frequency
            if(not sound_mode and i == 0):
                continue
            harms[i] = harms[i] * scalar

        population[p].set_harms(harms)

    elif c == 1:
        amps = population[p].get_amps()
        for i in range(gene_length):
            amps[i] = amps[i] * scalar

        population[p].set_amps(amps)

    elif c == 2:
        attack = population[p].get_a()
        for i in range(gene_length):
            attack[i] = attack[i] * scalar

        population[p].set_a(attack)

    elif c == 3: 
        decay = population[p].get_d()
        for i in range(gene_length):
            decay[i] = decay[i] * scalar

        population[p].set_d(decay)

    elif c == 4:
        sustain = population[p].get_s()
        for i in range(gene_length):
            sustain[i] = sustain[i] * scalar
            # Sustains need to be between 0 and 1, this handles edge cases where sustain is set to above 1.0
            if sustain[i] > 1.0:
                sustain[i] = 1.0

        population[p].set_s(sustain)

    elif c == 5:
        release = population[p].get_r()
        for i in range(gene_length):
            release[i] = release[i] * scalar

        population[p].set_r(release)

    return population



def mutate_member(population):

    # Random number generator from 0-7 will decide which member is picked
    p = random.randint(0, mems_per_pop - 1)

    # Coin flip to determine if scalar increases or decreases values
    a = random.randint(0,1)

    # Determines how aggresive mutation is
    if a:
        scalar = 1 - mutate_scalar
    else:
        scalar = 1 + mutate_scalar

    mem = population[p].get_genes()
    for i in range(num_genes):
        for j in range(gene_length):
            # Additional handling required for instrument mode to ignore base frequency
            if(sound_mode == False and i == 0 and j == 0):
                continue
            mem[i][j] = mem[i][j] * scalar
            # Special case to avoid sustain values being above 1.0
            if(i == 4 and mem[i][j] > 1.0):
                mem[i][j] = 1.0

    population[p].set_genes(mem)

    return population



def mutate_individual_weight(population):

    # Mutate each element in the indivudal weight array as an attempt to create diversity

    # Random number generator from 0-7 which decides which member is picked
    p = random.randint(0, mems_per_pop - 1)

    w = population[p].get_weights()

    for i in range(num_funcs):

        # Mutate weight by a random scalar
        scalar = numpy.random.uniform(0.0, 2.0)

        # Set weight array
        w[i] = w[i] * scalar

    population[p].set_weights(w)


    # Have a chance to turn a helper on or off

    s = population[p].get_weight_on_offs()

    for i in range(num_funcs):

        # Have a low chance to pick a helper function
        coin = random.randint(0, num_funcs)

        if(coin == 0):
            # Changes current on off switch for a helper function to its opposite
            if(s[i] == 0):
                s[i] = 1
            else:
                s[i] = 1

    return population




# def write_fitness_scores(scores):

#     # Writes all genes in a file, useful to verify everything is working as intended
#     # Use a for append or w for overwrite
#     f = open("GA_fitness_scores.txt", "a")
#     for i in range(mems_per_pop):
#         f.write("Member {0}'s score: {1}\n".format(i + 1, scores[i]))
            
#     f.write("---------------------------------------------------------------\n")
#     f.close()


# def write_helper_score(scores, num):

#     f = open("GA_fitness_scores.txt", "a")
#     #for i in range(mems_per_pop):
#     f.write("Helper {0}'s score: {1}\n".format(num + 1, scores))
            
#     #f.write("---------------------------------------------------------------\n")
#     f.close()




def print_generation(gen):

    # Prints all genes in each chromosome
    for i in range(mems_per_pop):
        print("chromosome {0}".format(i + 1))
        for j in range(num_genes):
            print("Gene {0}".format(j + 1))
            print(gen[i].genes[j])



def initial_gen():

    # Creates a new population using randomly generated values
    new_population = [0] * mems_per_pop

    for i in range(mems_per_pop):

        #print(i)

        temp = query.GA()
        temp.init_harms()

        new_population[i] = temp

        #print(new_population[i])
            
            # The base freq index will be equal to the value num_genes
            # In other parts of the code, the base_freq is usually referenced in the array using the constant num_genes
            # num_genes is currently set to 6 which doesn't actually reflect the total length of the array
            # The code is just set up in a way so base_freq and the weights array are not referenced for most of the helper functions
            # where as the h, m and adsr arrays are referenced far more in the helper functions

            
    return new_population

def single_island(param_pop):

    # Use local variable for population parameter
    new_population = param_pop

    # Creating new generations
    for c in range(gen_loops):

        # Calculates fitness scores using helper functions
        fit_scores = fitness_calc(new_population, helpers, c)

        # Determine which chromosomes will be used as parents
        # Chooses between list of selection methods, toggleable at top of file ADD THOSE TO TOP
        parents = eval(selection_list[selected_selection])

        # Creates new generation using parents
        # Chooses between list of crossover methods, toggleable at top of file ADD THOSE TO TOP
        new_population = eval(crossover_list[selected_crossover])

        # Shuffles around the order members are in array without mixing up their individual data
        # This is done because otherwise certain selection functions will always end up comparing 
        # children from the same parents, so things should be more mixed around so that doesn't happen as often
        random.shuffle(new_population)

        # Uses chance variable at top of file to determine if mutation occurs or not
        # MAKE THIS SECTION MORE MODULAR USING CONSTANTS, this could be done in other areas too
        p = random.randint(0, chance)
        if(p == 1):
            # Randomly chooses between list of mutation methods
            r = random.randint(0, 2)
            new_population = eval(mutation_list[r])

    # if c != (gen_loops - 1):
    #     return new_population

    # if there are issues with the crossover function updating gen_num, then use the code below to manually increment the gen_num
    # for i in range(mems_per_pop):
    #     temp = new_population[i].get_gen_number()
    #     new_population[i].set_gen_number(temp + 1)


    return new_population


def generate_wav_files(new_population):

    # Used to be part of single_island function, decided to make this section its own function
    # Currently handles a whole island of members, may need to modify later to handle a single member

    if not generate_files:
        return None


    # I'll include the directory stuff here but may have to modify
    # Will probably have to return the wav files directly or store them in one of the folders in website

    # Creating directory for latest population
    # Folder name includes the Month, day, year, hour and minute

    now = datetime.now()
    # Can add %S at the end to include seconds and %f to include millseconds as well
    date_string = now.strftime("%B %d %Y %H %M %S %f")
    directory_name = "Generation "
    directory_name = directory_name + date_string

    # Absolute path style
    #path = os.path.join("/Users/johnk/OneDrive/Computer Science/Lab stuff/sounds", directory_name)

    # Relative path style
    path = os.path.join("./sounds", directory_name)
    os.mkdir(path)

    # Generating file names

    names = [0] * mems_per_pop

    for i in range(mems_per_pop):
        filename = "Sound " + str(i + 1) +".wav"
        names[i] = filename


    # Generates wav files
    for c in range(mems_per_pop):

        population = new_population[c].get_genes()

        for z in range(num_genes):
            # Converts list from numpy floats to normal floats
            # Done this way to give variable types that pyo can use
            if isinstance(population[z][0], numpy.floating):
                population[z] = population[z].tolist()


        # Instrument mode will need to multiply frequency ratios by base freq
        # Uses sound_generation.py to generate wav files using pyo
        
        if(sound_mode):
            newSound = sound_generation.instrument(population[0], population[1], population[2], population[3], population[4], population[5], gene_length, names[c], directory_name)
        
        else:
            frequencies = [0] * gene_length
            for w in range(gene_length):
                frequencies[w] = population[0][w] * universal_base_freq
            newSound = sound_generation.instrument(frequencies, population[1], population[2], population[3], population[4], population[5], gene_length, names[c], directory_name)
        
        # Creates a wav files and stores it in a local folder called sounds
        # Methods stored in sound_generation.py
        newSound.play_note()


# Will likely have to modify this to take in parameters
def island_model():

    # Simulates the island model
    # Each island stores several members and islands will swap 
    # members occasionally to try and increase diversity
    # Will run generations using the single_island method repeatedly

    # Used to keep track of data and validate methods
    f = open("GA_output.txt", "w")
    f.write("New series of generations:\n")
    f.close()

    f = open("GA_fitness_scores.txt", "w")
    f.write("New series of generations:\n")
    f.close()


    empty_pop = ["empty"]

    islands = [0] * num_isles

    for i in range(num_isles):

        # Make new generation and use single_island to run 10 generations
        new_population = initial_gen()
        islands[i] = single_island(new_population)

    # intermingling occurs here
    # Use RANDOM.SHUFFLE to mix up array, lets us pick adjacent partners that aren't the same each time
    random.shuffle(islands)

    # This loops simply swaps members of islands to increase diversity
    for x in range(0, num_isles - 1, 2):

        rand_mem1 = random.randint(0, 7)
        rand_mem2 = random.randint(0, 7)

        transfer_member = islands[x][rand_mem1]
        islands[x + 1][rand_mem1] = islands[x][rand_mem2]
        islands[x + 1][rand_mem2] = transfer_member

    # Record data of each island
    for i in range(num_isles):
        if(sound_mode):
            write_generation(islands[i])
        else:
            write_ratio_generation(islands[i])


    # Repeats basically everything above except with existing islands instead of making new ones
    # somewhat redundant, can probably combine this and above section
    for i in range(island_loops):

        for i in range(num_isles):
            islands[i] = single_island(islands[i])

        random.shuffle(islands)

        for x in range(0, num_isles, 2):

            rand_mem1 = random.randint(0, 7)
            rand_mem2 = random.randint(0, 7)

            transfer_member = islands[x][rand_mem1]
            islands[x + 1][rand_mem1] = islands[x][rand_mem2]
            islands[x + 1][rand_mem2] = transfer_member

        for j in range(num_isles):
            if(sound_mode):
                write_generation(islands[j])
            else:
                write_ratio_generation(islands[j])


def two_islands(pop1, pop2):

    # Similar to island_model except only works with a pair of islands instead of many islands

    # Used to keep track of data and validate methods
    f = open("GA_output.txt", "w")
    f.write("New series of generations:\n")
    f.close()

    f = open("GA_fitness_scores.txt", "w")
    f.write("New series of generations:\n")
    f.close()

    # Loop amount is based on constant island_loops at top of file
    for i in range(island_loops):

        # Runs GA on individual islands
        pop1 = single_island(pop1)
        pop2 = single_island(pop2)
        
        # Swaps a member between two islands
        rand_mem1 = random.randint(0, mems_per_pop - 1)
        rand_mem2 = random.randint(0, mems_per_pop - 1)

        transfer_member = pop1[rand_mem1]
        pop1[rand_mem1] = pop2[rand_mem2]
        pop2[rand_mem2] = transfer_member

        if(sound_mode):
            write_generation(pop1[0])
        else:
            write_ratio_generation(pop2[0])


    islands = [pop1, pop2]

    return islands
    # Alternate return style
    # return pop1, pop2


def single_wav(member):

    # Modified version of generate_wav_files that only makes a wav file
    # for a single member instead of an entire island

    if not generate_files:
        return None


    # I'll include the directory stuff here but may have to modify
    # Will probably have to return the wav files directly or store them in one of the folders in website

    # Creating directory for latest population
    # Folder name includes the Month, day, year, hour and minute

    now = datetime.now()
    # Can add %S at the end to include seconds and %f to include millseconds as well
    date_string = now.strftime("%B %d %Y %H %M %S %f")
    directory_name = "Generation "
    directory_name = directory_name + date_string

    # Absolute path style
    #path = os.path.join("/Users/johnk/OneDrive/Computer Science/Lab stuff/sounds", directory_name)

    # Relative path style
    path = os.path.join("./sounds", directory_name)
    os.mkdir(path)

    # Generating file names
    name = "Sound 1.wav"

    # Generates wav files

    population = member.get_genes()

    for z in range(num_genes):
        # Converts list from numpy floats to normal floats
        # Done this way to give variable types that pyo can use
        if isinstance(population[z][0], numpy.floating):
            population[z] = population[z].tolist()


    # Instrument mode will need to multiply frequency ratios by base freq
    # Uses sound_generation.py to generate wav files using pyo
        
    if(sound_mode):
        newSound = sound_generation.instrument(population[0], population[1], population[2], population[3], population[4], population[5], gene_length, name, directory_name)
        
    else:
        frequencies = [0] * gene_length
        for w in range(gene_length):
            frequencies[w] = population[0][w] * universal_base_freq
        newSound = sound_generation.instrument(frequencies, population[1], population[2], population[3], population[4], population[5], gene_length, name, directory_name)
        
    # Creates a wav files and stores it in a local folder called sounds
    # Methods stored in sound_generation.py
    newSound.play_note()








# Used for testing purposes


#testing = query.GA()
#testing.init_harms()
#print(testing.harms)

#print("Now to show off all the genes")

#for i in range(num_genes):
#    print(testing.genes[i])

# new_population = initial_gen()

# for i in new_population:
#     pid1 = i.get_parent1()
#     pid2 = i.get_parent2()
#     print(pid1)
#     print(pid2)

#print(new_population)

#print(new_population)

#print_generation(new_population)

#for j in arr:
#    print(j.genes)
#    print("---------------------------------------------------------")


# initial_gen appears to work correctly, on to other code


#print(pop[0].genes[0][0])
# count or the third arg are used to keep track of looping so printing occurs at the last loop which is determined by gen_loops
# fit_scores = fitness_calc(new_population, helpers, 1)

#print(new_population)

# Early part of fitness calc done, now to add all the other helpers


# other part of the most basic GA is selection, crossover and mutation

# parents = tournament_selection(new_population, fit_scores)

#print(parents)

#print(new_population)

#print_generation(parents)

# new_population = deep_uniform_crossover(parents)

#print("---------------------------------------------------------------------------")
#print_generation(new_population)


#print(new_population)


# new_population = mutate_gene(new_population)

#print("---------------------------------------------------------------------------")

#print_generation(new_population)

#single_wav(new_population[0])


#new_population = single_island(new_population)

#gnum = new_population[0].get_gen_number()
#print(gnum)



#for i in new_population:
#    ga_query_functions.add_member(i, 2)



# single_wav(new_population[0])

# for i in new_population:
#     pid1 = i.get_parent1()
#     pid2 = i.get_parent2()
#     print(pid1)
#     print(pid2)


# mems = []
# a = 48
# for i in range(8):
#     temp = query.retrieve_member(a)
#     a += 1
#     mems.append(temp)

# mems = single_island(mems)

# gnum = mems[0].get_gen_number()
# print(gnum)






# comment out when not testing things out
# pop = initial_gen()
# single_island(pop)