#!/usr/bin/env python3

import sys
import datetime
import random
import math
from import_export import *


# questions for this session are questions due <= today
# or new questions
# session list is index of question in master list
def build_session_question_index(all_qs, today):
    session_ind = []
    for i in range(len(all_qs)):
        q = all_qs[i]
        if q['next_time'] <= today or q['repetitions'] == 0:
            session_ind.append(i)

    print("Questions available this session:", len(session_ind))
    return session_ind

# filter the session cards based on the tags selected
def filter_tags(all_qs, session_ind, tags):
    new_ind = []
    for ind in session_ind:
        q = all_qs[ind]
        for tag in tags:
            if tag in q['tags']:
                new_ind.append(ind)
    return new_ind

# update the question to set the next time we want to see it
def update_question(question, ease):
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
        question['interval'] = 1
    elif question['correct_run'] == 2:
        question['interval'] = 2
    else:
        question['interval'] *= question['ease']

    # calculate the date based off the new interval
    # calculate today in here in case user has program open for a long time
    today = datetime.datetime.now().date()
    question['next_time'] = today + datetime.timedelta(days=math.ceil(question['interval']))

    return question

def ask_question(question):
    print("Q:", question.question)
    input()
    print("A:", question.answer)

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

# ask the questions for this session and update based on answers
def session(all_qs, session_ind):
    print("Asking {} questions".format(len(qs)))
    print("Rate the ease of answering each question as follows:")
    print("""5 - Perfect response
4 - Correct response after a hesitation
3 - Correct response recalled with serious difficulty
2 - Incorrect response; where the correct one seemed easy to recall
1 - Incorrect response; the correct one remembered
0 - Complete blackout""")

    # ask the questions
    for ind in session_ind:
        q = all_qs[ind]
        ease = ask_question(q)

        # check for quitting
        if ease == -1:
            return all_qs

        # update question with results
        q = update_question(q, ease)

        all_qs[ind] = q


    return all_qs

def main():
    all_qs = load_questions_json('test.json')

    # get questions for this session
    today = datetime.datetime.now().date()
    session_ind = build_session_question_index(all_qs, today)

    session_ind = filter_tags(all_qs, session_ind, tags)

    # shuffle the questions
    random.shuffle(session_ind)

    all_qs = session(all_qs, session_ind)

    export_questions_json('test2.json', all_qs)


if __name__ == "__main__":
    main()
