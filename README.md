# GameTracker
A python based app that helps you manage a list of games. I originally had an Excel sheet that I used to manage this, but decided to make a quick program to do so instead. Itch has some features that could be used, but it was still too much work, and this also gives me a good excuse to try out Python. Might use Python more extensively in the future, considering how easy this turned out to be.

# How to Install
## Runnable Executable (Recommended)
This is the most painless way to test the code. Exe is compiled with pyinstall
1. Download the .exe from releases
2. Run GameTracker.exe in wanted file location
## Build from Source Code (Latest)
This only requires that you have python installed
1. Download the repo to your local machine
2. run GameTracker.py

Note: Again, this project is windows only. I haven't actually looked into it, but I believe the library I use requires different implementation for running on Linux or Mac

# Version History
## Version 2.0 (Release) (Current)
Complete recoding and overhaul of the system. Much better seperation of responsibility between classes (Now the UI isn't in charge of data management). The different features of the app no longer open in multiple windows, but all in the same window now, plus you can actually copy the link of games.
### Added Features
- Column Sorting
- Copy game link
- Scrollbar
- Context Menu
### Bugfixes
- Program will create both games.json, as well as the data directory if none exists
- Duplicate data is prevented, with the game name being the unique key
### Known Issues
- User resizing causes the app to stop updating layout for window size. I might disable resizing, because any solution I try just looks like crap
- 'Game Name' column changes when you sort it. I was tired when I added that feature, and I need to go back in and iron it out a little.
- Columns still show sorted arrows after you apply new filters, which undoes the sort. Read above
## Version 1.0 (Release)
Full release. I should have been uploading releases the entire time, but it wasn't until I had the project in a finished state that I thought to even upload it to Git. Program works just fine, but the code is pretty messy and full of clashing design choices.
### Added Features
- Load and save games to a JSON
- Sort games by filter
- Add/Remove games from list
- View and Edit game details
### Known Issues
- Will generate it's own games.json if none exists, but will not create it's own data folder
- Nothing prevents adding duplicate data to the list
