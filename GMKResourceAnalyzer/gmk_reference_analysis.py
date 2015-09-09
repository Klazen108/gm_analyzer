####################################################################
# Module      : gmk_reference_analysis.py
# Author      : Klazen108 (twitch.tv/klazen108)
# Date        : 2015-09-09
# Description : Searches Game Maker projects and counts references
#               of all resources.
####################################################################

import os
import sys
import traceback
import ntpath
from os.path import join, getsize
import re

import codecs

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def traverse(path,filter,index):
	#print('Scanning: ' + path.decode('utf-8'))
	
	#check if file matches filter, and if so, grabs the group (which will be the filename minus extension)
	#and then trims the path off the front to leave only the resource name
	#index.extend([match.group(1).split('\\')[-1] for file in files for match in [filter[1].search(file)] if match])
	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
	#filter(filter[1].match,files)
	index.extend([m.group(1) for file in files for m in [filter[1].search(file.decode('utf-8'))] if m])
	
	#traverses all directories in the current one that don't match the exclude filter
	dirs = [d for d in os.listdir(path) if (os.path.isdir(os.path.join(path, d)) and (filter[2] is None or not filter[2].match(d.decode('utf-8'))))]
	for dir in dirs:
		next_path = os.path.join(path, dir)
		traverse(next_path,filter,index)

def traverse_target(path,filter,index):
	#print('Scanning: ' + path.decode('utf-8'))
	
	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and filter[1].match(f.decode('utf-8'))]
	for file in files:
		file_path = os.path.join(path, file)
		print('--'+file.decode('utf-8'))
		for resource in index:
			if resource[0] in codecs.open(file_path, 'r', encoding='utf-8').read(): #open(file_path).read():
				resource.append(file_path.decode('utf-8'))
				print('matched '+resource[0])
	
	#traverses all directories in the current one that don't match the exclude filter
	dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	for dir in dirs:
		next_path = os.path.join(path, dir)
		traverse_target(next_path,filter,index)

# project_path - the root path of the project where the resources are located (the split output for gm8)
def main(project_path,is_gm8_str):
	#get project file path and ensure it exists
	is_gm8 = (is_gm8_str=='true')
	if project_path is None or project_path == '':
		project_path = input('Enter the project folder: ')
	
	if not os.path.exists(project_path):
		print('Folder '+project_path+' doesn\'t exist! Please try again.')
		sys.exit(-1)
	gmk_path = os.path.abspath(project_path)

	print('Scanning GMK resources located in: ' + gmk_path)

#	if output_path is None:
#		output_path = path_leaf(walk_dir)
#	if not os.path.exists(output_path):
#		os.makedirs(output_path)
	#set up the folder structure
	if is_gm8:
		#the following filters run against the entire path name
		#source filter - the resources to scan for, including a regex to match and get the path minus extension
		#regex really sucks so we'll trim the path off in another step
		#root filename / type
		#filename include regex (get object name)
		#folder exclude regex (for example exlcude '.events' folders in objects)
		source_filter = [
			['Backgrounds',re.compile(r'(.*)\.png',re.IGNORECASE),None],
			['Fonts',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE),None],
			['Objects',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE),re.compile(r'\.events$',re.IGNORECASE)],
			['Paths',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE),None],
			['Rooms',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE),None],
			['Scripts',re.compile(r'(.*)\.gml',re.IGNORECASE),None],
			['Sounds',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE),None],
			['Sprites',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE),re.compile(r'\.images$',re.IGNORECASE)],
			['Time Lines',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE),None]
		]
		#target filter - the places to scan
		#root filename / type
		#files to scan
		target_filter = [
			#['Objects',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE)],
			['Rooms',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE)]#,
			#['Time Lines',re.compile(r'(.*)(?<!\.list).xml',re.IGNORECASE)]
		]
	else:
		#todo - figure out gms structure
		target_folders = ['objects','rooms','timelines']
	
	print('Building Resource Index...')
	resource_index = []
	for source in source_filter:
		print('Analyzing '+source[0])
		traverse(os.path.join(gmk_path,source[0]).encode('utf-8'),source,resource_index)
	resource_index = [[r] for r in resource_index]
	#print(resource_index)
	
	print('Resource Index Built. Searching for matches...')
	for target in target_filter:
		print('Analyzing '+target[0])
		traverse_target(os.path.join(gmk_path,target[0]).encode('utf-8'),target,resource_index)
	print(resource_index)

if __name__ == "__main__":
	main(sys.argv[1],sys.argv[2])