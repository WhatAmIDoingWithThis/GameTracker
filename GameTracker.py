import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox

from library.DataManager import DataManager

MIN_HEIGHT = 100
MIN_WIDTH = 300

PLAY_STATUS_OPTIONS = ["", "To Play", "Completed", "Dropped"]
DEV_STATUS_OPTIONS = ["", "Active Development", "Completed", "Abandoned"]
GAME_VARIABLES = ["Name", "Link", "Latest Version", "DevState", "PlayStatus", "Notes", "Recommend"]

class GameTracker:

	# On start
	def __init__(self, root):
		
		# Create window
		self.root = root
		self.root.title("Game Tracker")
		self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
		
		# Access to data management
		self.dataManager = DataManager()
		
		# Main View Container
		self.viewFrame = tk.Frame(root)
		self.viewFrame.pack(fill = tk.BOTH, expand = True)
		self.build_main_view()
		
	# -------------------------------- VIEWS -----------------------------------------
		
	# Build standard view of game list
	def build_main_view(self):
		
		self.__clear_view()
			
		# Build filter frame
		filterFrame = tk.Frame(self.viewFrame)
		filterFrame.pack(padx = 5, pady = 5, fill = 'x')
		
		# Name Filter
		tk.Label(filterFrame, text = "Name:").pack(side = "left")
		self.nameFilter = tk.Entry(filterFrame, width = 15)
		self.nameFilter.pack(side = "left", padx = 2)
		
		# Play Filter
		tk.Label(filterFrame, text = "Play Status:").pack(side = "left")
		self.playFilter = ttk.Combobox(filterFrame, values = PLAY_STATUS_OPTIONS, state = "readonly")
		self.playFilter.pack(side = "left", padx = 2)
		
		# Dev Filter
		tk.Label(filterFrame, text = "Dev Status:").pack(side = "left")
		self.devFilter = ttk.Combobox(filterFrame, values = DEV_STATUS_OPTIONS, state = "readonly")
		self.devFilter.pack(side = "left", padx = 2)
		
		# Filter buttons
		tk.Button(filterFrame, text = "Apply Filter", command = self.apply_filters).pack(side = "left", padx = 5)
		tk.Button(filterFrame, text = "Clear", command = self.clear_filters).pack(side = "left", padx = 5)
		
		# Column sorting
		def sort_column(col, reverse):
			
			# Get current values
			data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
			
			# Sort alphabetically
			try:
				data.sort(key = lambda t: t[0].lower(), reverse = reverse)
			except Exception:
				data.sort(reverse = reverse)
				
			# Reorder rows
			for index, (val, child) in enumerate(data):
				self.tree.move(child, '', index)
				
			# Reverse order next time selected
			self.tree.heading(col, text=f"{col} {'▼' if not reverse else '▲'}", command=lambda: sort_column(col, not reverse))

		
		# Scrollbar
		treeFrame = tk.Frame(self.viewFrame)
		treeFrame.pack(fill = tk.BOTH, expand = True)
		scrollbar = ttk.Scrollbar(treeFrame, orient = "vertical")
		scrollbar.pack(side = "right", fill = "y")
		
		# List of Name, Play, Dev
		self.tree = ttk.Treeview(treeFrame, columns = ("Name", "Play Status", "Development Status"), show = "headings", yscrollcommand = scrollbar.set, height = 10)
		self.tree.heading("Name", text = "Game Name", command = lambda: sort_column("Name", False))
		self.tree.heading("Play Status", text = "Play Status", command = lambda: sort_column("Play Status", False))
		self.tree.heading("Development Status", text = "Development Status", command = lambda: sort_column("Development Status", False))
		self.tree.pack(fill = tk.BOTH, expand = True)
		
		scrollbar.config(command = self.tree.yview)
		
		# Add Game button
		addBtn = tk.Button(self.viewFrame, text = "Add Game", command = self.add_game_view)
		addBtn.pack(pady = 5)
		
		# Right Click Menu
		self.contextMenu = tk.Menu(self.tree, tearoff = 0)
		self.contextMenu.add_command(label = "Copy Link", command = self.copy_link)
		self.contextMenu.add_command(label = "View Details", command = self.view_selected_game)
		self.contextMenu.add_command(label = "Edit Game", command = self.edit_selected_game)
		self.contextMenu.add_command(label = "Delete Game", command = self.delete_selected_game)
		
		def show_context_menu(event):
			# Get row
			rowId = self.tree.identify_row(event.y)
			if rowId:
				self.tree.selection_set(rowId)
				self.tree.focus(rowId)
				self.contextMenu.post(event.x_root, event.y_root)
			else:
				self.contextMenu.unpost()
		
		def double_click(event):
			selectedItem = self.tree.focus()
			if not selectedItem:
				return
			
			gameName = self.tree.item(selectedItem)["values"][0]
			self.game_details_view(gameName)
		
		# Bindings
		self.tree.bind("<Double-1>", double_click)
		self.tree.bind("<Button-3>", show_context_menu)
		
		# Load games
		self.load_game_list()
		
	# Build add game view
	def add_game_view(self):
	
		self.__clear_view()
			
		# Text Entry fields
		labels = ["Name", "Download Link", "Latest Version", "Notes"]
		entries, row = self.build_form_fields(self.viewFrame, labels)
		
		# Combo boxes
		devCombo, row = self.build_combo(self.viewFrame, "Dev Status", DEV_STATUS_OPTIONS[1:], row)
		playCombo, row = self.build_combo(self.viewFrame, "Play Status", PLAY_STATUS_OPTIONS[1:], row)
		
		# Recommendation
		recVar = tk.BooleanVar()
		tk.Checkbutton(self.viewFrame, text = "Recommend", variable = recVar).grid(row = row, column = 1, sticky = "nesw")
		row += 1
		
		# Function to save game
		def save_game():
			game = {
				"Name": entries["Name"].get(),
				"Link": entries["Download Link"].get(),
				"Latest Version": entries["Latest Version"].get(),
				"DevState": devCombo.get(),
				"PlayStatus": playCombo.get(),
				"Notes": entries["Notes"].get(),
				"Recommend": recVar.get()
			}
			result = self.dataManager.add_new_game(game)
			if result == 0:
				self.build_main_view()
			elif result == 1:
				messagebox.showerror("Error", "Name is required.")
			elif result == 2:
				messagebox.showerror("Error", f"{game['Name']} already exists.")
		
		# Buttons
		tk.Button(self.viewFrame, text = "Back", command = self.build_main_view).grid(row = row, column = 0, pady = 10)
		tk.Button(self.viewFrame, text = "Save", command = save_game).grid(row = row, column = 1, pady = 10)
		
	# Build game details view
	def game_details_view(self, name):
		
		self.__clear_view()
			
		# Get game
		game = self.dataManager.get_game(name)
		
		# Title
		row = 0
		tk.Label(self.viewFrame, text = "Game Details", font = ("Arial", 16)).grid(row = row, column = 0, columnspan = 2, pady = 10)
		row += 1
		
		# Game details
		for field in GAME_VARIABLES:
			value = str(game.get(field, ""))
			tk.Label(self.viewFrame, text = f"{field}:").grid(row = row, column = 0, sticky = "nesw", padx = 5, pady = 2)
			tk.Label(self.viewFrame, text = value).grid(row = row, column = 1, sticky = "nesw", padx = 5, pady = 2)
			row += 1
			
		#Buttons
		buttonFrame = tk.Frame(self.viewFrame)
		buttonFrame.grid(row = row, column = 0, columnspan = 2, pady = 10)
		
		tk.Button(buttonFrame, text = "Back", command = self.build_main_view).pack(side = "left", padx = 5)
		tk.Button(buttonFrame, text = "Edit", command = lambda: self.edit_details_view(game["Name"])).pack(side = "left", padx = 5)
		tk.Button(buttonFrame, text = "Delete", command = lambda: self.delete_game(game["Name"])).pack(side = "left", padx = 5)
	
	# Edit game details view
	def edit_details_view(self, name):
	
		self.__clear_view()
			
		# Get existing data
		game = self.dataManager.get_game(name)
		if not game:
			messagebox.showerror("Error", f"'{name}' could not be found.")
			self.build_main_view()
			return
		
		# Text Entry
		labels = ["Name", "Download Link", "Latest Version", "Notes"]
		entries, row = self.build_form_fields(self.viewFrame, labels, {
			"Name": game["Name"],
			"Download Link": game["Link"],
			"Latest Version": game["Latest Version"],
			"Notes": game["Notes"]
		})
		
		# Combos
		devCombo, row = self.build_combo(self.viewFrame, "Dev Status", DEV_STATUS_OPTIONS[1:], row, game["DevState"])
		playCombo, row = self.build_combo(self.viewFrame, "Play Status", PLAY_STATUS_OPTIONS[1:], row, game["PlayStatus"])
		
		# Recommend
		recVar = tk.BooleanVar(value = game["Recommend"])
		tk.Checkbutton(self.viewFrame, text = "Recommend", variable = recVar).grid(row = row, column = 1, sticky = "nesw")
		row += 1
		
		# Save edits
		def save_edit():
			game = {
				"Name": entries["Name"].get(),
				"Link": entries["Download Link"].get(),
				"Latest Version": entries["Latest Version"].get(),
				"DevState": devCombo.get(),
				"PlayStatus": playCombo.get(),
				"Notes": entries["Notes"].get(),
				"Recommend": recVar.get()
			}
			result = self.dataManager.edit_game(name, game)
			if result == 0:
				messagebox.showinfo("Saved", "Game updated successfully")
				self.build_main_view()
			elif result == 1:
				messagebox.showerror("Error", "Name can not be empty")
			elif result == 2:
				messagebox.showerror("Error", f"'{game['Name']}' already exists")
			else:
				messagebox.showerror("Error", f"'{name}' could not be found")
				
		# Buttons
		tk.Button(self.viewFrame, text = "Back", command = lambda: self.game_details_view(name)).grid(row = row, column = 0, pady = 10)
		tk.Button(self.viewFrame, text = "Save", command = save_edit).grid(row = row, column = 1, pady = 10)
	
	# -------------------------------- HELPER FUNCTIONS ------------------------------
	
	# Function loads games from the DataManager into the main view
	def load_game_list(self):
		
		# Clear tree first
		for row in self.tree.get_children():
			self.tree.delete(row)
			
		# Insert filtered games
		for game in self.dataManager.get_filtered_games():
			self.tree.insert("", tk.END, values = (game["Name"], game["PlayStatus"], game["DevState"]))
			
	# Function that sends filters to the DataManager
	def apply_filters(self):
		name = self.nameFilter.get()
		dev = self.devFilter.get()
		play = self.playFilter.get()
		
		self.dataManager.apply_filters(name, dev, play)
		self.load_game_list()
		
	# Function that clears the filters of main view
	def clear_filters(self):
		self.nameFilter.delete(0, tk.END)
		self.playFilter.set("")
		self.devFilter.set("")
		self.apply_filters()
		
	# Function builds labeled entry fields. Returns entries and next row
	def build_form_fields(self, parent, fields, value = None, start_row = 0):
		entries = {}
		values = value or {}
		for i, label in enumerate(fields):
			row = start_row + i
			tk.Label(parent, text = label).grid(row = row, column = 0, sticky = "nesw", padx = 5, pady = 2)
			entry = tk.Entry(parent, width = 40)
			entry.insert(0, values.get(label, ""))
			entry.grid(row = row, column = 1, padx = 5, pady = 2)
			entries[label] = entry
		return entries, start_row + len(fields)
		
	# Function builds label and combobox, returns widget and row
	def build_combo(self, parent, labelText, values = [""], row = 0, currentValue = ""):
		tk.Label(parent, text = labelText).grid(row = row, column = 0, sticky = "nesw", padx = 5, pady = 2)
		combo = ttk.Combobox(parent, state = "readonly", values = values)
		combo.set(currentValue)
		combo.grid(row = row, column = 1, padx = 5, pady = 2)
		return combo, row + 1
		
	# Function deletes game given name
	def delete_game(self, name):
		confirm = messagebox.askyesno("Delete Game", f"Are you sure you want to delete '{name}'?")
		if confirm:
			if self.dataManager.delete_game(name):
				messagebox.showinfo("Deleted", f"{name} was deleted.")
				self.build_main_view()
			else:
				messagebox.showerror("Error", "Game could not be deleted")
		
	# Function to clear the view
	def __clear_view(self):
		for widget in self.viewFrame.winfo_children():
			widget.destroy()
		
	# Returns the name of the highlighted game in treeview
	def get_selected_game_name(self):
		selected = self.tree.focus()
		if not selected:
			return None
		return self.tree.item(selected)["values"][0]
		
	# Copies game link to clipboard
	def copy_link(self):
		name = self.get_selected_game_name()
		if name:
			game = self.dataManager.get_game(name)
			link = game.get("Link", "")
			if link:
				self.root.clipboard_clear()
				self.root.clipboard_append(link)
				messagebox.showinfo("Link Copied", f"Link copied to clipboard:\n{link}")
			else:
				messagebox.showwarning("No Link", "This game has no link.")
	
	# Routes right click menu to game details
	def view_selected_game(self):
		name = self.get_selected_game_name()
		if name:
			self.game_details_view(name)
			
	# Routes right click menu to edit game
	def edit_selected_game(self):
		name = self.get_selected_game_name()
		if name:
			self.edit_details_view(name)
			
	# Routes right click menu to delete game
	def delete_selected_game(self):
		name = self.get_selected_game_name()
		if name:
			self.delete_game(name)
		
# Run script
if __name__ == "__main__":
	root = tk.Tk()
	app = GameTracker(root)
	root.mainloop()