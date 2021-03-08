import fileinput
import sys
import os
import re
import numpy as np  # pip3 install numpy
import matplotlib.pyplot as plt
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


def graph_word(wordList, indx):
    sortedDictionary = dict(sorted(userDictionary.items(), key=lambda item: item[1][indx], reverse = False))
    usernames = []
    occurences = []
    for k, v in sortedDictionary.items():
        if(v[indx]>=constants.CHAT_THRESHOLD):
            tempname = k[:-5] #removes trailing #nnnn after username
            if(len(tempname) > constants.NAME_LENGTH_THRESHOLD):
                usernames.append(tempname[:constants.NAME_LENGTH_THRESHOLD])
            else:
                usernames.append(tempname)
            occurences.append((v[indx]))
    left = [1] * len(usernames)
    
    i = 1
    while(i <= len(left)):
        left[i-1] = left[i-1] * i
        i += 1
    
    plt.barh(usernames, occurences, height = constants.GRAPH_HEIGHT, color=constants.GRAPH_COLORS) 
  
    for index, value in enumerate(occurences): 
        plt.text(value, index, 
            str(value)) 
        
    plt.ylabel('usernames')
    plt.xlabel('Occurences of: ' + wordList[indx])
    plt.title('Number of times ' + wordList[indx] + " has been said")
    plt.show()


def main(argv):
    wordList = argv[1:]
    all_files = os.listdir("../input")
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
    for filein in txt_files:
        print("Reading File: " + filein)
        file = open(("../input/"+str(filein)), 'r', errors='ignore')
        process_file(file, wordList)
    print_dictionary(userDictionary, wordList)
    
    indx = 0
    for word in wordList:
        graph_word(wordList, indx)
        indx += 1


if __name__ == "__main__":
    main(sys.argv)
