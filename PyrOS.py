#---------------------------IMPORT LIBRARIES

import sqlite3
import random
import time
import os
import sys
import string

#---------------------------CONSTANTS

invalidChars = set(string.punctuation.replace("_", ""))
defaultList = ["install", "uninstall", "restart", "shutdown", "logout"]
modulesList = []
installList = ["calc", "games", "cipher"]
yes_no = ["yes", "no"]

#---------------------------DB SETUP

conn = sqlite3.connect("PyrOS.db")
c = conn.cursor()

try:
	c.execute("""CREATE TABLE credentials (
			username text,
			password text,
			moduleList text,
			installList text
			)""")
except:
	pass

#---------------------------STARTUP

def SUgetUsername():
	username = input("\r\nSTRICTLY NO SPECIAL CHARACTERS\nEnter your username:\n>>> ")
	if any(char in invalidChars for char in username):
		print("No SPECIAL CHARACTERS!!!")
		return SUgetUsername()
	else:
		c.execute("SELECT * FROM credentials WHERE username = ?", (username,))
		result = c.fetchall()
		if len(result) == 0:
			return username
		else:
			print("Username already in use.\nTry another one.")
			return SUgetUsername()

def LIgetUsername():
	username = input("\r\nSTRICTLY NO SPECIAL CHARACTERS\nEnter your username:\n>>> ")
	if any(char in invalidChars for char in username):
		print("No SPECIAL CHARACTERS!!!")
		return LIgetUsername()
	else:
		c.execute("SELECT * FROM credentials WHERE username = ?", (username,))
		result = c.fetchall()
		if len(result) == 0:
			return None
		else:
			return username

def getPassword():
	password = input("\r\nSTRICTLY NO SPECIAL CHARACTERS\nEnter your password:\n>>> ")
	if any(char in invalidChars for char in password):
		print("NO SPECIAL CHARACTERS!!!")
		return getPassword()
	else:
		return password

def signup():
	username = SUgetUsername()
	os.system('cls')
	password = getPassword()
	c.execute("INSERT INTO credentials VALUES (?, ?, ?, ?)", (username, password, '|'.join([]), '|'.join(["calc", "games", "cipher"])))
	conn.commit()
	os.system('cls')
	print("\r\nYou have successfully signed up!\nYou may now login!")
	startup()

def login():
	global username
	global modulesList
	global installList
	username = LIgetUsername()
	os.system('cls')
	if username == None:
		print("\r\nThis username has not been registered yet!\nPlease signup first before logging in.")
		startup()
	else:
		password = getPassword()
		os.system('cls')
		c.execute("SELECT * FROM credentials WHERE username = ? AND password = ?", (username, password))
		result = c.fetchall()
		if len(result) == 0:
			print("\r\nIncorrect Password.\nTry again.")
			login()
		else:
			modulesList = result[0][2].split('|')
			installList = result[0][3].split('|')
			if modulesList == ['']:
				modulesList = []
			if installList == ['']:
				installList = []
			main()

def startup():
	startupR = input("\r\nWelcome to the PyrOS Start Up Page!\nWould you like to login or signup?\nType 'shutdown' if you would like to shut down PyrOs.\n>>> ").lower()
	if startupR == "shutdown":
		shutdownModule()
	elif startupR == "login":
		login()
	elif startupR == "signup":
		os.system('cls')
		signup()
	else:
		os.system('cls')
		print(f"\r\n{startupR} is neither 'shutdown' nor 'login' nor 'signup'!")
		startup()

#---------------------------DEFAULT MODULES

def restartModule():
	for i in range(1, 101):
		print(f"Restarting PyrOS {i}% of 100%", end="\r")
		time.sleep(.01)
	os.system('cls')
	print("\r\nPyrOS restart completed.")
	main()

def shutdownModule():
	os.system('cls')
	for i in range(1, 101):
		print(f"Shutting down PyrOS {i}% of 100%", end="\r")
		time.sleep(.015)
	os.system('cls')
	print("\r\nPyrOS shut down.")
	sys.exit()

def installModule():
	global username
	installmsg = "\r\nPyrOS Module Installation\nHere are the modules available for installation:\n"
	for i in installList:
		installmsg += f"- {i}\n"
	installmsg += "Which module would you like to install?\nType 'exit' if you would like to exit.\n>>> "
	module = input(installmsg).lower()
	if module in installList:
		os.system('cls')
		installList.remove(module)
		for i in range(1, 101):
			print(f"Installing {module} module {i}% of 100%", end="\r")
			time.sleep(.01)
		os.system('cls')
		print(f"\r\nModule {module} successfully installed.")
		modulesList.append(module)
		c.execute("UPDATE credentials SET moduleList = ?, installList = ? WHERE username = ?", ('|'.join(modulesList) ,'|'.join(installList) ,username))
		conn.commit()
		main()
	elif module == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Module Installation...")
		main()
	else:
		os.system('cls')
		print(f"\r\n{module} is not an available module.\nPlease try again.")
		installModule()

def uninstallModule():
	global username
	installmsg = "\r\nPyrOS Module Uninstallation\nHere are the modules available for uninstallation:\n"
	for i in modulesList:
		installmsg += f"- {i}\n"
	installmsg += "Which module would you like to uninstall?\nType 'exit' if you would like to exit.\n>>> "
	module = input(installmsg).lower()
	if module in modulesList:
		if module in defaultList:
			os.system('cls')
			print(f"\r\nModule {module} is a system module.\nYou are unable to uninstall it.\nTry again with another module.")
			uninstallModule()
		else:
			os.system('cls')
			modulesList.remove(module)
			for i in range(1, 101):
				print(f"Uninstalling {module} module {i}% of 100%", end="\r")
				time.sleep(.01)
			os.system('cls')
			print(f"\r\nModule {module} successfully uninstalled.")
			installList.append(module)
			c.execute("UPDATE credentials SET moduleList = ?, installList = ? WHERE username = ?", ('|'.join(modulesList) ,'|'.join(installList) ,username))
			conn.commit()
			main()
	elif module == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Module Uninstallation...")
		main()
	else:
		os.system('cls')
		print(f"\r\n{module} is not an available module.\nPlease try again.")
		uninstallModule()

#---------------------------CIPHER MODULE

MAX_KEY_SIZE = 26

def cipherModule():
	response = input("\r\nPyrOS Cipher Module\nWould you like to \"encrypt\" or \"decrypt\"?\nType \"exit\" to exit.\n>>> ").lower()
	if response in ["encrypt", "decrypt"]:
		os.system('cls')
		mainCipher(response)
	elif response == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Cipher Module...")
		main()
	else:
		os.system('cls')
		print(f"\r\n{response} is not an available option.\nPlease try again.")
		cipherModule()

def getCipherMessage():
	return input("\r\nEnter your message.\n>>> ")

def getCipherKey():
	keyCipher = input(f"Enter the key number (1-{MAX_KEY_SIZE}).\n>>> ")
	try:
		keyCipher = int(keyCipher)
	except ValueError:
		os.system('cls')
		print(f"{keyCipher} isn't a number, try again.")
		return getCipherKey()
	if not (keyCipher >= 1 and keyCipher <= MAX_KEY_SIZE):
		os.system('cls')
		print(f"{keyCipher} is not within 1 and {MAX_KEY_SIZE}, try again.")
		return getCipherKey()
	return keyCipher

def mainCipher(mode):
	message = getCipherMessage()
	key = getCipherKey()
	if mode == "decrypt":
		key = -key
	translated = ''

	for symbol in message:
		if symbol.isalpha():
			num = ord(symbol)
			num += key

			if symbol.isupper():
				if num > ord('Z'):
					num -= 26
				elif num < ord('A'):
					num += 26
			elif symbol.islower():
				if num > ord('z'):
					num -= 26
				elif num < ord('a'):
					num += 26

			translated += chr(num)
		else:
			translated += symbol

	os.system('cls')
	print(f"\r\nYour translated message is {translated}.")
	cipherModule()

#---------------------------GAMES MODULE

gamesList =["guess_the_number", "hangman"]

def gamesModule():
	gamesMsg = "\r\nPyrOS Game Module\nHere are the available games to play:\n"
	for i in gamesList:
		gamesMsg += f"- {i}\n"
	gamesMsg += "Which game would you like to play?\nType 'exit' if you would like to exit.\n>>> "
	game = input(gamesMsg).lower()
	if game in gamesList:
		if game == "guess_the_number":
			os.system('cls')
			guess_the_numberGame()
		if game == "hangman":
			os.system('cls')
			hangmanGame()
	elif game == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Game Module...")
		main()
	else:
		os.system('cls')
		print(f"\r\n{game} is not an available game.\nPlease try again.")
		gamesModule()

#---------------------------HANGMAN GAME

HANGMAN_PICS = ['''
   +---+
       |
       |
       |
      ===''', '''
   +---+
   O   |
       |
       |
      ===''', '''
   +---+
   O   |
   |   |
       |
      ===''', '''
   +---+
   O   |
  /|   |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
  /    |
      ===''', '''
   +---+
   O   |
  /|\  |
  / \  |
      ===''', '''
    +---+
   [O   |
   /|\  |
   / \  |
       ===''', '''
    +---+
   [O]  |
   /|\  |
   / \  |
       ===''']
difficulty = 'X'
words = {
  'Colors':'red orange yellow green blue indigo violet white black brown'.split(),
  'Shapes':'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon septagon octagon'.split(),
  'Fruits':'apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(),
  'Animals':'bat bear beaver cat cougar crab deer dog donkey duck eagle fish frog goat leech lion lizard monkey moose mouse otter owl panda python rabbit rat shark sheep skunk squid tiger turkey turtle weasel whale wolf wombat zebra'.split()
}

def hangmanGenerateWord(wordDict):
  wordKey = random.choice(list(wordDict.keys()))
  wordIndex = random.randint(0, len(wordDict[wordKey]) - 1)
  return [wordDict[wordKey][wordIndex], wordKey]

def hangmanGraphics(missedLetters, correctLetters, word):
  print(f"\r\n{HANGMAN_PICS[len(missedLetters)]}")
  print(f"\r\nMissed Letters:", end=" ")
  for letter in missedLetters:
    print(f"{letter}", end=" ")
  blanks = "_" * len(word)
  for i in range(len(word)):
    if word[i] in correctLetters:
      blanks = blanks[:i] + word[i] + blanks[i+1:]
  hangmanMsg = "\nWord: "
  for letter in blanks:
    hangmanMsg += f"{letter} "
  print(hangmanMsg)

def hangmanGuess(alreadyGuessed):
  while True:
    guess = input("\r\nGuess a letter.\n>>> ").lower()
    if len(guess) != 1:
      print("\r\nPlease enter a single letter.")
    elif guess in alreadyGuessed:
      print("\r\nYou have already guessed that letter.\nChoose again.")
    elif guess not in "abcdefghijklmnopqrstuvwxyz":
      print("\r\nPlease enter a letter.")
    else:
      return guess

def hangmanWin(gameRunning, word):
  userInput = input(f"\r\nCongrats!\nThe word was {word}.\nYou won!\nPlay again? Yes or No\n>>> ").lower()
  if userInput in ["yes", "no"]:
    if userInput == "yes":
      hangmanGame()
    elif userInput == "no":
      gameRunning = False
      gamesModule()
  else:
    os.system('cls')
    print("\r\nHangman")
    print(f"\r\nYou entered neither yes nor no.\nTry again.")
    hangmanWin(gameRunning, word)

def hangmanLose(gameRunning, word):
  userInput = input(f"\r\nThe word was {word}.\nYou lost!\nPlay again? Yes or No\n>>> ").lower()
  if userInput in ["yes", "no"]:
    if userInput == "yes":
      hangmanGame()
    elif userInput == "no":
      gameRunning = False
      os.system('cls')
      gamesModule()
  else:
    os.system('cls')
    print("\r\nHangman")
    print(f"\r\nYou entered neither yes nor no.\nTry again.")
    hangmanLose(gameRunning, word)

def hangmanDifficulty():
  global difficulty
  difficulty = 'X'
  difficulty = input("\r\nEnter Difficulty:\nE - Easy, M - Medium, H - Hard.\n>>> ").upper()
  if difficulty not in ['E', 'M', 'H']:
    os.system('cls')
    print("\r\nHangman")
    print(f"\r\n{difficulty} is neither E nor M nor H.\nTry again.")
    hangmanDifficulty()
  elif difficulty == 'M':
    del HANGMAN_PICS[8]
    del HANGMAN_PICS[7]
  elif difficulty == 'H':
    del HANGMAN_PICS[8]
    del HANGMAN_PICS[7]
    del HANGMAN_PICS[5]
    del HANGMAN_PICS[3]

def hangmanReset():
  global HANGMAN_PICS
  HANGMAN_PICS = ['''
     +---+
         |
         |
         |
        ===''', '''
     +---+
     O   |
         |
         |
        ===''', '''
     +---+
     O   |
     |   |
         |
        ===''', '''
     +---+
     O   |
    /|   |
         |
        ===''', '''
     +---+
     O   |
    /|\  |
         |
        ===''', '''
     +---+
     O   |
    /|\  |
    /    |
        ===''', '''
     +---+
     O   |
    /|\  |
    / \  |
        ===''', '''
      +---+
     [O   |
     /|\  |
     / \  |
         ===''', '''
      +---+
     [O]  |
     /|\  |
     / \  |
         ===''']

def hangmanGame():
  os.system('cls')
  wordset = ''
  hangmanReset()
  print("\r\nHangman")
  hangmanDifficulty()
  
  missedLetters = ''
  correctLetters = ''
  word, wordset = hangmanGenerateWord(words)
  gameRunning = True

  while gameRunning:
    os.system('cls')
    print("\r\nHangman")
    print(f"\r\nThe word is in the set {wordset}")
    hangmanGraphics(missedLetters, correctLetters, word)
    guess = hangmanGuess(missedLetters + correctLetters)

    if guess in word:
      correctLetters += guess
      foundAllLetters = True
      for i in range(len(word)):
        if word[i] not in correctLetters:
          foundAllLetters = False
          break
      if foundAllLetters:
        os.system('cls')
        print("\r\nHangman")
        hangmanWin(gameRunning, word)
    elif guess not in word:
      missedLetters = missedLetters + guess
      if len(missedLetters) == len(HANGMAN_PICS) - 1:
        os.system('cls')
        print("\r\nHangman")
        hangmanGraphics(missedLetters, correctLetters, word)
        hangmanLose(gameRunning, word)

#---------------------------GUESS THE NUMBER GAME

guessesLeft = 0
number = 0
userName = ""

def guess_the_numberGame():

	global username
	global number
	global guessesLeft

	print("\r\nGuess The Number")
	guessesLeft = 8
	number = random.randint(1, 20)
	os.system('cls')
	print("\r\nGuess The Number")
	print(f"\r\nWell, {username}, I am thinking of a number between 1 and 20.")
	guessHandler()

def guessHandler():

	global username
	global number
	global guessesLeft

	if guessesLeft < 1:
		userInput = input(f"\r\nNope. my number was {number}.\nYou Lost.\nWould you like to play again? Yes or No.\n>>> ").lower()
		if userInput in yes_no:
			if userInput == "yes":
				os.system('cls')
				guess_the_numberGame()
			elif userInput == "no":
				os.system('cls')
				gamesModule()
		else:
			os.system('cls')
			print(f"\r\nYou entered neither yes nor no.\nTry again.")
			guessHandler()
	else:
		guess = input("\r\nTake a guess.\n>>> ")
		try:
			guess = int(guess)
		except ValueError:
			os.system('cls')
			print(f"\r\n{guess} is not a Number.\nTry again with a number.")
			guessHandler()
		if guess > 20 or guess < 1:
			os.system('cls')
			print(f"\r\n{guess} is not within the range of 1 to 20.\nTry again.")
			guessHandler()
		elif guess > number:
			if guess-number < 5:
				os.system('cls')
				guessesLeft -= 1
				print(f"\r\nVery close guess.\nYou now have {guessesLeft} guesses left.\nTry again.")
				guessHandler()
			elif guess-number < 8:
				os.system('cls')
				guessesLeft -= 1
				print(f"\r\nClose guess.\nYou now have {guessesLeft} guesses left.\nTry again.")
				guessHandler()
			else:
				os.system('cls')
				guessesLeft -= 1
				print(f"\r\nYour guess was too high.\nYou now have {guessesLeft} guesses left.\nTry again.")
				guessHandler()
		elif number > guess:
			if number-guess < 5:
				os.system('cls')
				guessesLeft -= 1
				print(f"\r\nVery close guess.\nYou now have {guessesLeft} guesses left.\nTry again.")
				guessHandler()
			elif number-guess < 8:
				os.system('cls')
				guessesLeft -= 1
				print(f"\r\nClose guess.\nYou now have {guessesLeft} guesses left.\nTry again.")
				guessHandler()
			else:
				os.system('cls')
				guessesLeft -= 1
				print(f"\r\nYour guess was too low.\nYou now have {guessesLeft} guesses left.\nTry again.")
				guessHandler()
		elif number == guess:
			guess_the_numberGameWin()

def guess_the_numberGameWin():
	global username
	userInput = input(f"\r\nGood job, {username}!\nYou guessed the number in {7-guessesLeft} guesses.\nPlay again? Yes or No\n>>> ").lower()
	if userInput in yes_no:
		if userInput == "yes":
			os.system('cls')
			guess_the_numberGame()
		elif userInput == "no":
			os.system('cls')
			gamesModule()
	else:
		os.system('cls')
		print(f"\r\nYou entered neither yes nor no.\nTry again.")
		guess_the_numberGameWin()

#---------------------------CALC MODULE

operandsList = ["+", "-", "/", "*", "**"]

def calcFunc(x, y, z):
	return {
	"+":x+y,
	"-":x-y,
	"/":x/y,
	"*":x*y,
	"**":x**y
	}.get(z)

def calcSub(x):
	if x == 1:
		output = input("\r\nEnter the first number.\n>>> ")
		try:
			int(output)
			os.system('cls')
			return int(output)
		except ValueError:
			os.system('cls')
			print(f"\r\n{output} is not a number.\nPlease try again.")
			return calcSub(1)
	elif x == 2:
		output = input("\r\nEnter the operand.\n+ or - or / or * or **\n>>> ")
		if output in operandsList:
			os.system('cls')
			return output
		else:
			os.system('cls')
			print(f"\r\n{output} is not an operand.\nTry again with + or - or / or * or **")
			return calcSub(2)
	elif x == 3:
		output = input("\r\nEnter the second number.\n>>> ")
		try:
			int(output)
			os.system('cls')
			return int(output)
		except ValueError:
			os.system('cls')
			print(f"\r\n{output} is not a number.\nPlease try again.")
			return calcSub(3)

def calcModule():
	os.system('cls')
	no1 = calcSub(1)
	operand = calcSub(2)
	no2 = calcSub(3)
	answer = calcFunc(no1, no2, operand)
	os.system('cls')
	print(f"\r\n{no1} {operand} {no2} = {answer}")
	main()

#---------------------------INITIALISATION/MAIN

def init():
	for i in range(1, 101):
		print(f"Starting PyrOS {i}% of 100%", end="\r")
		time.sleep(.015)
	print("PyrOS successfully started!")

def main():
	global username
	mainmsg = f"\r\nWelcome, {username}, to PyrOS!\nHere are the following modules you can use:\nSystem Modules:\n"
	for i in defaultList:
		mainmsg += f"- {i}\n"
	mainmsg += "Installed Modules:\n"
	for i in modulesList:
		mainmsg += f"- {i}\n"
	mainmsg += "What module would you like to use?\n>>> "
	module = input(mainmsg).lower()
	if module in modulesList or module in defaultList:
		if module == "install":
			os.system('cls')
			installModule()
		elif module == "calc":
			os.system('cls')
			calcModule()
		elif module == "uninstall":
			os.system('cls')
			uninstallModule()
		elif module == "shutdown":
			os.system('cls')
			shutdownModule()
		elif module == "restart":
			os.system('cls')
			restartModule()
		elif module == "logout":
			os.system('cls')
			print("\r\nSuccessfully logged out!")
			startup()
		elif module == "games":
			os.system('cls')
			gamesModule()
		elif module == "cipher":
			os.system('cls')
			cipherModule()
	else:
		os.system('cls')
		print(f"\r\n{module} is an unknown module.\nPlease try again.")
		main()

init()
startup()
