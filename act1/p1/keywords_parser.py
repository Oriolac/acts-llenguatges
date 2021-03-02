import keyword

def main():
    lines = keyword.kwlist
    words = ['(\"' + line + '\")' for line in lines]
    print(f"{'|'.join(words)}" + " {RESERVED_KEYWORD++;}", end='')

if __name__ == "__main__":
    main()