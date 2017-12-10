#!/usr/bin/python3
#coding: utf-8

import sys
from os.path import sep

sys.path.append("."+sep+"lib")
sys.path.append("."+sep+"lib"+sep+"config_reader")

'''
Created on 7 dic. 2016

@author: Diego Hernando Revenga
'''


import logging

import os.path
import pafy
import threading

from configReader import ConfigReader
from lib.Player import Player
from listReader import ListReader

listTrueValues=['true', '1', 't', 'y', 'yes', 'True', 'TRUE']

class YoutubePlayerList(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        logging.basicConfig(level=logging.DEBUG)
        self._path='./youtubePlayer.config'
        self._sSection='youtubePlayerConfiguration'
        
        self.configReader=self._getConfigReader()
        self._sAudioFolder=self.configReader.getValue('audioFolder')
        self._sUrlFile=self.configReader.getValue('urlFile')
        
        sPlayingLoop=self.configReader.getValue('loop')
        bPlayingLoop=sPlayingLoop in listTrueValues
        
        sPlayingRandom=self.configReader.getValue('random')
        bPlayingRandom=sPlayingRandom in listTrueValues
        
        self.listUrl=self._getListUrlFromDisk(self._sUrlFile)
        
        self.listUrl=self._parseListUrl(self.listUrl)
        
        self.bIsPlaying=False
        self._player=Player(isPlayInLoop=bPlayingLoop,isPlayRandom=bPlayingRandom) 
        
        #self._iChunk= 1024
        
        threadDownloader=ThreadDownloader(self.listUrl,self._sAudioFolder, self.initPlayingMedia,self._player.addPlayable,self._writeListUrlInDisk)
        threadDownloader.start()
        
        
    
        
            
    
    def _parseListUrl(self,listUrl):
        
        listUrlFolder=[]
        for sUrl in listUrl:
            listElementsUrl=sUrl.split('--')
            if(len(listElementsUrl)>=3):
                sPath=listElementsUrl[1]
                isList='list'==listElementsUrl[2]
            else:
                sPath=None
                isList=False
            listUrlFolder.append({'url':listElementsUrl[0],'path':sPath,'isList':isList})
        return listUrlFolder
            
    def initPlayingMedia(self):
        if(self._player._playable and not self.bIsPlaying):
            self.bIsPlaying=True
            self._player.play()    

    def _genConfigFile(self):
        fConfigFile = open(self._path, 'w')
        fConfigFile.write('['+self._sSection+']' + '''
urlFile=./urls.list
audioFolder=./audios
loop=true
random=true''')
        
        fConfigFile.close()
        fConfigFile=open(self._path, 'r+')
        return fConfigFile

    def _getConfigReader(self):
        fBufferConfig=None
        if os.path.isfile(self._path):
            fBufferConfig=open(self._path,'r+')
        else:
            fBufferConfig=self._genConfigFile()
            
        return ConfigReader(fBufferConfig,self._sSection)
         
    def _getListUrlFromDisk(self,sUrlFile):
        
        try:
            fUrlFile=open(sUrlFile,'r')
            
            listUrlReader=ListReader(fUrlFile)
            return listUrlReader.getAll()
            
        except (IOError, TypeError):
            logging.warn('Url file did not founded')
            
            return []
    def _writeListUrlInDisk(self, listUrl):
        try:
            fUrlFile=open(self._sUrlFile,'w')
            
            for sUrl in listUrl:
                fUrlFile.write(sUrl+'\n')
            fUrlFile.close()
            
                
        except (IOError, TypeError):
            logging.warn('Url file did not founded')
            
        
class ThreadDownloader  (threading.Thread):
     
    def __init__(self, listUrl,sAudioFolder, callbackInitPlaying, callbackAddMedia, callbackWriteListUrlInDisk):
        '''
        Thread's constructor, that sets the callbacks functions, urls from downloading the music and folder when It will download the music.
        
        @type listUrl: list[dict [str, str, bool]]
        @param listUrl : List that saves a dict by url, and this saves the keys url (str), path (str), isList(boolean).
        
        @type sAudioFolder: str
        @param sAudioFolder: It is a str with the path to the root where all downloads will be saved.
        
        @type callbackInitPlaying: function
        @param callbackInitPlaying: Function or method that will be executed when the first download has been finished.
        
        @type callbackAddMedia: function
        @param callbackAddMedia: Function that will be executed to put the path of an audio downloaded in the main thread.
        
        @type callbackWriteListUrlInDisk: function
        @param callbackWriteListUrlInDisk: Function that will be executed when all downloads have been finished and save a record of files downloaded in disk.
        '''
        
        super().__init__()
        self._listUrl=listUrl
        self._initPlaying=callbackInitPlaying
        self._addMedia=callbackAddMedia
        self._writeListUrlInDisk=callbackWriteListUrlInDisk
        self._sAudioFolder=sAudioFolder
    
    def _normalizationName(self,sName):
        """
        Method that changes the characters of sName by  compatible characters for file names.
        
        @type sName: Str
        @param sName:The name of the file to download.
        
        @rtype Str
        @return: File name with all its characters compatible.
        """ 
        def _filter(char):
            if char.isalnum():
                return char
            else:
                return '_'
            
        return "".join(_filter(x) for x in sName)
    
    def downloadPlayList(self,sUrl):
        """
        Method that downloads audios from videos that compose the list, wich is linked by the url saved in the var sUrl.
        
        @type sUrl:str
        @param sUrl: String with the url that links to a list of videos, and their audios will be downloaded.
        
        @raise ValueError: It is throwed when there is a problem with the url.
        
        """
        try:
            listPafy=pafy.get_playlist(sUrl['url'])
            sPathFolderList=''
            for pafyAudio in listPafy['items']:
                print('Downloading '+pafyAudio['pafy'].title)
                sPathFolderList=self._normalizationName(listPafy['title'])
                
                sAudioFolder=self._sAudioFolder+sep+sPathFolderList
                self.createFolderIfNotExist(sAudioFolder)
                self._downloadPafyStream(pafyAudio['pafy'],sAudioFolder)
            
            sUrl['path']=sAudioFolder
            sUrl['isList']=True
            
                
        except ValueError as exception:
            raise exception
        
           
    def downloadAudio(self,dictUrl):
        
        print('Downloading '+dictUrl['url'])
        pafyAudio=pafy.new(dictUrl['url'])
        dictUrl['path']= self._downloadPafyStream(pafyAudio)
        dictUrl['isList']=False
        
        
    def _downloadPafyStream(self,pafyStream, sAudioFolder=None):
        if sAudioFolder is None:
            sAudioFolder=self._sAudioFolder
        try:
            streamAudio=pafyStream.getbestaudio()
            sFormatAudio=streamAudio.__str__().split(':')[1].split('@')[0] #audio:webm@160k
            
            sPathAudio=sAudioFolder+sep+self._normalizationName(streamAudio.title)+'.'+sFormatAudio
            streamAudio.download(sPathAudio,quiet=True)
            self._addMedia(sPathAudio)
            self._initPlaying()
            return sPathAudio
        except TypeError:
            logging.warn('Error to download the audio')
        except Exception:
            logging.warn('This audio can not downdload')
    
    def _existsFile(self,sFile):
        return os.path.exists(sFile)
    
    def createFolderIfNotExist(self,sFolder):
        if(not self._existsFile(sFolder)):
            os.makedirs(sFolder)
            
    def download(self, dictUrl):
        
        if( dictUrl['path'] is None or not self._existsFile(dictUrl['path'])):
            
            try:
                self.downloadPlayList(dictUrl)
            except ValueError:
                try:
                    self.downloadAudio(dictUrl)
                except ValueError:
                    logging.error('Error downloading dictUrl')
            
    def _addListToMedia(self,sPath):
        
        for sFile in os.listdir(sPath):
            self._addMedia(sPath+sep+sFile)
               
    
    def _addMediaDownloadedToQueue(self,listUrls):
        for dictUrl in self._listUrl:
            if(not dictUrl['path'] is None and self._existsFile(dictUrl['path'])):
                if(dictUrl['isList']):
                    self._addListToMedia(dictUrl['path'])
                else:
                    self._addMedia(dictUrl['path'])
        self._initPlaying()
    def run(self):
        try:
            self._addMediaDownloadedToQueue(self._listUrl)
            for dictUrl in self._listUrl:
                self.download(dictUrl)
                self._savePathInFile(self._listUrl)
        except IndexError:
            logging.error('No media to play')
        
    
    def _savePathInFile(self,listUrl):
        listTextUrl=[]
        
        for dictUrl in listUrl:
            if not dictUrl['path'] is None:
                if dictUrl['isList']:
                    listTextUrl.append(dictUrl['url']+'--'+dictUrl['path']+'--list')
                else:
                    listTextUrl.append(dictUrl['url']+'--'+dictUrl['path']+'--audio')
            else:
                listTextUrl.append(dictUrl['url'])
        
        self._writeListUrlInDisk(listTextUrl)
 

if __name__ == "__main__":
    youtubePlayer=YoutubePlayerList()
    youtubePlayer.initPlayingMedia()           
            
        
    
    
        
