#!/usr/bin/env python3

import sys
import datetime
import random
import math
import argparse
from pathlib import Path

from . import import_export as impexp


# questions for this session are questions due <= today
# or new questions
# session list is index of question in master list
def build_session_question_index(all_qs, today):
    session_ind = []
    for i in range(len(all_qs)):
        q = all_qs[i]
        if q['next_time'] <= today or q['correct_run'] == 0:
            session_ind.append(i)

    print("Total questions available for this session:", len(session_ind))
    return session_ind

# filter the session cards based on the tags selected
# card is removed if it matches none of the tags
def filter_tags(all_qs, session_ind, tags):
    if tags == []:
        return session_ind

    new_ind = []
    for ind in session_ind:
        q = all_qs[ind]
        for tag in tags:
            if tag in q['tags']:
                new_ind.append(ind)
                break

    return new_ind

# update the question to set the next time we want to see it
def update_question(question, ease):
    question['times_answered'] += 1 # TODO this stat is unused

    # calculate new easiness for the question
    # based off past easiness
    ## TODO replace this with something else
    val = question['ease'] + (0.1 - (5.0 - ease) * (0.08 + (5.0 - ease) * 0.02))
    question['ease'] = max(1.3, val)

    # if we got it wrong then reset correct_run
    if ease < 3:
        question['correct_run'] = 0
    else:
        question['correct_run'] += 1

    # calculate the next interval to see the card
    if question['correct_run'] <= 1:
        question['interval'] = 0
    elif question['correct_run'] == 2:
        question['interval'] = 1
    elif question['correct_run'] == 3:
        question['interval'] = 3
    else:
        question['interval'] *= question['ease']

    # calculate the date based off the new interval
    # calculate today in here in case user has program open for a long time
    today = datetime.datetime.now().date()
    question['next_time'] = today + datetime.timedelta(days=math.ceil(question['interval']))

    return question

def ask_question(question):
    print("Q:", question['question'])
    if question['tags']:
        print("tags: ",*question['tags'])
    input()
    print("A:", question['answer'])

    # get ease of answer
    while True:
        inp = input('Ease [0..5] or (q)uit= ')

        if inp == 'q':
            return -1

        try:
            inp = int(inp)
        except:
            continue

        if inp < 0 or inp > 5:
            print(inp, "is not a valid choice")
            continue

        return inp

def print_startup(num_qs):
    print("Asking {} questions".format(num_qs))
    print("Rate the ease of answering each question as follows:")
    print("""5 - Perfect response
4 - Correct response after a hesitation
3 - Correct response recalled with serious difficulty
2 - Incorrect response; where the correct one seemed easy to recall
1 - Incorrect response; the correct one remembered
0 - Complete blackout""")
    print()

# ask the questions for this session and update based on answers
def session(all_qs, session_ind):
    if session_ind == []:
        return all_qs

    print_startup(len(session_ind))

    # ask the questions until no questions are due
    while True:
        still_due = []

        # ask due questions
        for ind in session_ind:
            q = all_qs[ind]
            ease = ask_question(q)

            # check for quitting
            if ease == -1:
                return all_qs

            # update question with results
            q = update_question(q, ease)
            all_qs[ind] = q

            # if interval is 0 then it is still due today
            if q['interval'] == 0:
                still_due.append(ind)

        # questions still due so continue loop
        if len(still_due) > 0:
            session_ind = still_due
            continue

        # if nothing is due then break
        break



    return all_qs

# handle importing questions
def importing_questions(fname, all_qs):
    imp_qs = impexp.import_questions_csv(fname)

    # none found then just return
    if imp_qs == []:
        return []

    # need to merge it with the original set of questions
    # TODO: duplicate question detection

    return all_qs + imp_qs

def get_user_dir():
    xdg_dir = Path.home().joinpath('.config', 'memory_aid')
    if Path.exists(xdg):
        return xdg_dir

    dirname = Path.home().joinpath('.memory_aid')

    if not Path.exists(dirname):
        Path.mkdir(dirname)
    return dirname

def main():
    # parse cmdline args
    parser = argparse.ArgumentParser(description='Memory helper/tester.')
    parser.add_argument('--tags',
                        nargs='*',
                        type=str,
                        help="Ask questions that match given tags.")
    parser.add_argument('--imp',
                        type=argparse.FileType('r'),
                        help="Import new questions from a given csv file.")
    args = parser.parse_args()

    # load in questions from user directory
    dirname = get_user_dir()

    question_file = dirname.joinpath('questions.json')

    all_qs = impexp.load_questions_json(question_file)

    # import questions from csv file, merge with existing questions
    # and then save to json
    # we import into existing or empty questions so do it here
    if args.imp:
        merged_qs = importing_questions(args.imp.name, all_qs)
        impexp.export_questions_json(question_file, merged_qs)
        print("Import Successful!")
        return

    # at this stage having no questions means something went wrong
    # since we aren't importing
    if all_qs == []:
        print("No questions were found try importing some questions first.")
        return

    # get questions for this session
    today = datetime.datetime.now().date()
    session_ind = build_session_question_index(all_qs, today)

    # filter questions that don't match desired tags
    tags = []
    if args.tags:
        tags = args.tags

    session_ind = filter_tags(all_qs, session_ind, tags)

    # shuffle the questions
    random.shuffle(session_ind)

    all_qs = session(all_qs, session_ind)

    impexp.export_questions_json(question_file, all_qs)


if __name__ == "__main__":
    main()
