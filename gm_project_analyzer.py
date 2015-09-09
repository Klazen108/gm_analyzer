import os
import sys
import ntpath
from os.path import join
import shutil
import subprocess

#import gmk_analysis module
sys.path.insert(0, 'GMKResourceAnalyzer')
import gmk_analysis

#gets the leaf node name of the path, or in other words, the filename or the directory name
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def main():
	#get project file path and ensure it exists
	found = False
	if len(sys.argv)>1:
		gmk_rel_path = sys.argv[1]
	else:
		gmk_rel_path = input('Enter the project folder: ')
	for file in os.listdir(gmk_rel_path):
		if file.endswith(".gmk") or file.endswith(".gm81"):
			gmk_rel_path = os.path.join(gmk_rel_path,file)
			is_gm8 = True
			found = True
			break
		elif file.endswith(".gmx"):
			is_gm8 = False
			found = True
			break;
	if not os.path.exists(gmk_rel_path):
		print('Folder '+gmk_rel_path+' doesn\'t exist! Please try again.')
		sys.exit(-1)
	if not found:
		print('No .gmk .gm81 or .project.gmx file found in folder '+gmk_rel_path+'! Please try again.')
		sys.exit(-1)
		
	gmk_path = os.path.abspath(gmk_rel_path)
	output_dir = path_leaf(gmk_path).split('.')[0]
	
	#check output directory
	if os.path.exists(output_dir):
		do_overwrite = (input('output directory '+output_dir+' exists. overwrite? y/n') == 'y')
		if not do_overwrite:
			sys.exit(0)
		else:
			shutil.rmtree(output_dir)
	analyze_output_path = os.path.join(output_dir,'gmk_analysis')
	
	#call gmksplit if it's an 8/8.1 project file
	if is_gm8:
		print('\nSplitting '+path_leaf(gmk_path)+' into component files...')
		split_output_path = os.path.join(output_dir,'gmk_split')
		args = ['GMKSplitter\\gmksplit.exe', gmk_path, split_output_path]
		subprocess.call(args) 
		print('Split complete!')
	else:
		split_output_path = gmk_rel_path
	
	#call gmk_analysis to grab resource sizes
	print('\nAnalyzing components...')
	gmk_analysis.main(split_output_path,analyze_output_path)

if __name__ == "__main__":
	main()
