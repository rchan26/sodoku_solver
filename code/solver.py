from math import sqrt
from copy import deepcopy
from functools import reduce
import random

def is_full(puzzle):
	#checks if the grid is full yet or not; returns True if puzzle is full
	n=len(puzzle)
	for i in range(n):
		for j in range(n):
			if (puzzle[i][j]==0) or (type(puzzle[i][j])==list):
				return False

	return True

def count_brute_force(puzzle):
	#counts the number of solutions we'd need to try if we went brute force route
	n = len(puzzle)
	mark_ups = []
	for i in range(n):
		for j in range(n):
			if (type(puzzle[i][j])==list):
				mark_ups.append(len(puzzle[i][j]))

	solutions = reduce(lambda x, y: x*y, mark_ups)

	return solutions

def first_smallest_mark_up(puzzle):
	#finds the first position with the least number of possibilities
	n=len(puzzle)
	smallest_len = n
	for i in range(n):
		for j in range(n):
			if (type(puzzle[i][j])==list) and (len(puzzle[i][j])<smallest_len):
				smallest_len=len(puzzle[i][j])

	(i,j)=(0,0)
	while not(type(puzzle[i][j])==list and len(puzzle[i][j])==smallest_len):
		while not(type(puzzle[i][j])==list and len(puzzle[i][j])==smallest_len):
			if j<(n-1):
				j+=1
			else:
				i+=1
				j=0

	return (i,j)

def error_check(puzzle):
	#checks for any errors in the puzzle; returns True if an error is found
	n=len(puzzle)

	#checking for any lists of length zero
	for i in range(n):
		for j in range(n):
			if (type(puzzle[i][j])==list) and (len(puzzle[i][j])==0):
				return True

	#checking if any number occurs more than once within a peer
	for i in range(n):
		for j in range(n):
			#checks the rows
			check = dict([(i, 0) for i in range(1, n+1)])
			for y in range(n):
				if (type(puzzle[i][y])==int) and puzzle[i][y]!=0:
					check[puzzle[i][y]]=check[puzzle[i][y]]+1
			for key in list(check.keys()):
				if (check[key]>1):
					return True
			#checks the columns
			check = dict([(i, 0) for i in range(1, n+1)])
			for x in range(n):
				if (type(puzzle[x][j])==int) and puzzle[x][j]!=0:
					check[puzzle[x][j]]=check[puzzle[x][j]]+1
			for key in list(check.keys()):
				if (check[key]>1):
					return True
			#checks the sqrt(n)xsqrt(n) sub-grids
			check = dict([(i, 0) for i in range(1, n+1)])
			x=int(int(i/sqrt(n)) * sqrt(n))
			y=int(int(j/sqrt(n)) * sqrt(n))
			for u in range(x, int(x+sqrt(n))):
				for v in range(y, int(y+sqrt(n))):
					if (type(puzzle[u][v])==int) and puzzle[u][v]!=0:
						check[puzzle[u][v]]=check[puzzle[u][v]]+1
			for key in list(check.keys()):
				if (check[key]>1):
					return True

	return False

def possibilities_puzzle(puzzle):
	#replaces the unknown values with a set of possible solutions
	n=len(puzzle)
	for i in range(n):
		for j in range(n):
			if (puzzle[i][j]==0) or (type(puzzle[i][j])==list):
				puzzle[i][j] = list(range(1,n+1))

				#checking the column values
				for x in range(n):
					if (puzzle[x][j] in puzzle[i][j]):
						puzzle[i][j].remove(puzzle[x][j])
				#checking the row values
				for y in range(n):
					if (puzzle[i][y] in puzzle[i][j]):
						puzzle[i][j].remove(puzzle[i][y])
				#checking the sqrt(n)xsqrt(n) square values
				x=int(int(i/sqrt(n)) * sqrt(n))
				y=int(int(j/sqrt(n)) * sqrt(n))
				for u in range(x, int(x+sqrt(n))):
					for v in range(y, int(y+sqrt(n))):
						if (puzzle[u][v] in puzzle[i][j]):
							puzzle[i][j].remove(puzzle[u][v])

	return puzzle

def definite_answers(puzzle):
	#takes a puzzle with unknown entries as list of possibilities
	#locks in any cells that are lists of length 1
	n=len(puzzle)
	for i in range(n):
		for j in range(n):
			if (type(puzzle[i][j])==list) and (len(puzzle[i][j])==1):
				puzzle[i][j]=(puzzle[i][j])[0]

	return puzzle

def update_possibilities(puzzle):
	#takes a puzzle with unknown entries as list of possibilities
	#updates the unknown entries to remove any possibilities that may have been
	#locked in by a step
	n=len(puzzle)

	for i in range(n):
		for j in range(n):
			if type(puzzle[i][j])==int:
				#checking the column values
				for x in range(n):
					if type(puzzle[x][j])==list:
						puzzle[x][j]=[item for item in puzzle[x][j] if item!=puzzle[i][j]]
				#checking the row values
				for y in range(n):
					if type(puzzle[i][y])==list:
						puzzle[i][y]=[item for item in puzzle[i][y] if item!=puzzle[i][j]]
				#checking the sqrt(n) x sqrt(n) square values
				x=int(int(i/sqrt(n)) * sqrt(n))
				y=int(int(j/sqrt(n)) * sqrt(n))
				for u in range(x, int(x+sqrt(n))):
					for v in range(y, int(y+sqrt(n))):
						if type(puzzle[u][v])==list:
							puzzle[u][v]=[item for item in puzzle[u][v] if item!=puzzle[i][j]]

	return puzzle

def peer_checker_col(puzzle, j):
	#implements the 'peer-checker' technique for a column
	#takes a puzzle with unknown entries as the set of possibilities
	#checks how many times a number occurs as a possibility in the column it's in
	n=len(puzzle)
	peer_column = dict([(i, 0) for i in range(1, n+1)])
	definite_answers = []

	#looping through the column to count how many times it occurs
	for x in range(n):
		if (type(puzzle[x][j])==list):
			for item in puzzle[x][j]:
				peer_column[item]=(peer_column[item]+1)
	#checking if any dictionary values are 1
	for key in list(peer_column.keys()):
		if (peer_column[key]==1):
			definite_answers.append(key)
	#values in definite_answers only occur in the column once, so can be locked in
	for x in range(n):
		if (type(puzzle[x][j])==list):
			for item in puzzle[x][j]:
				for answer in definite_answers:
					if item==answer:
						puzzle[x][j]=answer

	update_possibilities(puzzle)
	return puzzle

def peer_checker_row(puzzle, i):
	#implements the 'peer-checker' technique for a row
	#takes a puzzle with unknown entries as the set of possibilities
	#checks how many times a number occurs as a possibility in the row it's in
	n=len(puzzle)
	peer_row = dict([(i, 0) for i in range(1, n+1)])
	definite_answers = []

	#looping through the row to count how many times it occurs
	for y in range(n):
		if (type(puzzle[i][y])==list):
			for item in puzzle[i][y]:
				peer_row[item]=(peer_row[item]+1)
	#checking if any dictionary values are 1
	for key in list(peer_row.keys()):
		if (peer_row[key]==1):
			definite_answers.append(key)
	#values in definite_answers only occur in the row once, so can be locked in
	for y in range(n):
		if (type(puzzle[i][y])==list):
			for item in puzzle[i][y]:
				for answer in definite_answers:
					if item==answer:
						puzzle[i][y]=answer

	update_possibilities(puzzle)
	return puzzle

def peer_checker_square(puzzle, i, j):
	#implements the 'peer-checker' technique for a sub-grid
	#takes a puzzle with unknown entries as the set of possibilities
	#checks how any times a number occurs as a possibility inthe square it's in
	n=len(puzzle)
	peer_square = dict([(i, 0) for i in range(1, n+1)])
	definite_answers = []
	x=int(int(i/sqrt(n)) * sqrt(n))
	y=int(int(j/sqrt(n)) * sqrt(n))

	#loops through the possible values of each cell and counts them
	for u in range(x, int(x+sqrt(n))):
		for v in range(y, int(y+sqrt(n))):
			if (type(puzzle[u][v])==list):
				for item in puzzle[u][v]:
					peer_square[item]=(peer_square[item]+1)
	#checking if any dictionary values are 1
	for key in list(peer_square.keys()):
		if (peer_square[key]==1):
			definite_answers.append(key)
	#values in definite_answers only occur in the sub-grid once, so can be locked in
	for u in range(x, int(x+sqrt(n))):
		for v in range(y, int(y+sqrt(n))):
			if (type(puzzle[u][v])==list):
				for item in puzzle[u][v]:
					for answer in definite_answers:
						if item==answer:
							puzzle[u][v]=answer

	update_possibilities(puzzle)
	return puzzle

def naked_pairs(puzzle):
	#implements the 'naked pairs' technique
	#takes a puzzle with unknown entries as the set of possibilities
	#looks for lists of length 2 that are in the share the same peer
	n=len(puzzle)

	for i in range(n):
		for j in range(n):
			if (type(puzzle[i][j])==list) and len(puzzle[i][j])==2:
				#checks the columns
				for x in range(n):
					if x!=i and puzzle[i][j]==puzzle[x][j]:
						#execute if found a naked pair in its column
						for w in range(n):
							if w!=i and w!=x and type(puzzle[w][j])==list:
								puzzle[w][j]=[item for item in puzzle[w][j] if
									item not in puzzle[i][j]]
				#checks the rows
				for y in range(n):
					if y!=j and puzzle[i][j]==puzzle[i][y]:
						#execute if found a naked pair in its row
						for w in range(n):
							if w!=j and w!=y and type(puzzle[i][w])==list:
								puzzle[i][w]=[item for item in puzzle[i][w] if
									item not in puzzle[i][j]]
				#checks the sqrt(n) x sqrt(n) boxes
				x=int(int(i/sqrt(n)) * sqrt(n))
				y=int(int(j/sqrt(n)) * sqrt(n))
				for u in range(x, int(x+sqrt(n))):
					for v in range(y, int(y+sqrt(n))):
						if (i,j)!=(u,v) and puzzle[i][j]==puzzle[u][v]:
							for s in range(x, int(x+sqrt(n))):
								for t in range(y, int(y+sqrt(n))):
									if puzzle[s][t]!=puzzle[i][j] and type(puzzle[s][t])==list:
										puzzle[s][t]=[item for item in puzzle[s][t]
											if item not in puzzle[i][j]]

	definite_answers(puzzle)
	update_possibilities(puzzle)
	return puzzle

def same_row_check(coordinates):
	#if all i coordinates are the same, then they're in same row; return True
	n=len(coordinates)
	for coord in range(1,n):
		if coordinates[coord][0]!=coordinates[0][0]:
			return False

	return True

def same_col_check(coordinates):
	#if all j coordinates are the same, then they're in same column; return True
	n=len(coordinates)
	for coord in range(1,n):
		if coordinates[coord][1]!=coordinates[0][1]:
			return False

	return True

def locked_candidates(puzzle, i, j):
	#implements the 'locked candidates' technique
	#takes a puzzle with unknown entries as the set of possibilities
	#looks for candidates that only occur in a row or column in its sub-grid
	n=len(puzzle)
	candidates = dict([(i, 0) for i in range(1, n+1)])
	x=int(int(i/sqrt(n)) * sqrt(n))
	y=int(int(j/sqrt(n)) * sqrt(n))

	#loops through the possible values of each cell and counts them
	for u in range(x, int(x+sqrt(n))):
		for v in range(y, int(y+sqrt(n))):
			if (type(puzzle[u][v])==list):
				for item in puzzle[u][v]:
					candidates[item]=(candidates[item]+1)

	#checks if any occur between 2 and sqrt(n) times, then its possible they're locked
	for key in list(candidates.keys()):
		if candidates[key]<2 or candidates[key]>sqrt(n):
			candidates.pop(key)
		else:
			candidates[key]=[]

	#checking if the remaining candidates are locked; checks if appear in same row/column
	#seeing where they occur on the grid
	for u in range(x, int(x+sqrt(n))):
		for v in range(y, int(y+sqrt(n))):
			if (type(puzzle[u][v])==list):
				for item in puzzle[u][v]:
					for key in list(candidates.keys()):
						if item==key:
							candidates[key].append((u,v))

	#checking if they occur all in the same column or row
	for key in list(candidates.keys()):
		#checking columns
		if same_col_check(candidates[key]):
			for i in [i for i in range(n) if i not in range(x, int(x+sqrt(n)))]:
				j=candidates[key][0][1]
				if type(puzzle[i][j])==list and (key in puzzle[i][j]):
					puzzle[i][j].remove(key)
		#checking rows
		if same_row_check(candidates[key]):
			for j in [j for j in range(n) if j not in range(y, int(y+sqrt(n)))]:
				i=candidates[key][0][0]
				if type(puzzle[i][j])==list and (key in puzzle[i][j]):
					puzzle[i][j].remove(key)

	definite_answers(puzzle)
	update_possibilities(puzzle)
	return puzzle

def constraints(puzzle):
	#applys the logic rules and techniques to the Sudoku puzzle
	n=len(puzzle)

	change_checker = []
	while change_checker!=puzzle:
		change_checker=deepcopy(puzzle)
		definite_answers(puzzle)
		update_possibilities(puzzle)

	if not(is_full(puzzle)):
		#more advanced techniques are needed
		naked_pairs(puzzle)
		for i in range(0,n,int(sqrt(n))):
			for j in range(0,n,int(sqrt(n))):
				locked_candidates(puzzle,i,j)
		for i in range(n):
			peer_checker_row(puzzle,i)
		for j in range(n):
			peer_checker_col(puzzle,j)
		for i in range(0,n,int(sqrt(n))):
			for j in range(0,n,int(sqrt(n))):
				peer_checker_square(puzzle,i,j)

	#calling the function until the sudoku puzzle is solved or makes no changes
	if is_full(puzzle):
		return True
	elif puzzle==change_checker:
		return False
	else:
		constraints(puzzle)

def guess(stack, puzzle):
	#implements a backtracking algorithm to complete a Sudoku grid
	n=len(puzzle)

	while not(is_full(puzzle)) or error_check(puzzle):
		smallest_index=first_smallest_mark_up(puzzle)
		(i,j)=smallest_index
		#random.shuffle(puzzle[i][j])

		if len(puzzle[i][j])!=0:
			#if there's still possibilities, it will make a guess
			item=deepcopy(puzzle[i][j][0])
			puzzle[i][j].remove(puzzle[i][j][0])
			stack.append(deepcopy(puzzle))
			puzzle[i][j]=item
			constraints(puzzle)

		if error_check(puzzle):
			#if there's an error, go back to last item in stack
			if len(stack)!=1:
				puzzle=deepcopy(stack[-1])
				stack.pop()
			elif len(stack)==0:
				return False

	return solve(puzzle)

def solve(puzzle):
	n=len(puzzle)
	possibilities_puzzle(puzzle)
	constraints(puzzle)

	if constraints(puzzle):
		print("The solution:")
		for i in range(n):
			print(puzzle[i])
	elif not(constraints(puzzle)) and error_check(puzzle):
		#didn't solve it and has an error
		print("There has been an error in solving this puzzle")
	elif not(constraints(puzzle)):
		#didn't solve it but needs to search for a solution now
		stack=[deepcopy(puzzle)]
		return guess(stack,puzzle)

	return puzzle
