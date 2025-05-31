import json
import os

DATA_FILE = "./data/games.json"

# Function to read games from JSON file and return as a list
def load_games():

	# Check JSON file exists and is not empty
	if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
		# Create folder and file
		os.makedirs(os.path.dirname(DATA_FILE), exist_ok = True)
		return []
	
	# Open file
	with open(DATA_FILE, "r") as file:
		try:
			return json.load(file)
		except json.JSONDecodeError as error:
			print("CAUGHT ERROR: JSON Decode Error")
			print(f"Error details: {error}")
			return []
			
# Function takes data ands saves it to DATA_FILE
def save_games(games):

	# Ensure directory exists
	os.makedirs(os.path.dirname(DATA_FILE), exist_ok = True)
	
	# Save games
	with open(DATA_FILE, "w") as f:
		json.dump(games, f, indent = 4)