import os
import sys
import traceback
import ntpath
from os.path import join, getsize

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

#actually gets kB but whatever
def get_mb(size):
	return size/(1024.0)

#mode: 'hierarchy' for a "parent/child" relationship output
#mode: 'flat' for a flat directory structure output
def print_size(out_file,size,path,type,mode='flat'):
	if mode == 'hierarchy':
		og_list = path.decode("utf-8").split('\\')
		self_and_parent = list(reversed(og_list[-2:]))
		names='\t'.join(self_and_parent)
	else:
		#og_list = path.decode("utf-8").split('\\')
		#names='\t'.join(og_list)
		names=path.decode("utf-8")
	line = "%s\t%0.2f\t%s\n" % (names,get_mb(size),type)
	out_file.write(line)

def traverse(out_file,path,mode='flat'):
	#print('Scanning: ' + path.decode('utf-8'))
	size = 0
	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
	dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	
	for file in files:
		path_name = os.path.join(path, file)
		cur_size = os.path.getsize(path_name)
		print_size(out_file,cur_size,path_name,'file')
		size+=cur_size
	
	for dir in dirs:
		path_name = os.path.join(path, dir)
		size+=traverse(out_file,path_name)
	
	print_size(out_file,size,path,'dir')
	
	return size

def main(walk_dir,output_path):
	print('Scanning GMK resources located in: ' + walk_dir)

	if output_path is None:
		output_path = path_leaf(walk_dir)
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	dirs = [d for d in os.listdir(walk_dir) if os.path.isdir(os.path.join(walk_dir, d))]
	for root_dir in dirs:
		print('Analyzing '+root_dir)
		output_file = os.path.join(output_path,root_dir+'.csv')
		try:
			out_f = open(output_file,'w')
			out_f.write('entry\tsize (in kB)\n')
			traverse(out_f,os.path.join(walk_dir,root_dir).encode('utf-8'))
			out_f.close()
		except Exception as e:
			print('Error during scan of '+root_dir+' \nReason:'+str(e))
			print(traceback.format_exc())
			sys.exit(-1)
	print('Analysis complete. Results saved to ' + output_path)

if __name__ == "__main__":
	main(sys.argv[1],None)