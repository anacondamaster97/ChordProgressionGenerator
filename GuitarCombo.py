
import random
import math


def board():
	"""
	Creates fret board for guitar

	Returns:
		List[List[String]]: 2d array with guitar fretboard
	"""
	full = [['F','F#','G','G#','A','A#','B','C','C#','D','D#','E']
		['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
		['G#','A','A#','B','C','C#','D','D#','E','F','F#','G']
		['D#','E','F','F#','G','G#','A','A#','B','C','C#','D']
		['A#','B','C','C#','D','D#','E','F','F#','G','G#','A']
		['F','F#','G','G#','A','A#','B','C','C#','D','D#','E']]

	
	return full

def scales(note):
	#  W W H W W W H
	"""
	Generates scales with a base note

	Args:
		note (String): Note Ex: B or F#

	Returns:
		List[String]: returns a scale based on base note
	"""
	
	notes=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	starting_pos=notes.index(note)

	scale=[]

	notes_count=0

	count=12
	while(count>=0):
		scale.append(notes[starting_pos])
		if notes_count ==2 or notes_count==6:
			starting_pos+=1
			count-=1
		else:
			starting_pos+=2
			count-=2
		if starting_pos==12:
			starting_pos=0
		elif starting_pos>12:
			starting_pos=1

		
		notes_count+=1
	
	scale=scale[:len(scale)-1]
	return scale

def key_Chord(scale):
	#  M m m M M m Dim
	"""
	Attatches progression values to scale. Ex: Major and Minor patterns above

	Args:
		scale (List[String]): Musical scale from previous function

	Returns:
		List[String]: Scale with added progression values Ex: Major and Minor patterns
	"""
	for index in range(len(scale)):
		if index==1 or index ==2 or index==5:
			scale[index]+='m'
	return scale

def allScales():
	"""
	Generates every scale permutation with previous functions

	Returns:
		List[List[String]]: Every permutation of scales
	"""
	sc="CDEFGAB"
	allScales=[]
	for elems in sc:
		allScales.append(key_Chord(scales(elems)))
	print(allScales)
	return allScales


def whichKey(chordProg):
	"""
	Tells user the key based on chord progression

	Args:
		chordProg (List[String]): Any Chord Progression

	Returns:
		String: Scale of the chord progression given
	"""
	scales='CDEFGAB'
	scale=0
	count=0
	fullScales=allScales()
	for elems in fullScales:
		for vals in chordProg:
			if vals in elems:
				count+=1
		if count==len(chordProg):
			return scales[scale]
		count=0
		scale+=1

	return None

def setUp():
	"""
	Sets up the permutations of chord progressions, minor/major scale patters, and
	permutations of chord patterns for major and minor chord progressions

	Returns:
		Tuple(Dict(String:List[String]), Tuple(String, String),
		List[List[Int]], List[List[Int]]): Returns a tuple with progressions, scale_patterns
		(with major and minor scales inside), chord_patterns_major, and chord_patterns_minor
	"""
	progressions = {
		"A" : ["B","C","D","E","F","G"],
		"B" : ["C#","D","E","F","#G","A"],
		"C" : ["D","D#","F","G","G#","A#"],
		"D" : ["E","F","G","A","A#","C"],
		"E" : ["F#","G","A","B","C","D"],
		"F" : ["G", "G#", "A#","C","C#","D#"],
		"G" : ["A","A#","C","D","D#","F"]
	}
	minor_scale_patterns = "mdMmmMM" # major = M minor = m diminished = d
	major_scale_patterns = "MmmMMmd"
	scale_patterns = (major_scale_patterns, minor_scale_patterns)

	chord_patterns_major = [
		[1,4,5],
		[1,6,2,5],
		[1,3,4,5],
		[1,6,4,5],
		[1,5,6,4],
		[1,4,1,5],
		[1,4,2,5],
		[1,4,6,5],
		[2,5,1]
	]

	chord_patterns_minor = [
		[1,6,7],
		[1,6,3,7],
		[1,7,6,7],
		[1,4,7],
		[1,4,5,1],
		[1,4,1],
		[1,4,5],
		[6,7,1,1],
		[2,5,1]
	]
	return (progressions, scale_patterns, chord_patterns_major, chord_patterns_minor)


def optimize():
	"""
	Uses a Feedback loop to select random chord progressions based on mood and optimizes 
	to produce moods that are favorable to the user
	"""
	#l oading data from setUp()
	data = setUp() #tuple
	progressions = data[0]
	major_scale_patterns = data[1][0]
	minor_scale_patterns = data[1][1]
	chord_patterns_major = data[2]
	chord_patterns_minor = data[3]

	# creating optimizer metrics
	chord_pattern_major_optimizer = [1000/len(chord_patterns_major) for index in range(len(chord_patterns_major))]
	chord_pattern_minor_optimizer = [1000/len(chord_patterns_minor) for index in range(len(chord_patterns_minor))]



	progression_base = [note for note in progressions]

	running = True

	# adjustment values
	decrement_value = 0.9
	increment_value = 1.1

	major_length = 1000
	minor_length = 1000

	while(running):

		scale = random.choice(progression_base)
		print(scale)
		key = random.choice(["Minor", "Major"])
		print(key)
		print(chord_pattern_major_optimizer, chord_pattern_minor_optimizer)
		choice_value = 0
		choice = []
		if key == "Major":
			randomized = random.randrange(0, major_length)
			count = 0
			counter = 0
			while count < randomized:
				count+=chord_pattern_major_optimizer[counter]
				if counter == 8: break
				counter+=1
			
			choice = chord_patterns_major[counter]
			choice_value = counter
		else:
			
			randomized = random.randrange(0, minor_length)
			count = 0
			counter = 0
			while count < randomized:
				count+=chord_pattern_minor_optimizer[counter]
				if counter == 8: break
				counter+=1

			
			choice = chord_patterns_minor[counter]
			choice_value = counter
		print(choice)
		progression = []
		for counter, elems in enumerate(choice):
			if key == "Minor":
				if elems == 1:
					progression.append(scale+minor_scale_patterns[0])
				else:
					progression.append(progressions[scale][elems - 2]+minor_scale_patterns[elems - 1])
			if key == "Major":
				if elems == 1:
					progression.append(scale+major_scale_patterns[0])
				else:
					progression.append(progressions[scale][elems - 2]+major_scale_patterns[elems - 1])
		counter = 0
		print(progression)
		prompt = input("L for Like. D for Dislike. E for Exit:\n")
		factor = 0
		if prompt == 'E':
			running = False
		elif prompt == 'L':
			factor = increment_value
			
		elif prompt == 'D':
			factor = decrement_value
		else:
			running = False
			
		if key == "Major":
			if factor == decrement_value:
				major_length -= math.floor(chord_pattern_major_optimizer[choice_value]*(1-factor))
			else:
				major_length += math.floor(chord_pattern_major_optimizer[choice_value]*(factor-1))
			chord_pattern_major_optimizer[choice_value]*=factor
		if key == "Minor" :
			if factor == decrement_value:
				minor_length -= math.floor(chord_pattern_minor_optimizer[choice_value]*(1-factor))
			else:
				minor_length += math.floor(chord_pattern_minor_optimizer[choice_value]*(factor-1))
			chord_pattern_minor_optimizer[choice_value]*=factor

		
		







