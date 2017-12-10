#!/usr/bin/python3
# -*- coding: utf8 -*-

'''
Created on 8 dic. 2016

@author: Diego Hernando 
'''
import unittest

from io import StringIO
import sys 

sys.path.insert(0, '../')
from configReader import ConfigReader

class Test_ConfigReader(unittest.TestCase):


    def setUp(self):
        
        self.fTest=StringIO()
        self.sContentTest="""[Test]\n
        key1 = 2\n
        key2 = 1\n"""
        
        self.fTest.write(self.sContentTest)
        self.fTest.seek(0)
        self.configReader=ConfigReader(self.fTest,'Test')

    def tearDown(self):
        self.configReader.close()

    def testSections(self):
        listSections=['Test']
        self.assertEqual(self.configReader.getSections(),listSections,'Las secciones no son iguales')
        
    def testValues(self):
        dictValues={'key1':'2','key2':'1'}
        dictConfigReader=self.configReader.getAllValues()
        self.assertTrue(dictValues==dictConfigReader, 'Los valores no son iguales, correcto: '+dictValues.__str__()+\
                        '\n configReader: '+dictConfigReader.__str__())
    
    def testRemoveValue(self):
        self.assertTrue(self.configReader.removeValue('key1'))
        self.assertEqual(self.configReader.getValue('key1'), None, 'El elemento no ha sido borrado') 
        self.configReader.setValue('key1', '2')
        
        
    def testInsertValue(self):
        self.configReader.setValue('key3', '3')
        self.assertEqual(self.configReader.getValue('key3'), '3', 'El valor devuelto no es el mismo al introducido')
        
        self.configReader.removeValue('key3')
        
    def testModifyValue(self):
        self.configReader.setValue('key1', '10')
        self.assertEqual(self.configReader.getValue('key1'), '10', 'El valor devuelto no es el mismo al introducido')
        
        self.configReader.setValue('key1', '2')
        

    def testWriteTest(self):
        self.configReader.writeConfigFile()
        self.fTest.seek(0)
        
        sContentFile=self.fTest.read()
        
        self.assertEquals(sContentFile,self.sContentTest, 'El contenido del buffer que el original')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()