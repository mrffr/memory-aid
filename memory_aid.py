#!/usr/bin/env python3

import sys
import datetime
import random
from import_export import *


# questions for this session are questions due <= today
# or new questions
# session list is index of question in master list
def build_session_questions(all_qs, today):
    session_ind = []
    for i in range(len(all_qs)):
        q = all_qs[i]
        if q['next_time'] <= today or q['repetitions'] == 0:
            session_ind.append(i)

    print("Questions available this session:", len(session_ind))
    return session_ind

def update_question(all_qs, index, ease):
    pass

def ask_question(q):
    print("Q:", q.question)
    input()
    print("A:", q.answer)

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
        ease = ask_question(all_qs[ind])

        # check for quitting
        if ease == -1:
            return all_qs

        update_question(all_qs, ind, ease)


    return all_qs

def main():
    all_qs = load_questions_json('test.json')

    # get questions for this session
    today = datetime.datetime.now().date()
    session_ind = build_session_questions(all_qs, today)

    # shuffle the questions
    random.shuffle(session_ind)

    all_qs = session(all_qs, session_ind)

    pass

if __name__ == "__main__":
    main()
