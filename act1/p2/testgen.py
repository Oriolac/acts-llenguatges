import random
import sys

def main(filename):
    abc_range = range(ord('Z') - ord('A') + 1)
    lits = list(map(chr, (ord('A') + acc for acc in abc_range)))
    tokens = lits + list("!^∨()") + ['->', '<->']
    filewriter = open(filename, "w")
    for _ in range(500):
        token = lambda : tokens[random.randrange(len(tokens))]
        line = ' '.join([token() for _ in range(random.randrange(20, 30))])
        if (random.random() < 0.2):
            line += " # That's a comment! "
        print(line, file=filewriter)
    filewriter.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit()
    main(sys.argv[1])