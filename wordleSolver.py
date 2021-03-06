from wordfreq import zipf_frequency
from letterFreq import letterFrequency
from statistics import stdev

def getAllPatternPerm():
    '''
    Get a tuple of all possible pattern permutations.
    '''
    elements = ('0', '1', '2')
    return [a+b+c+d+e for a in elements for b in elements for c in elements for d in elements for e in elements]


pool = []

with open("wordle-answers-alphabetical.txt") as f:
    pool = f.readlines()

pool = list(map(lambda raw: raw[:-1] if raw[-1] == "\n" else raw, pool))
allPatterns = getAllPatternPerm()


def fitPattern(inputW:str, pattern:str, word:str):
    '''
    Improved version of fit pattern check function.
    Check if a input word fit a given word by a pattern
    A pattern must be a string of 5 numbers consists of only 0, 1, or 2.
    A word must be exactly 5 letters long.
    0: miss; 1: hit but wrong position; 2: hit and correct position.
    Pattern and word format should be handled by input function.

    e.g.
    input word = eeezz; pattern = 11000; word 1 = zzzee (True)
    '''
    word = word.upper()
    inputW = inputW.upper()

    for i, p in enumerate(pattern):
        ci = inputW[i]
        if p == '0':
            if ci in word:
                return False
        elif p == '2':
            cw = word[i]
            if ci != cw:
                return False
            word = word.replace(ci, '.', 1) # replace char with non-alphabet s.t. cannot be matched to again
        elif p == '1':
            if ci not in word:
                return False
            cw = word[i]
            if ci == cw:
                return False
            word = word.replace(ci, '.', 1) # replace char with non-alphabet s.t. cannot be matched to again
    return True


def getNextPoolSize(guess:str, pool:list, pattern:str):
    '''
    Given <guess> as the next guess, <pool> as the current pool of words left, <pattern> as the resulted pattern,
    return the size of the remaining valid words for the next round.
    '''
    if pattern == "22222":
        # word is a correct hit
        return 0
    nextPool = list(filter(lambda word: fitPattern(guess.upper(), pattern, word.upper()), pool))
    nextPoolSize = len(nextPool)
    return nextPoolSize


def sortByFreq(words:list):
    return sorted(words, key=wordScore, reverse=True)

def sortByWordScore(words:list):
    return sorted(words, key=(lambda word: wordScoreByNextIterPoolSize(word, words)))

def sortByFreqAndWordScore(words:list):
    return sorted(words, key=(lambda word: wordScoreByNextIterPoolSize(word, words) / wordScore(word)))

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

def wordScoreByNextIterPoolSize(guess:str, pool:list):
    '''
    Return a word score based on the spread of pool sizes from all possible patterns.
    Low value is good.
    '''
    
    res = []
    for p in allPatterns:
        s = getNextPoolSize(guess.upper(), pool, p)
        res.append(s)
    
    o = stdev(res)

    print(f"Word: {guess} | std_dev={o}")
    return o

def runWordleHelper():
    MAX_GUESSES = 6
    
    # DEFAULT_GUESS = 'CRANE'
    # DEFAULT_GUESS = 'SALET'
    # DEFAULT_GUESS = 'TRACE'
    # suggestions generated from all words
    SUGGESTIONS = ['RAISE', 'LATER', 'ARISE', 'LEAST', 'AROSE', 'IRATE', 'STARE', 'STORE', 'ALONE', 'ALERT']
    DEFAULT_GUESS = SUGGESTIONS[0]
    
    DEFAULT_PATTERN = "00000"
    remaining = pool
    currGuess = DEFAULT_GUESS
    currPattern = DEFAULT_PATTERN
    
    # first guess
    useDefault = input(f"Use default guess <{DEFAULT_GUESS}> ? (y/n)").upper()
    if useDefault != "Y":
        currGuess = inputFiveLetterWord()
    currPattern = inputPattern()

    # goal test
    if currPattern == "22222":
        # hit answer
        print(f"Answer found: {currGuess}")
        return
    
    # make first guess
    remaining = sortByFreqAndWordScore(list(filter(lambda word: fitPattern(currGuess, currPattern, word), remaining)))
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

        remaining = sortByFreqAndWordScore(list(filter(lambda word: fitPattern(currGuess, currPattern, word), remaining)))
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
        if not isPattern(result):
            continue
        break
    return result

def isPattern(pattern:str):
    return len(pattern) == 5 and set(pattern).issubset({'0', '1', '2'})

        
if __name__ == "__main__":
    runWordleHelper()
    input("Press enter to exit.")

    
   