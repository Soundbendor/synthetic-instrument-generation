# another small change

from pyo import *
import os


class instrument:
    def __init__(self, harms, amps, a, d, s, r, num, filename, directory):

        self.harms = harms
        self.amps = amps
        self.a = a
        self.d = d
        self.s = s
        self.r = r
        self.num = num
        self.filename = filename
        self.directory = directory

    def play_note(self):

        # Boot up server to play and record sound
        # TEST change sampling rate to lower, default is 44100
        ser = Server(sr=16000, audio='offline').boot()
        
        #i think I should actually change this?? actually never mind, directory represents the specific folder in this case but they can be in any order
        file_path = ".\sounds"

        # Includes the absolute filepath, the specific folder and the new file name
        path = os.path.join(file_path, self.directory, self.filename)
        ser.recordOptions(dur=5, filename=path, fileformat=0, sampletype=1 )

        # Create empty arrays that will be filled out using passed in parameters
        envsL = [0] * self.num
        envsR = [0] * self.num
        sinesL = [0] * self.num
        sinesR = [0] * self.num

        # Begins recording to generate wav file
        ser.recstart()
        
        # Create ADSR envelope and Sine wave that will be played and recorded
        for n in range(self.num):
            envsL[n] = Adsr(attack = self.a[n], decay = self.d[n], sustain = self.s[n], release = self.r[n], dur = 5)
            envsR[n] = Adsr(attack = self.a[n], decay = self.d[n], sustain = self.s[n], release = self.r[n], dur = 5)
            sinesL[n] = Sine(freq = self.harms[n], mul = envsL[n] * self.amps[n])
            sinesR[n] = Sine(freq = self.harms[n], mul = envsR[n] * self.amps[n])
            sinesL[n].out(0)
            sinesR[n].out(1)
            envsL[n].play()
            envsR[n].play()

        # Stops recording
        ser.recstop()

        ser.start()

        # Shuts down the server 
        ser.shutdown()

       
# !!! WARNING the generated wav file can be pretty loud so lower your volume a lot if you listen to it !!!

# Set up Flute representation
nums = 10
harms = [0] * nums

amps = [1.0, 0.65, 0.61, 0.15, 0.09, 0.02, 0.02, 0.01, 0.01, 0.01]

a = [0.01] * nums
d = [0.1] * nums
s = [0.5] * nums
r = [1.5] * nums  

freq = 247
for i in range(nums):
    harms[i] = (i+1) * freq

# Also set up the file name and the directory for where you want to put wav file

#file_name = "Flute_test.wav"
#directory = "sounds"

#randSound = instrument(harms, amps, a, d, s, r, nums, file_name, directory)
#randSound.play_note()