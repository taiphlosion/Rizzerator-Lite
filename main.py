import os
import time
import bcolors
from BTree import *

# Clearing the Screen
os.system('clear')

# Main Menu GUI
print("****************************************************************************************")
txt = 'Welcome to the Rizzerator!'
new_str = txt.center(85)
print(new_str)
txt = 'Presented by:'
new_str = txt.center(85)
print(new_str)
txt = f"{bcolors.bcolors.OKCYAN}The International Council of Confidence{bcolors.bcolors.ENDC}"
new_str = txt.center(93)
print(new_str)
print("****************************************************************************************")
print("\n")
open = True


while(open):

    # Menu Options
    print(f"{bcolors.bcolors.OKGREEN}\nLet's go! How would you like to use the Rizzerator?\n{bcolors.bcolors.ENDC}")
    print("1. Display the top 10 most commonly used words")
    print("2. Find top 10 words with the highest confidence rating")
    print("3. Find top 10 words with the lowest confidence rating")
    print("4. Look for words associated with a particular tag")
    print("5. Search for word data")
    print("6. Exit")
    value = input("\nSelect an option: ")

    # Loading data into Data Structures

    match value:
        case "1":
            print("")
            print("Top 10 most commonly used words:")
            time.sleep(1)
        case "2":
            print("")
            print("You can become a web developer.")
            time.sleep(1)
        case "3":
            print("")
            print("You can become a web developer.")
            time.sleep(1)
        case "4":
            print("")
            print("You can become a web developer.")
            time.sleep(1)
        case "5":
            print("")
            print("You can become a web developer.")
            time.sleep(1)
        case "6":
            print("")
            print("You can become a web developer.")
            open = False
        case _:
            print("Please try again.")
