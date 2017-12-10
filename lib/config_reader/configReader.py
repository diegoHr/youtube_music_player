#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
Created on 7 dic. 2016

@author: Diego Hernando
https://wiki.python.org/moin/ConfigParserExamples
'''

import configparser
from io import StringIO
class ConfigReader(object):
    '''
    classdocs
    '''


    def __init__(self, streamFile, defaultSection='ConfigFile'):
        '''
        Constructor
        
        '''
        
        self.streamFile=StringIO()
        self.configParser=configparser.ConfigParser()
        sContentStream=streamFile.read()
        self.configParser.read_string(sContentStream)
        
        self.sSection=defaultSection
        if not self.sSection in self.configParser.sections():
            self.configParser.add_section(self.sSection)
            
        
           
           
    
    def getAllValues(self, sSection=None):
        if sSection==None:
            sSection=self.sSection
            
        iterKeys=self.configParser.options(sSection)
        dictValues=dict()
        for key in iterKeys:
            dictValues[key]=self.configParser.get(sSection,key)
            
            
        return dictValues
    
    def getValue(self,sKey,sSection=None):
        
        if sSection==None:
            sSection=self.sSection
        
        try:
            value=self.configParser.get(sSection, sKey)
        except Exception:
            value=None
        return value
    
    def getSections(self):
        return self.configParser.sections()    
    
    
    def getConfigStream(self):
        return self.streamFile
    
    def setValue(self,sKey,sValue, sSection=None):

        if sSection==None:
            
            sSection=self.sSection
        
        
        self.configParser.set(sSection,sKey,sValue)
            
        
    
    def removeValue(self,sKey, sSection=None):
        bExito=True
        if sSection == None :
            sSection=self.sSection
            
        
        try:
            self.configParser.remove_option(sSection, sKey)
        except Exception:
            bExito=False
            
        return bExito
    
    def writeConfigFile(self):
        
        if self.streamFile.closed:
            raise ValueError('I/O operation on closed file')
        self.streamFile.seek(0)
        
        self.configParser.write(self.streamFile)
        
        self.streamFile.flush()
        
    def close(self):
        if not self.streamFile.closed:
            self.streamFile.close()
    
    def closed(self):
        self.streamFile.closed
    
    