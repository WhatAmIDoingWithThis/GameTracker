from library.FileManager import load_games, save_games

class DataManager:

	# Private variables
	__nameFilter = ""
	__devFilter = ""
	__playFilter = ""
	__gameList = []

	# ------------------------- Public Functions -------------------------------------

	# Retrieve list of games from the FileManager library
	def __init__(self):
		self.__gameList = load_games()
	
	# Sort list by games matching filter and return matching games only
	def get_filtered_games(self):
		filteredList = []
		for game in self.__gameList:
			if self.__nameFilter and self.__nameFilter not in game["Name"].lower():
				continue
			if self.__playFilter and game.get("PlayStatus") != self.__playFilter:
				continue
			if self.__devFilter and game.get("DevState") != self.__devFilter:
				continue
			filteredList.append(game)
		return filteredList
	
	# Takes three strings and saves the filter status
	def apply_filters(self, name, dev, play):
		self.__nameFilter = name.lower()
		self.__devFilter = dev
		self.__playFilter = play
		return self.get_filtered_games()
	
	# Takes game details and returns an integer.
	# 0: Success 1: Name is empty 2: Name is not unique
	def add_new_game(self, game):
		name = game["Name"]
	
		# Verify name exists
		if not name.strip():
			return 1
		
		# Verify name is unique
		if self.__find_game(name) != -1:
			return 2
			
		# Add game to game list
		self.__gameList.append(game)
		self.__sort_list()
		save_games(self.__gameList)
		return 0
	
	# Takes name of game to delete and removes it
	def delete_game(self, name):
		if not name.strip():
			return False
		index = self.__find_game(name)
		if index == -1:
			return False
		self.__gameList.pop(index)
		save_games(self.__gameList)
		return True
		
	# Takes the new details of game and updates it
	# 0: Success 1: Name is empty 2: Name is not unique 3: Game does not exist
	def edit_game(self, oldName, newGame):
	
		newName = newGame["Name"]
	
		# Test name is not empty
		if not newName.strip():
			return 1
			
		# Test name is unique
		newIndex = self.__find_game(newName)
		oldIndex = self.__find_game(oldName)
		if newIndex != -1 and newIndex != oldIndex:
			return 2
		
		# Edit game details
		if oldIndex == -1:
			return 3
		self.__gameList[oldIndex] = newGame
		self.__sort_list()
		save_games(self.__gameList)
		return 0
		
	# Takes game name and returns game
	def get_game(self, name):
		index = self.__find_game(name)
		if index == -1:
			return None
		return self.__gameList[index]
	
	# ---------------------------- Private Functions ------------------------------------	
	
	# Sorts the list alphabetically
	def __sort_list(self):
		self.__gameList.sort(key = lambda game: game["Name"])
		
	# Takes name of game, returns index. -1 if no game has that name
	def __find_game(self, name):
		for index, game in enumerate(self.__gameList):
			if name.lower() == game["Name"].lower():
				return index
		return -1