from art import *
import random
import math
import torch
import torch.nn as nn
import torch.optim as optim


def board():
	"""
	Creates fret board for guitar

	Returns:
		List[List[String]]: 2d array with guitar fretboard
	"""
	full = [['F','F#','G','G#','A','A#','B','C','C#','D','D#','E'],
		['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'],
		['G#','A','A#','B','C','C#','D','D#','E','F','F#','G'],
		['D#','E','F','F#','G','G#','A','A#','B','C','C#','D'],
		['A#','B','C','C#','D','D#','E','F','F#','G','G#','A'],
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

class setUp:
	"""
	Sets up the permutations of chord progressions, minor/major scale patters, and
	permutations of chord patterns for major and minor chord progressions

	Returns:
		Tuple(Dict(String:List[String]), Tuple(String, String),
		List[List[Int]], List[List[Int]]): Returns a tuple with progressions, scale_patterns
		(with major and minor scales inside), chord_patterns_major, and chord_patterns_minor
	"""
	def __init__(self):
		
		self.progressions_major = {'A': ['A', 'Bm', 'C#m', 'D', 'E', 'F#m', 'G#d'], 'B': ['B', 'C#m', 'D#m', 'E', 'F#', 'G#m', 'A#d'], 'C': ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bd'], 'D': ['D', 'Em', 'F#m', 'G', 'A', 'Bm', 'C#d'], 'E': ['E', 'F#m', 'G#m', 'A', 'B', 'C#m', 'D#d'], 'F': ['F', 'Gm', 'Am', 'A#', 'C', 'Dm', 'Ed'], 'G': ['G', 'Am', 'Dm', 'C', 'D', 'Em', 'F#dim']}
		self.progressions_minor = {'Am': ['Am', 'Bd', 'C', 'Dm', 'Em', 'F', 'G'], 'Bm': ['Bm', 'C#d', 'D', 'Em', 'F#m', 'G', 'A'], 'Cm': ['Cm', 'Dd', 'D#', 'Fm', 'Gm', 'G#', 'A#'], 'Dm': ['Dm', 'Ed', 'F', 'Gm', 'Am', 'A#', 'C'], 'Em': ['Em', 'F#d', 'G', 'Am', 'Bm', 'C', 'D'], 'Fm': ['Fm', 'Gd', 'G#', 'A#m', 'Cm', 'C#', 'D#'], 'Gm': ['Gm', 'Ad', 'A#', 'Cm', 'Dm', 'D#', 'F']}
  
		self.major_scale_patterns = "MmmMMmd"
		self.minor_scale_patterns = "mdMmmMM" # major = M minor = m diminished = d
		

		self.chord_patterns_major = [
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

		self.chord_patterns_minor = [
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

variables = setUp()

progressions_major = variables.progressions_major
progressions_minor = variables.progressions_minor

chord_patterns_major = variables.chord_patterns_major
chord_patterns_minor = variables.chord_patterns_minor

class ChordRecommender(nn.Module):
    def __init__(self):
        super(ChordRecommender, self).__init__()
        self.fc = nn.Linear(6, 1)  

    def forward(self, x):
        return self.fc(x)

model = ChordRecommender()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

def map_chord_pattern_to_progression(chord_pattern, progression):
    return [progression[i-1] for i in chord_pattern]

while True:
    key_type = input("Do you want a Major or Minor progression? (Enter 'Major' or 'Minor'): ").lower()
    
    if key_type == 'major':
        keys = list(progressions_major.keys())
        progressions = progressions_major
        patterns = chord_patterns_major
    elif key_type == 'minor':
        keys = list(progressions_minor.keys())
        progressions = progressions_minor
        patterns = chord_patterns_minor
    else:
        print("Invalid input. Please enter 'Major' or 'Minor'.")
        continue
    
    print("Available keys:", keys)
    key = input(f"Choose a key from the above options: ")
    
    if key not in progressions:
        print("Invalid key. Please choose a valid key.")
        continue
    
    chosen_pattern = random.choice(patterns)

    mapped_chords = map_chord_pattern_to_progression(chosen_pattern, progressions[key])
    print(f"Generated Chord Progression: {mapped_chords}")

    user_feedback = float(input("Rate this progression (0.0 to 1.0): "))
    
    while len(chosen_pattern) < 6:
        chosen_pattern.append(0)

    chosen_pattern_tensor = torch.tensor(chosen_pattern, dtype=torch.float32).view(1, -1)  # Reshape to (1, 6)
    
    output = model(chosen_pattern_tensor)  # Output is a 1x1 tensor
    target = torch.tensor([[user_feedback]], dtype=torch.float32)  # Make sure the target is 2D (1x1 tensor)
    
    loss = criterion(output, target)
    
    optimizer.zero_grad()  
    loss.backward()
    optimizer.step()

    print(f"Training iteration completed with loss: {loss.item()}")
    

    cont = input("Would you like to continue? (yes/no): ")
    if cont.lower() != 'yes':
        break
