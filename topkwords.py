import sys

def findTopKWords(input, k, output):

    wordcnt = {}

    with open(input) as f:
        for ln in f:
            ln = ln.lower().rstrip('\n')
            wordcnt = recsplit(ln, wordcnt, ' .,?;!-()' )
            # print("# WARNING: Running Word Count: ", wordcnt)

    sortedWords = sorted(wordcnt.items(),reverse=True,key=lambda tup: tup[1]) #sorted by value instead of key

    of = open(output, 'w+')
    of2 = open('finalwordcount.txt', 'w+')
    j = 0
    for wc in sortedWords:

        w = wc[0]
        c = wc[1]

        ln =  w + " " + str(c) + "\n"

        of2.write(ln)

        if j < k:
            of.write(ln)

        #at at kth word check if there are other words with same count
        if j == (k-1):
            cap = c

        if j >= k and cap == c:
            of.write(ln)

        j += 1

    of.close()
    of2.close()

def replaceAndSplit(s):
    """Pass a string s that contains only lower alphabetical characters"""

    punc = [' ', '.', ',', '?', ';', '!', '-', '(', ')']
    legalwords = []

    for e in punc:
        s = s.replace(e, 'X')

    # print("After the replace(): ", s)

    splitwords = s.split('X')
    for w in splitwords:
        if w.isalpha():
            legalwords.append(w)

    # print("legalwords = ", legalwords)

    return legalwords

def recsplit(s, wordcnt, seps):

    """"Parameter seps may be a string or list"""

    if len(seps) == 1:
        splitString = s.split(seps)
        print("******Split String: ", splitString)
        for spstr in splitString:
            if spstr.isalpha():
                if spstr in list(wordcnt):
                    wordcnt[spstr] += 1
                else:
                    wordcnt[spstr] = 1

        return wordcnt

    else:
        seps2 = seps[1:3]

        if len(seps2) > 1:
            currSep = seps[0]
            nextSep = seps[1]
        else:
            currSep = seps
            nextSep = ''

        splitString = s.split(currSep)
        print("Split String: ", splitString)

        for spstr in splitString:
            if spstr.isalpha():
                if spstr in list(wordcnt):
                    wordcnt[spstr] += 1
                else:
                    wordcnt[spstr] = 1
                splitString.remove(spstr)

        s = nextSep.join(splitString)

        return recsplit(s, wordcnt, seps[1:])

if __name__ == "__main__":

    args = sys.argv[1].split(';')

    if len(args) > 3:
        raise SyntaxError("Too many arguments")
    if len(args) < 3:
        raise SyntaxError("Not enough arguments")
    else:
        kw_args = {}
        for s in args:
            a = s.split("=")
            if a[0] in ('input', 'k', 'output'):
                kw_args[a[0]] = a[1]
            else:
                msg = 'Invalid argument keywords: ' + '***' + a[0] + '***' + ' not a keywords'
                raise SyntaxError(msg)

        try:
            int(kw_args['k'])
        except ValueError:
            raise ValueError("k must be an positive integer")

        findTopKWords(kw_args['input'], int(kw_args['k']), kw_args['output'])
