#---------------------------IMPORT LIBRARIES

import sqlite3
import random
import time
import os
import sys
import string
import requests
import webbrowser
import json
import re
import pyperclip

#---------------------------CONSTANTS

invalidChars = set(string.punctuation.replace("_", ""))
defaultList = ["install", "uninstall", "restart", "shutdown", "logout"]
modulesList = []
installList = ["calc", "games", "cipher"]
TOTAL_MODULE_LIST = ["calc", "games", "cipher"]
yes_no = ["yes", "no"]
version = 0.1
latest = float(requests.get("https://raw.githubusercontent.com/NicholasJohansan/PyrOS/master/version.txt").content)

#---------------------------DB SETUP

dir_path = os.path.join(os.environ['APPDATA'], 'PyrOS') #Set DB in AppData/Roaming
if not os.path.exists(dir_path):
	os.makedirs(dir_path)
file_path = os.path.join(dir_path, 'PyrOS.db')

conn = sqlite3.connect(file_path)
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

try:
	c.execute("""CREATE TABLE system (
			is_logged integer,
			username text
			)""")
	c.execute("INSERT INTO system VALUES (0, ?)", ("",))
	conn.commit()
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
			tempTotalList = []
			for module in modulesList:
				tempTotalList.append(module)
			for module in installList:
				tempTotalList.append(module)
			for module in TOTAL_MODULE_LIST:
				if module not in tempTotalList:
					installList.append(module)
			c.execute("UPDATE credentials SET installList = ? WHERE username = ?", ('|'.join(installList), username))
			conn.commit()
			c.execute("UPDATE system SET is_logged = 1, username = ?", (username,))
			conn.commit()
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
		time.sleep(.001)
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

cipherList = ["caesar", "playfair", "country"]


def cipherModule():
	cipherMsg = "\r\nPyrOS Cipher Module\nHere are the available ciphers:\n"
	for i in cipherList:
		cipherMsg += f"- {i}\n"
	cipherMsg += "Which cipher would you like to use?\nType 'exit' if you would like to exit.\n>>> "
	cipher = input(cipherMsg).lower()
	if cipher in cipherList:
		if cipher == "caesar":
			os.system('cls')
			caesar_cipherModule()
		elif cipher == "playfair":
			os.system('cls')
			playfair_cipherModule()
		elif cipher == "country":
			os.system('cls')
			country_cipherModule()
	elif cipher == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Cipher Module...")
		main()
	else:
		os.system('cls')
		print(f"\r\n{cipher} is not an available cipher.\nPlease try again.")
		cipherModule()

#---------------------------COUNTRY CIPHER
COUNTRY_CIPHER_DICT = json.loads(requests.get("https://raw.githubusercontent.com/NicholasJohansan/PyrOS/master/json/country_dict.json").content.decode())['3166-1']
COUNTRY_LIST = ['Aruba', 'Afghanistan', 'Angola', 'Anguilla', 'Albania', 'Andorra', 'United Arab Emirates', 'Argentina', 'Armenia', 'American Samoa', 'Antarctica', 'French Southern Territories', 'Antigua and Barbuda', 'Australia', 'Austria', 'Azerbaijan', 'Burundi', 'Belgium', 'Benin', 'Bonaire, Sint Eustatius and Saba', 'Burkina Faso', 'Bangladesh', 'Bulgaria', 'Bahrain', 'Bahamas', 'Bosnia and Herzegovina', 'Saint BarthÃ©lemy', 'Belarus', 'Belize', 'Bermuda', 'Bolivia, Plurinational State of', 'Brazil', 'Barbados', 'Brunei Darussalam', 'Bhutan', 'Bouvet Island', 'Botswana', 'Central African Republic', 'Canada', 'Cocos (Keeling) Islands', 'Switzerland', 'Chile', 'China', "CÃ´te d'Ivoire", 'Cameroon', 'Congo, The Democratic Republic of the', 'Congo', 'Cook Islands', 'Colombia', 'Comoros', 'Cabo Verde', 'Costa Rica', 'Cuba', 'CuraÃ§ao', 'Christmas Island', 'Cayman Islands', 'Cyprus', 'Czechia', 'Germany', 'Djibouti', 'Dominica', 'Denmark', 'Dominican Republic', 'Algeria', 'Ecuador', 'Egypt', 'Eritrea', 'Western Sahara', 'Spain', 'Estonia', 'Ethiopia', 'Finland', 'Fiji', 'Falkland Islands (Malvinas)', 'France', 'Faroe Islands', 'Micronesia, Federated States of', 'Gabon', 'United Kingdom', 'Georgia', 'Guernsey', 'Ghana', 'Gibraltar', 'Guinea', 'Guadeloupe', 'Gambia', 'Guinea-Bissau', 'Equatorial Guinea', 'Greece', 'Grenada', 'Greenland', 'Guatemala', 'French Guiana', 'Guam', 'Guyana', 'Hong Kong', 'Heard Island and McDonald Islands', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'Isle of Man', 'India', 'British Indian Ocean Territory', 'Ireland', 'Iran, Islamic Republic of', 'Iraq', 'Iceland', 'Israel', 'Italy', 'Jamaica', 'Jersey', 'Jordan', 'Japan', 'Kazakhstan', 'Kenya', 'Kyrgyzstan', 'Cambodia', 'Kiribati', 'Saint Kitts and Nevis', 'Korea, Republic of', 'Kuwait', "Lao People's Democratic Republic", 'Lebanon', 'Liberia', 'Libya', 'Saint Lucia', 'Liechtenstein', 'Sri Lanka', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Macao', 'Saint Martin (French part)', 'Morocco', 'Monaco', 'Moldova, Republic of', 'Madagascar', 'Maldives', 'Mexico', 'Marshall Islands', 'North Macedonia', 'Mali', 'Malta', 'Myanmar', 'Montenegro', 'Mongolia', 'Northern Mariana Islands', 'Mozambique', 'Mauritania', 'Montserrat', 'Martinique', 'Mauritius', 'Malawi', 'Malaysia', 'Mayotte', 'Namibia', 'New Caledonia', 'Niger', 'Norfolk Island', 'Nigeria', 'Nicaragua', 'Niue', 'Netherlands', 'Norway', 'Nepal', 'Nauru', 'New Zealand', 'Oman', 'Pakistan', 'Panama', 'Pitcairn', 'Peru', 'Philippines', 'Palau', 'Papua New Guinea', 'Poland', 'Puerto Rico', "Korea, Democratic People's Republic of", 'Portugal', 'Paraguay', 'Palestine, State of', 'French Polynesia', 'Qatar', 'RÃ©union', 'Romania', 'Russian Federation', 'Rwanda', 'Saudi Arabia', 'Sudan', 'Senegal', 'Singapore', 'South Georgia and the South Sandwich Islands', 'Saint Helena, Ascension and Tristan da Cunha', 'Svalbard and Jan Mayen', 'Solomon Islands', 'Sierra Leone', 'El Salvador', 'San Marino', 'Somalia', 'Saint Pierre and Miquelon', 'Serbia', 'South Sudan', 'Sao Tome and Principe', 'Suriname', 'Slovakia', 'Slovenia', 'Sweden', 'Eswatini', 'Sint Maarten (Dutch part)', 'Seychelles', 'Syrian Arab Republic', 'Turks and Caicos Islands', 'Chad', 'Togo', 'Thailand', 'Tajikistan', 'Tokelau', 'Turkmenistan', 'Timor-Leste', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Tuvalu', 'Taiwan, Province of China', 'Tanzania, United Republic of', 'Uganda', 'Ukraine', 'United States Minor Outlying Islands', 'Uruguay', 'United States', 'Uzbekistan', 'Holy See (Vatican City State)', 'Saint Vincent and the Grenadines', 'Venezuela, Bolivarian Republic of', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Viet Nam', 'Vanuatu', 'Wallis and Futuna', 'Samoa', 'Yemen', 'South Africa', 'Zambia', 'Zimbabwe']

def country_cipherModule():
	response = input("\r\nPyrOS Country Cipher\nWould you like to \"encrypt\" or \"decrypt\"?\nType \"exit\" to exit.\n>>> ").lower()
	if response in ["encrypt", "decrypt"]:
		os.system('cls')
		country_mainCipher(response)
	elif response == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Country Cipher...")
		cipherModule()
	else:
		os.system('cls')
		print(f"\r\n{response} is not an available option. \nPlease try again.")
		country_cipherModule()

def country_flag(code):
	OFFSET = ord('🇦') - ord('A')
	return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

def country_deflag(code):
	OFFSET = ord('A') - ord('🇦')
	return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

def country_findCountries(alphabet):
	alphabet = alphabet.upper()
	available_countries = []
	for country in COUNTRY_LIST:
		if country[0] == alphabet:
			available_countries.append(country)
	if len(available_countries) == 0:
		available_countries.append("None")
	return available_countries

def country_compile(text, c_type):
	compiled_text = ""
	for character in text:
		if not character.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			if character == " ":
				if c_type == "discord":
					compiled_text += "     "
				else:
					compiled_text += "   "
			else:
				compiled_text += character
		else:
			countries = country_findCountries(character)
			alpha_2 = ""
			if "None" in countries:
				compiled_text += f"[{character}]"
			else:
				country = random.choice(countries)
				for country_data in COUNTRY_CIPHER_DICT:
					if country_data["name"] == country:
						alpha_2 = country_data["alpha_2"]
						break
				if c_type == "discord":
					compiled_text += f":flag_{alpha_2.lower()}: "
				elif c_type == "whatsapp":
					compiled_text += f"{country_flag(alpha_2)}"
	return compiled_text

def country_decompile(text, c_type):
	decompiled_text = ""
	if c_type == "whatsapp":
		first = ""
		for character in text:
			if not character.upper() in "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿":
				first = ""
				decompiled_text += character
			else:
				if first == "":
					first = character
				else:
					alpha_2 = country_deflag(f"{first}{character}")
					for country_data in COUNTRY_CIPHER_DICT:
						if country_data['alpha_2'] == alpha_2:
							decompiled_text += (country_data['name'])[0].lower()
							break
					first = ""
		return decompiled_text
	elif c_type == "discord":
		decompiled_text = ""
		for word in text.split("     "):
			for flag_emoji in re.findall(":flag_[a-zA-Z][a-zA-Z]:", word):
				alpha_2 = flag_emoji[6:8].upper()
				for country_data in COUNTRY_CIPHER_DICT:
					if country_data['alpha_2'] == alpha_2:
						decompiled_text += (country_data['name'])[0].lower()
						break
			decompiled_text += " "
		return decompiled_text

def country_getType(mode):
	q = "Where did you get this message?"
	if mode == "encrypt":
		q = "Where do you want to send this message?"
	c_type = input(f"\r\n{q}\n\"WhatsApp\" or \"Discord\"?\n>>> ").lower()
	if c_type not in ["whatsapp", "discord"]:
		os.system('cls')
		print("You entered neither whatsapp nor discord.\nTry again!")
		return country_getType(mode)
	return c_type

def country_mainCipher(mode):
	message = input(f"\r\nEnter your message to {mode}.\nNote that only letters will be {mode}ed, the rest will be left in without any changes.\n>>> ")
	cipher_type = country_getType(mode)
	text = ""
	if mode == "encrypt":
		text = country_compile(message, cipher_type)
	else:
		text = country_decompile(message, cipher_type)
	pyperclip.copy(text)
	os.system('cls')
	print(f"\r\nYour {mode}ed message is:\n{text}.\nIt has been copied to your clipboard.")
	country_cipherModule()



#---------------------------PLAYFAIR CIPHER
def playfair_cipherModule():
	response = input("\r\nPyrOS Playfair Cipher\nWould you like to \"encrypt\" or \"decrypt\"?\nType \"exit\" to exit.\n>>> ").lower()
	if response in ["encrypt", "decrypt"]:
		os.system('cls')
		playfair_mainCipher(response)
	elif response == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Playfair Cipher...")
		cipherModule()
	else:
		os.system('cls')
		print(f"\r\n{response} is not an available option. \nPlease try again.")
		playfair_cipherModule()

def playfair_testExistence(char, table):
	for row in table:
		if char in row:
			return True
	return False

def playfair_genTable(key):
	key = (key.upper()).replace("J", "I")
	alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
	table = [
		[],
		[],
		[],
		[],
		[]
	]

	row = 0
	for char in key.upper():
		if not playfair_testExistence(char, table) and char in alphabet:
			if len(table[row]) == 5:
				row += 1
			table[row].append(char)

	for char in alphabet:
		if not playfair_testExistence(char, table):
			if len(table[row]) == 5:
				row += 1
			table[row].append(char)

	return table

def playfair_findChar(char, table):
	for row in table:
		if char in row:
			return table.index(row), row.index(char)

def playfair_boundaryHandler(point):
	#for encoding
	if point == 4:
		return 0
	return point+1

def playfair_boundaryHandler2(point):
	#for decoding
	if point == 0:
		return 4
	return point-1

def playfair_encodePair(a, b, table):
	if a == b:
		print("error")

	a_row, a_col = playfair_findChar(a, table)
	b_row, b_col = playfair_findChar(b, table)

	#print(f"{a}(row: {a_row}, column: {a_col}), {b}(row: {b_row}, column: {b_col})")
	
	if a_col == b_col:
		return(f"{table[playfair_boundaryHandler(a_row)][a_col]}{table[playfair_boundaryHandler(b_row)][b_col]}")
	elif a_row == b_row:
		return(f"{table[a_row][playfair_boundaryHandler(a_col)]}{table[b_row][playfair_boundaryHandler(b_col)]}")
	else:
		return(f"{table[a_row][b_col]}{table[b_row][a_col]}")

def playfair_decodePair(a, b, table):
	if a == b:
		print("error")

	a_row, a_col = playfair_findChar(a, table)
	b_row, b_col = playfair_findChar(b, table)

	if a_col == b_col:
		return(f"{table[playfair_boundaryHandler2(a_row)][a_col]}{table[playfair_boundaryHandler2(b_row)][b_col]}")
	elif a_row == b_row:
		return(f"{table[a_row][playfair_boundaryHandler2(a_col)]}{table[b_row][playfair_boundaryHandler2(b_col)]}")
	else:
		return(f"{table[a_row][b_col]}{table[b_row][a_col]}")

def playfair_format(text):
	cleaned = ""
	for char in text.upper():
		if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			if char == "J":
				char = "I"
			cleaned += char
	if len(cleaned)%2 == 1 or cleaned[len(cleaned)-1] == cleaned[len(cleaned)-2]:
		cleaned += "Z"
	first = ""
	pairs = []
	for char in cleaned:
		if first == "":
			first = char
		elif first:
			if first == char:
				pairs.append(f"{first}X")
				first = char
			else:
				pairs.append(f"{first}{char}")
				first = ""
	return pairs

def playfair_decodeFormat(text):
	cleaned = ""
	for char in text.upper():
		if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			cleaned += char
	first = ""
	pairs = []
	for char in cleaned:
		if first == "":
			first = char
		elif first:
			pairs.append(f"{first}{char}")
			first = ""
	return pairs

def playfair_getKey():
	key = input("Enter the key (Any word/sentence)\nNote that the key should only include letters, no numbers.\n>>> ")
	if key.replace(" ", "").isalpha():
		return key
	os.system('cls')
	print(f"{key} isn't completely made out of alphabets, please remove any numerals/symbol and try again.")
	return playfair_getKey()

def playfair_mainCipher(mode):
	compiled = ""
	precompiled = ""
	message = input(f"\r\nEnter your message to {mode}.\nNote that any characters other than alphabets will be ignored.\n>>> ")
	key = playfair_getKey()
	table = playfair_genTable(key)
	pairs = list()
	if mode == "encrypt":
		pairs = playfair_format(message)
		for char1, char2 in pairs:
			compiled += playfair_encodePair(char1, char2, table)
	else:
		pairs = playfair_decodeFormat(message)
		for char1, char2 in pairs:
			precompiled += playfair_decodePair(char1, char2, table)
		for char in precompiled:
			if char != "X" and char != "Z":
				compiled += char
	pyperclip.copy(compiled)
	os.system('cls')
	print(f"\r\nYour {mode}ed message is:\n{compiled}.\nIt has been copied to your clipboard.")
	playfair_cipherModule()

#---------------------------CAESAR CIPHER
CAESAR_MAX_KEY_SIZE = 26

def caesar_cipherModule():
	response = input("\r\nPyrOS Caesar Cipher\nWould you like to \"encrypt\" or \"decrypt\"?\nType \"exit\" to exit.\n>>> ").lower()
	if response in ["encrypt", "decrypt"]:
		os.system('cls')
		caesar_mainCipher(response)
	elif response == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Caesar Cipher...")
		cipherModule()
	else:
		os.system('cls')
		print(f"\r\n{response} is not an available option.\nPlease try again.")
		caesar_cipherModule()

def caesar_getCipherMessage():
	return input("\r\nEnter your message.\n>>> ")

def caesar_getCipherKey():
	keyCipher = input(f"Enter the key number (1-{CAESAR_MAX_KEY_SIZE}).\n>>> ")
	try:
		keyCipher = int(keyCipher)
	except ValueError:
		os.system('cls')
		print(f"{keyCipher} isn't a number, try again.")
		return caesar_getCipherKey()
	if not (keyCipher >= 1 and keyCipher <= CAESAR_MAX_KEY_SIZE):
		os.system('cls')
		print(f"{keyCipher} is not within 1 and {CAESAR_MAX_KEY_SIZE}, try again.")
		return caesar_getCipherKey()
	return keyCipher

def caesar_mainCipher(mode):
	message = caesar_getCipherMessage()
	key = caesar_getCipherKey()
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

	pyperclip.copy(translated)
	os.system('cls')
	print(f"\r\nYour {mode}ed message is {translated}.\nIt has been copied to your clipboard.")
	caesar_cipherModule()

#---------------------------GAMES MODULE

gamesList =["guess_the_number", "hangman", "robot_warfare"]

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
		if game == "robot_warfare":
			os.system('cls')
			robot_warfareGame()
	elif game == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Game Module...")
		main()
	else:
		os.system('cls')
		print(f"\r\n{game} is not an available game.\nPlease try again.")
		gamesModule()

#---------------------------ROBOT WARFARE GAME
robotWarfare_running = False

class Robot():

	def __init__(self, team, x, y, direction, hp):
		self.team = team
		self.x = x
		self.y = y
		self.direction = direction
		self.hp = hp

	def get_team(self):
		return self.team
	def get_health(self):
		return self.hp
	def get_direction(self):
		return self.direction

	def left90(self, direction):
		return {
			"N":"W",
			"W":"S",
			"S":"E",
			"E":"N"
		}.get(direction)

	def right90(self, direction):
		return {
			'N':"E",
			"E":"S",
			"S":"W",
			"W":"N"
		}.get(direction)

	def healthchange(self, world, hp):
		self.hp += hp
		if self.hp < 0: world.kill_robot(self.x, self.y)
		if self.hp > 50: self.hp = 50

	def get_next_pos(self, direction):
		return {
			"N":(self.x, self.y+1),
			"S":(self.x, self.y-1),
			"E":(self.x+1, self.y),
			"W":(self.x-1, self.y)
		}.get(direction)

	def forward(self, world):
		x, y = self.get_next_pos(self.direction)
		if (x > -1 and x < world.row) and (y > -1 and y < world.row):
			if world.test_pos(x, y):
				return False
			world.move_robot(self.x, self.y, x, y)
			self.x = x
			self.y = y
			return True
		else:
			self.direction = self.left90(self.direction)
			self.direction = self.left90(self.direction)
			return True

class AttackRobot(Robot):

	def __init__(self, team, x, y, direction, hp):
		Robot.__init__(self, team, x, y, direction, hp)

	def test_enemy(self, world, x, y):
		if world.test_pos(x, y).team == self.team:
			return False
		else:
			return True

	def run_turn(self, world):
		#check forward
		x, y = Robot.get_next_pos(self, self.direction)
		if (x > -1 and x < world.row) and (y > -1 and y < world.row):
			if world.test_pos(x, y):
				if self.test_enemy(world, x, y):
					world.test_pos(x, y).healthchange(world, -random.randint(1,6))
					return
		#check right
		x, y = Robot.get_next_pos(self, Robot.right90(self, self.direction))
		if (x > -1 and x < world.row) and (y > -1 and y < world.row):
			if world.test_pos(x, y):
				if self.test_enemy(world, x, y):
					self.direction = Robot.right90(self, self.direction)
					return
		#check left
		x, y = Robot.get_next_pos(self, Robot.left90(self, self.direction))
		if (x > -1 and x < world.row) and (y > -1 and y < world.row):
			if world.test_pos(x, y):
				if self.test_enemy(world, x, y):
					self.direction = Robot.left90(self, self.direction)
					return
		#random move
		randmove = random.choice(["F", "F", "L", "R"])
		if randmove == "F":
			Robot.forward(self, world)
		elif randmove == "L":
			self.direction = Robot.left90(self, self.direction)
		else:
			self.direction = Robot.right90(self, self.direction)
		return

class World():

	def __init__(self, size):
		self.row = size
		self.col = self.row
		self.board = []
		for row in range(self.row):
			self.board.append([])
			for col in range(self.col):
				self.board[row].append(None)

	def kill_robot(self, x, y):
		col, row = x, self.row-1-y
		self.board[row][col] = None

	def test_pos(self, x, y):
		col, row = x, self.row-1-y
		if self.board[row][col]: return self.board[row][col] 
		return None

	def add_attack_robot(self, team, x, y, direction):
		col, row = x, self.row-1-y
		self.board[row][col] = AttackRobot(team, x, y, direction, 50) #50 HP

	def add_medic_robot(self, team, x, y, direction):
		col, row = x, self.row-1-y
		self.board[row][col] = MedicRobot(team, x, y, direction, 50) #50 HP

	def move_robot(self, oldx, oldy, newx, newy):
		oldcol, oldrow, newcol, newrow = oldx, self.row-1-oldy, newx, self.row-1-newy
		self.board[oldrow][oldcol], self.board[newrow][newcol] = None, self.board[oldrow][oldcol]

	def run_turn(self):
		for row in range(self.row):
			for col in range(self.col):
				if self.board[row][col]:
					self.board[row][col].run_turn(self)

	def game_over(self):
		team1 = 0
		team2 = 0
		winner = None
		for row in range(self.row):
			for col in range(self.col):
				if self.board[row][col]:
					if self.board[row][col].team == 1:
						team1 += 1
					elif self.board[row][col].team == 2:
						team2 += 1
		if team1 == 0:
			winner = 2
		elif team2 == 0:
			winner = 1
		return winner

	def team_count(self):
		team1 = 0
		team2 = 0
		for row in range(self.row):
			for col in range(self.col):
				if self.board[row][col]:
					if self.board[row][col].team == 1:
						team1 += 1
					elif self.board[row][col].team == 2:
						team2 += 1
		return team1, team2

def rw_print_world(world):
	print("-" * 60)
	print("Robot Legend - [A50N, a50E]\nIf the first letter is capital, it is Team1, else, it is Team2!\nThe middle 2 digits are the health! Robots start with 50 HP!\nThe last letter stands for its direction! N - North, E - East, S - South, W - West!")
	print("-" * 60)
	for y in range(world.row-1, -1, -1):
		line = ""
		for x in range(0, world.row):
			r = world.test_pos(x, y)
			if not r:
				line += ".... "
			else:
				if isinstance(r, AttackRobot):
					rtype = "A"
				else:
					rtype = "!"
				if r.get_team() == 1:
					line += "%s%02i%s " % (rtype, r.get_health(), r.get_direction())
				else:
					line += "%s%02i%s " % (rtype.lower(), r.get_health(), r.get_direction())
		print(line)
	print("-" * 60)
	team1, team2 = world.team_count()
	print(f"{team1} Team 1 Robots left\n{team2} Team 2 Robots left")
	print("-" * 60)
	print("Press [Enter] to Continue")

def rw_response_handler(thing):
	if thing == "size":
		res = input("What size would you like the world to be?\nThe world will be the [number] you entered will be received in [number]x[number] size.\nFor e.g. if 5 is entered, the world is 5x5!\nThe recommended size is 15.\nEnter your number\n>> ")
		try:
			res = int(res)
			return res
		except ValueError:
			os.system('cls')
			print("You didn't enter a number! Try again!")
			return rw_response_handler('size')
	elif thing == "team1":
		res = input("How many robots do you want in Team 1?\nEnter the amount of robots in Team 1!\n>> ")
		try:
			res = int(res)
			return res
		except ValueError:
			os.system('cls')
			print("You didn't enter a number! Try again!")
			return rw_response_handler('team1')
	elif thing == "team2":
		res = input("How many robots do you want in Team 2?\nEnter the amount of robots in Team 2!\n>> ")
		try:
			res = int(res)
			return res
		except ValueError:
			os.system('cls')
			print("You didn't enter a number! Try again!")
			return rw_response_handler('team2')

def rw_addRobot(team, world, occupied):
	x = random.randrange(0, world.row)
	y = random.randrange(0, world.row)
	direction = random.choice(["N","E","S","W"])
	if (x, y) in occupied:
		rw_addRobot(team, world, occupied)
		return
	world.add_attack_robot(team, x, y, direction)
	occupied.append((x, y))
	return

def rw_runGame(world):
	global robotWarfare_running
	while robotWarfare_running:
		input()
		os.system('cls')
		rw_print_world(world)
		world.run_turn()
		if world.game_over():
			os.system('cls')
			print(f"Team {world.game_over()} won!\nGame Ended!\n")
			robotWarfare_running = False
			robot_warfareGame()

def run_robot_warfareGame():
	global robotWarfare_running
	input("Welcome to\nTotally Inaccurate Robot Warfare Simulator [TIRWS]\nPress Enter to Play!\n")
	size = rw_response_handler("size")
	os.system('cls')
	team1no = rw_response_handler('team1')
	os.system('cls')
	team2no = rw_response_handler('team2')
	os.system('cls')
	print("Setting Up World...")
	world = World(size)
	occupied = []
	full = False
	for i in range(team1no):
		if len(occupied) == (world.row)**2:
			full = True
			break
		rw_addRobot(1, world, occupied)
	for i in range(team2no):
		if len(occupied) == (world.row)**2:
			full = True
			break
		rw_addRobot(2, world, occupied)
	if full:
		print("The game have done setting up, but\nThere are more robots than space available!\nContinue at your own risk!\nEnter to continue or close the program to restart!\n")
	else:
		print("The game have done setting up!\nPress Enter when you are ready!\n")
	robotWarfare_running = True
	rw_runGame(world)

def robot_warfareGame():
	response = input("\r\nPyrOS Country Cipher\nType \"play\" to play or type \"exit\" to exit.\n>>> ").lower()
	if response == "play":
		os.system('cls')
		run_robot_warfareGame()
	elif response == "exit":
		os.system('cls')
		print("\r\nExiting PyrOS Robot Warfare...")
		gamesModule()
	else:
		os.system('cls')
		print(f"\r\n{response} is not an available option. \nPlease try again.")
		robot_warfareGame()


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
	userInput = input(f"\r\nGood job, {username}!\nYou guessed the number in {8-guessesLeft} guesses.\nPlay again? Yes or No\n>>> ").lower()
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
		time.sleep(.005)
	print("PyrOS successfully started!")

def main():
	global username
	global modulesList
	global installList
	global latest
	global version
	try:
		str(username)
	except Exception as e:
		c.execute("SELECT * FROM system")
		result = c.fetchall()
		username = result[0][1]
		c.execute("SELECT * FROM credentials WHERE username = ?", (username,))
		result = c.fetchall()
		modulesList = result[0][2].split('|')
		installList = result[0][3].split('|')
		if modulesList == ['']:
			modulesList = []
		if installList == ['']:
			installList = []
		tempTotalList = []
		for module in modulesList:
			tempTotalList.append(module)
		for module in installList:
			tempTotalList.append(module)
		for module in TOTAL_MODULE_LIST:
			if module not in tempTotalList:
				installList.append(module)
	needUpdate = False
	latest = float(requests.get("https://raw.githubusercontent.com/NicholasJohansan/PyrOS/master/version.txt").content)
	mainmsg = f"\r\nWelcome, {username}, to PyrOS v{version}, "
	if latest == version:
		mainmsg += f"you are up to date"
	elif latest > version:
		needUpdate = True
		mainmsg += f"v{latest} is out!\nTo update, type \"update\" instead of the module name"
	else:
		mainmsg += f"you are on a developmental version"
	mainmsg += f"!\n\nHere are the following modules you can use:\nSystem Modules:\n"
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
			c.execute("UPDATE system SET is_logged = 0, username = ?", ("",))
			conn.commit()
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
		if module == "update":
			if needUpdate:
				webbrowser.open_new(f"https://github.com/NicholasJohansan/PyrOS/releases/download/v{latest}/PyrOS.exe")
			else:
				os.system('cls')
				print(f"\r\nYou are up to date!\nYou do not need to update.")
				main()
		else:
			os.system('cls')
			print(f"\r\n{module} is an unknown module.\nPlease try again.")
			main()

init()
c.execute("SELECT * FROM system")
result = c.fetchall()
if bool(result[0][0]):
	main()
else:
	startup()
