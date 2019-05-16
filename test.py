#!/usr/bin/env python3

import unittest
import memory_aid as ma
import datetime

class TestMemoryAid(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(1, 1)

    def test_import_export(self):
        self.assertEqual(ma.import_questions('not_a_file'), None)
        qs = ma.import_questions('import_test.csv')
        self.assertNotEqual(qs, None)

        # test exporting the questions to json
        self.assertEqual(ma.export_questions('test.json', qs), True)



    def test_question(self):
        now = datetime.datetime.now()
        q = ma.question("q", "a", now)
        self.assertEqual(q.question, "q")
        self.assertEqual(q.answer, "a")
        self.assertEqual(q.next_time, now)
        self.assertEqual(q.interval, 1)
        self.assertEqual(q.ease, 2.5)
        self.assertEqual(q.times_answered, 0)
        self.assertEqual(q.tags, [])


if __name__ == '__main__':
    unittest.main()
