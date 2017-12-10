'''
Created on 10 dic. 2016

@author: diego
'''
import unittest
from io import StringIO
import sys 

sys.path.insert(0, '../')
from listReader import ListReader

class Test_ListReader(unittest.TestCase):


    def setUp(self):
        self.fTest=StringIO()
        self.sContentTest="""Line1
        Line2
         #Comment
        """
        
        self.fTest.write(self.sContentTest)
        self.fTest.seek(0)
        self.configReader=ListReader(self.fTest)


    def tearDown(self):
        self.configReader.close()


    def testGetAllElements(self):
        
        listConfig=self.configReader.getAll()
        listCorrect=['Line1','Line2']
        self.assertEqual(listConfig,listCorrect,'La lista de elementos recibida no se corresponde con el fichero leido')
    
    def testGetElement(self):
        self.assertEqual(self.configReader.get(0), 'Line1', 'El primer elemento de la lista no es Line1')
        
    def testAddRemoveElement(self):
        self.configReader.add('Line3')
        self.assertTrue('Line3' in self.configReader,'Line3 no ha sido insertado ')
        self.configReader.remove('Line3')
        self.assertFalse('Line3' in self.configReader,'Line3 no ha sido borrado')
        
    def testQuitComments(self):
        self.assertFalse(' #Comment' in self.configReader,'No ha suprimido los comentarios al leer el archivo de configuración')
    
    
    def testWriteFile(self):
        self.configReader.write()
        self.fTest.seek(0)
        
        configProbe=ListReader(self.fTest)
        
        
        self.assertEqual(self.configReader.getAll(), configProbe.getAll(), 'El fichero original no se corresponde con el escrito')    
    
    def testWriteTwoTimes(self):
        self.testWriteFile()
        self.configReader.add('Line3')
        self.testWriteFile()
        self.configReader.remove('Line3')    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()