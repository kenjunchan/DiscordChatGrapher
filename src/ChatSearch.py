import fileinput, sys, os, re
import numpy as np  # pip3 install numpy
import constants


def print_fileinput(file):
    '''
    Prints the file entirely in console
    Parameters:
        param1 (file)
    Returns:
        none
    '''
    print(os.path.basename(file.name))
    for line in file:
        print(line, end='')
    print("\n")

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

def count_occurences(file, wordList):
    '''
    Returns the number of occurences of all given words in a given file
    Parameters:
        param1 (file)
        param2 (string[])
    Returns:
        count (number[])
    '''
    countList = [0] * len(wordList)
    for line in file:
        i = 0
        while (i < len(wordList)):
            if(not re.search('\[[0-9]{2}\-.{3}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\s.{2}\]', line, re.IGNORECASE)):
                countList[i] += count_words(wordList[i], line)
            i += 1
    return countList


def print_occurences(wordList, countList):
    '''
    Prints the occurences of all the words in wordList
    Parameters:
        param1 (string[])
        param2 (number[])
    Returns:
        none
    '''
    for word, count in zip(wordList, countList):
        print("Number of Occurences of \"" + word + "\": " + str(count))


def main(argv):
    wordList = argv[1:]
    total_occurences = [0] * len(wordList)
    all_files = os.listdir("../input")
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
    for filein in txt_files:
        print("Reading File: " + filein)
        file = open(("../input/"+str(filein)), 'r', errors='ignore')
        total_occurences = np.add(count_occurences(
            file, wordList), total_occurences)
    print_occurences(wordList, total_occurences)


if __name__ == "__main__":
    main(sys.argv)
