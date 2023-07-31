# -*- coding: UTF-8 -*-.
import unittest
import json
import os
import runpy

try:
    import dictdiffer

    def printdiff(dict_1, dict_2):
        """
        This is an utility for showing the difference line by line of two
        dictionaries.
        """
        for diff in list(dictdiffer.diff(dict_1, dict_2)):
            print(diff)


except ImportError:
    # pip install dictdiffer
    pass
# unittest.util._MAX_LENGTH=500000
# python -m unittest tests.py -v

prj_dir = os.getcwd()
example_dir = os.path.join(prj_dir, "examples")

from unittest import TestCase

examplesList = [i for i in os.listdir(example_dir) if i.endswith(".py")]

class TestDemonstrateSubtest(TestCase):
    def test_examples(self):
        for example in examplesList:
            with self.subTest(msg=f"Error in {example}"):
                examplePath = os.path.join(example_dir,example)
                var = runpy.run_path(examplePath)
                reference = var['r']
                output = var['anno'].to_json()
                self.assertDictEqual(output,reference)

if __name__ == "__main__":
    unittest.main()
