import pymysql

# Examples for pymysql
# https://pymysql.readthedocs.io/en/latest/user/examples.html

# Potential examples for optimizing inserts, specifically the "Row construction to insert multiple records" section seems useful
# https://www.digitalocean.com/community/tutorials/sql-insert-multiple-rows


import numpy
import random
# import sound_generation        #commented out temporarily for testing purposes
import os
import math
from datetime import datetime
import json

# Used to pull constant values from config file
with open('config.json') as config_file:
    data = json.load(config_file)

# List of global constants

# Number of chromosomes in each generation
mems_per_pop = data["mems_per_pop"]

# Number of chromosomes used for matingpool, should be half of mems_per_pop
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



class GA:
    # Stores the harms, amps, adsr env, weights, and base freq if applicable

    def __init__(self):

        # Set up most of the values, will still need a setter method for certain edge cases

        self.harms = numpy.random.uniform(low=50.0, high=2500.0, size=gene_length)
        self.amps = numpy.random.uniform(low=0.0, high = 1 / gene_length, size=gene_length)
        self.a = numpy.random.uniform(low=0.0, high=0.2, size=gene_length)
        self.d = numpy.random.uniform(low=0.0, high=0.2, size=gene_length)
        self.s = numpy.random.uniform(low=0.0, high=1.0, size=gene_length)
        self.r = numpy.random.uniform(low=0.0, high=3.0, size=gene_length)
        self.weights = numpy.random.uniform(low=0.0, high=5.0, size=num_funcs)
        self.base_freq = random.uniform(50.0, 170.0)

        # Database relevant parts
        self.populationID = 0
        self.chromosomeID = 0
        self.geneID = 0
        self.parent1 = 0
        self.parent2 = 0
        self.gennum = 0


        self.genes = [self.harms, self.amps, self.a, self.d, self.s, self.r]


    def init_harms(self):

        # Used to account for whether the program is running or sound mode or ratio mode
        # By default. __init__ will generate the harms as if they were in sound mode
        # init_harms should still be called even if you're running in sound mode 

        if(not sound_mode):
            self.harms = numpy.random.uniform(low=1.0, high=20.0, size=gene_length)
            self.harms = numpy.sort(self.harms)
            self.harms[0] = 1.0
            self.genes[0] = self.harms
        else:
            #print("No need to change, it's in sound mode")
            return


    def set_harms(self, h):

        # Function is given an array that will become the new self.harms
        # Keep in mind that self.genes is updated to otherwise genes would not get the change from self.harms

        self.harms = h
        self.genes[0] = h


    def set_amps(self, a):

        # Function is given an array that will become the new self.amps
        # Keep in mind that self.genes is updated to otherwise genes would not get the change from self.amps

        self.amps = a
        self.genes[1] = a


    def set_a(self, a):

        # Function is given an array that will become the new self.a
        # Keep in mind that self.genes is updated to otherwise genes would not get the change from self.a

        self.a = a
        self.genes[2] = a


    def set_d(self, d):

        # Function is given an array that will become the new self.d
        # Keep in mind that self.genes is updated to otherwise genes would not get the change from self.d

        self.d = d
        self.genes[3] = d


    def set_s(self, s):

        # Function is given an array that will become the new self.s
        # Keep in mind that self.genes is updated to otherwise genes would not get the change from self.s

        self.s = s
        self.genes[4] = s


    def set_r(self, r):

        # Function is given an array that will become the new self.r
        # Keep in mind that self.genes is updated to otherwise genes would not get the change from self.r

        self.r = r
        self.genes[5] = r


    def set_genes(self, g):

        # Function is given an array that will become the new self.genes
        # Keep in mind that the harms, amps etc. are updated since otherwise changing genes would not change self.harms, self.amps etc.

        self.genes = g

        self.harms = g[0]
        self.amps = g[1]
        self.a = g[2]
        self.d = g[3]
        self.s = g[4]
        self.r = g[5]

    def set_weights(self, w):

        # Function is given an array that will become self.weights

        self.weights = w

    def set_base_freq(self, freq):

        # Setter for base frequency
        self.base_freq = freq


    def get_harms(self):

        # Returns harmonics
        return self.harms

    def get_amps(self):

        # Returns amplitudes
        return self.amps

    def get_a(self):

        # Returns attack of adsr envelope
        return self.a

    def get_d(self):

        # Returns decay of adsr envelope
        return self.d

    def get_s(self):

        # Returns sustain of adsr envelope
        return self.s

    def get_r(self):

        # Returns release of adsr envelope
        return self.r

    def get_weight(self, index):

        # Returns the weight of a specific fitness helper determined by index
        return self.weights[index]

    def get_weights(self):

        # Returns the entire weight array instead of a specific weight
        return self.weights

    def get_genes(self):

        # Returns harms, amps and ADSR envelope as an array
        return self.genes

    def get_base_freq(self):

        # Getter for base frequency
        return self.base_freq

    def set_popID(self,popID):

        # Setter method for populationID
        self.populationID = popID

    def set_chromosomeID(self, chromoID):

        # Setter method for chromosomeID
        self.chromosomeID = chromoID 

    def set_geneID(self, geneID):

        # Setter method for geneID
        self.geneID = geneID

    def set_parent1(self, par1):

        # Setter method for parent1
        self.parent1 = par1

    def set_parent2(self, par2):

        # Setter method for parent2
        self.parent2 = par2

    def set_gen_number(self, num):

        # Setter for gen_num
        self.gennum = num

    def get_popID(self):

        # Getter method for populationID
        return self.populationID

    def get_chromosomeID(self):

        # Getter method for chromosomeID
        return self.chromosomeID

    def get_geneID(self):

        # Getter method for geneID
        return self.geneID

    def get_parent1(self):

        # Getter method for parent1
        return self.parent1

    def get_parent2(self):

        # Getter method for parent2
        return self.parent2

    def get_gen_number(self):

        # Getter method for gen_number
        return self.gennum


    def reset(self):

        self.harms = numpy.random.uniform(low=50.0, high=2500.0, size=gene_length)
        self.amps = numpy.random.uniform(low=0.0, high = 1 / gene_length, size=gene_length)
        self.a = numpy.random.uniform(low=0.0, high=0.2, size=gene_length)
        self.d = numpy.random.uniform(low=0.0, high=0.2, size=gene_length)
        self.s = numpy.random.uniform(low=0.0, high=1.0, size=gene_length)
        self.r = numpy.random.uniform(low=0.0, high=3.0, size=gene_length)
        self.weights = numpy.random.uniform(low=0.0, high=5.0, size=num_funcs)
        self.base_freq = random.uniform(50.0, 170.0)

        self.genes = [self.harms, self.amps, self.a, self.d, self.s, self.r]



db = pymysql.connect(host = 'sigdb.cmnz4advdpzd.us-west-2.rds.amazonaws.com',
                user = 'admin',
                password = 'Beaver!1',
                database = 'sig')

cursor = db.cursor()

# Retrieves all the tables, just their title not the content
# sql = '''show tables'''
# cursor.execute(sql)
# print(cursor.fetchall())


# Read a single record

# sql = "SELECT `populationID`, `generation_number` FROM `populations`"
# # cursor.execute(sql, ('webmaster@python.org',))
# cursor.execute(sql)
# result = cursor.fetchone()
# print(result)

# Takes the value item from the amplitudes table, converts them to floats and puts them in a list


# Need to do some fancy work arounds to make sql queries modular
# gid = 1
# concat = "WHERE `geneID` = {0}".format(gid)
# sql = "SELECT `value` FROM `amplitudes`"
# sql = sql + concat
# cursor.execute(sql)

# values = []

# for i in range(5):
#     result = cursor.fetchone()
#     result = float(result[0])
#     values.append(result)
#     # print(result)

# print(values)



# for both retrieve and add member, need to handle weights as well
# may need to add indices to all the genes in case queries to not retrieve the data in the same order every time
# need to modify GA to store database related info


def retrieve_member(chromosomeID):

    # in the future, will probably need to pick member based on a different criteria than their chromosome ID

    # Finds a member given their chromosome ID then returns the harmonics, amplitudes and adsr values of that member

    # Gets the geneID with the corresponding chromosomeID
    sql = "SELECT `geneID` FROM `genes` WHERE `chromosomeID` = %s"
    cursor.execute(sql, (chromosomeID))
    result = cursor.fetchone()
    geneID = str(result[0])

    # Get the populationID with corresponding chromosomeID
    sql = "SELECT `populationID` FROM `chromosomes` WHERE `chromosomeID` = %s"
    cursor.execute(sql, (chromosomeID))
    result = cursor.fetchone()
    populationID = str(result[0])

    # Get the generation number
    sql = "SELECT `generation_number` FROM `populations` WHERE `populationID` = %s"
    cursor.execute(sql, (populationID))
    result = cursor.fetchone()
    gen_num = int(result[0])


    # The input in sql query needs to be a string, not an int
    sql = "SELECT `value` FROM `harmonics` WHERE `geneID` =%s"
    cursor.execute(sql, (geneID))

    harms = []

    # To make this more modular, the 10 could be changed to gene_length when integrated into the GA file
    for i in range(gene_length):
        result = cursor.fetchone()
        result = float(result[0])
        harms.append(result)

    # print(harms)


    sql = "SELECT `value` FROM `amplitudes`WHERE `geneID`=%s"
    cursor.execute(sql, (geneID))

    amps = []

    for i in range(gene_length):
        result = cursor.fetchone()
        result = float(result[0])
        amps.append(result)

    # print(amps)


    sql = "SELECT `value` FROM `attacks`WHERE `geneID`=%s"
    cursor.execute(sql, (geneID))

    a = []

    for i in range(gene_length):
        result = cursor.fetchone()
        result = float(result[0])
        a.append(result)

    # print(a)


    sql = "SELECT `value` FROM `decays`WHERE `geneID`=%s"
    cursor.execute(sql, (geneID))

    d = []

    for i in range(gene_length):
        result = cursor.fetchone()
        result = float(result[0])
        d.append(result)

    # print(d)


    sql = "SELECT `value` FROM `sustains`WHERE `geneID`=%s"
    cursor.execute(sql, (geneID))

    s = []

    for i in range(gene_length):
        result = cursor.fetchone()
        result = float(result[0])
        s.append(result)

    # print(s)


    sql = "SELECT `value` FROM `releases`WHERE `geneID`=%s"
    cursor.execute(sql, (geneID))

    r = []

    for i in range(gene_length):
        result = cursor.fetchone()
        result = float(result[0])
        r.append(result)

    # print(r)


    # Also should retrieve weights of helper functions

    sql = "SELECT `value` FROM `weights`WHERE `chromosomeID`=%s  ORDER BY `helper_func` ASC"
    cursor.execute(sql, (chromosomeID))

    w = []

    # @@@@@@@@ will later need to set this to num_funcs @@@@@@@@
    for i in range(num_funcs):
        result = cursor.fetchone()
        result = float(result[0])
        w.append(result)


    
    # Also should return populationID, chromosomeID, geneID, parent1 and parent2


    # Retrieves first parent from corresponding chromosome
    sql = "SELECT `parent1` FROM `chromosomes` WHERE `chromosomeID` = %s" 
    cursor.execute(sql, (chromosomeID))
    result = cursor.fetchone()
    parent1 = str(result[0])

    # Retrieves second parent from corresponding chromosome
    sql = "SELECT `parent2` FROM `chromosomes` WHERE `chromosomeID` = %s" 
    cursor.execute(sql, (chromosomeID))
    result = cursor.fetchone()
    parent2 = str(result[0])

    member = GA()

    member_genes = [harms,amps,a,d,s,r]

    member.set_weights(w)

    member.set_genes(member_genes)
    member.set_popID(populationID)
    member.set_chromosomeID(chromosomeID)
    member.set_geneID(geneID)
    member.set_parent1(parent1)
    member.set_parent2(parent2)
    member.set_gen_number(gen_num)



    return member


def add_population(gen_number):

    # Create a new island with the generation number given
    sql = "INSERT INTO `populations` (`generation_number`) VALUES (%s)"
    cursor.execute(sql, (gen_number))

    # For now, have it return the population id of this newly created population
    sql = "SELECT `populationID` FROM `populations` WHERE `populationID`=(SELECT max(`populationID`) FROM `populations`)"
    cursor.execute(sql)
    result = cursor.fetchone()
    populationID = str(result[0])


    # The database won't actually receive anything without this commit
    # @@@@@@@@@@@@@@@ UNCOMMENT THIS LINE when you are ready to actually send the inserts @@@@@@@@@@@@@@@ 
    # db.commit()

    return populationID



# In the future, will probably want it so that a new population is created as well
# and instead of populationID being the param, the generation number is the param

def add_member(member, populationID):


    p1 = member.get_parent1()
    p1 = str(p1)
    p2 = member.get_parent2()
    p2 = str(p2)

    popID = str(populationID)
    

    # Creates a new chromosome
    sql = "INSERT INTO `chromosomes` (`populationID`, `parent1`, `parent2`) VALUES (%s, %s, %s)"
    cursor.execute(sql, (popID, p1, p2))


    # problem: how do we keep track of this newly created chromosome's chromosome ID?
    # Find the largest ID since that will correspond to the most recent aka the one just created since the ID is set to autoincrement
    # Retrieve the chromosomeID
    sql = "SELECT `chromosomeID` FROM `chromosomes` WHERE `chromosomeID`=(SELECT max(`chromosomeID`) FROM `chromosomes`)"
    cursor.execute(sql)
    result = cursor.fetchone()
    chromosomeID = str(result[0])

    # Adds a geneID entry for corresponding chromosome
    sql = "INSERT INTO `genes` (`chromosomeID`) VALUES (%s)"
    cursor.execute(sql, (chromosomeID))

    # Retrieve the geneID
    sql = "SELECT `geneID` FROM `genes` WHERE `chromosomeID`=%s"
    cursor.execute(sql, (chromosomeID))
    result = cursor.fetchone()
    geneID = str(result[0])


    harms = member.get_harms()
    # Insert the harmonics of the member
    # harm = str(harms[i])
    sql = "INSERT INTO `harmonics` (`value`, `geneID`) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)"
    # cursor.execute(sql, (str(harms[0]), geneID), (str(harms[1]), geneID), (str(harms[2]), geneID), (str(harms[3]), geneID), (str(harms[4]), geneID), (str(harms[5]), geneID), (str(harms[6]), geneID), (str(harms[7]), geneID), (str(harms[8]), geneID), (str(harms[9]), geneID))
    cursor.execute(sql, (str(harms[0]), geneID, str(harms[1]), geneID, str(harms[2]), geneID, str(harms[3]), geneID, str(harms[4]), geneID, str(harms[5]), geneID, str(harms[6]), geneID, str(harms[7]), geneID, str(harms[8]), geneID, str(harms[9]), geneID))


    amps = member.get_amps()
    # Insert the amplitudes of the member
    # amp = str(amps[i])
    sql = "INSERT INTO `amplitudes` (`value`, `geneID`) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)"
    cursor.execute(sql, (str(amps[0]), geneID, str(amps[1]), geneID, str(amps[2]), geneID, str(amps[3]), geneID, str(amps[4]), geneID, str(amps[5]), geneID, str(amps[6]), geneID, str(amps[7]), geneID, str(amps[8]), geneID, str(amps[9]), geneID))


    a = member.get_a()
    # Insert the attacks of the member
    # a = str(attack[i])
    sql = "INSERT INTO `attacks` (`value`, `geneID`) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)"
    cursor.execute(sql, (str(a[0]), geneID, str(a[1]), geneID, str(a[2]), geneID, str(a[3]), geneID, str(a[4]), geneID, str(a[5]), geneID, str(a[6]), geneID, str(a[7]), geneID, str(a[8]), geneID, str(a[9]), geneID))

    d = member.get_d()
    # Insert the decays of the member
    # d = str(decay[i])
    sql = "INSERT INTO `decays` (`value`, `geneID`) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)"
    cursor.execute(sql, (str(d[0]), geneID, str(d[1]), geneID, str(d[2]), geneID, str(d[3]), geneID, str(d[4]), geneID, str(d[5]), geneID, str(d[6]), geneID, str(d[7]), geneID, str(d[8]), geneID, str(d[9]), geneID))

    s = member.get_s()
    # Insert the sustains of the member
    # s = str(sustain[i])
    sql = "INSERT INTO `sustains` (`value`, `geneID`) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)"
    cursor.execute(sql, (str(s[0]), geneID, str(s[1]), geneID, str(s[2]), geneID, str(s[3]), geneID, str(s[4]), geneID, str(s[5]), geneID, str(s[6]), geneID, str(s[7]), geneID, str(s[8]), geneID, str(s[9]), geneID))

    r = member.get_r()
    # Insert the releases of the member
    # r = str(release[i])
    sql = "INSERT INTO `releases` (`value`, `geneID`) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)"
    cursor.execute(sql, (str(r[0]), geneID, str(r[1]), geneID, str(r[2]), geneID, str(r[3]), geneID, str(r[4]), geneID, str(r[5]), geneID, str(r[6]), geneID, str(r[7]), geneID, str(r[8]), geneID, str(r[9]), geneID))

    w = member.get_weights()
    # Insert the weights of the helper functions of each members
    # w = str(weight[i])
    # dex = str(i + 1)
    sql = "INSERT INTO `weights` (`value`, `chromosomeID`, `helper_func`) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)"
    cursor.execute(sql, (str(w[0]), chromosomeID, '1', str(w[1]), chromosomeID, '2', str(w[2]), chromosomeID, '3', str(w[3]), chromosomeID, '4', str(w[4]), chromosomeID, '5', str(w[5]), chromosomeID, '6', str(w[6]), chromosomeID, '7', str(w[7]), chromosomeID, '8', str(w[8]), chromosomeID, '9', str(w[9]), chromosomeID, '10', str(w[10]), chromosomeID, '11', str(w[11]), chromosomeID, '12', str(w[12]), chromosomeID, '13', str(w[13]), chromosomeID, '14', str(w[14]), chromosomeID, '15', str(w[15]), chromosomeID, '16', str(w[16]), chromosomeID, '17', str(w[17]), chromosomeID, '18', str(w[18]), chromosomeID, '19', str(w[19]), chromosomeID, '20', str(w[20]), chromosomeID, '21', str(w[21]), chromosomeID, '22', str(w[22]), chromosomeID, '23', str(w[23]), chromosomeID, '24'))
    
    # The database won't actually receive anything without this commit
    # @@@@@@@@@@@@@@@ UNCOMMENT THIS LINE when you are ready to actually send the inserts @@@@@@@@@@@@@@@ 
    #db.commit()



def count_votes(chromosomeID):

    # Will take in the chromosome id of a member, find the number of votes they won and then divide them by
    # the number of votes they participated in to get a percentage/average that will be used to determine that member's fitness score

    total = 0
    votes = 0
    ratio = 0

    # Records the number of votes this member won
    sql = "SELECT `voteID` FROM `votes` WHERE `winnerID` = %s"
    cursor.execute(sql, (chromosomeID))
    result = cursor.fetchall()

    # Handles edge case where this particular member has won no votes
    if(len(result) == 0):
        print("has not won any votes")
        return 0

    votes = len(result)
    total += votes

    # Records the number of votes this member was in but didn't win and adds that to total
    sql = "SELECT `voteID` FROM `votes` WHERE `opponentID` = %s"
    cursor.execute(sql, (chromosomeID))
    result = cursor.fetchall()


    # Handles edge case where this particular member only won votes
    if(len(result) == 0):
        print("has not lost any votes")
        return 1

    total += len(result)

    # Calculates the percentage of votes won/votes participated in
    ratio = votes / total
    return ratio

    # will need to test once database has votes in it


# look for two islands at the same generation level, swap two members by updating each member's population id
def swap_island_members():
    # For now just do it randomly, but later versions could have population ids passed in as parameters

    # find a random valid generation number
    sql = "SELECT `generation_number` FROM `populations` HAVING COUNT(*) > 1 ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    gen_num = cursor.fetchone()

    # Pick two random islands with the same generation number
    sql = "SELECT `populationID` FROM `populations` WHERE `generation_number` = %s ORDER BY RAND() LIMIT 2"
    #sql = "SELECT `populationID` FROM `populations` GROUP BY `populationID` HAVING COUNT(*) > 1 ORDER BY RAND() LIMIT 2"
    cursor.execute(sql, (gen_num))
    island1 = cursor.fetchone()
    island2 = cursor.fetchone()


    # Select a random member from island 1
    sql = "SELECT `chromosomeID` FROM `chromosomes` WHERE `populationID` = %s ORDER BY RAND()"
    cursor.execute(sql, (island1))
    mem1 = cursor.fetchone()


    # Select a random member from island 2
    sql = "SELECT `chromosomeID` FROM `chromosomes` WHERE `populationID` = %s ORDER BY RAND()"
    cursor.execute(sql, (island2))
    mem2 = cursor.fetchone()


    # Update each mem with the other island's population id to effectively swap their places on the islands
    sql = "UPDATE `chromosomes` SET `populationID` = %s WHERE `chromosomeID` = %s"
    cursor.execute(sql, (island2, mem1))

    sql = "UPDATE `chromosomes` SET `populationID` = %s WHERE `chromosomeID` = %s"
    cursor.execute(sql, (island1, mem2))

    # The database won't actually receive anything without this commit
    # @@@@@@@@@@@@@@@ UNCOMMENT THIS LINE when you are ready to actually send the inserts @@@@@@@@@@@@@@@ 
    #db.commit()



# Will eventually need an update member function that can be used when a mutation occurs


# TESTER CODE


# chromoID = 2
# new_mem = retrieve_member(chromoID)

# popID = new_mem.get_popID()
# har = new_mem.get_harms()
# gi = new_mem.get_geneID()

# print(popID)
# print(gi)
# print(har)

# weight = new_mem.get_weights()
# print(weight)

# num = new_mem.get_gen_number()
# print(num)



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

weights = [3.2] * num_funcs

# FOR REFACTOR VERSION will need to use setters to make this happen
ideal_set1 = GA()
temp_set1 = [harms, amps, a, d, s, r]
ideal_set1.set_genes(temp_set1)
ideal_set1.set_weights(weights)
ideal_set1.set_base_freq(freq)
ideal_set1.set_parent1(3)
ideal_set1.set_parent2(2)
ideal_set1.set_popID(2)

pop = ideal_set1.get_popID()

#add_member(ideal_set1, pop)


# popID = add_population(5)
# print(popID)



# sql = "SELECT * FROM `populations`"
# cursor.execute(sql)

# result = cursor.fetchone()
# while result:
#     print(result)
#     result = cursor.fetchone()


# new_mem = retrieve_member(53)

# ws = new_mem.get_weights()
# print(ws)

# add_member(new_mem, 2)



# See what happens with null values
# sql = "SELECT `chromosomeID` FROM `chromosomes` WHERE `chromosomeID`= %s"
# cursor.execute(sql, ("3155"))
# result = cursor.fetchall()
# chromosomeID = print(result)
# if(chromosomeID == None):
#     print("there's nothing!!!")
# Returns None

# print(count_votes("3139"))

# swap_island_members()



# Insert example using pymysql
# with connection:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))