# gm_analyzer
Resource Analyzer for Game Maker Projects


Usage:
python gm_project_analyzer.py [project_folder]

project folder argument is optional. if you don't specify, it'll ask during runtime.

Checks the project folder for a .gmk, .gm81, or .gmx file
If there is a gm8/8.1 project file, splits it into its component files
If it's a gmx, then the files are already there, no need to split!

The components are then analyzed, and the results saved as CSV files for import into your spreadsheet program of choice.

currently working on a reference counter for resources, so you can tell what's being used where