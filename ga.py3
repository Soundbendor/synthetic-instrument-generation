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

# Number of values in each gene
gene_length = 10

# Maximum score of functions used to normalize values into range
max_score = gene_length

# Absolute value of +- range, (-1, 1) is default, then multiplied by this scalar
abs_range = 1

# Number of generations made on a single island before cross mingling occurs
gen_loops = 10

# Number of times islands swap members and run generations
island_loops = 3

# Used to determine chance of mutation occurence in each generation
chance = 1

# Used to determine how many fitness helper we have in total
num_funcs = 24

# Used to scale how aggresively the mutation function changes the genes
mutate_scalar = 0.05

# Number of selection functions
num_selection = 5

# Determines which crossover function is used, 0 for tournament, 1 for elitism, 2 for variety, 3 for roulette, 4 for rank
selected_selection = 4

# Number of crossover functions
num_crossover = 3

# Determines which crossover function is used, 0 for midpoint, 1 for uniform, 2 for deep uniform
selected_crossover = 2

# Number of mutation functions
num_mutation = 3

# For testing purposes, makes it so wav files aren't generated if you don't want them
dont_generate_files = False

# Number of islands each generation in representation, with current representation should always be an even number
num_isles = 20

# Boolean that switches between sound version (floats) and instrument version (ratios)
sound_mode = False

# Used for generating wav files so we can better understand the meaningful differences between the sounds
universal_base_freq = 260


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

ideal_set1 = [harms, amps, a, d, s, r]


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
# helper functions will need at least population, scores and helper.weights[i] and an int to indicate the helper function being used as parameters
# helper weights are used to normalize each helper function
# the on off switch determines which helper functions are used in the first place

helper.weights[0] = 1
helper.funcs[0] = "dummy_fitness_helper(population, ideal_set1, scores, helper.weights[0], 0)"
helper.on_off_switch[0] = True

helper.weights[1] = 5
helper.funcs[1] = "dummy_fitness_helper(population, ideal_set2, scores, helper.weights[1], 1)"
helper.on_off_switch[1] = True

helper.weights[2] = 0.1
helper.funcs[2] = "check_bad_amps(population, scores, helper.weights[2], 2)"
helper.on_off_switch[2] = True

helper.weights[3] = 0.1
helper.funcs[3] = "check_increasing_harmonics(population, scores, helper.weights[3], 3)"
helper.on_off_switch[3] = True

helper.weights[4] = 5
helper.funcs[4] = "check_true_harmonics(population, scores, helper.weights[4], 4)"
helper.on_off_switch[4] = True

helper.weights[5] = 5
helper.funcs[5] = "check_wobbling(population, scores, helper.weights[5], 5)"
helper.on_off_switch[5] = True

helper.weights[6] = 5
helper.funcs[6] = "check_octaves(population, scores, helper.weights[6], 6)"
helper.on_off_switch[6] = True

helper.weights[7] = 5
helper.funcs[7] = "check_fifths(population, scores, helper.weights[7], 7)"
helper.on_off_switch[7] = True

helper.weights[8] = 0.5
helper.funcs[8] = "amps_sum(population, scores, helper.weights[8], 8)"
helper.on_off_switch[8] = True

helper.weights[9] = 0.0025
helper.funcs[9] = "error_off_partial(population, scores, helper.weights[9], 9)"
helper.on_off_switch[9] = True

helper.weights[10] = 1
helper.funcs[10] = "error_off_amps(population, scores, helper.weights[10], 10)"
helper.on_off_switch[10] = True

helper.weights[11] = 0.16
helper.funcs[11] = "check_decreasing_attacks(population, scores, helper.weights[11], 11)"
helper.on_off_switch[11] = True

helper.weights[12] = 1
helper.funcs[12] = "check_amp_sum(population, scores, helper.weights[12], 12)"
helper.on_off_switch[12] = True

helper.weights[13] = 0.05
helper.funcs[13] = "check_pads(population, scores, helper.weights[13], 13)"
helper.on_off_switch[13] = True

helper.weights[14] = 0.05
helper.funcs[14] = "check_stacatos(population, scores, helper.weights[14], 14)"
helper.on_off_switch[14] = True

helper.weights[15] = 0.05
helper.funcs[15] = "check_percussive_sounds(population, scores, helper.weights[15], 15)"
helper.on_off_switch[15] = True

helper.weights[16] = 0.0333
helper.funcs[16] = "check_transients(population, scores, helper.weights[16], 16)"
helper.on_off_switch[16] = True

helper.weights[17] = 20.0
helper.funcs[17] = "check_amp_sparseness(population, scores, helper.weights[17], 17)"
helper.on_off_switch[17] = True

helper.weights[18] = 0.2
helper.funcs[18] = "avoid_too_quiet(population, scores, helper.weights[18], 18)"
helper.on_off_switch[18] = True

helper.weights[19] = 0.2
helper.funcs[19] = "check_decreasing_amps(population, scores, helper.weights[19], 19)"
helper.on_off_switch[19] = True

helper.weights[20] = 0.5
helper.funcs[20] = "fundamental_freq_amp(population, scores, helper.weights[20], 20)"
helper.on_off_switch[20] = True

helper.weights[21] = 0.6666667
helper.funcs[21] = "inverse_squared_amp(population, scores, helper.weights[21], 21)"
helper.on_off_switch[21] = True

helper.weights[22] = 0.6666667
helper.funcs[22] = "check_freq_sparseness(population, scores, helper.weights[22], 22)"
helper.on_off_switch[22] = True

helper.weights[23] = 0.6666667
helper.funcs[23] = "check_multiples_band(population, scores, helper.weights[23], 23)"
helper.on_off_switch[23] = True


# Set up for choosing selection
# In main function, will use eval to run one of these functions stored in the list

selection_list = [0] * num_selection

selection_list[0] = "tournament_selection(new_population, fit_scores)"
selection_list[1] = "elitism_selection(new_population, fit_scores)"
selection_list[2] = "variety_selection(new_population, fit_scores)"
selection_list[3] = "roulette_selection(new_population, fit_scores)"
selection_list[4] = "rank_selection(new_population, fit_scores)"


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
mutation_list[1] = "mutate_member(new_population)"
mutation_list[2] = "mutate_individual_weight(new_population)"


def dummy_fitness_helper(population, ideal_set, scores, weight, weight_index):

    # Used to store score
    temp_score = 0

    # Goes through each element in array to see the difference between it and the ideal set version
    for i in range(mems_per_pop):
        for j in range(num_genes):
            for k in range(gene_length):
                # Calculates score of each element in gene array
                if(sound_mode == False and i == 0):
                    temp_score += abs(ideal_set[j][k] - (population[i][j][k] * population[i][j][num_genes]) )      
                else:
                    temp_score += abs(ideal_set[j][k] - population[i][j][k])
                    
        # At this point, score should be the sum of scores of all elements in all the genes of the current parent
        # Then we average it by dividing by the total number of elements in each parent
        temp_score = temp_score / (num_genes * gene_length)
    
        # Make the score the inverse so the larger scores are picked for the mating pool
        if(sound_mode):
            scores[i] += (1 / temp_score) * weight
        else:
        # population[i][num_genes + 1][weight_index] is the individual member weight for this helper function in the weight array
            scores[i] += (1 / temp_score) * weight * population[i][num_genes + 1][weight_index] 
        temp_score = 0;

    return scores


def check_bad_amps(population, scores, weight, weight_index):

    # Rewards parents that do not have any extreme amplitudes
    # The goal of this helper is too avoid one or a few partials being over centralizing 
    # Made to get rid of parents that are too loud

    temp_score = 0

    for i in range(mems_per_pop):
        # Takes array of amplitudes from population array
        amplitude = population[i][1]

        for j in range(gene_length):
            if(amplitude[j] < 0.18):
                # Increase score if amplitude is not "too loud"
                temp_score = temp_score + 1

        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight 
        else:
            scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]
        temp_score = 0

    return scores


def check_increasing_harmonics(population, scores, weight, weight_index):

    # Gives good fitness scores to parents that have increasing partials
    # That pattern of partials is generally more desirable than random changes in partials
    # Don't need to change for instrument mode since the ratios ideally will increase anyway

    temp_score = 0

    for i in range(mems_per_pop):
        # Takes array of harmonics from population array
        frequency = population[i][0] 

        #frequency.sort()

        # Current method only checks adjacent harmonics
        for j in range(gene_length - 1):
            if(frequency[j] < frequency[j + 1]):
                temp_score = temp_score + 1

        temp_score /= max_score
        
        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]
        temp_score = 0

    return scores


def check_true_harmonics(population, scores, weight, weight_index):

    # Rewards true harmonics by comparing the base frequency and checking for multiples

    temp_score = 0

    
    for i in range(mems_per_pop):

        # Take the first frequency in the harmonics array of one member
        if(sound_mode):
            base_freq = population[i][0][0] 
        else:
            base_freq = population[i][num_genes]

        for j in range(gene_length - 1):

            # Uses int division to round
            if(sound_mode):
                if(population[i][0][j + 1] // base_freq == 0 and population[i][0][j + 1] > base_freq):
                    temp_score = temp_score + 1
                #print(int(population[i][0][j + 1]))
                #print(int(base_freq))
            else:
                if(population[i][0][j + 1] % 1 == 0.0):
                    temp_score = temp_score + 1

        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]
        temp_score = 0

    return scores


def check_wobbling(population, scores, weight, weight_index):

    # Punishes frequencies that are too close to the base frequency

    temp_score = 0

    for i in range(mems_per_pop):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0]

        for j in range(gene_length - 1):

            if(sound_mode):
                # Instead of 10, may want to change it to a smaller range like 5
                if(abs(base_freq - population[i][0][j + 1]) < 10):
                    temp_score = temp_score + 1 
            else:
                if(abs(population[i][0][j + 1] - 1) < 0.1):
                    temp_score = temp_score + 1 
                    
        temp_score /= max_score
        
        if(sound_mode):
            scores[i] -= temp_score * weight
        else:
            scores[i] -= temp_score * weight * population[i][num_genes + 1][weight_index]
        temp_score = 0

    return scores


def check_octaves(population, scores, weight, weight_index):

    # Rewards members that have octaves 

    temp_score = 0

    for i in range(mems_per_pop):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0] 

        for j in range(gene_length - 1):

            if(sound_mode):
                # Checks if there is a direct octave to base frequency
                if(int(population[i][0][j + 1]) == int(base_freq) * 2 ):
                    temp_score = temp_score + 1
            else:
                if(population[i][0][j + 1] == 2.0):
                    temp_score = temp_score + 1
                    
        temp_score /= max_score
        
        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]
        temp_score = 0

    return scores


def check_fifths(population, scores, weight, weight_index):

    # Rewards members that have perfect fifths in them

    temp_score = 0

    for i in range(mems_per_pop):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0] 

        for j in range(gene_length - 1):

            if(sound_mode):
                # Checks if there is a perfect fifth to base frequency
                if(int(population[i][0][j + 1]) * 2 == int(base_freq) * 3 ):
                    temp_score = temp_score + 1
            else:
                if(population[i][0][j + 1] == 1.5):
                    temp_score = temp_score + 1

        temp_score /= max_score
        
        if(sound_mode):
            scores[i] += temp_score * weight 
        else:
            scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]
        temp_score = 0

    return scores

def amps_sum(population, scores, weight, weight_index):

    # Punishes members if their sum of amplitudes is to large to avoid clipping

    for i in range(mems_per_pop):

        amp_sum = 0

        for j in range(gene_length):
            amp_sum += population[i][1][j]
            amp_sum += 1

        if(amp_sum > 1):
            if(sound_mode):
                scores[i] -= (weight / max_score) 
            else:
                scores[i] -= (1 * weight * population[i][num_genes + 1][weight_index]) / max_score

    return scores


def closestMultiple(n, x):
    if x > n:
        return x;
    z = (int)(x / 2);
    n = n + z;
    n = n - (n % x);
    return n; 


def error_off_partial(population, scores, weight, weight_index):

    # Rewards members that have frequencies that are closer to partials

    #mems_per_pop
    for i in range(mems_per_pop):

        # Used to help calculate partials
        if(sound_mode):
            base_freq = population[i][0][0]
        else:
            base_freq = population[i][num_genes]

        temp_sum = 0

        for j in range(gene_length - 1):

            if(sound_mode):
                # Finds the the multiple of base freq that is closest to current freq
                if base_freq > population[i][0][j + 1]:
                    temp_sum += pow(base_freq - population[i][0][j + 1], 2)
            
                else:    
                    # Runs if base freq is smaller than the current freq
                    n = closestMultiple(population[i][0][j + 1], base_freq)

                    if(population[i][0][j + 1] - n > 0.5):
                        n = n + 1
                    temp_sum += pow(population[i][0][j + 1] - n, 2)
            else:
                nearest_partial = round(population[i][0][j + 1])
                temp_sum += pow(population[i][0][j + 1] - nearest_partial, 2)

        temp_sum = math.tanh(temp_sum)

        if(sound_mode):
            scores[i] -= (math.sqrt(temp_sum) * weight)
        else:
            scores[i] -= math.sqrt(temp_sum) * weight * population[i][num_genes + 1][weight_index]
            

    return scores

 
def error_off_amps(population, scores, weight, weight_index):

    # Rewards members that have frequencies that are closer to partials

    for i in range(mems_per_pop):

        temp_sum = 0

        for j in range(gene_length - 1):
            temp_sum += pow(population[i][1][j] / 2 - population[i][1][j + 1], 2)

        temp_sum = math.tanh(temp_sum)

        if(sound_mode):
            scores[i] -= math.sqrt(temp_sum) * weight
        else:
            scores[i] -= math.sqrt(temp_sum) * weight * population[i][num_genes + 1][weight_index]

    return scores       


def check_decreasing_attacks(population, scores, weight, weight_index):

    # Rewards members that have decreasing attack values

    temp_score = 0

    for i in range(mems_per_pop):
        # Takes array of attacks from population array
        attack = population[i][2] 

        # Current method only checks adjacent harmonics
        for j in range(gene_length - 1):
            if(attack[j] > attack[j + 1]):
                temp_score += 1
                
        temp_score /= max_score
        
        if(sound_mode):
            scores[i] += temp_score * weight 
        else:
            scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]
        temp_score = 0

    return scores


def check_amp_sum(population, scores, weight, weight_index):

    # checks and rewards sounds that overall have an amplitude less than 1

    amp_sum = 0

    for i in range(mems_per_pop):

        amps = population[i][1]
        
        for j in (range(gene_length)):
            amp_sum += amps[j]
            
        if amp_sum < 1:
            if(sound_mode):
                scores[i] += weight
            else:
                scores[i] += weight * population[i][num_genes + 1][weight_index]
        amp_sum = 0

    return scores


def check_pads(population, scores, weight, weight_index):

    # checks and rewards ADSR envelopes that have long attacks and long release

    # sum of attack and release values
    A_sum = 0
    R_sum = 0

    for i in range(mems_per_pop):

        attacks = population[i][2]
        releases = population[i][5]

        for j in (range(gene_length)):
            if attacks[j] > 0.15:
                A_sum += 1
            if releases[j] > 2.25:
                R_sum += 1

        A_sum /= max_score
        R_sum /= max_score

        if(sound_mode):
            scores[i] += R_sum * weight
        else:
            scores[i] += R_sum * weight * population[i][num_genes + 1][weight_index]
        
        if(sound_mode):
            scores[i] += A_sum * weight
        else:
            scores[i] += A_sum * weight * population[i][num_genes + 1][weight_index]

        A_sum = 0
        R_sum = 0

    return scores


def check_stacatos(population, scores, weight, weight_index):

    # checks and rewards ADSR envelopes with short attacks and short releases

    # sum of attack and release values
    A_sum = 0
    R_sum = 0

    for i in range(mems_per_pop):

        attacks = population[i][2]
        releases = population[i][5]

        for j in (range(gene_length)):
            if releases[j] < 0.75:
                R_sum += 1
            if attacks[j] < 0.05:
                A_sum += 1
        
        A_sum /= max_score
        R_sum /= max_score
        
        if(sound_mode):
            scores[i] += R_sum * weight
        else:
            scores[i] += R_sum * weight * population[i][num_genes + 1][weight_index]
        
        if(sound_mode):
            scores[i] += A_sum * weight
        else:
            scores[i] += A_sum * weight * population[i][num_genes + 1][weight_index]
        A_sum = 0
        R_sum = 0

    return scores


def check_percussive_sounds(population, scores, weight, weight_index):

    # checks and rewards ADSR envelopes with short attacks and long releases

    # sum of attack and release values
    A_sum = 0
    R_sum = 0

    for i in range(mems_per_pop):

        attacks = population[i][2]
        releases = population[i][5]

        for j in (range(gene_length)):
            if releases[j] > 2.25:
                R_sum += 1

            if attacks[j] < 0.05:
                A_sum += 1

        A_sum /= max_score
        R_sum /= max_score
        
        if(sound_mode):
            scores[i] += (R_sum + A_sum) * weight
        else:
            scores[i] += (R_sum + A_sum) * weight * population[i][num_genes + 1][weight_index]
        A_sum = 0
        R_sum = 0

    return scores



def check_transients(population, scores, weight, weight_index):

    # checks and rewards ADSR envelopes with short sustains and longer decays

    # sum of decay and sustain values
    D_sum = 0
    S_sum = 0

    for i in range(mems_per_pop):

        decays = population[i][3]
        sustains = population[i][4]

        for j in (range(gene_length)):
            if sustains[j] > 2.25:
                S_sum += 1

            if decays[j] < 0.05:
                D_sum += 1

        S_sum /= max_score
        D_sum /= max_score
        
        if(sound_mode):
            scores[i] += (D_sum + S_sum) * weight
        else:
            scores[i] += (D_sum + S_sum) * weight * population[i][num_genes + 1][weight_index]
        D_sum = 0
        S_sum = 0

    return scores


def check_amp_sparseness(population, scores, weight, weight_index):

    # checks and rewards a more consistent set of amplitudes instead of one central amplitude
    # uses standard deviation to calculate consistency

    for i in range(mems_per_pop):
        amp_mean = 0
        temp = 0
        amps = population[i][1]

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
            scores[i] -= temp * weight * population[i][num_genes + 1][weight_index]


    return scores



def avoid_too_quiet(population, scores, weight, weight_index):

    # checks and rewards any amp above a certain threshold 

    temp_score = 0

    for i in range(mems_per_pop):

        amps = population[i][1]

        for j in amps:
            if(j > 0.05):
                temp_score += 1
                
        temp_score /= max_score
        
        if(sound_mode):
            scores[i] += temp_score * weight 
        else:
            scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]

        temp_score = 0

    return scores


def check_decreasing_amps(population, scores, weight, weight_index):

    temp_score = 0

    for i in range(mems_per_pop):
        # Takes array of harmonics from population array
        frequency = population[i][0]
        amplitudes = population[i][1] 


        # Current method only checks adjacent harmonics
        for j in range(gene_length - 1):
            if(frequency[j] < frequency[j + 1] and amplitudes[j] > amplitudes[j + 1]):
                temp_score = temp_score + 1
                
        temp_score /= max_score

        if(sound_mode):
            scores[i] += temp_score * weight 
        else:
            scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]
        temp_score = 0

    return scores


def fundamental_freq_amp(population, scores, weight, weight_index):

    # punishes any partial that is louder than the base freq/fundamental freq

    for i in range(mems_per_pop):

        # will need to search through each amplitude of each member
        amplitude = population[i][1]

        for j in range(gene_length - 1):
            if amplitude[j + 1] > amplitude[0]:
                if(sound_mode):
                    scores[i] -= (0.5 * weight) / (max_score / 2)
                else:
                    scores[i] -= (0.5 * weight * population[i][num_genes + 1][weight_index] / (max_score / 2))

    return scores



def inverse_squared_amp(population, scores, weight, weight_index):

    # Rewards functions that amps are closer to equaling 1/(index^2)
    # Takes the difference between the actual value and 1/(index^2)

    for i in range(mems_per_pop):

        amplitude = population[i][1]

        for j in range(gene_length):

            ideal_amp = 1 / pow(j + 1, 2)
            temp_score = abs(ideal_amp - amplitude[j])
            
        temp_score = math.tanh(temp_score)
        
        if(sound_mode):
            scores[i] -= temp_score * weight
        else:
            scores[i] -= temp_score * weight * population[i][num_genes + 1][weight_index]

    return scores



def check_freq_sparseness(population, scores, weight, weight_index):

    # Punishes partials that are too close to each other
    for i in range(mems_per_pop):

        frequencies = population[i][0]
        frequencies.sort()

        temp_score = 0

        for j in range(gene_length - 1):

            if(frequencies[j + 1] - frequencies[j] < 0.5):
                if(sound_mode):
                    temp_score -= 0.5 * weight
                else:
                    temp_score -= 0.5 * weight * population[i][num_genes + 1][weight_index]
        temp_score /= (max_score / 2)
        scores[i] -= temp_score 
                    

    return scores

def check_multiples_band(population, scores, weight, weight_index):
    
    # Favors partials that are within given band range of multiples of fundamental

    bandwidth = 0.05

    for i in range(mems_per_pop):
        temp_score = 0
        base_freq = population[i][num_genes]
        for j in range(gene_length - 1):
            if(
                ((population[i][0][j + 1]) > round(population[i][0][j + 1]) - 0.05) and
                ((population[i][0][j + 1]) < round(population[i][0][j + 1]) + 0.05)
            ):
                temp_score = temp_score + 1
                
        temp_score /= max_score
        
        scores[i] += temp_score * weight * population[i][num_genes + 1][weight_index]
    return scores


def fitness_calc(population, helpers, count):
    
    # Stores average scores of all chromosomes
    # Make sure to use += in helper functions when calculating scores to avoid overwriting scores 

    # Each member of the population has their own score
    scores = [0] * mems_per_pop
    for i in range(num_funcs):

        if(helper.on_off_switch[i]):
            eval(helper.funcs[i])

        if(count == (gen_loops - 1)):
            # for the future, it may be useful to show scores of each member after each fitness helper as an alternative
            write_helper_score(scores, i)

    if(count == (gen_loops - 1)):
        f = open("GA_fitness_scores.txt", "a")
        f.write("---------------------------------------------------\n")
        f.close()

    return scores


def tournament_selection(population, scores):

    # Picks best parents sort of like tournament style with a bracket

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

        # Zeroes out the maximums score so it the loop can find the other highest scores
        scores[index_of_max] = 0
        # Adds the member with the latest maximum score to become parents

        matingpool[i] = population[index_of_max]

    return matingpool



def variety_selection(population, scores):

    # Picks the most different members in the list (which should hopefully
    # be those with the most different scores) to try and create more diverse populations

    matingpool = [0] * num_parents

    temp_scores = scores

    temp_scores.sort()

    # Used to determine number of loops and indexing
    t = num_parents // 2

    maxs = [0] * t
    mins = [0] * t

    for i in range(t):

        # Finds the maxiumum and minimum scores
        maxs[i] = temp_scores[i]
        mins[i] = temp_scores[mems_per_pop - 1 - i] 

        # maxs[i] = temp_scores[0]
        # mins[i] = temp_scores[t - 1 - i]

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
    while(len(mate_index) < 4):
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

    # Sorts in descending order instead of ascending order
    temp_scores.sort(reverse=True)

    # Sum up all the scores to get the upper bound of the roulette wheel
    maximum = 0
    for i in scores:
        maximum += i

    # Keeps track of selected parents indices
    mate_index = []

    for k in range(num_parents):

        wheel = random.uniform(0, maximum)
        curr = 0

        for j in range(len(temp_scores)):
            curr += temp_scores[j] 
            if curr > wheel and j not in mate_index:
                # returns the index of scores that corresponds to the element in the sorted scores
                mate_index.append(scores.index(temp_scores[j]))
                break

    c = 0
    # This accounts for edge cases when not enough elements are added to mate_index
    while(len(mate_index) < 4):
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


        if(sound_mode):
            num_loops = num_genes
        else:
            num_loops = num_genes + 1

        for i in range(num_loops):


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
    new_generation = [[0 for x in range(num_genes + 1)] for y in range(mems_per_pop)]
    z = 0

    for c in range(num_parents):

        # This code is for testing purposes, will eventually delete
        #print(parents)

        # New children created this way to keep it a numpy type list
        # This allows the main function to be more modular later on

        harms = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        amps = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        a = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        d = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        s = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        r = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        w = numpy.random.uniform(low=0.0, high=10.0, size=num_funcs)
        
        base_freq = 0
        if(sound_mode):
            child1 = [harms, amps, a, d, s, r]
        else:
            child1 = [harms, amps, a, d, s, r, base_freq, w]

        # New variables are created because otherwise child1 and child2 hold the same data

        harms2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        amps2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        a2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        d2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        s2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        r2 = numpy.random.uniform(low=0.0, high=10.0, size=gene_length)
        w2 = numpy.random.uniform(low=0.0, high=10.0, size=num_funcs)
        

        if(sound_mode):
            child2 = [harms2, amps2, a2, d2, s2, r2]
        else:
            child2 = [harms2, amps2, a2, d2, s2, r2, base_freq, w2]

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

            # Additional handling required for instrument mode
            if(sound_mode == False):
                coin = random.randint(0, 1)


                if(coin):
                    child1[num_genes] = parent1[num_genes]
                    child2[num_genes] = parent2[num_genes]

                    # swaps around the weight arrays, may want to add it so it swaps individual members
                    child1[num_genes + 1] = parent1[num_genes + 1]
                    child2[num_genes + 1] = parent2[num_genes + 1]
                else:
                    child1[num_genes] = parent2[num_genes]
                    child2[num_genes] = parent1[num_genes]

                    # swaps around the weight arrays, may want to add it so it swaps individual members
                    child1[num_genes + 1] = parent2[num_genes + 1]
                    child2[num_genes + 1] = parent1[num_genes + 1]


            # Add two new members to new population
            new_generation[z] = child1
            # z = z + 1
            new_generation[z + 1] = child2
            z = z + 2
            
            # used to have a break statement, did not break out all of loops
            # so instead a return was used to exit out of the function properly

            return new_generation

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

        # Additional handling required for instrument mode
        if(sound_mode == False):
                coin = random.randint(0, 1)

                if(coin):
                    child1[num_genes] = parent1[num_genes]
                    child2[num_genes] = parent2[num_genes]

                    # swaps around the weight arrays, may want to add it so it swaps individual members
                    child1[num_genes + 1] = parent1[num_genes + 1]
                    child2[num_genes + 1] = parent2[num_genes + 1]
                else:
                    child1[num_genes] = parent2[num_genes]
                    child2[num_genes] = parent1[num_genes]

                    # swaps around the weight arrays, may want to add it so it swaps individual members
                    child1[num_genes + 1] = parent2[num_genes + 1]
                    child2[num_genes + 1] = parent1[num_genes + 1]

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
            # Additional handling required for instrument/ratio mode to ignore base frequency
            if( sound_mode == False and i == 0):
                continue
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


def mutate_member(population):

    # Random number generator from 0-7, will decide which member is picked
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
            # Additional handling required for instrument mode to ignore base frequency
            if(sound_mode == False and i == 0 and j == 0):
                continue
            population[p][i][j] = population[p][i][j] * scalar
            


    return population


def mutate_individual_weight(population):

    # Mutate each element in the individual weight array as an attempt to create diversity

    # Random number generator from 0-7, will decide which member is picked to mutate
    p = random.randint(0,num_parents - 1)

    # Must be in ratio mode since weight array is only created in ratio mode 
    if(sound_mode == False):

        for i in range(num_funcs):

            # Mutate weight by a random scalar
            scalar = numpy.random.uniform(0.0, 2.0)

            # The 7 corresponds to the weight array
            population[p][7][i] = population[p][7][i] * scalar

    return population

def intial_gen():

    # Creates a new population using randomly generated values
    new_population = [0] * mems_per_pop

    if(sound_mode):
        for i in range(mems_per_pop):
            new_population[i] = [0] * num_genes
    else:
        for i in range(mems_per_pop):
            new_population[i] = [0] * (num_genes + 1)

    for i in range(mems_per_pop):

        # May want to change high range of m if wav files are too loud/peaking
        m = numpy.random.uniform(low=0.0, high = 1 / gene_length, size=gene_length)
        a = numpy.random.uniform(low=0.0, high=0.2, size=gene_length)
        d = numpy.random.uniform(low=0.0, high=0.2, size=gene_length)
        s = numpy.random.uniform(low=0.0, high=1.0, size=gene_length)
        r = numpy.random.uniform(low=0.0, high=3.0, size=gene_length)

        if(sound_mode):
            h = numpy.random.uniform(low=50.0, high=2500.0, size=gene_length)
            new_population[i] = [h, m, a, d, s, r]
        else:
            h = numpy.random.uniform(low=1.0, high=20.0, size=gene_length)
            h = numpy.sort(h)
            
            # The base freq index will be equal to the value num_genes
            # In other parts of the code, the base_freq is usually referenced in the array using the constant num_genes
            # num_genes is currently set to 6 which doesn't actually reflect the total length of the array
            # The code is just set up in a way so base_freq and the weights array are not referenced for most of the helper functions
            # where as the h, m and adsr arrays are referenced far more in the helper functions

            base_freq = random.uniform(50.0, 170.0)
            # The weight array contains weights for each helper function
            w = numpy.random.uniform(low=0.0, high=5.0, size=num_funcs)

            new_population[i] = [h, m, a, d, s, r, base_freq, w]
            
    return new_population


def print_generation(gen):

    # Prints all genes in each chromosome
    for i in range(mems_per_pop):
        print("chromosome {0}".format(i + 1))
        for j in range(num_genes):
            print("Gene {0}".format(j + 1))
            print(gen[i][j])


def print_ratio_generation(gen):

    for i in range(mems_per_pop):
        print("chromosome {0}".format(i + 1))
        for j in range(num_genes + 1):
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


def write_ratio_generation(gen):

    f = open("GA_output.txt", "a")
    for i in range(mems_per_pop):
        f.write("chromosome {0}\n".format(i + 1))
        for j in range(num_genes + 1):
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


# At the end it returns the latest population
def single_island(param_pop):

    # Use local variable for population parameter
    new_population = param_pop
    # Creating new generations
    for c in range(gen_loops):
        # Calculates fitness scores using helper functions
        fit_scores = fitness_calc(new_population, helper, c)

        # Determintes which chromosomes will be used as parents
        # Chooses between list of selection methods, toggleable at top of file
        parents = eval(selection_list[selected_selection])

        # Creates new generation using parents
        # Chooses between list of crossover methods, toggleable at top of file
        
        #print(eval(crossover_list[0]))
        ##@@@@@@@@@@@@@@@@@@@@@@@@@## Issue with crossover methods
        new_population = eval(crossover_list[2])

        # Shuffles around the order members are in array without mixing up their individual data 
        # This is done because otherwise certain selection functions will always end up comparing children
        # from the same parent, so things should be more mixed around so that doesn't happen as often
        random.shuffle(new_population)

        # Uses chance variable at top of file to determine if mutation occurs or not
        p = random.randint(0,chance)
        if(p == 1):
            # Randomly chooses between list of mutation methods
            r = random.randint(0,2)
            new_population = eval(mutation_list[r])


    # Generating wav file section, seperate from actual GA loop

    if(dont_generate_files):
        return new_population


    if(c != (gen_loops - 1)):
        return new_population


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
        #print(new_population[c][0])

        for z in range(num_genes):
            # Converts list from numpy floats to normal floats
            # Done this way to give variable types that pyo can use
            #print(new_population[c][z])
            new_population[c][z] = new_population[c][z].tolist()



        # instrument mode will need to multiply frequency ratios by base freq
        # Uses sound_generation.py to generate wav files using pyo
        
        if(sound_mode):
            newSound = sound_generation.instrument(new_population[c][0], new_population[c][1], new_population[c][2], new_population[c][3], new_population[c][4], new_population[c][5], gene_length, names[c], directory_name)
        else:
            frequencies = [0] * gene_length
            for w in range(gene_length):
                frequencies[w] = new_population[c][0][w] * universal_base_freq
            newSound = sound_generation.instrument(frequencies, new_population[c][1], new_population[c][2], new_population[c][3], new_population[c][4], new_population[c][5], gene_length, names[c], directory_name)
            #print(frequencies)
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
    
    for i in range(num_isles):

        # Make new generation and use single_island to run 10 generations
        new_population = intial_gen()
        islands[i] = single_island(new_population)

    # intermingling occurs here
    # Use RANDOM.SHUFFLE to mix up array, so we can still just trade with adjacent pairs since they will be different everytime
    random.shuffle(islands)

    # This loops simply swaps members of islands to hopefully avoid all members on an islands being the exact same
    for x in range(0, num_isles - 1, 2):

        rand_mem1 = random.randint(0, 7)
        rand_mem2 = random.randint(0, 7)

        transfer_member = islands[x][rand_mem1]
        islands[x + 1][rand_mem1] = islands[x][rand_mem2]
        islands[x + 1][rand_mem2] = transfer_member


    for i in range(num_isles):
        if(sound_mode):
            write_generation(islands[i])
        else:
            write_ratio_generation(islands[i])
    
    # Repeats basically everything above except with existing islands instead of making new ones
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



main()