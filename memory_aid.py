#!/usr/bin/env python3

import sys
import csv
import datetime

class question:
    def __init__(self, q, a, next_time,
                 interval = 1, ease = 2.5,
                 times_answered = 0, tags = []):
        self.question = q
        self.answer = a

        self.next_time = next_time
        self.interval = interval
        self.ease = ease

        self.times_answered = times_answered
        self.tags = tags


class deck:
    def __init__(self):
        self.questions = []


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

    # get the time now
    now = datetime.datetime.now()

    # import each question
    questions = []
    count = 0
    for line in csvr:
        # question format is q, a, [tags, ]
        if len(line) < 2 or len(line) > 3:
            continue
        # found a question
        count += 1
        q, a, *tags = line
        print("Found:", q, a, tags)

        new_q = question(q, a, now, tags = tags)
        questions.append(new_q)

    f.close()

    print("Import successful:", count, "new questions found.")

    return questions

def export_questions(fname):
    pass

def main():
    pass

if __name__ == "__main__":
    main()
