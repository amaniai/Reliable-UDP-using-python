#open the manifest file to read
manifestfile= open("manifest.txt","rb") 
#Read the first line 
pyisart =manifestfile.readline()
#open the orignal file name in folder named output 
outputpdf= open("output/pyisart.pdf","wb")
#write the first part to original file name
outputpdf.write(pyisart)
#using for loop to read and then write the remaining parts to produce the merged PDF
for pdfpart in manifestfile.readlines():
		print "Adding "+pdfpart.strip()+" to new original PDF file"
		#open next part
		pdfpart=open("part/"+pdfpart.strip(),"rb")
		#read the chunk from part file
		chunk= pdfpart.read()
		#write the chunk to the new original file
		outputpdf.write(chunk)

print "PDF parts were merged successflly !!"
