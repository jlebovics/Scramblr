""" 
3x3x3 Rubik's Cube random-move scrambler and timer
by Jamie Lebovics

This project was done just for fun and is not being updated or mantained
"""

from random import randint
import time
import csv
import sys
import datetime
import re



if len(sys.argv) >=2:
	targetfile = sys.argv[1]
else:
	targetfile = "scramblr_session_"+str(datetime.date.today())+".csv"

with open(targetfile, 'a') as csvfile:
	print ""

newfile = False
solves = []

with open(targetfile, 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row == "":
			newfile = True
		else:
			if row['Time'] == "DNF":
				solves.append("DNF")
			else:
				solves.append(float(row['Time']))

	csvfile.seek(0) 
	first_char = csvfile.read(1) 
	if not first_char:
		newfile = True

if newfile:
	with open(targetfile, 'a') as csvfile:
			csvfile.write ("Time,Scramble,Ao5,Ao12,Ao50,Ao100\n")




def avg (lst):
	num_to_avg = len(lst)-2
	total = 0.0
	highest = lst[0]
	lowest = lst[0]

	numDNF = 0
	for e in lst:
		if e=="DNF":
			numDNF += 1
	if numDNF > 1:
		return "DNF"

	else:
		for e in lst:
			if e != "DNF":
				total += e
			if e > highest:
				highest = e
			if e < lowest:
				lowest = e
		if highest != "DNF":
			total -= highest 

		total -= lowest

		return total/num_to_avg

def ao5():
	if len(solves) < 5:
		return ""
	else:
		return shortfloat(avg(solves[-5:]))

def ao12():
	if len(solves) < 12:
		return ""
	else:
		return shortfloat(avg(solves[-12:]))

def ao50():
	if len(solves) < 50:
		return ""
	else:
		return shortfloat(avg(solves[-50:]))

def ao100():
	if len(solves) < 100:
		return ""
	else:
		return shortfloat(avg(solves[-100:]))

def aox(x,lst):
	if len(lst) < x:
		return ""
	else:
		return shortfloat(avg(lst[-x:]))

def best_avg(x):
	avgs = []

	for i in range(x, len(solves)+1):
		avgs.append(aox(x,solves[0:i]))
	return min(avgs)

def view_stats():
	print "Current: "+shortfloat(solves[-1])
	print "Best: "+shortfloat(min(solves))
	if ao5() != "":
		print "Current Ao5: "+ao5()
		print "Best Ao5: "+best_avg(5)
	if ao12() != "":
		print "Current Ao12: "+ao12()
		print "Best Ao12: "+best_avg(12)
	if ao50() != "":
		print "Current Ao50: "+ao50()
		print "Best Ao50: "+best_avg(50)
	if ao100() != "":
		print "Current Ao100: "+ao100()
		print "Best Ao100: "+best_avg(100)

def plus_two():
	solves[-1] += 2
	print shortfloat(solves[-1])

def delete_last_solve():
	solves.pop()

def dnf():
	solves[-1] = "DNF"

def shortfloat(x):
	if x=="DNF":
		return "DNF"
	else:
		m = re.match('([0-9]*\.[0-9]{3})', str(x))
		return m.group(1)



scramble = ""
numscramble = []
moves = {1:"R2",2:"L2",3:"U2",4:"D2",5:"F2",6:"B2",
7:"R",8:"L",9:"U",10:"D",11:"F",12:"B",
13:"R\'",14:"L\'",15:"U\'",16:"D\'",17:"F\'",18:"B\'"}

movesets = [[1,2,7,8,13,14],[3,4,9,10,15,16],[5,6,11,12,17,18]]

playing = True

def valid_next_move(m):
	remainder = m % 6
	if remainder == numscramble[-1] % 6:
		return False
	else:
		if remainder == 1 or remainder == 2:
			for i in range(len(numscramble),0):
				if i not in movesets[0]:
					return True
			return False
		if remainder == 3 or remainder == 4:
			for i in range(len(numscramble),0):
				if i not in movesets[1]:
					return True
			return False
		if remainder == 5 or remainder == 0:
			for i in range(len(numscramble),0):
				if i not in movesets[2]:
					return True
			return False





while playing:
	count = 0
	prev_m = -1
	while count < 19:
		m = randint(1,18)
		if m % 6 != prev_m % 6:
			scramble += moves.get(m) + " "
			numscramble.append(m)
			count += 1

	print scramble

	raw_input("Press Enter to Start Timer")
	start = time.time()
	raw_input("Press Enter to Stop Timer")
	end = time.time()
	print shortfloat(end - start)
	solves.append (float(end - start))

	user_input = raw_input("Options:\n+2 | DNF | delete | view_stats | exit\nFor a new scramble, press Enter\n")
	user_input = user_input.split()

	if "exit" in user_input:
		playing = False
	if "+2" in user_input:
		plus_two()
	if "DNF" in user_input:
		dnf()
	if "delete" in user_input:
		delete_last_solve()
	else:
		with open(targetfile, 'a') as csvfile:
			csvfile.write (shortfloat(solves[-1])+","+scramble+","+ao5()+","+ao12()+","+ao50()+","+ao100()+"\n")
	if "view_stats" in user_input:
		view_stats()

	scramble = ""





