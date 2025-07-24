import os
import PyPDF2
#from PyPDF2 import PdfReader


def file_finder(dir):
    for root, dirs, files in os.walk(dir):
        print(root)
        for file in files:
            print(type(file))
        print("")
        for dir in dirs:
            file_finder(dir)

def parse_any(filepath):
    '''
    Input: direntry object

    '''
    ext = get_ext(filepath)
    match ext:
        case '':
            return
        case '.pdf':
            return parse_pdf(filepath)
        case '.xls' | '.xlsx' | '.xlsm':
            return parse_xls(filepath) 
        case _:
            return

def parse_pdf(filepath):
    '''
    Input: pdf file path
    Output: string list
    '''
    outputArray = []
    reader = PyPDF2.PdfReader(filepath, strict=0)
    for page in reader.pages:
        outputArray += page.extract_text().splitlines()
    return outputArray 
        


def parse_xls(path):
    '''
    Input: xls file path
    Output: string list
    '''
    pass


def get_ext(filepath):
    '''
    Input: file path
    Output: extension string
    '''
    return os.path.splitext(filepath)[1].lower()



testpath = "C:/Users/ae62922/HCP/Documents/Granskning/2025-04-17 SFA VE07 HD4"
testfile = "C:/Users/ae62922/HCP/Documents/Granskning/2025-04-17 SFA VE07 HD4/Ritning_PDF/AH-V-FBD-8-5765.PDF"

for file in os.scandir(testpath):
    #print(parse_pdf(file.path))
    #print(get_ext(filepath))
    pass

#print(parse_pdf(testfile))


fileFinder(testpath)