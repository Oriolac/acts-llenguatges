import sys

def main():
    result, correct = sys.argv[1:3]
    resultf = open(result, "r")
    correctf = open(correct, "r")
    numline = 0
    errors = 0
    for line1, line2 in zip(resultf.readlines(), correctf.readlines()):
        if line1[-1] == '\n':
            line1 = line1[:-1]
        if line2[-1] == '\n':
            line2 = line2[:-1]
        if line1 != line2:
            errors += 1
            print(f"Error line {numline}.")
            print(f"\tExpected:\n\t\t{line2}\n\tbut was\n\t\t{line1}")
        numline += 1
    print(f"Errors: {errors}")
    resultf.close()
    correctf.close()

if __name__ == "__main__":
    main()