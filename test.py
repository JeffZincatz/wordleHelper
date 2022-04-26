from wordleSolver import fitPattern

def test_fp(tests:tuple):
    for i, (inputWord, pattern, word) in enumerate(tests):
        res = fitPattern(inputWord, pattern, word)
        if res:
            print(f"Test case {i}: Passed.")
        else:
            print(f"Test case {i}: Failed. Input: {inputWord}. Pattern: {pattern}. Word: {word}.")



if __name__ == "__main__":
    tests = (('SHOOT', '22200', 'SHOWN'), ('SHOOT', '22200', 'SHOWN'))
    test_fp(tests)