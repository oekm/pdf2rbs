import re
import os
import argparse
from PyPDF2 import PdfReader

def main(inputPath, filter):
    taglist = [] #fill with tuples ("tag", "filename")

    pdfList = fileFinder(inputPath, ".pdf")[1]
    
    # print(pdfList)

    for pdf in pdfList:
       taglist.append(extractSubstrings(pdf, filter))

    print(taglist)
    
def extractSubstrings(filePath, filterString):
    reader = PdfReader(filePath)
    numberOfPages = len(reader.pages)
    allText = ""
    for i in range (0, numberOfPages):
        page = reader.pages[i]
        allText += page.extract_text()
    allTextNoSpaces = re.sub("\s+","", allText)

    matchList = re.findall(filterString, allTextNoSpaces)
    tupleList = []
    for i in range (0, len(matchList)):
        tupleList.append((matchList[i],filePath))
    return tupleList

def fileFinder(dir, ext):
    subfolders = []
    files = [] 
    
    #case 1: inputPath is a pdf
    if os.path.isfile(dir):
        if os.path.splitext(dir)[-1].lower() == ext:
            files.append(os.path.normpath(dir))

    #case 2: inputPath is a directory
    if os.path.isdir(dir):
         #separate subfolders and files in current wd
        for f in os.scandir(dir):
            if f.is_dir():
                subfolders.append(f.path)
            if f.is_file():
                if os.path.splitext(f.name)[-1].lower() == ext:
                    files.append(f.path)
        #recurse into subfolders, append lists
        for subfolder in list(subfolders):
            sf, f  = fileFinder(subfolder, ext) 
            subfolders.extend(sf)
            files.extend(f)
    #returning sf for recursion, call with [1] if only files needed
    return subfolders, files

    
    

# if __name__ == "__main__":
#     main()

path = "./testfile.pdf"
path2 = "./testfolder"
regex = "https?://[a-z./]+" 
main(path2, regex)