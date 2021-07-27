import unittest
from loginPage import *

class testToTuple(unittest.TestCase):
    def testTuple(self):
        # Make sure the tuple protects against bad params
        self.assertEqual(toTuple('05/04/2020', 'Name1', 568, 942, 'text'), ('05/04/2020', 'Name1', '$568.00', '$942.00', '-$374.00', 'text'))
        self.assertEqual(toTuple('06/31/2021', 'Name2', 6, 6), ('06/31/2021', 'Name2', '$6.00', '$6.00', '$0.00', ""))
        self.assertEqual(toTuple('06/31/2021', 57, 6400000, 70.634), ('06/31/2021', '57', '$6,400,000.00', '$70.63', '$6,399,929.37', ""))

    def testGrabDate(self):
        self.assertEqual(grabDate('05/25/2021'), ['05', '25', '2021'])
        self.assertEqual(grabDate('12/01/1944'), ['12', '01', '1944'])
        self.assertEqual(grabDate('01/04/1008'), ['01', '04', '1008'])
    
    def testUpdateTable(self):
        self.assertEqual(updateTable('06'), 0)
        self.assertEqual(updateTable('13'), -1)
        self.assertEqual(updateTable('hello'), -1)
        self.assertEqual(updateTable(False), -1)

    def testEmailCheck(self):
        self.assertEqual(check("test@mail.com"), True)
        self.assertEqual(check("hello"), False)
        self.assertEqual(check("x@y.c"), False)
        self.assertEqual(check("ReallyLongStringForANormalEmailIGuess@mail.com".lower()), True)
        self.assertEqual(check("ReallyLongStringForANormalEmailIGuess@mail.com"), False)

    def testUpperCheck(self):
        self.assertEqual(uppercase_check("Hello"), True)
        self.assertEqual(uppercase_check("dadesfesfllo"), False)
        self.assertEqual(uppercase_check("344775ujda76u"), False)
        self.assertEqual(uppercase_check("SEOFJEOIF"), True)
        self.assertEqual(uppercase_check("Turtles07"), True)   
        
    def testLowerCheck(self):
        self.assertEqual(lowercase_check("Hello"), True)
        self.assertEqual(lowercase_check("dadesfesfllo"), True)
        self.assertEqual(lowercase_check("4U64TW5G5"), False)
        self.assertEqual(lowercase_check("SEOFJEOIF"), False)
        self.assertEqual(lowercase_check("Turtles07"), True)

        
    def testDigitCheck(self):
        self.assertEqual(digit_check("Hello"), False)
        self.assertEqual(digit_check("dadesfesfllo"), False)
        self.assertEqual(digit_check("4U64TW5G5"), True)
        self.assertEqual(digit_check("SEOFJEOIF5"), True)
        self.assertEqual(digit_check(""), False)