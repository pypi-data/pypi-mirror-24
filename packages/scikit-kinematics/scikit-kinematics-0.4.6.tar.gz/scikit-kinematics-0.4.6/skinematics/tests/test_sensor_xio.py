
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '..', '..'))

import unittest
from skinematics import imus
from time import sleep

class TestSequenceFunctions(unittest.TestCase):
    
    def test_import_xio(self):
        # Get data, with a specified input from an XIO system
        inFile = os.path.join(myPath, 'data', 'data_xio', '00033_CalIntertialAndMag.csv')
        data = imus.import_data(inFile, inType='xio', paramList=['rate', 'acc', 'omega', 'mag'])
        rate = data[0]
        acc = data[1]
        omega = data[2]
        
        self.assertAlmostEqual((rate - 256), 0)
        self.assertAlmostEqual( (omega[0,2] -10.125), 0)
        
if __name__ == '__main__':
    unittest.main()
    print('Thanks for using programs from Thomas!')
    sleep(2)
