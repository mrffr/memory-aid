#!/usr/bin/env python3

import unittest
import memory_aid as ma
import datetime

class TestMemoryAid(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(1, 1)

    def test_import_export(self):
        self.assertEqual(ma.import_questions_csv('not_a_file'), None)
        qs = ma.import_questions_csv('import_test.csv')
        self.assertNotEqual(qs, None)

        # test exporting the questions to json
        self.assertEqual(ma.export_questions_json('test.json', qs), True)

        # test loading the questions again
        loaded = ma.load_questions_json('test.json')
        self.assertEqual(loaded, qs)

        self.assertEqual(ma.load_questions_json('not_a_file'), None)

    def test_question(self):
        now = datetime.datetime.now()
        q = ma.construct_question("q", "a", now)
        self.assertEqual(q['question'], "q")
        self.assertEqual(q['answer'], "a")
        self.assertEqual(q['next_time'], now)
        self.assertEqual(q['interval'], 1)
        self.assertEqual(q['ease'], 2.5)
        self.assertEqual(q['times_answered'], 0)
        self.assertEqual(q['tags'], [])

    def test_session(self):
        now = datetime.datetime.now().date()
        test_qs = [{'next_time': now, 'repetitions': 1}]
        self.assertEqual(ma.build_session_question_index(test_qs, now), [0])


if __name__ == '__main__':
    unittest.main()
