import operator # needed to sort the dictionary
from operator import itemgetter # used for selecting elements in the dictionary
import re # used for string manipulation
from sys import getsizeof #used to determine the size of a variable
import os #needed for file sizes
from bitstring import BitArray # for writing binary
import json #used for storing the tree as json

def compress(originalfile,treefile='treefile.json',compressedfile='compressedfile.bin'):
  """
  The compress function compresses the originalfile, and stores
  the tree as "treefile" and the compressed file as "compressedfile"

  """
  #creates a blank dictionary
  thecharacters = {}
  tree={}
  #opnes the textfile with utf8 encoding as f
  with open(originalfile, encoding = 'utf8') as f:
    #loops until the file has ended
    while True:
      #reads the
      c = f.read(1)
      #if c is blank
      if not c:
        #stop the timer as the file is finished and exit the loop
        break
      #if it appears in the dictionary
      if c in thecharacters:
        #add 1 to the counter of frequency
          thecharacters[c] += 1
      #if c doesnt appear in the dictionary
      if c not in thecharacters:
        #add the item to the dictionary
          thecharacters[c]=1
  f.close()
  for key in thecharacters:
      tree[key[0]] = ''
      
  """
  create the tree
  smallest value gets assigned as 0 and 1
  old dictionary altered to reflect the combined values
  new dictionary created with the single elements and binary didgts for each character
  assign the new bits to the end of the dictionary value
  repeat until length of old dictionary is 1
  """
  
  while len(thecharacters) > 1:
    smallest2 = sorted(thecharacters.items(), key=itemgetter(1))[:2]
    
    del thecharacters[smallest2[0][0]]
    del thecharacters[smallest2[1][0]]
    thecharacters[smallest2[0][0]+'㋡'+smallest2[1][0]] = int(smallest2[0][1])+int(smallest2[1][1])

    for i in smallest2[0][0].split('㋡'):
      tree[i] += '0'
    for i in smallest2[1][0].split('㋡'):
      tree[i] += '1'

  """
  When tree is created, need to flip the binary values back to front to give the actual values
  """
  for i in tree:
    tree[i] = tree[i][::-1]

  #write json file with the huffman tree
  json.dump(tree,open(treefile,'w'))
  
  """
  read the file
  compare the character to the dictionary
  find the binary
  write it to file
  """
  binstring = ''
  file = open(compressedfile, "wb")
  with open(originalfile, encoding = 'utf8') as f:
    #loops until the file has ended
    while True:
      c = f.read(1)
      #if character appears in the dictionary
      if c in tree:
        #writes the value to the file
        binstring += tree[c]
      if not c:
        a = BitArray(bin=binstring)
        a.tofile(file)
        file.close()
        f.close()
        break

  original = int(os.stat(originalfile).st_size)
  final = int(os.stat(compressedfile).st_size)
  treesize = int(os.stat(treefile).st_size)
  print(originalfile)
  print("Original file size: ", os.stat(originalfile).st_size, "bits")
  print("Compresd file size: ", os.stat(compressedfile).st_size, "bits")
  print("The tree file size: ", os.stat(treefile).st_size, "bits")
  print("The totl file size: ", final+treesize, "bits")  
  print((((final+treesize)-original)/original)*100, "% change")


def decompress(compressedfile,output,treefile='treefile.json'):
  """
  File now written to with bitstring 
  """

  with open(compressedfile, 'rb') as f:
          b = BitArray(f.read())

  tree = json.load(open(treefile)) 

  """
  Binary values returned here as string
  need to create a loop to go through and scan until a match it found
  start with 1 bit, loop until ended
  write to file when bit is found
  """

  newfile = open(output, "a", encoding="utf-8")
  while len(b.bin) >= 0:
    x=0
    i=1
    while x==0:
      tosearch = b.bin[0:i]
      try:
        towrite=list(tree.keys())[list(tree.values()).index(tosearch)]
        newfile.write(towrite)
        newfile.close()
        newfile = open(output, "a", encoding="utf-8")
        b.bin=b.bin[i:]
        x=1
      except:
        i+=1
