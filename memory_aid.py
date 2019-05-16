#!/usr/bin/env python3

import sys
import csv
import datetime
import json


# question is dictionary of key values
def construct_question(q, a, next_time,
                       interval = 1, ease = 2.5,
                       times_answered = 0, tags = []):
    return {
        "question" : q,
        "answer" : a,

        "next_time" : next_time,
        "interval" : interval, # in days
        "ease" : ease,

        "times_answered" : times_answered,
        "tags" : tags
        }


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

    # get the date
    now = datetime.datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0) # day

    # import each question
    questions = []
    for line in csvr:
        # question format is q, a, [tags, ]
        if len(line) < 2 or len(line) > 3:
            continue

        # found a question
        q, a, *tags = line
        print("Found:", q, a, tags)

        # create question and add to question list
        new_q = construct_question(q, a, now, tags = tags)
        questions.append(new_q)

    f.close()

    print("Import successful:", len(questions), "new questions found.")

    return questions

# export questions to json file
def export_questions(fname, questions):
    try:
        f = open(fname, 'w')
    except OSError as e:
        print("Export failed:", e)
        return False

    # convert datetime object to isoformat for json serizlization
    # https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    def serial_helper(obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        raise TypeError("Type {} is not serializable".format(type(obj)))

    f.write(json.dumps(questions, default=serial_helper))


    f.close()

    return False

# load questions from json file
def load_questions(fname):
    # read in json file
    try:
        f = open(fname, 'r')
    except OSError as e:
        print("Loading failed:", e)

    json_file = json.load(f)
    f.close()


    pass

def main():
    pass

if __name__ == "__main__":
    main()
