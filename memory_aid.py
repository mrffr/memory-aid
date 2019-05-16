#!/usr/bin/env python3

import sys
import datetime
import random
from import_export import *


# questions for this session are questions due <= today
# or new questions
def build_session_questions(all_qs, today):
    session = []
    for q in all_qs:
        if q['next_time'] <= today or q['repetitions'] == 0:
            session.append(q)

    print("Questions available this session:", len(session))
    return session

def ask_questions(qs):
    # shuffle the questions
    random.shuffle(qs)

    print("Asking {} questions".format(n))
    print("Rate the ease of answering each question as follows:")
    print("""5 - perfect response
4 - correct response after a hesitation
3 - correct response recalled with serious difficulty
2 - incorrect response; where the correct one seemed easy to recall
1 - incorrect response; the correct one remembered
0 - complete blackout.""")

    pass

def main():
    all_qs = load_questions_json('test.json')

    # get questions for this session
    today = datetime.datetime.now().date()
    session_qs = build_session_questions(all_qs, today)

    ask_questions(session_qs)

    pass

if __name__ == "__main__":
    main()
