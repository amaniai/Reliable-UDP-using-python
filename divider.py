#Reading the orignal pdf file from input folder as binary
originalfile= open("input/pyisart.pdf","rb") 
#Declare variable to sort the resulted files 
part= 1
#Read the first chunk from the original file and assign size to be read
chunk= originalfile.read(256*1024)
#Open a first chunk in folder part
outputfile= open("part/chunk0.pdf","wb")
#Write the first divided part to the first chunk 
outputfile.write(chunk)
#Creat manifest text file
manifestfile= open("manifest.txt","wb")
#Wirte the name of the original pdf file into the manifest text file
manifestfile.write("pyisart.pdf\n")
#Wirte the name of the first chunk into the manifest text file
manifestfile.write("chunk0.pdf\n")
#using while loop to write the remaining chunks
while chunk :
	#write divided pdf files into folder: part while incrementing chunk name "part" by 1
	outputfile= open("part/chunk"+str(part)+".pdf","wb")
	#write 256KB for each chunk
	chunk= originalfile.read(256*1024)
	outputfile.write(chunk)
	#write the names of the divided pdf files into the manifestfile
	manifestfile.write("chunk"+str(part)+".pdf \n")
	part+=1
print "PDF file was successfully divided !!"
#close files
originalfile.close()
outputfile.close()
manifestfile.close()
 
