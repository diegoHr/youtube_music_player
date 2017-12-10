#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
Created on 17 dic. 2016
ad
@author: Diego Hernando Revenga
'''
import sys
from os.path import sep


sys.path.append("."+sep+"vlc")

from vlc import vlc
import time
from threading import Thread, Lock
import random



class Player(object):
    '''
    classdocs
    '''


    def __init__(self, isPlayInLoop=True, isPlayRandom=False):
        '''
        Constructor
        '''
        random.seed(time.clock())
        self._vlcBinding=vlc.MediaPlayer()
        self._listPlayables=[]
        self._iIndexPlay=0
        self._playable=False
        self._isPlayInLoop=isPlayInLoop
        self._isPlayRandom=isPlayRandom
        self._processAudioNext=None
        self._bEndAudioProcess=False
        self._lockbEndAudioProcess=Lock()
        
        self._isPaused=False
        self._lockIsPaused=Lock()
        

    def addPlayable(self,sPath):
        self._listPlayables.append(sPath)
        self._randomizeIndexToPlay()
        
        self._playable=True
        
    
    def playByIndex(self,iIndex):
        self._iIndexPlay=iIndex
        self.play()
        
    def play(self):
      
        if self._playable:
            
            self._vlcBinding.set_mrl(self._listPlayables[self._iIndexPlay])
            self._vlcBinding.play()
            print('Playing '+self._listPlayables[self._iIndexPlay])
            self._setIsPaused(False)
            
            self._setEndAudioProcess(False)                                                                  
            self._processAudioNext=Thread(name='processAudioNext',target=self._nextAudioFromList)
            self._processAudioNext.start()
            
 
    def _nextAudioFromList(self):
        time.sleep(10)
        while self.isPlaying() or self.isPaused():
            time.sleep(3)
                
        self._updateIndexToPlay()
        if len(self._listPlayables)>self._iIndexPlay:
            self._playable=True
            
        else:
            self._finishAudioList()
        if(not self._bGetEndAudioProcess()):
            self.stop()
            self.play()
    
    def _randomizeIndexToPlay(self):
        if self._isPlayRandom:
            iRandomIndex=random.randint(0,len(self._listPlayables)-1)
            if len(self._listPlayables)>1 and iRandomIndex==self._iIndexPlay:
                self._randomizeIndexToPlay()
            self._iIndexPlay=iRandomIndex      
    def _updateIndexToPlay(self):
         
        if self._isPlayRandom:
            self._randomizeIndexToPlay()
        else:
            self._iIndexPlay=self._iIndexPlay+1
        
        
    def _finishAudioList(self):
        if self._isPlayInLoop:
            self._playable=True
            self._iIndexPlay=0
        else:
            self._playable=False
    
    def stop(self):
        self._setEndAudioProcess(True)
        self._vlcBinding.stop()
        
    
    def pause(self):
        self._setIsPaused(not self.isPaused())
        self._vlcBinding.pause()
        
    
    def goTo(self, iPercentage):
        iPercentage=iPercentage/100
        self._vlcBinding.set_position(iPercentage)
    
    def _setIsPaused(self, isPaused):
        def callbackSetIsPaused():
            self._isPaused=isPaused
        self._execLockedOperation(self._lockIsPaused, callbackSetIsPaused)
    def isPaused(self):
        return self._getLockedVar(self._lockIsPaused, self._isPaused)
        
    def _bGetEndAudioProcess(self):
        return self._getLockedVar(self._lockbEndAudioProcess, self._bEndAudioProcess)
    
    def _setEndAudioProcess(self, bEndAudioProcess):
        def callbackSetEndAudioProcess():
            self._bEndAudioProcess=bEndAudioProcess
        self._execLockedOperation(self._lockbEndAudioProcess, callbackSetEndAudioProcess)
 
        
    def _execLockedOperation(self,lock,callbackOperation):
        lock.acquire()
        callbackOperation()
        lock.release()
    
    def _getLockedVar(self,lock,var):
        lock.acquire()
        copyVar=var
        lock.release()
        return copyVar    
    
    def isPlaying(self):
        return bool(self._vlcBinding.is_playing())
    
    def __str__(self):
        sMessage=''
        try:
            sMessage= 'Now is playing '+ self._listPlayables[self._iIndexPlay]
        except IndexError:
            sMessage='Not exist media to play\n'
            
        return sMessage
    
    def getListAudios(self):
        return self._listPlayables
    def playingStatus(self):
        while(self._playable):
            time.sleep(3)
            print(self)
if __name__ == "__main__":
    
    s=Player()    
    print ('Player console mode:')
    
    sInput=''
    while(sInput!='end'):
        sInput=input()
        if(sInput=='status'):
            print(s)
        elif(sInput=='add'):
            sInput=input('Write path of media to play:')
            s.addPlayable(sInput)
        elif(sInput=='play'):
            s.play()
        elif(sInput=='stop'):
            s.stop()
        elif (sInput=='isPlaying'):
            print(s.playingStatus())
        elif(sInput=='pause'):
            s.pause()
        elif(sInput=='changeTime'):
            sInput=input('Write percentage of time where you want to go:')
            s.goTo(sInput)
        elif (sInput=='changeMedia'):
            listPathAudios=s.getListAudios()
            for index in range(len(listPathAudios)):
                print(str(index)+') '+listPathAudios[index]+'\n')
                
            def inputIndex ():
                sInput=input('Write the audio index:')
                bExit=True
                try:
                    iIndex= int(sInput)
                    if iIndex>= len(listPathAudios):
                        bExit=False
                except ValueError:
                    bExit=False
                
                if bExit:
                    return iIndex
                else:
                    print ('You only can write the index numbers of the list.\n')
                    return inputIndex()
                     
            s.playByIndex(inputIndex())
        
                
            
    
        
