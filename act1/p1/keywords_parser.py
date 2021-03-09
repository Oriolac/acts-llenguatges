import keyword


def main():
    lines = keyword.kwlist
    words = ['\"' + line + '\"' for line in lines]
    macros_file = open('reserved.macros', 'w')
    regex_file = open('reserved.regex', 'w')
    for i, regex in enumerate(words):
        word = regex[1:-1]
        print(f"#define KEY_{word} {i+1}", file=macros_file)
        print(f"{word}\t\t\treturn KEY_{word};", file=regex_file)


if __name__ == "__main__":
    main()
