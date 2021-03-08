import fileinput
import sys
import os
import re
import numpy as np  # pip3 install numpy
import constants

userDictionary = {}


def get_username_from_line(line):
    return line[21:]


def process_file(file, wordList):
    global userDictionary
    username = ""
    for line in file:
        if(bool(re.search('\[[0-9]{2}\-.{3}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\s.{2}\]', line, re.IGNORECASE))):
            username = ' '.join(get_username_from_line(line).split())
            if(not username in userDictionary):
                userDictionary[username] = [0] * len(wordList)
        else:
            if (username != ""):
                countList = [0] * len(wordList)
                i = 0
                while (i < len(wordList)):
                    countList[i] += len(re.findall(
                        r'(?<!\w){}(?!\w)'.format(wordList[i]), line, re.IGNORECASE))
                    i += 1
                userDictionary[username] = np.add(
                    userDictionary.get(username), countList)


def print_dictionary(userDict, word):
    print("\nUsername : Occurences of " + str(word) + "\n")
    for k, v in userDict.items():
        if(sum(v) >= constants.CHAT_THRESHOLD):
            print(k + ' : ' + " [" + ', '.join([str(elem)
                                                for elem in v]) + "]")


def main(argv):
    wordList = argv[1:]
    all_files = os.listdir("../input")
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
    for filein in txt_files:
        print("Reading File: " + filein)
        file = open(("../input/"+str(filein)), 'r', errors='ignore')
        process_file(file, wordList)
    print_dictionary(userDictionary, wordList)


if __name__ == "__main__":
    main(sys.argv)
