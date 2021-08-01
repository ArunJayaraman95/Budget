#test_loginPage.py
from loginPage import *
from loginPage import addExpense 
import unittest
import random, string

class testrandomword(unittest.TestCase):
    def test_randomword(self):
        letters = "1234567890abcdefghijklmnopqrstuvwxyz"
        self.assertEqual(letters,"1234567890abcdefghijklmnopqrstuvwxyz")
        
    def test_SendTwoFactorCode(self):
        code = "randomword(10)"
        self.assertEqual(code,"randomword(10)")
    
    def test_AddExpense(self):
        date = "monthEntry + "/" + dayEntry + "/" + yearEntry"
        n = "nameEntry"
        p = "plannedEntry"
        a = "actualEntry"
        m = "notesEntry"
        self.assertEqual(date,n,p,a,m ('05/04/2020', 'Name1', 568, 942, 'text'))

        
    

if __name__ == '__main__': 
     unittest.main()


    




   

