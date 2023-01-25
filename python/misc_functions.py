import os
import itertools
import glob
from pathlib import Path
import numpy as np
import pandas as pd
import rioxarray 

def multiple_file_types(input_directory, patterns, recursive=False):
    """
    Return iterable with files that have a common pattern. Will search
    in a recursive or non recursive way.
    Args:
        input_directory (str): directory where files with common pattern
        will be searched.
        patterns (list): list of patterns to search for.
    Returns:
        iterable with files that have a common pattern.
    """
    if recursive:
        expression = "/**/*"
    else:
        expression = "/*"
    return itertools.chain.from_iterable(glob.iglob(input_directory + \
                                                    expression + pattern,
                                                    recursive=recursive) for pattern in patterns)

def listdirs(path):
    """
    Create a list of folders in a given path.
    """
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def filename(path):
    """
    Extract the filename from a path without extension.
    """
    return Path(path).stem

def swap_values(flattened_np,listOfInLists,listOfSwappingValues):
	"""
	Takes each list in listOfInLists and swaps it by the
	corresponding value in listOfSwappingValues.
    For example if 
    listOfInLists=[[1,2],[3,4]] and  
    listOfSwappingValues=[10,11] then
    1 and 2 will become 10
    3 and 4 will become 11
    """
	aux=flattened_np
	if len(listOfInLists)!=len(listOfSwappingValues):
		print("Lists must be of the same length.")
	else:
		for i in range(len(listOfInLists)):
			# list to numpy array
			nparray = np.array(listOfInLists[i])
			found_idx = np.in1d(flattened_np,nparray)
			aux[found_idx]=listOfSwappingValues[i]
	aux = aux.astype(int)
	return aux