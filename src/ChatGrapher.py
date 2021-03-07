import fileinput
import sys
import os
import re
import numpy as np #pip3 install numpy
import constants

userDictionary = {}
            
def get_username_from_line(line):
    return line[21:]

def process_file(file, word):
    global userDictionary
    username = ""
    for line in file:
        if(bool(re.search('\[[0-9]{2}\-.{3}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\s.{2}\]', line, re.IGNORECASE))):
            username = ' '.join(get_username_from_line(line).split())
            if(not username in userDictionary):
                userDictionary[username] = 0
        else:
            if (username != ""):
                userDictionary[username] += len(re.findall(rf'\b{word}\b', line, re.IGNORECASE))
                
                

def print_dictionary(userDict, word):
    print("\nUsername : Amount of Occurences of | " + word + "\n")
    sortedDict = dict(sorted(userDict.items(), key=lambda item: item[1], reverse = True))
    for k,v in sortedDict.items():
        if(v >= constants.CHAT_THRESHOLD):
            print(k,':',v)
    
def main(argv):
    wordList = argv[1:]
    all_files = os.listdir("../input")
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
    for filein in txt_files:
        print("Reading File: " + filein)
        file = open(("../input/"+str(filein)), 'r', errors = 'ignore')
        process_file(file, argv[1])
    print_dictionary(userDictionary, argv[1])
    
if __name__ == "__main__":
    main(sys.argv)