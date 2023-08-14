import re
import os
import argparse
from PyPDF2 import PdfReader

def main(inputPath, runMode):
    tagList = [] #fill with tuples ("tag", "filename")

    #compile filters
    filterf1 = re.compile(r"(([A-Z]{2})((\.[A-Z]{2}[A-Z0-9]{2})((\.[A-Z]{2}(([1-9][0-9]{2,3})|([0-9]{2}))){1,3}(_[A-Z]{2}[0-9]{2})?)?)?)")
    filterf2 = re.compile(r"(([A-Z]{2})((\.[A-Z]{2}[A-Z0-9]{2})((\.[A-Z]{2}(([1-9][0-9]{2,3})|([0-9]{2}))){1,3}(_[A-Z]{2}[0-9]{2})?)?))")
    filterf3 = re.compile(r"(([A-Z]{2})((\.[A-Z]{2}[A-Z0-9]{2})((\.[A-Z]{2}(([1-9][0-9]{2,3})|([0-9]{2}))){1,3}(_[A-Z]{2}[0-9]{2})?)))")
    filterp1 = re.compile(r"(H[DESU]{1}(\.[A-D][0-9]{2}(\.[0-9]{2}){0,3})?(?!\S))")
    filterp2 = re.compile(r"(H[DESU]{1}\.[A-D][0-9]{2}(\.[0-9]{2}){0,3}(?!\S))")
    filterp3 = re.compile(r"(([A-Z]{2})((\.[A-Z]{2}[A-Z0-9]{2})((\.[A-Z]{2}(([1-9][0-9]{2,3})|([0-9]{2}))){1,3}(_[A-Z]{2}[0-9]{2})?)))")

    #determine regex filter based on runmode
    match runMode:
        case "f1":
            filter = filterf1
        case "f2":
            filter = filterf2
        case "f3":
            filter = filterf3
        case "p1":
            filter = filterp1
        case "p2":
            filter = filterp2
        case "p3":
            filter = filterp3
        case _:
            if runVerbose:
                print("no runMode selected")
            filter = filterf3
             
    #get list of pdfs from inputPath
    pdfList = fileFinder(inputPath, ".pdf")[1]

    #get list of tag-file pairs from each pdf, add them to tagList
    for pdf in pdfList:
       tagList.extend(extractSubstrings(pdf, filter))

    #output each tag-file pair from tagList
    for tag in tagList:
        print(tag)
    
def extractSubstrings(filePath, searchPattern):
    reader = PdfReader(filePath)
    numberOfPages = len(reader.pages)
    allText = ""
    if runVerbose:
        print("File: "+filePath)
    for i in range (0, numberOfPages):
        page = reader.pages[i]
        if runVerbose:
            print("Page "+str(i+1)+"/"+str(numberOfPages)+"...")
        allText += page.extract_text()

    cleanText = re.sub(r"\s*\.\s*", r".", allText)
    if runVerbose:
        print("allText length: "+str(len(allText)))
        print(cleanText)

    matchList = searchPattern.findall(cleanText)

    if runVerbose:
        print("Matchlist length: "+str(len(matchList)))
    

    tupleList = []
    for i in range (0, len(matchList)):
        tupleList.append((matchList[i][0],filePath))
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-i", "--inputPath", help="Path to file or folder", default="./")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-f", "--funktion", help="Extrahera funktionsbeteckningar med minst n (1-3) nivåer", type=int, choices={1,2,3})
    mode.add_argument("-p", "--placering", help="Extrahera placeringsbeteckningar med minst n (1-3) nivåer", type=int, choices={1,2,3})
    args = parser.parse_args()
    
    #set runmode based on f/p value
    runMode = "" #default
    if args.funktion == 1:
        runMode = "f1"
    if args.funktion == 2:
        runMode = "f2"
    if args.funktion == 3:
        runMode = "f3"
    if args.placering == 1:
        runMode = "p1"
    if args.placering == 2:
        runMode = "p2"
    if args.placering == 3:
        runMode = "p3"

    runVerbose = 0
    if args.verbose:
        runVerbose = 1

    # for arg in vars(args):
    #     print(arg, getattr(arg, args))

    main(args.inputPath, runMode)
else:
   path = "./testfile.pdf"
   path2 = "./testfolder"
   regex = "https?://[a-z./]+" 
   main(path2, regex)