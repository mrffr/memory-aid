#!/usr/bin/env python3

import sys
import csv

# import questions from csv file and return list of questions
# questions are in format: q,a
def import_questions(fname):
    print("Importing questions from", fname)

    try:
        f = open(fname, 'r')
    except OSError as e:
        print("Import failed:", e)
        return None

    csvr = csv.reader(f)

    # import each question
    questions = []
    count = 0
    for line in csvr:
        # question format is q, a
        if len(line) != 2:
            continue
        # found a question
        count += 1
        q, a = line
        print("Found:", q, a)

        questions.append([q,a])

    f.close()

    print("Import successful:", count, "new questions found.")

    return questions

def export_questions(fname):
    pass

def main():
    pass

if __name__ == "__main__":
    main()
