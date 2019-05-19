#!/usr/bin/env python3

import unittest
import os
from memory_aid import memory_aid as ma
from memory_aid import import_export as impexp
import datetime

class TestMemoryAid(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(1, 1)

    def test_import_export(self):
        dirname = os.path.dirname(__file__)

        self.assertEqual(impexp.import_questions_csv('not_a_file'), [])

        test_csv_file = os.path.join(dirname, 'import_test.csv')
        qs = impexp.import_questions_csv(test_csv_file)
        self.assertNotEqual(qs, [])

        # test exporting the questions to json
        test_json_file = os.path.join(dirname, 'test.json')
        self.assertEqual(impexp.export_questions_json(test_json_file, qs), True)

        # test loading the questions again
        loaded = impexp.load_questions_json(test_json_file)
        self.assertEqual(loaded, qs)

        self.assertEqual(impexp.load_questions_json('not_a_file'), [])

    def test_question(self):
        now = datetime.datetime.now()
        q = impexp.construct_question("q", "a", now)
        self.assertEqual(q['question'], "q")
        self.assertEqual(q['answer'], "a")
        self.assertEqual(q['next_time'], now)
        self.assertEqual(q['interval'], 0)
        self.assertEqual(q['ease'], 2.5)
        self.assertEqual(q['times_answered'], 0)
        self.assertEqual(q['tags'], [])

    def test_session(self):
        now = datetime.datetime.now().date()
        test_qs = [{'next_time': now, 'repetitions': 1}]
        self.assertEqual(ma.build_session_question_index(test_qs, now), [0])

    def test_filter_tags(self):
        now = datetime.datetime.now().date()
        test_qs = [impexp.construct_question("q","a",now,tags=["1","2"]),
                   impexp.construct_question("q2","a2",now,tags=["2"]),
                   impexp.construct_question("q3","a3",now,tags=["3"])]

        session_ind = ma.build_session_question_index(test_qs, now)
        self.assertEqual(ma.filter_tags(test_qs, session_ind, ["1"]), [0])
        self.assertEqual(ma.filter_tags(test_qs, session_ind, ["2"]), [0,1])
        self.assertEqual(ma.filter_tags(test_qs, session_ind, ["3"]), [2])
        self.assertEqual(ma.filter_tags(test_qs, session_ind, ["4","-1","1"]), [0])
        self.assertEqual(ma.filter_tags(test_qs, session_ind, ["4","-1","tech"]), [])
        self.assertEqual(ma.filter_tags(test_qs, session_ind, []), [0,1,2])
        self.assertEqual(ma.filter_tags([], [], []), [])

    def test_update_question(self):
        now = datetime.datetime.now()
        q = impexp.construct_question("q", "a", now)

        orig_q = dict(q) # copy dict for comparisons below

        # test we got it wrong
        q['ease'] = 3
        upd_q = ma.update_question(q, 0)
        self.assertEqual(upd_q['ease'], 2.2)
        self.assertEqual(upd_q['correct_run'], 0)
        self.assertEqual(upd_q['interval'], 0)

        # we got it right
        q = dict(orig_q) # reset question
        q['correct_run'] = 1
        upd_q = ma.update_question(q, 5)
        self.assertEqual(upd_q['ease'], 2.6)
        self.assertEqual(upd_q['correct_run'], 2)
        self.assertEqual(upd_q['interval'], 1)

        # right again
        upd_q = ma.update_question(q, 5)
        self.assertEqual(upd_q['ease'], 2.7)
        self.assertEqual(upd_q['correct_run'], 3)
        self.assertEqual(upd_q['interval'], 2)

        # wrong
        upd_q = ma.update_question(q, 2)
        self.assertEqual(upd_q['ease'], 2.38)
        self.assertEqual(upd_q['correct_run'], 0)
        self.assertEqual(upd_q['interval'], 0)




if __name__ == '__main__':
    unittest.main()
