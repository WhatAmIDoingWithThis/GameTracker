import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from library.dataHandler import loadGames, addGame

class GameTracker:
	
	# On initialization function
	def __init__(self, root):
		self.root = root
		self.root.title("Game Tracker")
		
		# Filters
		filterFrame = tk.Frame(root)
		filterFrame.pack(padx = 5, pady = 5, fill = "x")
		
		tk.Label(filterFrame, text="Name:").pack(side="left")
		self.nameFilter = tk.Entry(filterFrame, width=15)
		self.nameFilter.pack(side="left", padx=2)
		
		tk.Label(filterFrame, text="Play Status:").pack(side="left")
		self.playFilter = ttk.Combobox(filterFrame, values=["", "To Play", "Completed", "Dropped"], state="readonly")
		self.playFilter.pack(side="left", padx = 2)
		
		tk.Label(filterFrame, text="Dev Status:").pack(side="left")
		self.devFilter = ttk.Combobox(filterFrame, values=["", "Active Development", "Completed", "Abandoned"], state="readonly")
		self.devFilter.pack(side="left", padx = 2)
		
		tk.Button(filterFrame, text="Apply Filter", command = self.LoadGameList).pack(side="left", padx=5)
		tk.Button(filterFrame, text = "Clear", command = self.clearFilters).pack(side="left", padx=5)
		
		# Create viewable list of games
		self.tree = ttk.Treeview(root, columns = ("Name", "Play Status", "Development Status"), show = "headings")
		self.tree.heading("Name", text = "Name")
		self.tree.heading("Play Status", text = "Play Status")
		self.tree.heading("Development Status", text = "Development Status")
		self.tree.pack(fill = tk.BOTH, expand = True)
		self.tree.bind("<Double-1>", self.viewGameDetails)
		
		# Add Game Button
		addBtn = tk.Button(root, text = "Add Game", command = self.AddGameWindow)
		addBtn.pack(pady = 5)
		
		# Load list of games
		self.LoadGameList()
		
	# Function to load games from JSON
	def LoadGameList(self):
		# Clear current list of games
		self.tree.delete(*self.tree.get_children())
		games = loadGames()
		
		# Apply Filters
		nameKeyword = self.nameFilter.get().lower()
		playStatus = self.playFilter.get()
		devStatus = self.devFilter.get()
			
		# Get games with filters
		self.currentGames = []
		for i, game in enumerate(games):
			if nameKeyword and nameKeyword not in game["Name"].lower():
				continue
			if playStatus and game.get("PlayStatus") != playStatus:
				continue
			if devStatus and game.get("DevState") != devStatus:
				continue
			self.currentGames.append((i, game))
			self.tree.insert("", tk.END, values=(game["Name"], game["PlayStatus"], game["DevState"]))
	
	# Function to open a window to add games
	def AddGameWindow(self):
		addWindow = tk.Toplevel(self.root)
		addWindow.title("Add Game")
		
		numRow = 0;
		
		# Data Entries
		labels = ["Name", "Download Link", "Latest Version", "Notes"];
		entries = {}
		for label in labels:
			tk.Label(addWindow, text=label).grid(row = numRow, column = 0, sticky = "e")
			entry = tk.Entry(addWindow, width = 40)
			entry.grid(row = numRow, column = 1, padx = 5, pady = 2)
			entries[label] = entry
			numRow += 1
			
		# Development status combobox
		tk.Label(addWindow, text = "Dev Status").grid(row = numRow, column = 0, sticky = "e")
		devCombo = ttk.Combobox(addWindow, state = "readonly", values = ["Active Development", "Completed", "Abandoned"])
		devCombo.grid(row = numRow, column = 1, padx = 5, pady = 2)
		numRow += 1
		
		# Play status combobox
		tk.Label(addWindow, text = "Play Status").grid(row = numRow, column = 0, sticky = "e")
		playCombo = ttk.Combobox(addWindow, state = "readonly", values = ["To Play", "Completed", "Dropped"])
		playCombo.grid(row = numRow, column = 1, padx = 5, pady = 2)
		numRow += 1
			
		# Reccomendation check box
		recVar = tk.BooleanVar()
		tk.Checkbutton(addWindow, text = "Recommend", variable = recVar).grid(row = numRow, column = 1, sticky = "w")
		numRow += 1
		
		def submit():
			game = {
				"Name": entries["Name"].get(),
				"Link": entries["Download Link"].get(),
				"Latest Version": entries["Latest Version"].get(),
				"DevState": devCombo.get(),
				"PlayStatus": playCombo.get(),
				"Notes": entries["Notes"].get(),
				"Recommend": recVar.get()
			}
			if not game["Name"]:
				messagebox.showwarning("Missing Info", "Game must have a name.")
				return
			addGame(game)
			self.LoadGameList()
			addWindow.destroy()
			
		tk.Button(addWindow, text="Save", command = submit).grid(row = numRow, column = 1, pady = 5)
			
	def viewGameDetails(self, event):
		selected = self.tree.focus()
		if not selected:
			return
			
		index = self.tree.index(selected)
		realIndex, game = self.currentGames[index]
		
		detailWin = tk.Toplevel(self.root)
		detailWin.title(f"Details for {game['Name']}")
		
		row = 0
		for key, value in game.items():
			tk.Label(detailWin, text = f"{key}:").grid(row = row, column = 0, sticky = "e", padx = 5, pady = 2)
			tk.Label(detailWin, text = str(value)).grid(row = row, column = 1, sticky = "w", padx = 5, pady = 2)
			row += 1
			
		tk.Button(detailWin, text="Edit", command=lambda: [detailWin.destroy(), self.editGameWindow(realIndex, game)]).grid(row = row, column = 0, pady = 10)
		tk.Button(detailWin, text="Delete", command = lambda: self.deleteGame(index, detailWin)).grid(row = row, column = 1, pady = 10)
		
	def editGameWindow(self, index, game):
		editWin = tk.Toplevel(self.root)
		editWin.title(f"Edit Game: {game['Name']}")
		
		fields = ["Name", "Link", "Latest Version", "Notes"]
		entries = {}
		row = 0
		for field in fields:
			tk.Label(editWin, text = field).grid(row = row, column = 0, sticky = "e")
			entry = tk.Entry(editWin, width = 40)
			entry.insert(0, game.get(field, ""))
			entry.grid(row = row, column = 1, padx = 5, pady = 2)
			entries[field] = entry
			row += 1
			
		# Dev Status
		tk.Label(editWin, text="Dev Status").grid(row = row, column = 0, sticky = "e")
		devCombo = ttk.Combobox(editWin, values = ["Active Development", "Completed", "Abandoned"], state = "readonly")
		devCombo.set(game["DevState"])
		devCombo.grid(row=row, column=1)
		row += 1
		
		# Play Status
		tk.Label(editWin, text = "Play Status").grid(row = row, column = 0, sticky = "e")
		playCombo = ttk.Combobox(editWin, values = ["To Play", "Completed", "Dropped"], state="readonly")
		playCombo.set(game["PlayStatus"])
		playCombo.grid(row=row, column = 1)
		row += 1
		
		recVar = tk.BooleanVar(value=game["Recommend"])
		tk.Checkbutton(editWin, text="Recommend", variable=recVar).grid(row=row, column=1, sticky="w")
		row+=1
			
		def saveEdits():
			updated_game= {
				"Name": entries["Name"].get(),
				"Link": entries["Link"].get(),
				"Latest Version": entries["Latest Version"].get(),
				"DevState": devCombo.get(),
				"PlayStatus": playCombo.get(),
				"Notes": entries["Notes"].get(),
				"Recommend": recVar.get()
			}
			from library.dataHandler import editGame
			editGame(index, updated_game)
			self.LoadGameList()
			editWin.destroy()
			
		tk.Button(editWin, text = "Save", command = saveEdits).grid(row=row, column = 1, pady = 10)
				
		def deleteGame(self, index, window=None):
			from library.dataHandler import deleteGame
			if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this game?"):
				deleteGame(index)
				self.LoadGameList()
				if window:
					window.destroy()
					
	def clearFilters(self):
		self.nameFilter.delete(0, tk.END)
		self.playFilter.set("")
		self.devFilter.set("")
		self.LoadGameList()
		
# Create the main window
root = tk.Tk()
app = GameTracker(root)
root.mainloop()