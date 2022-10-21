import unittest

from test_cases import error_off_partial
from test_cases import error_off_amps
from test_cases import amps_sum
from test_cases import check_octaves
from test_cases import check_fifths
from test_cases import check_wobbling
from test_cases import check_true_harmonics
from test_cases import sound_check_wobbling
from test_cases import sound_check_octaves
from test_cases import sound_error_off_partial
from test_cases import check_multiples_band
from test_cases import reward_freq_sparseness
from test_cases import inverse_squared_amp
from test_cases import fundamental_freq_amp
from test_cases import check_decreasing_amps
from test_cases import avoid_too_quiet
from test_cases import reward_amp_sparseness
from test_cases import reward_transients
from test_cases import reward_percussive_sounds
from test_cases import check_stacatos
from test_cases import check_pads
from test_cases import check_amp_sum
from test_cases import check_decreasing_attacks
from test_cases import check_increasing_harmonics
from test_cases import check_bad_amps


class TestError(unittest.TestCase):
	def test_error_off_partial(self):

		population = [0] * 1
		population[0] = [0] * 6

		population[0][0] = [1, 2, 3.5, 4, 5, 7.2, 8.8, 9.4, 10.1, 11]

		scores = [0]
		weight = 1

		result = error_off_partial(population, scores, weight)
		self.assertEqual(result, [-0.5])


		scores = [0]
		weight = 1


		population[0][0] = [5, 4.5, 4, 4, 5, 3, 1, 3, 1, 3]
		result = error_off_partial(population, scores, weight)
		self.assertEqual(result, [-46.25])	


		scores = [0]
		weight = 1
		
		population[0][0] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		result = error_off_partial(population, scores, weight)
		self.assertEqual(result, [0])	
  
		scores = [0]
		weight = 1
		
		population[0][0] = [10000000000000, 101.9, 0.000001, -10000000000000, 10000000000000, 23191923.52610000000000009, 238238923, 8239238, 129021.99, 913090123]
		result = error_off_partial(population, scores, weight)
		self.assertEqual(result, [-1.0999763431044688e+27])	



	def test_error_amp_off(self):

		population = [0] * 1
		population[0] = [0] * 6

		scores = [0]
		weight = 1

		population[0][1] = [512, 256, 128, 64, 32, 16, 8, 4, 2, 1]
		result = error_off_amps(population, scores, weight)
		self.assertEqual(result, [0])


		scores = [0]
		weight = 1

		population[0][1] = [1024, 256, 128, 64, 32, 16, 8, 4, 2, 1]
		result = error_off_amps(population, scores, weight)
		self.assertEqual(result, [-256])
  
  
		scores = [0]
		weight = 1

		population[0][1] = [10000000000000, 101.9, 0.000001, -10000000000000, 10000000000000, 23191923.52610000000000009, 238238923, 8239238, 129021.99, 913090123]
		result = error_off_amps(population, scores, weight)
		self.assertEqual(result, [-19364910744538.973])


	def test_error_amps_sum(self):

		population = [0] * 1
		population[0] = [0] * 6

		scores = [0]
		weight = 1

		population[0][1] = [0.1, 0.04, 0.06, 0.02, 0.05, 0.3, 0.01, 0.09, 0.01, 0.02]
		result = amps_sum(population, scores, weight)
		self.assertEqual(result, [0])


		scores = [0]
		weight = 1

		population[0][1] = [0.1, 0.4, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.1]
		result = amps_sum(population, scores, weight)
		self.assertEqual(result, [-4])
  
  
  		# If inputs are too loud, the time it takes to process this, is very long. Of course this is unrealistic but worth mentioning
  
  		# scores = [0]
		# weight = 1
		# population[0][1] = [10000000000000, 101.9, 0.000001, -10000000000000, 10000000000000, 23191923.52610000000000009, 238238923, 8239238, 129021.99, 913090123]
		# result = amps_sum(population, scores, weight)
		# self.assertEqual(result, [-4])
  
  
		scores = [0]
		weight = 1
		
		population[0][1] = [10, 10.2, 0.000001, -100, 1000, 77.238238223992032238434312, 22, 23, 17.2, 166]
		result = amps_sum(population, scores, weight)
		self.assertEqual(result, [-1225])
  

  
  


	def test_check_octaves(self):

		population = [0] * 1
		population[0] = [0] * 6

		scores = [0]
		weight = 1

		population[0][0] = [1, 2, 4, 8, 5, 7, 3, 2, 4, 10]
		result = check_octaves(population, scores, weight)
		self.assertEqual(result, [2])


		scores = [0]
		weight = 1

		population[0][0] = [1, 11, 4, 8, 5, 7, 3, 1.5, 4, 10]
		result = check_octaves(population, scores, weight)
		self.assertEqual(result, [0])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [10000000000000, 101.9, 0.000001, -10000000000000, 10000000000000, 23191923.52610000000000009, 238238923, 8239238, 129021.99, 913090123]
		result = check_octaves(population, scores, weight)
		self.assertEqual(result, [0])


	def test_check_fifths(self):

		population = [0] * 1
		population[0] = [0] * 6

		scores = [0]
		weight = 1

		population[0][0] = [2, 2, 4, 8, 5, 7, 3, 2, 4, 10]
		result = check_fifths(population, scores, weight)
		self.assertEqual(result, [1])


		scores = [0]
		weight = 1

		population[0][0] = [1, 1.5, 4, 8, 5, 7, 3, 2, 4, 10]
		result = check_fifths(population, scores, weight)
		self.assertEqual(result, [0])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [10000000000000, 101.9, 0.000001, -10000000000000, 10000000000000, 23191923.52610000000000009, 238238923, 8239238, 129021.99, 913090123]
		result = check_fifths(population, scores, weight)
		self.assertEqual(result, [0])


	def test_check_wobbling(self):

		population = [0] * 1
		population[0] = [0] * 6

		scores = [0]
		weight = 1

		population[0][0] = [10, 15, 30, 50, 12, 80, 102, 140, 569, 332]
		result = check_wobbling(population, scores, weight)
		self.assertEqual(result, [-2])


		scores = [0]
		weight = 1

		population[0][0] = [5, 15, 30, 50, 12, 80, 102, 140, 569, 332]
		result = check_wobbling(population, scores, weight)
		self.assertEqual(result, [-1])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [10000000000000, 101.9, 0.000001, -10000000000000, 10000000000000, 23191923.52610000000000009, 238238923, 8239238, 129021.99, 913090123]
		result = check_wobbling(population, scores, weight)
		self.assertEqual(result, [-1])


	def test_check_true_harmonics(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.0, 3.1, 4.3, 5.0, 6.0, 7.45, 8.99, 9.0002, 10.5]
		result = check_true_harmonics(population, scores, weight)
		self.assertEqual(result, [3])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [10000000000000, 101.9, 0.000001, -10000000000000, 10000000000000, 23191923.52610000000000009, 238238923, 8239238, 129021.99, 913090123]
		result = check_true_harmonics(population, scores, weight)
		self.assertEqual(result, [5])



	def test_sound_check_wobbling(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.0, 2.11, 2.20, 5.91, 6.0, 7.45, 8.99, 9.0002, 10.5]
		result = sound_check_wobbling(population, scores, weight)
		self.assertEqual(result, [-3])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [10000000000000, 10000000000000.01, 0.000001, -10000000000000, 10000000000000, 23191923.52610000000000009, 238238923, 8239238, 129021.99, 913090123]
		result = sound_check_wobbling(population, scores, weight)
		self.assertEqual(result, [-1])


	def test_sound_check_octaves(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.0, 2.11, 2.20, 5.91, 6.0, 7.45, 8.99, 9.0002, 10.5]
		result = sound_check_octaves(population, scores, weight)
		self.assertEqual(result, [1])
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.0, 2.11, 3.00000000000000000000000000001, 5.91, 6.0, 7.45, 8.99, 9.0002, 10000000000000000000000]
		result = sound_check_octaves(population, scores, weight)
		self.assertEqual(result, [1])


	def test_sound_error_off(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1, 2, 3.25, 4, 5, 7.5, 8.5, 9.5, 10, 11]
		result = sound_error_off_partial(population, scores, weight)
		self.assertEqual(result, [-0.9013878188659973])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.0, 2.11, 3.00000000000000000000000000001, 5.91, 6.0, 7.45, 8.99, 9.0002, 10000000000000000000000]
		result = sound_error_off_partial(population, scores, weight)
		self.assertEqual(result, [-0.4720169912195959])
	
 
	def test_check_multiples_band(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 1.98, 3.04, 4.3, 5.019, 5.96, 7.45, 8.99, 9.0002, 10.4]
  
		result = check_multiples_band(population, scores, weight)
		self.assertEqual(result, [6])
	
 
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.0, 2.11, 3.00000000000000000000000000001, 5.91, 6.0, 7.45, 8.99, 9.0002, 10000000000000000000000]
  
		result = check_multiples_band(population, scores, weight)
		self.assertEqual(result, [5])


	def test_reward_freq_sparseness(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.4, 3.0, 4.0, 4.4, 6.0, 7.3, 8.0, 8.2, 10.0]
  
		result = reward_freq_sparseness(population, scores, weight)
		self.assertEqual(result, [-1.0])
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.0, 2.11, 3.00000000000000000000000000001, 5.91, 6.0, 7.45, 8.99, 9.0002, 10000000000000000000000]
  
		result = reward_freq_sparseness(population, scores, weight)
		self.assertEqual(result, [-1.5])
  
  
	def test_inverse_squared_amp(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 0.66, 0.04, 0.03, 0.015625, 0.01, 0.001, 0.0002, 0.0004]
  
		result = inverse_squared_amp(population, scores, weight)
		self.assertEqual(result, [-0.6307205089443185])
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, .000000000000000001]
  
		result = inverse_squared_amp(population, scores, weight)
		self.assertEqual(result, [-0.08496571104542958])


	def test_fundamental_freq_amp(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
  
		result = fundamental_freq_amp(population, scores, weight)
		self.assertEqual(result, [-1.0])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 1000000000000000]
  
		result = fundamental_freq_amp(population, scores, weight)
		self.assertEqual(result, [-0.5])


	def test_check_decreasing_amps(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
		population[0][1] = [1.0, 2.4, 3.0, 4.0, 4.4, 6.0, 7.3, 8.0, 8.2, 10.0]
  
		result = check_decreasing_amps(population, scores, weight)
		self.assertEqual(result, [6])
  
  
		scores = [0]
		weight = 1
  
		population[0][0] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
		population[0][1] = [1.0, 2.4, 3.0, 4.0, 4.4, 6.0, 7.3, 8.0, 8.2, 10.0]
  
		result = check_decreasing_amps(population, scores, weight)
		self.assertEqual(result, [7])
  
  
	def test_avoid_too_quiet(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
  
		result = avoid_too_quiet(population, scores, weight)
		self.assertEqual(result, [4])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = avoid_too_quiet(population, scores, weight)
		self.assertEqual(result, [6])
  
  
	def test_reward_amp_sparseness(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
  
		result = reward_amp_sparseness(population, scores, weight)
		self.assertEqual(result, [-0.7354409919600472])
  
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = reward_amp_sparseness(population, scores, weight)
		self.assertEqual(result, [-3.1644458315990854e+25])


	def test_reward_transients(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][3] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
		population[0][4] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
  
		result = reward_transients(population, scores, weight)
		self.assertEqual(result, [9.686825])
  
  
		scores = [0]
		weight = 1

		population[0][3] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
		population[0][4] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = reward_transients(population, scores, weight)
		self.assertEqual(result, [5.478802020121112])
  
  
	def test_reward_percussive_sounds(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][2] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
		population[0][5] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
  
		result = reward_percussive_sounds(population, scores, weight)
		self.assertEqual(result, [9.686825])  
  
  
		scores = [0]
		weight = 1

		population[0][2] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
		population[0][5] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = reward_percussive_sounds(population, scores, weight)
		self.assertEqual(result, [5.478802020121112])  
  
  
	def test_check_stacatos(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][2] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
		population[0][5] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
  
		result = check_stacatos(population, scores, weight)
		self.assertEqual(result, [0.3131749999999993])  
  
  
		scores = [0]
		weight = 1

		population[0][2] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
		population[0][5] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = check_stacatos(population, scores, weight)
		self.assertEqual(result, [2.5211979798788886])  
  
  
	def test_check_pads(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][2] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
		population[0][5] = [1.0, 0.25, 2.1, 0.04, 0.03, 0.015625, 1.25, 0.001, 0.0002, 0.0004]
  
		result = check_pads(population, scores, weight)
		self.assertEqual(result, [9.373650000000001])  
  
  
		scores = [0]
		weight = 1

		population[0][2] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
		population[0][5] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = check_pads(population, scores, weight)
		self.assertEqual(result, [2.957604040242223])  
  
  
	def test_check_amp_sum(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [0.4, 0.2, 0.1, 0.05, 0.025, 0.0125, 0.0625, 0.03125, 0.015625, 0.0078125]
  
		result = check_amp_sum(population, scores, weight)
		self.assertEqual(result, [1])  
  
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = check_amp_sum(population, scores, weight)
		self.assertEqual(result, [0])  
  
  
	def test_check_decreasing_attacks(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][2] = [0.4, 0.2, 0.1, 0.05, 0.025, 0.0125, 0.0625, 0.03125, 0.015625, 0.0078125]
  
		result = check_decreasing_attacks(population, scores, weight)
		self.assertEqual(result, [8])  
  
  
		scores = [0]
		weight = 1

		population[0][2] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = check_decreasing_attacks(population, scores, weight)
		self.assertEqual(result, [7])  
  
  
	def test_check_increasing_harmonics(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [1.0, 2.4, 3.0, 4.0, 4.4, 6.0, 7.3, 8.0, 8.2, 10.0]
  
		result = check_increasing_harmonics(population, scores, weight)
		self.assertEqual(result, [8])  
  
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = check_increasing_harmonics(population, scores, weight)
		self.assertEqual(result, [1])  
  
  
	def test_check_bad_amps(self):
		population = [0] * 1
		population[0] = [0] * 7

		scores = [0]
		weight = 1

		population[0][0] = [0.4, 0.2, 0.1, 0.05, 0.025, 0.0125, 0.0625, 0.03125, 0.015625, 0.0078125]
  
		result = check_bad_amps(population, scores, weight)
		self.assertEqual(result, [7])  
  
  
		scores = [0]
		weight = 1

		population[0][0] = [1.0, 0.25, 0.1111111111111111, 0.0625, 0.052, 0.0022, 0.00099, .00000000899, .00000090002, 100000000000000000000000000]
  
		result = check_bad_amps(population, scores, weight)
		self.assertEqual(result, [7])  


if __name__ == '__main__':
	# main runs the tests under the functions in TestError class made here
	# It checks the __init__.py file in the test_cases folder and the TestError
	# functions use that to check and assert that they return the correct numbers
		unittest.main()