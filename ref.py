import os
import tkinter as tk
from tkinter import filedialog

class Reference:
    def __init__(self,reference,context,source,type):
        self.reference = reference
        self.context = context
        self.source = source
        self.type = type

class Document: 
    def __init__(self,name,path):
        self.name = name
        self.path = path
        self.func_ref_list = []
        self.loc_ref_list = []
        self.doc_ref_list = []



def main_menu():
    path = ""
    while True: 
        print("1. Välj mapp/fil att scanna. Nuvarande val:", path)
        print("2. Scanna")
        print("3. Avsluta")
        choice = input("Väl något av alternativen ovan: ")
        if choice == "1":
            path = file_picker()
        elif choice == "2":
            init_scan(path)
        elif choice == "3":
            break
        else:
            print("Inte ett val, försök igen.")

def path_menu():
    path_input = input("Ange en sökväg: ")
    if os.path.exists(path_input):
        print("Path:", path_input)
        return path_input
    else:
        print("Ogiltig sökväg")

def file_picker():
    return filedialog.askdirectory()

def init_scan(path):
    if os.path.isdir(path):
        for file in os.scandir(path):
            print(file.path)

main_menu()
