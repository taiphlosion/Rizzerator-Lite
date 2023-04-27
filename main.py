import os
import time

# t = time.process_time()
# #do some stuff
# elapsed_time = time.process_time() - t

import bcolors
from BTree import *
from HashTable import *
import pandas as pd

# Clearing the Screen
os.system('clear')

# Main Menu GUI
print(f"{bcolors.bcolors.WARNING}****************************************************************************************{bcolors.bcolors.ENDC}")
txt = 'Welcome to the Rizzerator!'
new_str = txt.center(85)
print(new_str)
txt = 'Presented by:'
new_str = txt.center(85)
print(new_str)
txt = f"{bcolors.bcolors.OKCYAN}The International Council of Confidence{bcolors.bcolors.ENDC}"
new_str = txt.center(93)
print(new_str)
print(f"{bcolors.bcolors.WARNING}****************************************************************************************{bcolors.bcolors.ENDC}")
print("\n")
open = True

# Loading data into Hash Table
data = pd.read_csv("word_scores.csv")
ht = HashTable(300000)
error_words = []
for key, value in data.values:
    rounded_val = round(value, 2)
    if type(key) == str:
        ht.insert(key, rounded_val)


while(open):

    # Menu Options
    print(f"{bcolors.bcolors.UNDERLINE}\nLet's go! How would you like to use the Rizzerator?\n{bcolors.bcolors.ENDC}")
    print("1. Display the top 10 most commonly used words")
    print("2. Find top 10 words with the highest confidence rating")
    print("3. Find top 10 words with the lowest confidence rating")
    print("4. Search for word data")
    print("5. Exit")
    value = input("\nSelect an option: ")

    match value:
        case "1":
            print("Bruh")
        case "2":
            os.system('clear')
            print()
            print()
            print(
                f"{bcolors.bcolors.OKGREEN}Find top 10 words with the highest confidence rating:{bcolors.bcolors.ENDC}")
            print()

            t = time.process_time()
            list = ht.get_top_scores()
            elapsed_time = time.process_time() - t

            for idx, pair in enumerate(list):
                print(f"{idx+1}" + ".", pair[0].capitalize())
            print()
            print(f"{bcolors.bcolors.HEADER}Hash Table{bcolors.bcolors.ENDC}")
            print("Elapsed time:", round(elapsed_time, 3), "seconds")

            t = time.process_time()
            # Todo: Implement function for BTree
            elapsed_time = time.process_time() - t

            print()
            print(f"{bcolors.bcolors.HEADER}BTree{bcolors.bcolors.ENDC}")
            print("Elapsed time:", round(elapsed_time, 3), "seconds")
            time.sleep(2)
        case "3":
            os.system('clear')
            print()
            print()
            print(
                f"{bcolors.bcolors.OKGREEN}Find top 10 words with the lowest confidence rating:{bcolors.bcolors.ENDC}")
            print()

            t = time.process_time()
            list = ht.get_top_scores_lowest()
            elapsed_time = time.process_time() - t

            for idx, pair in enumerate(list):
                print(f"{idx+1}" + ".", pair[0].capitalize())
            print()
            print(f"{bcolors.bcolors.HEADER}Hash Table{bcolors.bcolors.ENDC}")
            print("Elapsed time:", round(elapsed_time, 3), "seconds")

            t = time.process_time()
            # Todo: Implement function for BTree
            elapsed_time = time.process_time() - t

            print()
            print(f"{bcolors.bcolors.HEADER}BTree{bcolors.bcolors.ENDC}")
            print("Elapsed time:", round(elapsed_time, 3), "seconds")
            time.sleep(2)
        case "4":
            os.system('clear')
            print()
            print()
            print(
                f"{bcolors.bcolors.OKGREEN}Search for word data:{bcolors.bcolors.ENDC}")
            print()
            retry = True
            while(retry):
                value = input("Input a word: ")

                t = time.process_time_ns()
                score = ht.search(value.lower())
                elapsed_time = time.process_time_ns() - t

                if score == None:
                    print()
                    print(
                        f"{bcolors.bcolors.FAIL}Input Invalid, please try again...{bcolors.bcolors.ENDC}")
                    time.sleep(1)
                else:
                    print(
                        f"{bcolors.bcolors.BOLD}Word:{bcolors.bcolors.ENDC}", value.capitalize())
                    print(
                        f"{bcolors.bcolors.BOLD}Score:{bcolors.bcolors.ENDC}", score)
                    print()
                    print(
                        f"{bcolors.bcolors.HEADER}Hash Table{bcolors.bcolors.ENDC}")
                    print("Elapsed time:", round(
                        elapsed_time, 3), "nanoseconds")
                    retry = False

            t = time.process_time()
            # Todo: Implement function for BTree
            elapsed_time = time.process_time() - t

            print()
            print(f"{bcolors.bcolors.HEADER}BTree{bcolors.bcolors.ENDC}")
            print("Elapsed time:", round(elapsed_time, 3), "seconds")
            time.sleep(2)
        case "5":
            print("Thank you for Rizzing with us!")
            open = False
        case _:
            print("Please try again.")
