import numpy
import random
import os
from datetime import datetime
import unittest
import math

# add boolean for sound mode
sound_mode = False 

def closestMultiple(n, x):
    if x > n:
        return x
    z = (int)(x / 2)
    n = n + z
    n = n - (n % x)
    return n

def error_off_partial(population, scores, weight):

    # Rewards members that have frequencies that are closer to partials

    for i in range(1):

        # Used to help calculate partials
        base_freq = population[i][0][0]

        temp_sum = 0

        for j in range(9):

            # Finds the the multiple of base freq that is closest to current freq
            if base_freq > population[i][0][j + 1]:
                temp_sum += pow(base_freq - population[i][0][j + 1], 2)
                
            else:
                # Runs if base freq is smaller than the current freq
                n = closestMultiple(population[i][0][j + 1], base_freq)
                # SHOULD BE POPULATION AND N, n is like the base freq but the closest multiple of other using base_freq

                # might need to check for edge cases, if the difference is ever above 0.5, subtract .5 from n because it will always
                # choose the lowest multiple (comparing 1 and 8.8 will yield 8 instead of 9)

                if(population[i][0][j + 1] - n > 0.5):
                    n = n + 1 

                temp_sum += pow(population[i][0][j + 1] - n, 2)


            #print(temp_sum)

        # Use inverse of score because a bigger sum means a larger off error which is bad

        # maybe just subtract from score to make it simpler? inverse skews the ratio and also doesn't reward if the partials are exactly lined up
        # AKA subtracting makes it easier to deal with edge cases

        #scores[i] += 1 / (temp_sum / (9)) * weight
        scores[i] -= temp_sum * weight



    #print(scores)
    return scores


def error_off_amps(population, scores, weight):
    
    # Rewards members that have frequencies that are closer to partials

    for i in range(1):

        temp_sum = 0

        for j in range(8):
            temp_sum += pow(population[i][1][j] / 2 - population[i][1][j + 1], 2)

        if(sound_mode):
            scores[i] -= math.sqrt(temp_sum) * weight
        else:
            scores[i] -= math.sqrt(temp_sum) * weight

    return scores           


def amps_sum(population, scores, weight):

    # Punishes members if their sum of amplitudes is to large aka too loud

    for i in range(1):

        amp_sum = 0

        for j in range(10):
            amp_sum += population[i][1][j]

        while(amp_sum > 1):
            scores[i] -= 1 * weight
            amp_sum -= 1

    # actually shouldn't need to return scores in helper fitness functions
    return scores


def check_octaves(population, scores, weight):

    # Rewards members that have octaves in them

    temp_score = 0

    for i in range(1):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0] 

        for j in range(9):

            # Checks if there is a direct octave to base frequency
            if(int(population[i][0][j + 1]) == int(base_freq) * 2 ):
                temp_score = temp_score + 1

        scores[i] += temp_score * weight
        temp_score = 0

    return scores


def check_fifths(population, scores, weight):

    # Rewards members that have perfect fifths in them

    temp_score = 0

    for i in range(1):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0] 

        for j in range(9):

            # Checks if there is a perfect fifth to base frequency
            if(int(population[i][0][j + 1]) * 2 == int(base_freq) * 3 ):
                temp_score = temp_score + 1

        scores[i] += temp_score * weight
        temp_score = 0

    return scores

def check_wobbling(population, scores, weight):

    # Punishes frequencies that are too close to the base frequency
    # An alternate version that checks each frequency against each other may be useful

    temp_score = 0

    for i in range(1):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0]

        for j in range(9):

            # Instead of 10, may want to change it to a smaller range like 5
            if(abs(base_freq - population[i][0][j + 1]) < 10):
                temp_score = temp_score + 1 

        scores[i] -= temp_score * weight
        temp_score = 0

    return scores


def check_true_harmonics(population, scores, weight):

    # Rewards true harmonics by comparing the base frequency and checking for multiples

    temp_score = 0

    # for some reason this is looping 16 times instead of 8
    # ACTUALLY THERE APPEARS TO BE AN INFINITE LOOP somewhere
    # problem seems to lie with functions that reference base_freq as the 7th element in population array
    for i in range(1):

        # Take the first frequency in the harmonics array of one member
        if(sound_mode):
            base_freq = population[i][0][0] 
            #print("looping")
        else:
            #print(population[i])
            #print(len(population))
            base_freq = population[i][6]
            #print("looping")

        for j in range(9):

            # Uses int division to round
            if(sound_mode):
                if(population[i][0][j + 1] // base_freq == 0 and population[i][0][j + 1] > base_freq):
                    temp_score = temp_score + 1
                #print(int(population[i][0][j + 1]))
                #print(int(base_freq))
            else:
                if(population[i][0][j + 1] % 1 == 0.0):
                    temp_score = temp_score + 1

        scores[i] += temp_score * weight 
        temp_score = 0

    return scores


def sound_check_wobbling(population, scores, weight):

    # Punishes frequencies that are too close to the base frequency
    # An alternate version that checks each frequency against each other may be useful

    temp_score = 0

    for i in range(1):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0]

        for j in range(9):

            if(sound_mode):
                # Instead of 10, may want to change it to a smaller range like 5
                if(abs(base_freq - population[i][0][j + 1]) < 10):
                    temp_score = temp_score + 1 
            else:
                if(abs(population[i][0][j] - population[i][0][j + 1]) < 0.1):
                    temp_score = temp_score + 1 

        scores[i] -= temp_score * weight 
        temp_score = 0

    return scores


def sound_check_octaves(population, scores, weight):

    # Rewards members that have octaves in them

    temp_score = 0

    for i in range(1):

        # Take the first frequency in the harmonics array of one member
        base_freq = population[i][0][0] 

        for j in range(9):

            if(sound_mode):
                # Checks if there is a direct octave to base frequency
                if(int(population[i][0][j + 1]) == int(base_freq) * 2 ):
                    temp_score = temp_score + 1
            else:
                if(population[i][0][j + 1] == 2.0):
                    temp_score = temp_score + 1

        scores[i] += temp_score * weight 
        temp_score = 0

    return scores

def sound_error_off_partial(population, scores, weight):

    # Rewards members that have frequencies that are closer to partials

    #mems_per_pop
    for i in range(1):

        # Used to help calculate partials
        if(sound_mode):
            base_freq = population[i][0][0]
        else:
            base_freq = population[i][6]
            # issue with infinite loops
            #print("LOOPING")

        temp_sum = 0

        for j in range(9):

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
                


        # Use inverse of score because a bigger sum means a larger off error which is bad
        scores[i] -= math.sqrt(temp_sum) * weight 
    return scores


def check_multiples_band(population, scores, weight):
    
    # Favors partials that are within given band range of multiples of fundamental
    temp_score = 0

    bandwidth = 0.05

    for i in range(1):

        base_freq = population[i][0][0]

        for j in range(9):
            if(
                ((population[i][0][j + 1]) > round(population[i][0][j + 1]) - 0.05) and
                ((population[i][0][j + 1]) < round(population[i][0][j + 1]) + 0.05)
            ):
                temp_score = temp_score + 1
        scores[i] += temp_score * weight
        temp_score = 0

    return scores


def reward_freq_sparseness(population, scores, weight):
    
    # Punishes partials that are too close to each other

    for i in range(1):

        frequencies = population[i][0]
        frequencies.sort()

        for j in range(9):
            if(frequencies[j + 1] - frequencies[j] < 0.5):

                if(sound_mode):
                    scores[i] -= 0.5 * weight
                else:
                    scores[i] -= 0.5

    return scores


def inverse_squared_amp(population, scores, weight):
    
    # Rewards functions that amps are closer to equaling 1/(index^2)
    # Takes the difference between the actual value and 1/(index^2)

    for i in range(1):

        amplitude = population[i][0]

        for j in range(9):

            ideal_amp = 1 / pow(j + 1, 2)
            temp_score = abs(ideal_amp - amplitude[j])
            if(sound_mode):
                scores[i] -= temp_score * weight
            else:
                scores[i] -= temp_score
    return scores


def fundamental_freq_amp(population, scores, weight):
    
    # punishes any partial that is louder than the base freq/fundamental freq

    for i in range(1):

        # will need to search through each amplitude of each member
        amplitude = population[i][0]

        for j in range(9):
            if amplitude[j + 1] > amplitude[0]:
                if(sound_mode):
                    scores[i] -= 0.5 * weight 
                else:
                    scores[i] -= 0.5 * weight

    return scores


def check_decreasing_amps(population, scores, weight):
    
    temp_score = 0

    for i in range(1):
        # Takes array of harmonics from population array
        frequency = population[i][1]
        amplitudes = population[i][0] 


        # Current method only checks adjacent harmonics
        for j in range(9):
            if(frequency[j] < frequency[j + 1] and amplitudes[j] > amplitudes[j + 1]):
                temp_score = temp_score + 1

        if(sound_mode):
            scores[i] += temp_score * weight 
        else:
            scores[i] += temp_score * weight
        temp_score = 0

    return scores


def avoid_too_quiet(population, scores, weight):
    
    # checks and rewards any amp above a certain threshold 

    temp = 0

    for i in range(1):

        amps = population[i][0]

        for j in amps:
            if(j > 0.05):
                temp += 1

        if(sound_mode):
            scores[i] += temp * weight 
        else:
            scores[i] += temp * weight

        temp = 0

    return scores


def reward_amp_sparseness(population, scores, weight):
    
    # checks and rewards a more consistent set of amplitudes instead of one central amplitude
    # uses standard deviation to calculate consistency

    for i in range(1):
        amp_mean = 0
        temp = 0
        amps = population[i][0]

        for j in amps:
            amp_mean += j

        amp_mean /= 9

        for j in amps:
            temp += math.pow(j - amp_mean, 2)

        temp /= 9
        temp = math.sqrt(temp)

        if(sound_mode):
            scores[i] += temp * weight 
        else:
            scores[i] -= temp * weight


    return scores


def reward_transients(population, scores, weight):
    
    # checks and rewards ADSR envelopes with short sustains and longer decays

    # sum of decay and sustain values
    D_sum = 0
    S_sum = 0

    for i in range(1):

        decays = population[i][3]
        sustains = population[i][4]

        for j in (range(9)):
            S_sum += sustains[j]

            if decays[j] < 0.05:
                D_sum += 1

        
        if(sound_mode):
            scores[i] += (D_sum + S_sum) * weight
        else:
            scores[i] += (D_sum + S_sum) * weight
        D_sum = 0
        S_sum = 0

    return scores


def reward_percussive_sounds(population, scores, weight):
    
    # checks and rewards ADSR envelopes with short attacks and long releases

    # sum of attack and release values
    A_sum = 0
    R_sum = 0

    for i in range(1):

        attacks = population[i][2]
        releases = population[i][5]

        for j in (range(9)):
            R_sum += releases[j]

            if attacks[j] < 0.05:
                A_sum += 1

        
        if(sound_mode):
            scores[i] += (R_sum + A_sum) * weight
        else:
            scores[i] += (R_sum + A_sum) * weight
        A_sum = 0
        R_sum = 0

    return scores


def check_stacatos(population, scores, weight):
    
    # checks and rewards ADSR envelopes with short attacks and short releases

    # sum of attack and release values
    A_sum = 0
    R_sum = 0

    for i in range(1):

        attacks = population[i][2]
        releases = population[i][5]

        for j in (range(9)):
            R_sum += releases[j]

            if attacks[j] < 0.05:
                A_sum += 1

        
        if(sound_mode):
            scores[i] += R_sum * weight
        else:
            scores[i] -= R_sum * weight
        

        if(sound_mode):
            scores[i] += A_sum * weight
        else:
            scores[i] += A_sum * weight
        A_sum = 0
        R_sum = 0

    return scores


def check_pads(population, scores, weight):
    
    # checks and rewards ADSR envelopes that have long attacks and long release

    # sum of attack and release values
    AR_sum = 0

    for i in range(1):

        attacks = population[i][2]
        releases = population[i][5]

        for j in (range(9)):
            AR_sum += attacks[j] + releases[j]

        
        if(sound_mode):
            scores[i] += AR_sum * weight
        else:
            scores[i] += AR_sum * weight
        AR_sum = 0

    return scores


def check_amp_sum(population, scores, weight):
    
    # checks and rewards sounds that overall have an amplitude less than 1

    amp_sum = 0

    for i in range(1):

        amps = population[i][0]

        for j in (range(9)):
            amp_sum += amps[j]

        if amp_sum < 1:
            if(sound_mode):
                scores[i] += weight
            else:
                scores[i] += weight
        amp_sum = 0

    return scores


def check_decreasing_attacks(population, scores, weight):
    
    # Rewards members that have decreasing attack values

    temp_score = 0

    for i in range(1):
        # Takes array of attacks from population array
        attack = population[i][2] 
        
        # Current method only checks adjacent harmonics
        for j in range(9):
            if(attack[j] > attack[j + 1]):
                temp_score = temp_score + 1

        if(sound_mode):
            scores[i] += temp_score * weight 
        else:
            scores[i] += temp_score * weight
        temp_score = 0

    return scores


def check_increasing_harmonics(population, scores, weight):
    
    # Gives good fitness scores to parents that have increasing partials
    # That pattern of partials is generally more desirable than random changes in partials
    # Don't need to change for instrument mode since the ratios ideally will increase anyway

    temp_score = 0

    for i in range(1):
        # Takes array of harmonics from population array
        frequency = population[i][0] 

        #frequency.sort()

        # Current method only checks adjacent harmonics
        for j in range(8):
            if(frequency[j] < frequency[j + 1]):
                temp_score = temp_score + 1

        if(sound_mode):
            scores[i] += temp_score * weight
        else:
            scores[i] += temp_score * weight
        temp_score = 0

    return scores


def check_bad_amps(population, scores, weight):
    
    # Rewards parents that do not have any extreme amplitudes
    # The goal of this helper is too avoid one or a few partials being over centralizing 
    # Made to get rid of parents that are too loud

    temp_score = 0

    for i in range(1):
        # Takes array of amplitudes from population array
        amplitude = population[i][0]
        for j in range(9):
            if(amplitude[j] < 0.18):
                # Increase score if amplitude is not "too loud"
                temp_score = temp_score + 1

        if(sound_mode):
            scores[i] += temp_score * weight 
        else:
            scores[i] += temp_score * weight
        temp_score = 0

    return scores