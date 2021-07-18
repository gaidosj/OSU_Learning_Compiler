import parent_dir
import unittest
from src import hello


class TestCase(unittest.TestCase):

    def test1(self):
        out = "Hello"
        self.assertEqual(hello.hello(), out)

    def test2(self):
        out = "Goodbye"
        self.assertNotEqual(hello.hello(), out)

    def test3(self):
        out = "testpull"
        self.assertNotEqual(hello.hello(), out)


if __name__ == '__main__':
    unittest.main()
