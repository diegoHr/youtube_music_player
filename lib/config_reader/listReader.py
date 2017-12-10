#!/usr/bin/python3
# -*- coding: utf8 -*-

'''
Created on 10 dic. 2016

@author: Diego Hernando Revenga
'''

class ListReader(object):
    '''
    classdocs
    '''


    def __init__(self, bufferFile):
        '''
        Constructor
        '''
        self._bufferFile=bufferFile
        
        self._listElements=self._readListElementsFromBuffer(bufferFile)

        self._listElementsToWrite=[]
        
        
        
    def _readListElementsFromBuffer(self,bufferFile):
        
        listLinesFile=bufferFile.readlines()
        listElements=[]

        index=0;
        for sLine in listLinesFile:
            if len(sLine.strip())>0:
                if sLine.strip()[0]!='#':
                    sLine=self._formatLine(sLine)
                    listElements.append(sLine)
                
            index=index+1
        return listElements
    
    def _formatLine(self, sLine):
        if (sLine[-1]=='\n'):
            sLine=sLine[0:-1]
        
        sFormatLine=''
        for index in range(len(sLine)-1):
            if ' ' != sLine[index] and '\t' != sLine[index]:
                sFormatLine=sLine[index:]
                break
        return sFormatLine
                
                
            
            
        
    def add(self,sElement):
        try:
            self._listElementsToWrite.append(sElement)
            self._listElements.append(sElement)
        except Exception as e:
            raise e
    
    def remove(self,sElement):
        try:
            self._listElements.remove(sElement)
            if sElement in self._listElementsToWrite:
                self._listElementsToWrite.remove(sElement)
        except Exception as e:
            raise e
        
    def get(self, index):
        return self._listElements[index]
    
    def getAll(self):
        return self._listElements
    
    def write(self):
        
        self._bufferFile.seek(0)
        iPos=self._bufferFile.seek(2)
        self._bufferFile.seek(iPos)
        
        sEndFile=self._bufferFile.read()
        if sEndFile !='\n':
            self._bufferFile.write('\n')
        
        for sElementToWrite in self._listElementsToWrite:
            self._bufferFile.write(sElementToWrite+'\n')
        
        self._bufferFile.flush()
        self._listElementsToWrite=[]
        
        
    
        
        
        
    def close(self):
        if not self._bufferFile.closed:
            self._bufferFile.close()  
    
    def closed(self):   
        return self._bufferFile.closed
    
    def __contains__(self,element):
        return element in self._listElements