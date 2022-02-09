from wordfreq import zipf_frequency
from letterFreq import letterFrequency

pool = []

with open("wordle-answers-alphabetical.txt") as f:
    pool = f.readlines()

pool = list(map(lambda raw: raw[:-1] if raw[-1] == "\n" else raw, pool))


def fitPattern(input:str, pattern:str, word:str):
    '''
    A pattern must be a string of 5 numbers consists of only 0, 1, or 2.
    A word must be exactly 5 letters long.
    0: miss; 1: hit but wrong position; 2: hit and correct position.
    Pattern and word format should be handled by input function.
    '''
    
    word = word.upper()

    # check for any hit in word
    remainedStr = "" # all char except those hit
    hitIndex = []
    for i in range(5):
        if pattern[i] == '2':
            # hit
            hitIndex.append(i)
    
    for j in range(5):
        if j not in hitIndex:
            remainedStr += word[j]
    
    # check for not perfect hits / no hits
    for i in range(5):
        p = pattern[i]
        if p == '0' and input[i] in remainedStr:
            return False
        elif p == '1' and (input[i] not in word or input[i] == word[i]):
            return False
        elif p == '2' and (input[i] != word[i]):
            return False
    return True

def sortByFreq(words:list):
    return sorted(words, key=wordScore, reverse=True)

def wordScore(word:str):
    '''
    Give a score to a 5-letter word.
    '''
    if len(word) != 5 or not word.isalpha():
        raise Exception("Input must be a 5-letter word.")
    
    letterFreqScore = 0
    for each in word.upper():
        letterFreqScore += letterFrequency[each]
    
    letterFreqScore /= 5

    wordFreq = zipf_frequency(word, 'en')

    return wordFreq * 0.45 + letterFreqScore * 0.55

def runWordleHelper():
    MAX_GUESSES = 6
    DEFAULT_GUESS = "CRANE"
    DEFAULT_PATTERN = "00000"
    remaining = pool
    currGuess = DEFAULT_GUESS
    currPattern = DEFAULT_PATTERN
    
    # first guess
    useDefault = input("Use default guess <CRANE> ? (y/n)").upper()
    if useDefault != "Y":
        currGuess = inputFiveLetterWord()
    currPattern = inputPattern()

    # goal test
    if currPattern == "22222":
        # hit answer
        print(f"Answer found: {currGuess}")
        return
    
    # make first guess
    remaining = sortByFreq(list(filter(lambda word: fitPattern(currGuess, currPattern, word), remaining)))
    print(f"Remaining words: \n {remaining}")
    if len(remaining) == 0:
        print("Run out of words! The pattern is not possible, or there are errors in program logic. Please check.")
        return

    for i in range(2, MAX_GUESSES):
        currGuess = inputFiveLetterWord()
        currPattern = inputPattern()

        # goal test
        if currPattern == "22222":
            # hit answer
            print(f"Answer found in {i} steps: {currGuess}")
            return

        remaining = sortByFreq(list(filter(lambda word: fitPattern(currGuess, currPattern, word), remaining)))
        print(f"Suggested words: \n {remaining}")
        if len(remaining) == 0:
            print("Run out of words! The pattern is not possible, or there are errors in program logic. Please check.")
            return
    
    # failed to find answer:
    print("Did not find answer within 6 guesses.")
    return


def inputFiveLetterWord():
    result = ""
    while True:
        result = input("Enter a 5-letter word: ")
        if isFiveLetterWord(result):
            return result.upper()

def isFiveLetterWord(word:str):
    return word.isalpha() and len(word) == 5

def inputPattern():
    result = ""
    while True:
        result = input("Enter resulted pattern: ")
        if len(result) != 5 or not set(result).issubset({'0', '1', '2'}):
            continue
        break
    return result
        

if __name__ == "__main__":
    runWordleHelper()
