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
        ser = Server(audio='offline').boot()
        
        # Includes the absolute filepath, the specific folder and the new file name
        path = os.path.join("/Users/johnk/OneDrive/Computer Science/Lab stuff/sounds", self.directory, self.filename)
        ser.recordOptions(dur=5, filename=path, fileformat=0, sampletype=1 )

        # Create empty arrays that will be filled out using passed in parameters
        envs = [0] * self.num
        sines = [0] * self.num

        # Begins recording to generate wav file
        ser.recstart()

        # Create ADSR envelope and Sine wave that will be played and recorded
        for n in range(self.num):
            envs[n] = Adsr(attack = self.a[n], decay = self.d[n], sustain = self.s[n], release = self.r[n], dur = 5)
            sines[n] = Sine(freq = self.harms[n], mul = envs[n] * self.amps[n])
            #sines[n] = Sine(freq = self.harms[n], mul = (envs[n] * self.amps[n])/2) 
            sines[n].out()
            envs[n].play()

        # Stops recording
        ser.recstop()


        ser.start()

        # Shuts down the server 
        ser.shutdown()

       

