import sys

def main():
    with open(sys.argv[1]) as reader:
        lines = [line.split() for line in reader.readlines()]
        for line in lines:
            word = line[1][4:]
            print(line[1], word)

if __name__ == "__main__":
    main()