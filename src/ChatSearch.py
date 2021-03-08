import fileinput, sys, os, re
import numpy as np  # pip3 install numpy
import constants


def print_fileinput(file):
    print(os.path.basename(file.name))
    for line in file:
        print(line, end='')
    print("\n")


def count_occurences(file, wordList):
    countList = [0] * len(wordList)
    for line in file:
        i = 0
        while (i < len(wordList)):
            if(not re.search('\[[0-9]{2}\-.{3}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\s.{2}\]', line, re.IGNORECASE) and bool(re.search(rf'\b{wordList[i]}\b', line, re.IGNORECASE))):
                countList[i] += len(re.findall(
                    rf'\b{wordList[i]}\b', line, re.IGNORECASE))
            i += 1
    return countList


def print_occurences(wordList, countList):
    for word, count in zip(wordList, countList):
        print("Number of Occurences of \"" + word + "\": " + str(count))


def count_matches(file):
    print("Counting Matches in: " + os.path.basename(file.name))
    count = 0
    for line in file:
        if(bool(re.search('\[[0-9]{2}\-.{3}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\s.{2}\]', line, re.IGNORECASE))):
            count += 1
    print("Number of Occurences: " + str(count))


def main(argv):
    wordList = argv[1:]
    total_occurences = [0]*3
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
