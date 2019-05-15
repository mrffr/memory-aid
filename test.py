#!/usr/bin/env python3

import unittest
import memory_aid

class TestMemoryAid(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(1, 1)

    def test_import(self):
        self.assertEqual(memory_aid.import_questions('not_a_file'), None)
        self.assertNotEqual(memory_aid.import_questions('import_test.csv'), None)


if __name__ == '__main__':
    unittest.main()
