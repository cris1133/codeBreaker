import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time
from sets import Set
import thread
import random
from pyfiglet import figlet_format
from itertools import chain, repeat, islice

def main(stdscr):

	global start
	start = time.time()

	def calcx(string1):
		y, x = myscreen.getmaxyx()
		return int(x)/2-len(string1)/2

	def generateNumber():
		return random.randint(0, 9999)
	global numberRandom
	numberRandom = generateNumber()

	def pad(iterable, size):
		return ([0] * (14 - len(iterable))) + iterable

	def bitfield(n):
	    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

	def bits(n):
		return pad(bitfield(n), 14)

	def checkNumber(number):
		sm = [i for i, j in zip(bits(numberRandom), bits(number)) if i == j]
		similarity = (len(sm))
		if similarity > 3:
			return True
		else:
			return False	

	# Let's start etching out the basic GUI
	def window():
		temp_right_panel_numbers = set(right_panel_numbers)
		temp_right_panel_numbers = list(temp_right_panel_numbers)

		myscreen.border(0)
		myscreen.addstr(20, 1, "-"*78, curses.color_pair(1))
		for i in range(1, 20):
			myscreen.addstr(i, 50, "|", curses.color_pair(1))
		for i in range(20, 23):
			myscreen.addstr(i, 50, "|", curses.color_pair(1))
		for i in range(21, 23):
			myscreen.addstr(i, 8, "|", curses.color_pair(1))
		for i in range(len(temp_right_panel_numbers)):
			myscreen.addstr(i+1, 52, str(temp_right_panel_numbers[i]))

		# Range parameters
		myscreen.addstr(21, 9, str(range_first), curses.color_pair(3))
		myscreen.addstr(22, 9, str(range_second), curses.color_pair(3))

	current_window = 1
	up_down = 1
	right_panel_numbers = []
	range_first = 0
	range_second = 9999
	global game
	game = 1

	global pad_y
	pad_y = 1

	def refresh():
		curcode = 0
		range_first_temp = range_first
		global game
		if game == 0:
			end = time.time()
			myscreen.clear()
			myscreen.addstr(8, 1, figlet_format('Game Over!', font='big', justify = 'center'), curses.color_pair(3))
			myscreen.addstr(15, 32, "Code is: ", curses.color_pair(3))
			myscreen.addstr(15, 41, str(numberRandom), curses.color_pair(2))
			myscreen.addstr(16, calcx(("Time Elapsed: "+str(int(end-start)))) - 2,"Time Elapsed: " + str(int(end-start)), curses.color_pair(1))
			myscreen.refresh()
			myscreen.getch()
			raise SystemExit
		while game == 1:
			if range_first_temp != range_first:
				curcode = 0
				range_first_temp = range_first
			if range_first + curcode > range_second:
				curcode = 0
			if (curcode + range_first) == numberRandom:
				game = 0
				refresh()
				break
			temp_right_panel_numbers = set(right_panel_numbers)
			temp_right_panel_numbers = list(temp_right_panel_numbers)

			myscreen.border(0)
			myscreen.addstr(20, 1, "-"*78, curses.color_pair(1))
			for i in range(1, 20):
				myscreen.addstr(i, 50, "|", curses.color_pair(1))
			for i in range(20, 23):
				myscreen.addstr(i, 50, "|", curses.color_pair(1))
			for i in range(21, 23):
				myscreen.addstr(i, 8, "|", curses.color_pair(1))

			# Right Panel
			for i in range((min((19 * (pad_y-1)), len(temp_right_panel_numbers))),(min((19 * pad_y), len(temp_right_panel_numbers))) ):
				pos = i - (19* (pad_y-1))
				if checkNumber(temp_right_panel_numbers[i]) == True:
					myscreen.addstr(pos+1, 52, str(temp_right_panel_numbers[i]).zfill(4), curses.color_pair(3))
				else:
					myscreen.addstr(pos+1, 52, str(temp_right_panel_numbers[i]).zfill(4), curses.color_pair(2))

			# Page Number
			myscreen.addstr(1, 68, "Page #"+str(pad_y), curses.color_pair(1))

			# Range parameters
			myscreen.addstr(21, 9, str(range_first).zfill(4), curses.color_pair(3))
			myscreen.addstr(22, 9, str(range_second).zfill(4), curses.color_pair(3))

			if checkNumber((curcode + range_first)) == True:
				myscreen.addstr(10, 23, str(curcode + range_first).zfill(4), curses.color_pair(3))
			else:
				myscreen.addstr(10, 23, str(curcode + range_first).zfill(4), curses.color_pair(2))
				right_panel_numbers.append(curcode + range_first)
			
			# myscreen.addstr(11, 23, str(numberRandom).zfill(4), curses.color_pair(3))
			curcode = curcode + 1
			myscreen.refresh()
			time.sleep(0.1)

	thread.start_new_thread(refresh, ())

	while game == 1:
		myscreen.clear()

		if current_window == 1:
			myscreen.addstr(20 + up_down, 1, "> ", curses.color_pair(2))

		if current_window == 2:
			myscreen.addstr(22, 51, "> ", curses.color_pair(2))

		key = myscreen.getch()
		if key == curses.KEY_RIGHT:
			current_window = 2
		if key == curses.KEY_LEFT:
			current_window = 1
		if current_window == 1:
			if key == curses.KEY_UP:
				up_down = 1
			if key == curses.KEY_DOWN:
				up_down = 2
		if current_window == 2:
			if key == curses.KEY_UP:
				if pad_y > 1:
					pad_y = pad_y - 1
			if key == curses.KEY_DOWN:
				pad_y = pad_y + 1

		# Handle input of numbers
		if key != curses.KEY_RIGHT and key != curses.KEY_LEFT and key != curses.KEY_UP and key != curses.KEY_DOWN and key < 256 and key > -1:
			if current_window == 2:
				my_input = []
				for i in range(1, 6):
					if key == curses.KEY_LEFT:
						current_window = 1
						break
					if key == curses.KEY_RIGHT:
						break
					if key == curses.KEY_UP:
						if pad_y > 1:
							pad_y = pad_y - 1
					if key == curses.KEY_DOWN:
						pad_y = pad_y + 1
					if chr(key).isdigit() and i < 5:
						myscreen.addstr(22, 52 + i, chr(key))
						my_input.append(int(chr(key)))
					elif chr(key) == "\n" and i == 5:
						final_input = (my_input[0]*1000) + (my_input[1]*100) + (my_input[2]*10) + (my_input[3])
						right_panel_numbers.append(final_input)
						if final_input == numberRandom:
							game = 0
							refresh()
							break
					else:
						break
					key = myscreen.getch()
			if current_window == 1:
				my_input = []
				for i in range(1, 6):
					if key == curses.KEY_RIGHT:
						current_window = 2
						break
					if key == curses.KEY_LEFT:
						break
					if key == curses.KEY_UP:
						break
					if key == curses.KEY_DOWN:
						break
					if chr(key).isdigit() and i < 5:
						myscreen.addstr(20 + up_down, 2 + i, chr(key))
						my_input.append(int(chr(key)))
					elif chr(key) == "\n" and i == 5:
						final_input = (my_input[0]*1000) + (my_input[1]*100) + (my_input[2]*10) + (my_input[3])
						if up_down == 1:
							range_first = final_input
						if up_down == 2:
							range_second = final_input
					else:
						break
					key = myscreen.getch()

def startScreen(stdscr):
	# Basic definitions, colors, etc.
	global myscreen
	myscreen = curses.initscr()
	curses.start_color()
	curses.curs_set(0)
	curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
	option = 1
	key = 1

	while 1==1:


		# Title
		myscreen.clear()
		myscreen.addstr(1, 1, figlet_format('Code Breaker', font='big', justify = 'center'), curses.color_pair(3))

		# Play option
		if option == 1:
			myscreen.addstr(9, 36, "Play", curses.color_pair(2)|curses.A_BOLD)
		else:
			myscreen.addstr(9, 36, "Play", curses.color_pair(2))
		if key == ord('\n') and option == 1:
			main(stdscr)

		# Instructions option
		if option == 2:
			myscreen.addstr(11, 32, "Instructions", curses.color_pair(2)|curses.A_BOLD)
		else:
			myscreen.addstr(11, 32, "Instructions", curses.color_pair(2))
		if key == ord('\n') and option == 2:
			instructions(stdscr)

		myscreen.addstr(13, 26, "Game By: Cristopher Bello", curses.color_pair(1)|curses.A_BOLD)

		# Allow scrolling through the options
		if key == curses.KEY_UP:
			if option > 1:
				option = option - 1

		if key == curses.KEY_DOWN:
			if option < 2:
				option = option + 1

		myscreen.refresh()
		key = myscreen.getch()

def instructions(stdscr):
	
	# Title
	myscreen.clear()
	myscreen.addstr(1, 1, figlet_format('Code Breaker', font='big', justify = 'center'), curses.color_pair(3))

	# Instructions
	def calcx(string1):
		y, x = myscreen.getmaxyx()
		return int(x)/2-len(string1)/2

	line1 = "The objective of the game is to find the correct code."
	line2 = "The code is being automatically bruteforced on the left side of the screen."
	line3 = "The menu on the bottom-left lets you enter a range for the bruteforcer."
	line4 = "The menu on the right lets you try and test numbers."
	line5 = "If you test the right number or the bruteforcer finds it, you win."
	line6 = "Green numbers have 4 bits in common with the code, red numbers do not."
	line7 = "You are going to need a programmer's calculator to play this game."
	line8 = "One can be found by switching your computer's calculator to Programmer mode."
	line9 = "Press any key to go back to the main menu."

	myscreen.addstr(9, calcx(line1), line1)
	myscreen.addstr(10, calcx(line2), line2)
	myscreen.addstr(11, calcx(line3), line3)
	myscreen.addstr(12, calcx(line4), line4)
	myscreen.addstr(13, calcx(line5), line5)
	myscreen.addstr(14, calcx(line6), line6)
	myscreen.addstr(15, calcx(line7), line7)
	myscreen.addstr(16, calcx(line8), line8)
	myscreen.addstr(18, calcx(line9), line9, curses.color_pair(1)|curses.A_BOLD)

	# Press any key to continue
	myscreen.refresh()
	myscreen.getch()
	startScreen(stdscr)

wrapper(startScreen)
