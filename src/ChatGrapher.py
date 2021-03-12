import fileinput
import sys
import os
import re
import numpy as np  # pip3 install numpy
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import constants

userDictionary = {}


def get_username_from_line(line):
    '''
    Returns the username from the username line
    Parameters:
        param1 (string)
    Returns:
        username (string)
    '''
    return line[21:]

def count_words(word, line):
    '''
    Returns the number of occurences of a word in a given line
    Parameters:
        param1 (string)
        param2 (string)
    Returns:
        count (number)
    '''
    return len(re.findall(r'(?<!\w){}(?!\w)'.format(word), line, re.IGNORECASE))

def is_emote(word):
    '''
    returns true if the word is an emote or a special word, false otherwise
    Parameters:
        param1 (string)
    Returns:
        boolean
    '''
    if(len(word) >= 3):
        if(word[0] == ':' and word[len(word) - 1] == ':'):
            return True
    if(word.lower() in (word.lower() for word in constants.SPECIAL_WORDS)):
        return True
    return False


def count_emotes(word, line):
    '''
    Returns the number of occurences of a given word in a given line
    Parameters:
        param1 (string)
        param2 (string)
    Returns:
        count (number)
    '''
    return line.lower().count(word.lower())

def process_file(file, wordList):
    '''
    Processes the given files, going line by line and adding up all occurences of every word in the wordlist
    Parameters:
        param1 (file)
        param2 (string[])
    Returns:
        none
    '''
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
                    if(is_emote(wordList[i])):
                        countList[i] += count_emotes(wordList[i], line)
                    else:
                        countList[i] += count_words(wordList[i], line)
                    #countList[i] += count_words(wordList[i], line)
                    i += 1
                userDictionary[username] = np.add(userDictionary.get(username), countList)


def print_dictionary(userDict, word):
    '''
    Prints the dictionary
    Parameters:
        param1 (Dictionary)
        param2 (string)
    Returns:
        none
    '''
    print("\nUsername : Occurences of " + str(word) + "\n")
    for k, v in userDict.items():
        if(sum(v) >= constants.CHAT_THRESHOLD):
            print(k + ' : ' + " [" + ', '.join([str(elem)
                                                for elem in v]) + "]")


def graph_word(wordList, indx):
    '''
    graphs the occurences of the word with horizontal bar graph given the words to graph
    Parameters:
        param1 (string[])
        param2 (number)
    Returns:
        none
    '''
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
    
    plt.figure(indx + 1)
    plt.barh(usernames, occurences, height = constants.GRAPH_BAR_HEIGHT, color=constants.GRAPH_COLORS) 
  
    for index, value in enumerate(occurences): 
        plt.text(value, index, 
            str(value)) 
        
    plt.ylabel('usernames')
    plt.xlabel('Occurences of: \"' + wordList[indx] + "\"")
    plt.title('Number of times \"' + wordList[indx] + "\" has been said")

def main(argv):
    wordList = argv[1:]
    all_files = os.listdir("../input")
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
    for filein in txt_files:
        print("Reading File: " + filein)
        file = open(("../input/"+str(filein)), 'r', errors='ignore')
        process_file(file, wordList)
    print_dictionary(userDictionary, wordList)
    plt.rcParams["figure.figsize"] = constants.GRAPH_WIDTH_HEIGHT
    indx = 0
    for word in wordList:
        graph_word(wordList, indx)
        indx += 1
    plt.show()
    
if __name__ == "__main__":
    main(sys.argv)
