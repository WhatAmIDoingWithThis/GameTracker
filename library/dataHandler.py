import json
import os

DATA_FILE = "./data/games.json"

def loadGames():
	if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
		return []
	with open(DATA_FILE, "r") as f:
		try:
			return json.load(f)
		except json.JSONDecodeError:
			print("SOFT ERROR: JSON Decode Error")
			return []
		
def saveGames(games):
	with open(DATA_FILE, "w") as f:
		json.dump(games, f, indent=4)
		
def addGame(game):
	games = loadGames()
	games.append(game)
	saveGames(games)
	
def editGame(index, new_game):
	games = loadGames()
	if 0 <= index < len(games):
		games[index] = new_game
		saveGames(games)
		
def deleteGame(index):
	games = loadGames()
	if 0 <= index < len(games):
		games.pop(index)
		saveGames(games)