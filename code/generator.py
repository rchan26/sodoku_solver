import random
from copy import deepcopy
from itertools import permutations

def derangement(list_of_permutations):
	#takes a list of possible permutations and returns a list of derangements

	replicate=deepcopy(list_of_permutations)
	#loops through the replicate list
	for i in range(1,len(replicate)):
		for item in range(len(replicate[i])):
			#if there's object in the same position, then remove from list
			if replicate[i][item]==replicate[0][item] and (replicate[i] in list_of_permutations):
				list_of_permutations.remove(replicate[i])

	if len(replicate)>0:
		list_of_permutations.remove(replicate[0])

	return list_of_permutations

def order(derangements,m):
	#takes a set of possible derangements and gives an order for the next (m-1) choices

	#first shuffling the derangements to get a random one to choose first
	random.shuffle(derangements)
	#chooses the next row
	order=[derangements[0]]
	#loops through the derangements to keep deleting the ones that are not possible
	for i in range(m):
		derangement(derangements)
		if len(derangements)>0:
			order.append(derangements[0])

	return order

def create_sudoku(m=3):
	n=m**2
	puzzle = [[0 for i in range(n)] for j in range(n)]

	##### Step 1: Getting a permutation of n numbers (n! possibilities) #####

	numbers = list(range(1, n+1))
	random.shuffle(numbers)
	puzzle[0]=numbers

	##### Step 2: Getting the first m rows #####

	#splitting the list into lists of length m
	chunks = [numbers[x:x+m] for x in range(0,n,m)]

	#gets a possible derangements of the next (m-1) rows and gets a new order
	derangements = derangement(list(permutations(chunks)))
	random.shuffle(derangements)
	new_order = order(derangements,m)

	#expanding the chunks into just one list and making them the next (m-1) rows
	for i in range(1,m):
		for item in new_order:
			for chunk in item:
				random.shuffle(chunk)
		puzzle[i]=[item for sublist in new_order[i-1] for item in sublist]

	##### Step 3: Getting the columns #####

	#getting a list of lists which contain the columns of the first m rows
	columns = [[] for i in range(n)]
	for j in range(n):
		for i in range(m):
			columns[j].append(puzzle[i][j])

	column_chunks = [columns[x:x+m] for x in range(0,n,m)]

	#getting possible derangements for the columns and get a new order
	column_derangements = []
	for i in range(len(column_chunks)):
		column_derangements.append(derangement(list(permutations(column_chunks[i]))))
	new_order_col = []
	for i in range(len(column_derangements)):
		new_order_col.append(order(column_derangements[i], m))

	#col_band is the columns for each band
	col_band=dict((band,[]) for band in range(1,m))
	for column in range(m):
		for band in range(1,m):
			col_band[band].append(new_order_col[column][band-1])

	for band in range(1,m):
		col_band[band]=[item for sublist in col_band[band] for item in sublist]

	#now putting these into the right squares
	for band in range(1,m):
		for i in range((band*m), (band*m)+m):
			for j in range(n):
				puzzle[i][j]=col_band[band][j][i%m]

	##### Step 4: Permute the rows for the horizontal bands #####

	#get possible permutations of each band
	new_permutation=[]
	for i in range(0,m):
		possible_perms=list(permutations(poss for poss in range((i*m),(i*m)+m)))
		permutation_choice=possible_perms[random.randint(0,len(possible_perms)-1)]
		for row_choice in permutation_choice:
			new_permutation.append(row_choice)
	puzzle=[puzzle[i] for i in new_permutation]

	return puzzle

#code to generate puzzles using the Solver algorithm:
#first uncomment line 394 in the guess function
"""
import solver
solver.solve([[0 for i in range(9)] for j in range(9)])
"""
