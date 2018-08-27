# -*- coding: utf-8 -*-

import unittest

@unittest.skip("Have not yet added doctests to Readme")
class DocumentationTest(unittest.TestCase):
    def test_readme(self):
        [failure_count, return_count] = doctest.testfile("../README.md")
        self.assertEqual(failure_count, 0)
