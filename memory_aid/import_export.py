#!/usr/bin/env python3

import csv
import copy
import json
import datetime
import sys

# question is dictionary of key values
# returns base question
def construct_question(q, a, next_time, tags = []):
    return {
        "question" : q,
        "answer" : a,

        "next_time" : next_time, # date
        "interval" : 1, # in days
        "ease" : 2.5,
        "correct_run": 0,

        "times_answered" : 0,
        "tags" : tags
        }


# import questions from csv file and return list of questions
# questions are in format: q,a
def import_questions_csv(fname):
    print("Importing questions from", fname)

    try:
        f = open(fname, 'r')
    except OSError as e:
        print("Import failed:", e)
        return []

    csvr = csv.reader(f)

    # get the date
    today = datetime.datetime.now().date()

    # import each question
    questions = []
    for line in csvr:
        # question format is q, a, [tags, ]
        if len(line) < 2:
            continue

        # found a question
        q, a, *tags = line
        print("Found:", q, a, tags)

        # create question and add to question list
        new_q = construct_question(q, a, today, tags = tags)
        questions.append(new_q)

    f.close()

    print(len(questions), "new questions found.")

    return questions

# export questions to json file
def export_questions_json(fname, questions):
    if questions == []:
        return False

    try:
        f = open(fname, 'w')
    except OSError as e:
        print("Export failed:", e)
        return False

    # create copy of questions to handle
    # converting datetime object to a formatted string for json
    temp_q = copy.deepcopy(questions)
    for q in temp_q:
        q['next_time'] = q['next_time'].strftime("%Y-%m-%d")

    # write to file
    json.dump(temp_q, f)

    f.close()
    return True

# load questions from json file
def load_questions_json(fname):
    # read in json file
    try:
        f = open(fname, 'r')
    except OSError as e:
        print("Loading failed:", e)
        return []

    json_file = json.load(f)
    f.close()

    # convert time string to datetime object
    qs = []
    for q in json_file:
        q['next_time'] = datetime.datetime.strptime(q['next_time'], "%Y-%m-%d").date()
        qs.append(q)

    print("Load successful:", len(qs), "questions loaded.")

    return qs
