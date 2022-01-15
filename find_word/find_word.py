import csv
import re
from pprint import pprint


def main():
    csv_file = open("./test_words.csv", "r")
    f = csv.reader(csv_file, delimiter=",")
    for row in f:
        words = row

    chara = input("探したい文字を入れてください: ")
    search = "^(?=.*" + ")(?=.*".join(chara) + ").*$"
    # ORの場合はre.search("f|t", word)の書き方ができるらしい
    print(search)

    match_words = []
    for w in words:
        if re.search(search, w):
            match_words.append(w)

    pprint(match_words, width=5)


if __name__ == "__main__":
    main()
