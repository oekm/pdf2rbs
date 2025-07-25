import re
import os
import csv
import argparse
from PyPDF2 import PdfReader

def main(inputPath, runMode):
    tagList = [] #fill with tuples ("tag", "filename")
    #inputPath = os.path.abspath(inputPath)

    #compile filters
    filterf1 = re.compile(r"(([A-Z]{2})((\.[A-Z]{2}[A-Z0-9]{2})((\.[A-Z]{2}(([1-9][0-9]{2,3})|([0-9]{2}))){1,3}(_[A-Z]{2}[0-9]{2})?)?)?)")
    filterf2 = re.compile(r"(([A-Z]{2})((\.[A-Z]{2}[A-Z0-9]{2})((\.[A-Z]{2}(([1-9][0-9]{2,3})|([0-9]{2}))){1,3}(_[A-Z]{2}[0-9]{2})?)?))")
    filterf3 = re.compile(r"(([A-Z]{2})((\.[A-Z]{2}[A-Z0-9]{2})((\.[A-Z]{2}(([1-9][0-9]{2,3})|([0-9]{2}))){1,3}(_[A-Z]{2}[0-9]{2})?)))")
    filterf4 = re.compile(r"((\.*QM[0-9]{2,4}))")
    filterf5 = re.compile(r"((A[A-Z]{1})((\.[A-Z\.]{1,5}[A-Z0-9]{0,2})((\.[A-Z]{1,2}(([0-9]{2,4}))){1,3}(-[A-Z]{1,2}[0-9]{1,2})?)))")
    filterp1 = re.compile(r"((H[DESU]{1}(\.[A-D][0-9]{2}(\.[0-9]{2}){0,3})?))")
    filterp2 = re.compile(r"((H[DESU]{1}\.[A-D][0-9]{2}(\.[0-9]{2}){0,3}))")
    filterp3 = re.compile(r"((H[DESU]{1}\.[A-D][0-9]{2}(\.[0-9]{2}){1,3}))")

    
    nofilter = re.compile(r"(.*)")

    #determine regex filter based on runmode
    match runMode:
        case "f1":
            filter = filterf1
        case "f2":
            filter = filterf2
        case "f3":
            filter = filterf3
        case "f4":
            filter = filterf4
        case "f5":
            filter = filterf5
        case "p1":
            filter = filterp1
        case "p2":
            filter = filterp2
        case "p3":
            filter = filterp3
        case "nf":
            filter = nofilter
        case _:
            filter = filterf3
             
    #get list of pdfs from inputPath
    pdfList = fileFinder(inputPath, ".pdf")[1]

    #get list of tag-file pairs from each pdf, add them to tagList
    for pdf in pdfList:
       tagList.extend(extractSubstrings(pdf, filter))

    #output each tag-file pair from tagList
    for tag in tagList:
        print(tag[0]+"\t"+tag[1])

    # with open(workDirPath, 'w') as outputFile:
    #     writer = csv.writer(outputFile)
    #print(workDirPath)

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

def extractSubstrings(filePath, searchPattern):
    reader = PdfReader(filePath, strict=0)
    numberOfPages = len(reader.pages)
    allText = ""
    if runVerbose:
        print("File: "+filePath)
    for i in range (0, numberOfPages):
        page = reader.pages[i]
        if runVerbose:
            print("Page "+str(i+1)+"/"+str(numberOfPages)+"...")
        allText += page.extract_text()

        try:
            for annot in page['/Annots']:
                obj=annot.get_object()
                if 'AutoCAD SHX Text' in obj.values():
                    #print (obj['/Contents'],obj['/Rect'])
                    allText += (obj['/Contents'])
        except:
            if runVerbose:
                print("No annotations in file")
            else:
                pass


    #remove whitespace before and after ./_ to merge broken tags
    cleanText = re.sub(r"\s*(\.|\_)\s*", r"\1", allText)
    if runVerbose:
        print("allText length: "+str(len(allText)))
        print(cleanText)

    matchList = searchPattern.findall(cleanText)

    if runVerbose:
        print("Matchlist length: "+str(len(matchList)))
    leaf = os.path.basename(filePath)

    #populate output array with text matchlist
    tupleList = []
    for i in range (0, len(matchList)):
        tupleList.append((matchList[i][0],leaf))
    return tupleList

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-i", "--inputPath", help="Path to file or folder", default="./")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-f", "--funktion", help="Extrahera funktionsbeteckningar med minst n (1-3) nivåer", type=int, choices={1,2,3,4,5})
    mode.add_argument("-p", "--placering", help="Extrahera placeringsbeteckningar med minst n (1-3) nivåer", type=int, choices={1,2,3})
    args = parser.parse_args()
    
    #set runmode based on f/p value
    runMode = "f3" #default
    if args.funktion == 1:
        runMode = "f1"
    if args.funktion == 2:
        runMode = "f2"
    if args.funktion == 3:
        runMode = "f3"
    if args.funktion == 4:
        runMode = "f4"
    if args.funktion == 5:
        runMode = "f5"
    if args.placering == 1:
        runMode = "p1"
    if args.placering == 2:
        runMode = "p2"
    if args.placering == 3:
        runMode = "p3"
    if args.funktion == 0:
        runmode = "nf"

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