import os
import tkinter as tk
from tkinter import filedialog

class Reference:
    def __init__(self,reference,context,source,type):
        self.reference = reference
        self.context = context
        self.source = source
        self.type = type

    def __lt__(self,other):
        return self.reference < other.reference
    
class Document: 
    def __init__(self,name,path):
        self.name = name
        self.path = path
        self.func_ref_list = []
        self.loc_ref_list = []
        self.doc_ref_list = []

    def __str__(self):
        return('Name: ' + str(self.name) + ', Path: ' + str(self.path))

def main_menu():
    path = '' 
    while True: 
        print('\n1. Välj mapp att scanna. Nuvarande val:', path)
        print('2. Scanna')
        print('3. Avsluta')
        choice = input('Väl något av alternativen ovan: ')
        if choice == '1':
            path = file_picker()
        elif choice == '2':
            main_function(path)
        elif choice == '3':
            break
        else:
            print('Inte ett val, försök igen.')

def main_function(path):
    files = scan_tree(path)
    doclist = []
    for file in files:
        doclist.append(make_document(file))
    for doc in doclist:
        print(doc)

def file_picker():
    path = filedialog.askdirectory()
    print(type(path))
    return path

def scan_tree(path):
    '''Tar en sökväg till en mapp och returnerar lista med filer
    Indata: path (string)
    Returvärde: lista av DirEntry-objekt (list)
    '''
    file_list = []
    if os.path.isdir(path):
        for file in os.scandir(path):
            if os.path.isdir(file):
                file_list += scan_tree(file)
            else:
                file_list.append(file)
    return file_list

def make_document(dir_entry):
    return Document(dir_entry.name,dir_entry.path)
        
def scan_file(file):
    pass

def scan_document(doc):
    pass

#main_menu()
main_function('C:/Users/ae62922/HCP/Documents/Dokumentmall')
