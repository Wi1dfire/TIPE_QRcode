from main import *
import structure as st
import unittest

# https://docs.python.org/3/library/unittest.html

class TestMyQrCode(unittest.TestCase):

    def test_upper(self):
        L = st.Gen_QRcode(29,True)
        n=len(L)-1
        alignement = st.alignment()
        L = st.insert(L,alignement,(n-8,n-8))
        c = cases_interdites(L)

        # Test whatever you want using asserts
        self.assertTrue(c)

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()