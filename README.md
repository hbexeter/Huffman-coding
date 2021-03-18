# Huffman-coding

This Huffman Coding algorithm takes a file and de/compresses it.

To compress the file call the function compress(originalfile,treefile,compressedfile)

originalfile = String name of your file e.g. "book.txt"
treefile = the file your tree will be stored at, set to "treefile" as default
compressedfile = the file location your compressed file will go to, set to "compressedfile.bin" as default

To decompress use: decompress(compressedfile,output,treefile):

Compressedfile = a .bin file that you compressed
output = the output location for the uncompressed file
treefile = the location of your tree file
